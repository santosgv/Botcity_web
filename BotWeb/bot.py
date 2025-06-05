
from botcity.web import WebBot, Browser, By
import time
from botcity.web import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from botcity.web.util import element_as_select
from botcity.web.parsers import table_to_dict
import os
import datetime
import shutil
import logging

logger = logging.getLogger(__name__)

from botcity.maestro import *

BotMaestroSDK.RAISE_NOT_CONNECTED = False

def arquivos_modificados_hoje(diretorio):
    logging.basicConfig(filename='Arquivos_modificados.log', level=logging.INFO)
    logger.info('Inicio...')

    hoje = datetime.date.today()
    arquivos_hoje = []

    for arquivo in os.listdir(diretorio):
        caminho_completo = os.path.join(diretorio, arquivo)
        print(arquivo)
        if os.path.isfile(caminho_completo):
            data_modificacao = datetime.date.fromtimestamp(os.path.getmtime(caminho_completo))
            if data_modificacao == hoje:
                arquivos_hoje.append(caminho_completo)
    
    logger.info(f'Arquivos na data de {hoje}/{arquivos_hoje}')
    return arquivos_hoje

def posta_arquivo_lorenzeti(login,senha):
    logging.basicConfig(filename='posta_arquivo_lorenzeti.log', level=logging.INFO)
    logger.info('Inicio')
    pasta=r'P:\Lorenzetti'
    logger.info(f'Pasta arquivo Origem {pasta}')

    arquivos_para_upload =arquivos_modificados_hoje(pasta)

    bot = WebBot()
    bot.headless = True
    bot.browser = Browser.CHROME
    bot.driver_path =r"C:\GitHub\Botcity_web\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe"
    bot.browse("https://informa.lorenzetti.com.br/Login.aspx?ReturnUrl=%2f")
    if not bot.find( "Login", matching=0.97, waiting_time=10000):
        not_found("Login")
    bot.click_relative(17, 43)
    bot.paste(login)
    bot.tab()
    bot.paste(senha)
    bot.enter()
    bot.navigate_to('https://informa.lorenzetti.com.br/DocumentosEnviadosEDIListar.aspx?IDItem=31')

    bot.sleep(500)

    bot.find_element(selector='PHPrincipal_btnAdicionarDocumento',by=By.ID).click()
    bot.sleep(500)

    for arquivo in arquivos_para_upload:
        bot.sleep(500)
        input_file = bot.driver.find_element(By.ID, "PHPrincipal_arquivo_up")
        input_file.send_keys(arquivo)
        bot.key_enter()
        bot.sleep(100)
        bot.driver.find_element(By.ID, "PHPrincipal_btnSalvar").click()
        logger.info(f'Enviado arquivo {arquivo}')
        bot.back()
        bot.sleep(1000)
        bot.find_element(selector='PHPrincipal_btnAdicionarDocumento',by=By.ID).click()

    logger.info(f'Finalizado...')

    bot.close_page()
    
def baixa_arquivo_lorenzeti(login,senha):
    logging.basicConfig(filename='baixa_arquivo_lorenzeti.log', level=logging.INFO)
    logger.info('Inicio')
    PASTA_DOWNLOAD = "C:\GitHub\Botcity_web\BotWeb"
    PASTA_DESTINO = "P:\Lorenzetti\Receber"

    bot = WebBot()
    bot.headless = True
    bot.browser = Browser.CHROME
    bot.driver_path =r"C:\GitHub\Botcity_web\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe"
    bot.browse("https://informa.lorenzetti.com.br/Login.aspx?ReturnUrl=%2f")
    if not bot.find( "Login", matching=0.97, waiting_time=10000):
        not_found("Login")
    bot.click_relative(17, 43)
    bot.paste(login)
    bot.tab()
    bot.paste(senha)
    bot.enter()
    bot.navigate_to('https://informa.lorenzetti.com.br/DocumentosRecebidosEDIListar.aspx?IDItem=32')

    nomes_na_tabela = [
    elem.text for elem in bot.find_elements(
        by=By.CSS_SELECTOR,
        selector='span[id^="PHPrincipal_gridDocumentos_Descricao1_"]'
    )
    ]
    
    arquivos = bot.find_elements(selector='a.btn-action.glyphicons.download.btn-success',by=By.CSS_SELECTOR)


    for inx,arquivo in enumerate(arquivos):
        arquivo.click()
        time.sleep(10)

    bot.close_page()
    
    
    for arquivo in os.listdir(PASTA_DOWNLOAD):
        if  arquivo in nomes_na_tabela:
            caminho_origem = os.path.join(PASTA_DOWNLOAD, arquivo)
            caminho_destino = os.path.join(PASTA_DESTINO, arquivo)
            shutil.move(caminho_origem, caminho_destino)
            logger.info(f"Arquivo movido de: {caminho_origem} -> {caminho_destino}")
            
    logger.info('Finalizado')

    

def main():
    # Runner passes the server url, the id of the task being executed,
    # the access token and the parameters that this task receives (when applicable).
    maestro = BotMaestroSDK.from_sys_args()
    ## Fetch the BotExecution with details from the task, including parameters
    execution = maestro.get_execution()

    print(f"Task ID is: {execution.task_id}")
    print(f"Task Parameters are: {execution.parameters}")

    #posta_arquivo_lorenzeti('@','@')
    baixa_arquivo_lorenzeti('@','@')



def not_found(label):
    print(f"Element not found: {label}")


if __name__ == '__main__':
    main()


