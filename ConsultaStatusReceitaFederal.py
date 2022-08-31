from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from twocaptcha import TwoCaptcha
from time import sleep
import os

# --------------------------------------- // ---------------------------------------
#                                    INÍCIO_PROJETO
# --------------------------------------- // ---------------------------------------
#Inicio de abertura de browser CHROME e correção de erros (corrigidos manualmente)

chrome_options = Options() 
chrome_options.add_experimental_option("detach", True)
url = 'https://servicos.receita.fazenda.gov.br/servicos/cpf/consultasituacao/consultapublica.asp'
navegador = webdriver.Chrome(options=chrome_options)
navegador.get(url)

# --------------------------------------- // ---------------------------------------
#Preenchimentos de campos para pesquisa de CPF regular na Receita Federal

navegador.find_element('xpath', '//*[@id="txtCPF"]').click()
sleep(0.7) #Importante fazer funções sleep entre operações de find element para o sistema reconhecer como "humano"
navegador.find_element('xpath', '//*[@id="txtCPF"]').send_keys('XXX.XXX.XXX-XX') #Coloque o CPF para consulta na receita federal aqui
sleep(0.7)

navegador.find_element('xpath', '//*[@id="txtDataNascimento"]').click()
sleep(0.7)
navegador.find_element('xpath', '//*[@id="txtDataNascimento"]').send_keys('XX/XX/XXXXX') #Coloque a Data de Nascimento para consulta na receita federal aqui
sleep(0.7)

navegador.find_element('xpath', '//*[@id="fieldForm"]').click()
sleep(0.7)

# Lembrando que não há necessidade de abrir o iframe do hcaptcha para resolvê-lo.
# A biblioteca do 2captcha fará isso assim que chamada a função

# --------------------------------------- // ---------------------------------------
# Início solução resolução com API 2Captcha

#Abertura de função
def solvehCaptcha(url):
    api_key = os.getenv('APIKEY_2CAPTCHA', 'XXXXXXXXXXXXXXXXXXXXXXXXXXX') #Coloque sua chave de API aqui

    #Lançando informações de chave chamando o TwoCaptcha
    solver = TwoCaptcha(api_key)

    try:
       result = solver.hcaptcha(sitekey = navegador.find_element(By.XPATH, '//*[@id="hcaptcha"]').get_attribute('data-sitekey'), # data-sitekey é encontrado dentro do html da página desejada
            url='https://servicos.receita.fazenda.gov.br/servicos/cpf/consultasituacao/consultapublica.asp',
        )

    except Exception as e:
        print("Retorno Exception: " + e)
        return False

    else:
        return result

WebDriverWait(navegador, 10).until(EC.presence_of_element_located(
    (By.CSS_SELECTOR, '#hcaptcha > iframe')))

# Chamando função para executar comandos de solução de hcaptcha
resultado = solvehCaptcha(url)

# --------------------------------------- // ---------------------------------------
# Retorno com resultado positivo de leitura e quebra de hcaptcha

if resultado: # Se caso resultado retornar como positivo ou diferente de zero, o mesmo retornará a página de consulta da receita federal com a informação se o CPF está ou não regularizado.
    codigo = resultado['codigo']
    
    navegador.execute_script(
        "document.querySelector(" + "'" + '[name="h-captcha-response"]' + "'" + ").innerHTML = " + "'" + codigo + "'")

    navegador.find_element('xpath', '//*[@id="id_submit"]').click()

else:
    print("Programa retornado com erro de retorno, timeout ou informações estão incorretas. Corrija o código e tente novamente.")

# --------------------------------------- // ---------------------------------------
#                                      FIM_PROJETO
# --------------------------------------- // ---------------------------------------

# --------------------------------------- // ---------------------------------------
#                                        30/08/2022
#                                Desenvolvido por: Yan Falcão
#                         Agradecimento especial à: Davi Grisolia
#
#     Sistema desenvolvido para fins didáticos de uso de linguagem Python em ambiente 
#     de trabalho e também, solucionar hcaptchas com intuito de aprimorar uso de APIs.
# --------------------------------------- // ---------------------------------------
