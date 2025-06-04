
from botcity.web import WebBot, Browser, By
import time
import requests
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

        if os.path.isfile(caminho_completo):
            data_modificacao = datetime.date.fromtimestamp(os.path.getmtime(caminho_completo))
            if data_modificacao == hoje:
                arquivos_hoje.append(caminho_completo)

    logger.info(f'Arquivos na data de {hoje}/{arquivos_hoje}')
    return arquivos_hoje

def estado_es(CNPJ):
    bot = WebBot()
    # Configure whether or not to run on headless mode
    bot.headless = False

    # Uncomment to change the default Browser to Firefox
    bot.browser = Browser.CHROME

    # Uncomment to set the WebDriver path
    bot.driver_path =r"C:\GitHub\Botcity_web\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe"
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

    time.sleep(15)
    bot.find_element(selector='BtnPesquisarCodInscrMf',by=By.ID).click()
  
    

    DADOS = bot.find_elements("tabContribuinte", By.ID)

    for linha in DADOS:
        print(f'''{linha.text}
    ''')

def posta_arquivo_lorenzeti(login,senha):
    logging.basicConfig(filename='posta_arquivo_lorenzeti.log', level=logging.INFO)
    logger.info('Inicio')
    pasta=r'P:\vitor'
    logger.info(f'Pasta arquivo Origem {pasta}')

    arquivos_para_upload =arquivos_modificados_hoje(pasta)

    bot = WebBot()
    bot.headless = False
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
        

    bot.close_page()
    
def baixa_arquivo_lorenzeti(login,senha):
    logging.basicConfig(filename='baixa_arquivo_lorenzeti.log', level=logging.INFO)
    logger.info('Inicio')
    PASTA_DOWNLOAD = "C:\GitHub\Botcity_web\BotWeb"
    PASTA_DESTINO = "P:\Lorenzetti\Receber"

    bot = WebBot()
    bot.headless = False
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
    #maestro = BotMaestroSDK.from_sys_args()
    ## Fetch the BotExecution with details from the task, including parameters
    #execution = maestro.get_execution()

    #print(f"Task ID is: {execution.task_id}")
    #print(f"Task Parameters are: {execution.parameters}")

    #estado_es('33.048.204/0001-51') # 33.048.204/0001-51 aceita os caracteres
    #estado_sp('05328923000190') # 05.328.923/0001-90 exemplo nao aceita com . /-
    #estado_mg('42.274.696/0096-55') # mg 42.274.696/0096-55
    #posta_arquivo_lorenzeti('login','senha')
    baixa_arquivo_lorenzeti('login','senha')



def not_found(label):
    print(f"Element not found: {label}")


if __name__ == '__main__':
    main()


