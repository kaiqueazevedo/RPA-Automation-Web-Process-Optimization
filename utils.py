import configparser
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

def carregar_config(caminho='config.ini'):
    config = configparser.ConfigParser()
    config.read(caminho)
    return config['DEFAULT']

def registrar_log(caminho_log, mensagem):
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(caminho_log, 'a', encoding='utf-8') as f:
        f.write(f"[{agora}] {mensagem}\n")

def enviar_email(relatorio, destinatario, assunto="Relatório Automação Beneficiários"):
    # Configurar seu servidor SMTP abaixo:
    smtp_host = 'smtp.seuprovedor.com'  # Exemplo: smtp.gmail.com
    smtp_port = 587
    smtp_usuario = 'seu_email@dominio.com'
    smtp_senha = 'sua_senha'

    msg = MIMEText(relatorio)
    msg['Subject'] = assunto
    msg['From'] = smtp_usuario
    msg['To'] = destinatario

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as servidor:
            servidor.starttls()
            servidor.login(smtp_usuario, smtp_senha)
            servidor.send_message(msg)
        print("Email enviado com sucesso.")
    except Exception as e:
        print(f"Falha ao enviar email: {e}")

def gerar_relatorio(total, sucesso, falhas):
    texto = f"""Relatório de Processamento - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Total de contratos: {total}
Contratos processados com sucesso: {sucesso}
Contratos com falhas: {len(falhas)}

Lista de contratos com falha:
{', '.join(map(str, falhas)) if falhas else 'Nenhum'}

"""
    return texto

def carregar_contratos_processados(arquivo):
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            return set(f.read().splitlines())
    except FileNotFoundError:
        return set()

def salvar_contrato_processado(arquivo, contrato):
    with open(arquivo, 'a', encoding='utf-8') as f:
        f.write(f"{contrato}\n")
