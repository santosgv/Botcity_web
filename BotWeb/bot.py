
from botcity.web import WebBot, Browser, By
import time
import requests
from botcity.web import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from botcity.web.util import element_as_select
from botcity.web.parsers import table_to_dict


from botcity.maestro import *

BotMaestroSDK.RAISE_NOT_CONNECTED = False

import whisper

# Carrega o modelo de IA uma vez (evitar recarregar múltiplas vezes)
model = whisper.load_model("base")  # Pode usar "small" ou "tiny" para menos recursos

def download_audio(url, filename="audio.mp3"):
    """Baixa um arquivo de áudio de uma URL e salva localmente"""
    if not url.startswith("http"):
        print("URL inválida!")
        return None

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        with open(filename, "wb") as file:
            file.write(response.content)

        print(f"Áudio salvo como {filename}")
        return filename
    except requests.RequestException as e:
        print(f"Erro ao baixar áudio: {e}")
        return None

def transcribe(audio_content):

    model = whisper.load_model("base")
    resposta = model.transcribe(audio_content)
    return resposta['text']

def solve_audio_captcha(driver):
    """Resolve completamente o desafio de áudio do reCAPTCHA"""
    try:
        # 1. Localiza o elemento de áudio
        audio_source = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "rc-audiochallenge-tdownload"))
        )
        print('link do audio',audio_source.get_attribute('src'))
        audio_url = audio_source.get_attribute('src')
        
        # 2. Baixa o áudio
        audio_content = download_audio(audio_url)
        if not audio_content:
            return False
        
        # 3. Transcreve o áudio
        transcription = transcribe(audio_content)
        if not transcription:
            return False
        
        print(f"Texto transcrito: {transcription}")
        
        # 4. Preenche a resposta
        audio_response = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "audio-response"))
        )
        audio_response.clear()
        audio_response.send_keys(transcription)
        
        # 5. Clica no botão de verificação
        verify_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "recaptcha-verify-button"))
        )
        verify_button.click()
        
        return True
        
    except TimeoutException:
        print("Tempo limite excedido ao localizar elementos do CAPTCHA.")
        return False
    except Exception as e:
        print(f"Erro inesperado ao resolver CAPTCHA: {str(e)}")
        return False

def request_audio_version(driver):
    try:
        driver.switch_to.default_content()
        
        # Aguarda até 10 segundos pelo iframe do desafio
        challenge_frame = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//iframe[contains(@title, 'desafio') or contains(@title, 'challenge')]")
            )
        )
        driver.switch_to.frame(challenge_frame)
        
        # Aguarda até 10 segundos pelo botão de áudio
        audio_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "recaptcha-audio-button"))
        )
        audio_button.click()
        
        driver.switch_to.default_content()
        return True
        
    except TimeoutException:
        print("Tempo limite excedido ao localizar elemento.")
        return False
    except Exception as e:
        print(f"Erro: {str(e)}")
        return False

def estado_es(CNPJ):
    bot = WebBot()
    # Configure whether or not to run on headless mode
    bot.headless = False

    # Uncomment to change the default Browser to Firefox
    bot.browser = Browser.CHROME

    # Uncomment to set the WebDriver path
    bot.driver_path =r"C:\GitHub\Botcity_web\chromedriver-win64\chromedriver.exe"
    #bot.driver_path ="/home/vitor/Documents/Projetos/Botcity_web/chromedriver-linux64/chromedriver"

    bot.browse("http://www.sintegra.es.gov.br/index.php")

    CNPJ = bot.find_element(selector='num_cnpj', by=By.ID)
    CNPJ.click()
    CNPJ.send_keys(f'{CNPJ}') # 33.048.204/0001-51 exemplo

    time.sleep(25)

    bot.find_element(selector='botaoConsultar', by=By.ID).click()


    DADOS = bot.find_elements(selector='valor',by=By.CLASS_NAME)

    for ind,x in enumerate(DADOS):
        print(f'Index: {ind} | Texto: {x.text}')


    # Wait 3 seconds before closing
    bot.wait(3000)

    # Finish and clean up the Web Browser
    # You MUST invoke the stop_browser to avoid
    # leaving instances of the webdriver open
    #bot.stop_browser()

    # Uncomment to mark this task as finished on BotMaestro
    # maestro.finish_task(
    #     task_id=execution.task_id,
    #     status=AutomationTaskFinishStatus.SUCCESS,
    #     message="Task Finished OK."
    # )

