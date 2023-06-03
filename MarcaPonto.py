import requests
import datetime
import holidays
import random
import smtplib
import time
from datetime import date
import os
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

def log_and_print(msg, level="info"):
    print(msg)
    if level == "info":
        logging.info(msg)
    elif level == "warning":
        logging.warning(msg)
    elif level == "error":
        logging.error(msg)

def ensure_file_exists(file_name):
    """
    Verifica se o arquivo existe. 
    Se o arquivo não existir, ele é criado.
    """
    if not os.path.exists(file_name):
        with open(file_name, "w") as file:
            pass
            
def clear_file_content(file_name):
    """
    Limpa o conteúdo do arquivo. 
    """
    with open(file_name, "w") as file:
        pass

def ensure_current_day_log_file(today):
    """
    Essa função garante que o arquivo "pontos.txt" contenha apenas as entradas do dia atual.
    As entradas de dias anteriores são removidas.
    """
    date_str = today.strftime("%Y-%m-%d")
    with open("pontos.txt", "r") as file:
        lines = file.readlines()
    with open("pontos.txt", "w") as file:
        for line in lines:
            date, _, _ = line.strip().split(',')
            # mantém apenas as linhas cuja data corresponde à data atual
            if date == date_str:
                file.write(line)

#Enviando Email
def send_email(subject, body, timestamp=None):
    sender_email = 'SEU_E-MAIL_AQUI'
    receiver_email = 'SEU_E-MAIL_AQUI'
    password = 'SENHA_DO_SEU_E-MAIL_AQUI'

    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    if timestamp:
        body += f"\nData e hora da marcação: {timestamp}"
        
    message = f"Subject: {subject}\n\n{body}"
    try:
        server = smtplib.SMTP('smtp.office365.com', 587)  # SERVIDOR SMTP MICROSOFT!
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
  
#Validando se é feriado ou final de semana        
def is_valid_day(today, holidays_br, holidays_global):
    if today.weekday() >= 5:
        return False, 'Hoje é final de semana, não é possível marcar ponto!'
    elif today.date() in holidays_br or today.date() in holidays_global:
        return False, 'Hoje é feriado, não é possível marcar ponto!'
    return True, ''

