import argparse
import pandas as pd
from utils import carregar_config, registrar_log, gerar_relatorio, enviar_email, carregar_contratos_processados, salvar_contrato_processado
from processamento import processar_contratos

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Automação Hapvida - Download Beneficiários')
    parser.add_argument('--planilha', type=str, required=True, help='Caminho da planilha Excel com contratos')
    parser.add_argument('--email', type=str, help='Email para login')
    parser.add_argument('--senha', type=str, help='Senha para login')
    parser.add_argument('--chromedriver', type=str, help='Caminho para chromedriver.exe')
    parser.add_argument('--log', type=str, help='Caminho para arquivo de log')
    parser.add_argument('--processados', type=str, help='Arquivo para contratos processados')
    parser.add_argument('--enviar-email', action='store_true', help='Enviar relatório por email ao final')

    args = parser.parse_args()

    config = carregar_config()

    # Sobrescreve config.ini com parâmetros passados na linha de comando (se houver)
    if args.email:
        config['email'] = args.email
    if args.senha:
        config['senha'] = args.senha
    if args.chromedriver:
        config['chromedriver_path'] = args.chromedriver
    if args.log:
        config['log_path'] = args.log
    if args.processados:
        config['processados_path'] = args.processados

    df = pd.read_excel(args.planilha)
    contratos = df['Novo Código Modelo Hapvida']

    contratos_processados = carregar_contratos_processados(config['processados_path'])

    total, sucesso, falhas = processar_contratos(contratos, contratos_processados, config['processados_path'], config)

    relatorio = gerar_relatorio(total, sucesso, falhas)
    print(relatorio)
    registrar_log(config['log_path'], "=== Final da execução ===")
    registrar_log(config['log_path'], relatorio)

    if args.enviar_email:
        destinatario = config['email']  # ou outro e-mail que queira notificar
        enviar_email(relatorio, destinatario)