def estado_sp(CNPJ):
    bot = WebBot()
    # Configure whether or not to run on headless mode
    bot.headless = False

    # Uncomment to change the default Browser to Firefox
    bot.browser = Browser.CHROME

    # Uncomment to set the WebDriver path
    bot.driver_path =r"C:\GitHub\Botcity_web\chromedriver-win64\chromedriver.exe"
    #bot.driver_path ="/home/vitor/Documents/Projetos/Botcity_web/chromedriver-linux64/chromedriver"

    bot.browse("https://www.cadesp.fazenda.sp.gov.br/(S(d011sknoerhidcw141efdci0))/Pages/Cadastro/Consultas/ConsultaPublica/ConsultaPublica.aspx")

    label = bot.find_element(selector='ctl00_conteudoPaginaPlaceHolder_filtroTabContainer_filtroEmitirCertidaoTabPanel_tipoFiltroDropDownList', by=By.ID)
    
    label = element_as_select(label)
    label.select_by_value(value='1')

    time.sleep(3)

    input = bot.find_element(selector='//*[@id="ctl00_conteudoPaginaPlaceHolder_filtroTabContainer_filtroEmitirCertidaoTabPanel_valorFiltroTextBox"]',by=By.XPATH)
    input.click()
    input.send_keys(f'{CNPJ}')
    
    time.sleep(25)

    bot.find_element(selector='ctl00$conteudoPaginaPlaceHolder$filtroTabContainer$filtroEmitirCertidaoTabPanel$consultaPublicaButton', by=By.NAME).click()


    DADOS = bot.find_elements(selector='dadoDetalhe',by=By.CLASS_NAME)

    for ind,x in enumerate(DADOS):
        print(f'Index: {ind} | Texto: {x.text}')


    # Wait 3 seconds before closing
    bot.wait(3000)

    # Finish and clean up the Web Browser
    # You MUST invoke the stop_browser to avoid
    # leaving instances of the webdriver open
    #bot.stop_browser()

    # Uncomment to mark this task as finished on BotMaestro
    # maestro.finish_task(
    #     task_id=execution.task_id,
    #     status=AutomationTaskFinishStatus.SUCCESS,
    #     message="Task Finished OK."
    # )

def estado_mg(CNPJ):
    bot = WebBot()
    # Configure whether or not to run on headless mode
    bot.headless = False

    # Uncomment to change the default Browser to Firefox
    bot.browser = Browser.CHROME

    # Uncomment to set the WebDriver path
    bot.driver_path =r"C:\GitHub\Botcity_web\chromedriver-win64\chromedriver.exe"
    #bot.driver_path ="/home/vitor/Documents/Projetos/Botcity_web/chromedriver-linux64/chromedriver"

    bot.browse("https://dfe-portal.svrs.rs.gov.br/NFE/CCC")

    label=bot.find_element(selector='CodUf',by=By.ID)
    label = element_as_select(label)
    label.select_by_value(value='31')
    time.sleep(3)

    form = bot.find_element(selector='CodInscrMf',by=By.ID)
    form.click()
    form.send_keys(CNPJ)

    time.sleep(20)
    bot.find_element(selector='BtnPesquisarCodInscrMf',by=By.ID).click()
  
    

    elemento_tabela = bot.find_element("ListaContribuintes", By.ID)
    dados_tabela = table_to_dict(table=elemento_tabela)

    print(dados_tabela)

    for linha in dados_tabela:
        print(f'''{linha}
    ''')

    


def main():
    # Runner passes the server url, the id of the task being executed,
    # the access token and the parameters that this task receives (when applicable).
    maestro = BotMaestroSDK.from_sys_args()
    ## Fetch the BotExecution with details from the task, including parameters
    execution = maestro.get_execution()

    print(f"Task ID is: {execution.task_id}")
    print(f"Task Parameters are: {execution.parameters}")

    #estado_es('33.048.204/0001-51') # 33.048.204/0001-51 aceita os caracteres
    #estado_sp('05328923000190') # 05.328.923/0001-90 exemplo nao aceita com . /-
    #estado_mg('42.274.696/0096-55') # mg 42.274.696/0096-55



def not_found(label):
    print(f"Element not found: {label}")


if __name__ == '__main__':
    main()
