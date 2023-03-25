# Script de Marcação de Ponto Automatizado

Este script foi desenvolvido em Python para automatizar a marcação de ponto. Ele utiliza a biblioteca `requests` para enviar requisições POST, e `smtplib` para enviar e-mails de notificação. Além disso, verifica se o dia atual é um feriado ou final de semana usando a biblioteca `holidays`.

## Dependências

- requests
- datetime
- holidays
- random
- smtplib
- email.mime.text

## Funcionalidades

1. Verifica se o dia atual é um feriado ou final de semana.
2. Gera horários aleatórios para a marcação de ponto.
3. Envia a requisição POST para a URL fornecida.
4. Envia um e-mail de notificação com o resultado da marcação de ponto.

## Uso

Antes de executar o script, é necessário preencher as seguintes informações:

- SEU_EMAIL: Insira seu endereço de e-mail.
- E-MAIL DE DESTINO: Insira o endereço de e-mail de destino para receber notificações.
- SUA SENHA: Insira a senha do seu e-mail.
- SEU LOGIN: Insira o login para acessar o sistema de marcação de ponto.

Após preencher as informações, execute o script em um ambiente Python com as bibliotecas necessárias instaladas. Ele irá verificar se o dia atual é válido para marcação de ponto e, em caso positivo, realizará a marcação e enviará um e-mail de notificação.

## Notas

- Este script foi projetado para funcionar com o servidor SMTP da Microsoft. Se você estiver usando outro provedor de e-mail, pode ser necessário modificar as configurações de SMTP.
- Certifique-se de que as informações fornecidas estejam corretas e que você tenha permissão para acessar o sistema de marcação de ponto. 
