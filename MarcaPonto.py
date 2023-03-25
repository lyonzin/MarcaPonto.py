import requests
import datetime
import holidays
import random
import smtplib
from email.mime.text import MIMEText

#Enviando Email
def send_email(subject, body, timestamp=None):
    sender_email = 'SEU_EMAIL'
    receiver_email = 'E-MAIL DE DESTINO'
    password = 'SUA SENHA'

    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    if timestamp:
        body += f"\nData e hora da marcação: {timestamp}"

    message = f"Subject: {subject}\n\n{body}"
    try:
        server = smtplib.SMTP_SSL('smtp-mail.outlook.com', 465) # SERVIDOR SMTP MICROSOFT ! 
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.encode('utf-8'))
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
    return datetime.datetime.combine(today.date(), min_time) + datetime.timedelta(
        minutes=random.randint(0, (max_time - min_time).seconds // 60)
    )

#Request
def send_request(url, payload, headers):
    response = requests.post(url, data=payload, headers=headers)
    response_data = response.json()
    return response_data

#Função Principal onde chamado tudooo
def main():
    horario_entrada_min = datetime.time(8, 55)
    horario_entrada_max = datetime.time(9, 10)
    horario_saida_almoco_min = datetime.time(12, 0)
    horario_saida_almoco_max = datetime.time(12, 20)
    horario_retorno_almoco_min = datetime.time(13, 0)
    horario_retorno_almoco_max = datetime.time(13, 15)
    horario_saida_min = datetime.time(18, 0)
    horario_saida_max = datetime.time(18, 10)

    today = datetime.datetime.today()
    current_year = today.year
    holidays_br = holidays.Brazil(years=current_year)
    holidays_global = holidays.CountryHoliday('BR', years=current_year)

    valid, reason = is_valid_day(today, holidays_br, holidays_global)
    if not valid:
        print(reason)
        send_email('[BOT] - MARCAÇÃO DE PONTO', reason)
        exit()

    horario_entrada = generate_random_time(today, horario_entrada_min, horario_entrada_max)
    horario_saida_almoco = generate_random_time(today, horario_saida_almoco_min, horario_saida_almoco_max)
    horario_retorno_almoco = generate_random_time(today, horario_retorno_almoco_min, horario_retorno_almoco_max)
    horario_saida = generate_random_time(today, horario_saida_min, horario_saida_max)

    url = 'https://cliente.apdata.com.br/everisparceiro/.net/index.ashx/SaveTimmingEvent'
    
    payload = {
    'deviceID': '8001',
    'userName': 'SEU LOGIN',
    'password': 'SUA SENHA',
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

    response_data = send_request(url, payload, headers)
    
    print('RETORNO DO SERVIDOR:')
    print(response_data)

    # Verificando resposta da requisição
    if response_data['success'] and 'MARCACAO EFETUADA' in response_data['msg']['msg']:
        print('Marcação realizada com sucesso!')
        send_email('[BOT] - MARCAÇÃO DE PONTO', 'Marcação realizada com sucesso!', timestamp=datetime.datetime.now())
    else:
        print('Usuário / Senha inválidos!')
        send_email('[BOT] - MARCAÇÃO DE PONTO', 'Usuário / Senha inválidos!')


if __name__ == "__main__":
    main()