#Randomizador de tempo
def generate_random_time(today, min_time, max_time):
    min_time_delta = datetime.timedelta(hours=min_time.hour, minutes=min_time.minute)
    max_time_delta = datetime.timedelta(hours=max_time.hour, minutes=max_time.minute)
    random_minutes = random.randint(0, int((max_time_delta - min_time_delta).total_seconds() // 60))
    return datetime.datetime.combine(today.date(), min_time) + datetime.timedelta(minutes=random_minutes)

def is_valid_execution_time(current_time, start_time, end_time):
    current_time_without_ms = datetime.time(current_time.hour, current_time.minute, current_time.second)
    if start_time <= current_time_without_ms <= end_time:
        return True
    return False

#Verifica se uma marcação de ponto já foi registrada no arquivo de registro.
def check_previous_point(today, point_type):
    date_str = today.strftime("%Y-%m-%d")
    with open("pontos.txt", "r") as file:
        for line in file:
            date, time, point = line.strip().split(',')
            if date == date_str and point == point_type:
                return True
    return False

#Registra uma marcação de ponto no arquivo de registro
def record_point(today, time, point_type):
    date_str = today.strftime("%Y-%m-%d")
    time_str = time.strftime("%H:%M:%S")
    with open("pontos.txt", "a") as file:
        file.write(f"{date_str},{time_str},{point_type}\n")

#Request
def send_request(url, payload, headers):
    response = requests.post(url, data=payload, headers=headers)
    response_data = response.json()
    return response_data

# Variável global para armazenar o dia atual
current_day = None

#Função Principal onde chamado tudooo
def main():
    
    # move a declaração de 'today' para dentro da função 'main'
    today = datetime.datetime.today()

    ensure_file_exists("pontos.txt")
    ensure_file_exists("horarios.txt")
    # Mantém apenas as entradas de ponto do dia atual no arquivo "pontos.txt"
    ensure_current_day_log_file(today)
        
    #Definindo em qual horario o script pode rodar.
    execution_start_time = datetime.time(8, 55)
    execution_end_time = datetime.time(18, 10)
        
    horario_entrada_min = datetime.time(8, 55)
    horario_entrada_max = datetime.time(9, 10)
    horario_saida_almoco_min = datetime.time(12, 0)
    horario_saida_almoco_max = datetime.time(12, 20)
    horario_retorno_almoco_min = datetime.time(13, 0)
    horario_retorno_almoco_max = datetime.time(13, 15)
    horario_saida_min = datetime.time(18, 0)
    horario_saida_max = datetime.time(18, 10)
    
    horario_entrada = generate_random_time(today, horario_entrada_min, horario_entrada_max)
    horario_saida_almoco = generate_random_time(today, horario_saida_almoco_min, horario_saida_almoco_max)
    horario_retorno_almoco = generate_random_time(today, horario_retorno_almoco_min, horario_retorno_almoco_max)
    horario_saida = generate_random_time(today, horario_saida_min, horario_saida_max)
    
    current_time = datetime.datetime.now().time()
    current_time_without_ms = datetime.time(current_time.hour, current_time.minute, current_time.second)
    
    current_year = today.year
    holidays_br = holidays.Brazil(years=current_year)
    holidays_global = holidays.CountryHoliday('BR', years=current_year)
    
    global current_day  # Isso é necessário para modificar a variável global dentro desta função
    
    url = 'https://cliente.apdata.com.br/everisparceiro/.net/index.ashx/SaveTimmingEvent'
    
    payload = {
        'deviceID': '8001',
        'userName': 'SEU_LOGIN',
        'password': 'SUA_SENHA',
        'eventType': '1',
        'cracha': '',
        'costCenter': '',
        'leave': '',
        'func': '0',
        'captcha': '',
        'tenantName': '',
        'tsc': '',
        'sessionID': '0',
        'selectedEmployee': '0',
        'selectedCandidate': '0',
        'selectedVacancy': '0',
        'dtFmt': 'd/m/Y',
        'tmFmt': 'H:i:s',
        'shTmFmt': 'H:i',
        'dtTmFmt': 'd/m/Y H:i:s',
        'language': '0',
        'idEmployeeLogged': '0'
    }

    headers = {
        'Content-Length': '306',
        'Sec-Ch-Ua': '"Chromium";v="109", "Not_A Brand";v="99"',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Sec-Ch-Ua-Mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.120 Safari/537.36',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Accept': '*/*',
        'Origin': 'https://cliente.apdata.com.br',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://cliente.apdata.com.br/everisparceiro/',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cookie': 'X-Oracle-BMC-LBS-Route=bb089166a4d059141e589f5733aa94f02d71e92b; clockDeviceToken8001=nH6C/qScdsJSxp4tyTbzcGMegpWY8nGrKJ7+ZjgmX3xHmIA=; acceptedRequiredCookies=COOKIEACCEPTED; acceptedOptionalCookies=COOKIEACCEPTED; Aplanguage=0; FIN_COOKIE=true; apdataCookieIsEnabled=none; __zjc7220=5264592017; __z_a=1442784464723815612723815; authenticated=false; SessionID=; dynSID=; ts=; loginOK=false; dashPublicImg=dpi; X-Oracle-BMC-LBS-Realm=1'
    }
        
# Se estamos em um novo dia ou ainda não foram gerados horários
    if today.day != current_day or not os.path.exists("horarios.txt"):
        current_day = today.day
        # Gerar novos horários aleatórios
        with open("horarios.txt", "w") as file:
            for point_type, min_time, max_time in [
                ("entrada", datetime.time(8, 55), datetime.time(9, 10)),
                ("saida_almoco", datetime.time(12, 0), datetime.time(12, 20)),
                ("retorno_almoco", datetime.time(13, 0), datetime.time(13, 15)),
                ("saida", datetime.time(18, 0), datetime.time(18, 10)),
            ]:
                random_time = generate_random_time(today, min_time, max_time)
                file.write(f"{point_type},{random_time.hour}:{random_time.minute}:{random_time.second}\n")
    
    # é Aqui que eu valido se é feriado ou fim de semana
    valid, reason = is_valid_day(today, holidays_br, holidays_global)
    if not valid:
        print(reason)
        send_email('[BOT] - MARCAÇÃO DE PONTO', reason)
        exit()
        
    if not is_valid_execution_time(current_time_without_ms, execution_start_time, execution_end_time):
        print(f"O horário atual ({current_time_without_ms}) está fora do intervalo de execução permitido. Encerrando o script.")
        exit()        
     
    # Inicialize uma lista com informações sobre os pontos a serem marcados
    point_steps = [
        ("entrada", horario_entrada),
        ("saida_almoco", horario_saida_almoco),
        ("retorno_almoco", horario_retorno_almoco),
        ("saida", horario_saida),
    ]

    # Verifica se a hora atual é maior ou igual ao horário de ponto
    with open("horarios.txt", "r") as file:
        for line in file:
            point_type, point_time = line.strip().split(',')
            hour, minute, second = map(int, point_time.split(':'))
            if datetime.datetime.now().time() >= datetime.time(hour, minute, second):
                # Se a marcação do ponto ainda não foi registrada, registra
                if not check_previous_point(today, point_type):
                    # Resto do código para registrar o ponto e enviar a solicitação...
                    send_email('[BOT] - MARCAÇÃO DE PONTO', f'Marcação de ponto {point_type}: {datetime.datetime.now().time()}')
                    record_point(today, datetime.datetime.now().time(), point_type)
                    print(f"Marcação de ponto '{point_type}' realizada com sucesso.")
                    time.sleep(2)            
                    response_data = send_request(url, payload, headers)
                else:
                    print(f"Marcação de ponto '{point_type}' já realizada. Ignorando.")
 
    print('RETORNO DO SERVIDOR:')
    print(response_data)

    # Verificando resposta da requisição
    if response_data['success'] and 'MARCACAO EFETUADA' in response_data['msg']['msg']:
        print('Marcação realizada com sucesso!')
        send_email('[BOT] - MARCAÇÃO DE PONTO', 'Marcação realizada com sucesso!', timestamp=datetime.datetime.now())
    else:
        print('Usuário / Senha inválidos!')
        send_email('[BOT] - MARCAÇÃO DE PONTO', 'Usuário / Senha inválidos!')
       
    log_and_print("Starting script...")


if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
        time.sleep(60)     # Espera 60 segundos antes de executar novamente
