from email.mime import image
from platform import system
from tabnanny import verbose
from tkinter import N
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
from twocaptcha import TwoCaptcha
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chave_api = 'b62d6a42ca11a2ff523f96c68971e3fb'

# --------------------------------------- // ---------------------------------------
#Inicio de abertura de browser CHROME e correçao de erros (corrigidos manualmente)

chrome_options = Options() 
chrome_options.add_experimental_option("detach", True)
url = 'https://servicos.receita.fazenda.gov.br/servicos/cpf/consultasituacao/consultapublica.asp'
navegador = webdriver.Chrome(options=chrome_options)
navegador.get(url)

# --------------------------------------- // ---------------------------------------
#Preenchimentos de campos para pesquisa de CPF regular na Receita Federal

navegador.find_element('xpath', '//*[@id="txtCPF"]').click()
sleep(0.7)
navegador.find_element('xpath', '//*[@id="txtCPF"]').send_keys('02715388802')
sleep(0.7)

navegador.find_element('xpath', '//*[@id="txtDataNascimento"]').click()
sleep(0.7)
navegador.find_element('xpath', '//*[@id="txtDataNascimento"]').send_keys('11/01/1964')
sleep(0.7)

navegador.find_element('xpath', '//*[@id="fieldForm"]').click()
sleep(0.7)

navegador.find_element('xpath', '//*[@id="hcaptcha"]/iframe').click()
sleep(0.7)



# --------------------------------------- // ---------------------------------------

def solvehCaptcha(url):
    api_key = os.getenv('APIKEY_2CAPTCHA', 'b62d6a42ca11a2ff523f96c68971e3fb')

    solver = TwoCaptcha(api_key)

    try:
       result = solver.hcaptcha(
            sitekey = navegador.find_element(By.XPATH, '//*[@id="hcaptcha"]').get_attribute('data-sitekey'),
            url='https://servicos.receita.fazenda.gov.br/servicos/cpf/consultasituacao/consultapublica.asp',
        )

    except Exception as e:
        print("Retorno Exception: " + e)
        return False

    else:
        return result

WebDriverWait(navegador, 10).until(EC.presence_of_element_located(
    (By.CSS_SELECTOR, '#hcaptcha > iframe')))

resultado = solvehCaptcha(url)
#print(resultado)

if resultado:
    code = resultado['code']

    navegador.execute_script(
    "document.querySelector(" + "'" + '[name="h-captcha-response"]' + "'" + ").innerHTML = " + "'" + code + "'")

    navegador.find_element('xpath', '/html/body/div[3]/div[1]/iframe').click()
    navegador.find_element('xpath', '/html/body/div[2]/div[8]').click()

    #navegador.find_element(
    #        ('xpath', "body > div:nth-child(4) > div:nth-child(1) > iframe").click()
    #)

    #navegador.switch_to("")
    #navegador.find_element('xpath', "/html/body/div[2]/div[8]").click()
    #navegador.switch_to_default_content()

    navegador.find_element(
        By.CSS_SELECTOR, "#hcaptcha > iframe").click()












# ABAIXO, CONSEGUI PUXAR O SITEKEY CORRETO

#print("\n")
#print ("site_key:" + sitekey)
#print("\n")

#print("result: ")
#print(result)
#print("\n")

#print("config:")
#print(config)   
#print("\n")

#print("solver:")
#print(solver)
#print("\n")

#solver.report(id, True) # captcha solved correctly

#if result != 0:
#   navegador.switch_to_frame(navegador.find_element('xpath', '/html/body/div[2]/div[8]/div'))

print("Final TESTE")

# --------------------------------------- // ---------------------------------------

# --------------------------------------- // ---------------------------------------