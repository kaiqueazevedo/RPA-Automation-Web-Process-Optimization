import time
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from navegador import iniciar_navegador, fazer_login, verificar_login
from utils import registrar_log, salvar_contrato_processado

def processar_contratos(contratos, contratos_processados, progresso, config):
    total = len(contratos)
    sucesso = 0
    falhas = []

    for contrato in contratos:
        if str(contrato) in contratos_processados:
            continue

        tentativa = 0
        MAX_TENTATIVAS = 3
        processado_com_sucesso = False

        while tentativa < MAX_TENTATIVAS and not processado_com_sucesso:
            try:
                browser = iniciar_navegador(config['chromedriver_path'])
                fazer_login(browser, config['email'], config['senha'])

                if not verificar_login(browser):
                    registrar_log(config['log_path'], f"Contrato {contrato}: Falha - Login inválido.")
                    browser.quit()
                    break

                salvar_contrato_processado(progresso, contrato)
                contratos_processados.add(str(contrato))

                menu_busca_svg = WebDriverWait(browser, 30).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "div.MuiStack-root.css-zm6l5c div:nth-child(2) div div:nth-child(4) div button svg"))
                )
                menu_busca_svg.click()

                campo_busca = WebDriverWait(browser, 20).until(
                    EC.visibility_of_element_located((By.ID, "mui-4"))
                )
                campo_busca.send_keys(contrato)

                time.sleep(2)

                botao_buscar = WebDriverWait(browser, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[text()='Buscar']"))
                )
                botao_buscar.click()

                time.sleep(4)

                avancar = WebDriverWait(browser, 30).until(
                    EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/main/div/div/main/div[2]/div/div[2]/div/div/div[2]/div/div[6]/div/button"))
                )
                avancar.click()

                botao_lista = WebDriverWait(browser, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[.//p[text()='Lista de beneficiários']]"))
                )
                browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao_lista)
                time.sleep(0.5)
                botao_lista.click()

                time.sleep(2)

                botao_exportar = WebDriverWait(browser, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Exportar beneficiários')]"))
                )
                botao_exportar.click()

                time.sleep(5)
                botao_fechar = WebDriverWait(browser, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[div[text()='Fechar']]"))
                )
                botao_fechar.click()

                time.sleep(7)
                botao_baixar = WebDriverWait(browser, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Baixar beneficiários')]"))
                )
                botao_baixar.click()
                time.sleep(7)

                browser.quit()
                registrar_log(config['log_path'], f"Contrato {contrato}: Finalizado com sucesso.")
                sucesso += 1
                processado_com_sucesso = True

            except (TimeoutException, NoSuchElementException) as e:
                registrar_log(config['log_path'], f"Contrato {contrato}: Falha - Elemento não encontrado ou timeout. Detalhe: {e}")
                try:
                    browser.quit()
                except:
                    pass
                falhas.append(contrato)
                break

            except WebDriverException as e:
                tentativa += 1
                registrar_log(config['log_path'], f"Contrato {contrato}: Tentativa {tentativa} falhou por erro crítico: {e}")
                try:
                    browser.quit()
                except:
                    pass
                time.sleep(5)

        if not processado_com_sucesso and tentativa >= MAX_TENTATIVAS:
            registrar_log(config['log_path'], f"Contrato {contrato}: Falha após {MAX_TENTATIVAS} tentativas.")
            falhas.append(contrato)

    return total, sucesso, falhas
