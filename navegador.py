from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def iniciar_navegador(chromedriver_path):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-extensions')
    options.add_argument("--log-level=3")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    service = Service(chromedriver_path)
    browser = webdriver.Chrome(service=service, options=options)
    return browser

def fazer_login(browser, email, senha):
    url_login = ('https://hapvidaadb2bprd.b2clogin.com/hapvidaadb2bprd.onmicrosoft.com/oauth2/v2.0/authorize?'
                 'p=B2C_1_portal-empresa-login&client_id=a873a0fd-ed81-4cf2-bb25-0f6dca61bc46&nonce=defaultNonce&'
                 'redirect_uri=https%3A%2F%2Fportal-empresa.hapvidagndi.com.br%2Fautenticando&scope=openid%20'
                 'offline_access&response_type=code+id_token&prompt=login')

    browser.get(url_login)
    WebDriverWait(browser, 30).until(EC.visibility_of_element_located((By.ID, "email"))).send_keys(email)
    WebDriverWait(browser, 30).until(EC.visibility_of_element_located((By.ID, "password"))).send_keys(senha)
    browser.find_element(By.ID, "next").click()

def verificar_login(browser):
    try:
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.MuiStack-root'))
        )
        return True
    except:
        return False
