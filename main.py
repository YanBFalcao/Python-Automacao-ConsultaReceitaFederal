from tkinter import N
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
from twocaptcha import TwoCaptcha

chave = 'b62d6a42ca11a2ff523f96c68971e3fb'

chrome_options = Options() 
chrome_options.add_experimental_option("detach", True)
url = 'https://servicos.receita.fazenda.gov.br/servicos/cpf/consultasituacao/consultapublica.asp'
navegador = webdriver.Chrome(options=chrome_options)
navegador.get(url)


# --------------------------------------- // ---------------------------------------

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

# ABAIXO, CONSEGUI PUXAR O SITEKEY CORRETO
sitekey = navegador.find_element(By.XPATH, '//*[@id="hcaptcha"]').get_attribute('data-sitekey')
print("\n")
print (sitekey)
print("\n")

sitekey_clean = sitekey.split('" data-callback')[2].split('data-sitekey"')[4]
print("\n")
print(sitekey_clean)




# --------------------------------------- // ---------------------------------------











