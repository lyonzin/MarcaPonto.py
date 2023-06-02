# Script de Marcação de Ponto Automatizado

Este script foi desenvolvido em Python para automatizar a marcação de ponto. Ele utiliza a biblioteca `requests` para enviar requisições POST, e `smtplib` para enviar e-mails de notificação. Além disso, verifica se o dia atual é um feriado ou final de semana usando a biblioteca `holidays`.

## Dependências

- `requests`: para realizar as requisições HTTP para o serviço de marcação de ponto.
- `datetime`: para trabalhar com datas e horários.
- `random`: para gerar horários aleatórios.
- `smtplib` e `email.mime.text.MIMEText`: para enviar e-mails.
- `holidays`: para verificar se uma data é um feriado.

## Principais Funcionalidades

1. **Geração de horários aleatórios**: O script gera horários aleatórios para entrada, saída para almoço, retorno do almoço e saída do trabalho. Esses horários são gerados dentro de um intervalo de tempo específico para cada evento.
2. **Validação do dia**: Antes de fazer a marcação, o script verifica se o dia atual é um dia útil (não é um final de semana ou feriado).
3. **Envio de e-mails**: O script envia um e-mail após a realização de cada marcação de ponto, informando o tipo de marcação (entrada, saída para almoço, retorno do almoço, saída) e o horário da marcação.
4. **Verificação de marcações de ponto já realizadas**: Antes de cada marcação, o script verifica se a marcação já foi realizada para evitar marcações duplicadas.
5. **Registro das marcações de ponto**: O script grava cada marcação de ponto em um arquivo de texto (`pontos.txt`). O arquivo contém a data, o horário e o tipo de cada marcação de ponto.


## Uso

Para usar o script, você deve configurar os seguintes parâmetros:

- As credenciais do seu e-mail na função `send_email()`.
- As credenciais para o serviço de marcação de ponto na função `main()` (no objeto `payload`).
- Os intervalos de tempo para a geração de horários aleatórios na função `main()`.

Depois disso, basta executar o script. Ele fará a marcação de ponto automaticamente e enviará um e-mail para você com os detalhes de cada marcação.

**Nota**: 

- Certifique-se de ter todas as dependências instaladas no seu ambiente Python. Você pode instalá-las usando o comando `pip install <nome da biblioteca>`.
- Este script foi projetado para funcionar com o servidor SMTP da Microsoft. Se você estiver usando outro provedor de e-mail, pode ser necessário modificar as configurações de SMTP.
- Certifique-se de que as informações fornecidas estejam corretas e que você tenha permissão para acessar o sistema de marcação de ponto.
