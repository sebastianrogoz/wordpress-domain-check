from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver import ActionChains
import time

#----------WCZYTANIE NAZW DOMEN----------
# - ogarnac wczytywanie csv wypluwanych przez Majestica
domainsToCheck = []
with open('wordpress-available.csv','r') as file:
    domainsToCheck = file.read().splitlines()


#----------INICJALIZACJA DRIVERA----------
driver = webdriver.Firefox() #uruchamia przegladarke


#----------OD ZERA DO BOHATERA CZYLI DROGA DO start/domains----------

#lecimy na wordpressa
baseUrl = "https://wordpress.com"
driver.get(baseUrl + "/")

#click getStarted na stronie startowej
getStartedBtn = driver.find_element_by_id("hero-cta")
getStartedBtn.click()

#wybieramy rodzaj bloga
try:
    wait = WebDriverWait(driver, 15).until( # czekamy az element sie pojawi
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Start with a blog')]"))
    )
except TimeoutException:
    print("blad na stronie wyboru rodzaju bloga")
else:
    startBlogBtn = driver.find_element_by_xpath("//*[contains(text(), 'Start with a blog')]")
    startBlogBtn.click()

#wybor pierwszego motywu z listy
try:
    wait = WebDriverWait(driver, 15).until( #czekamy az element sie pojawi
        EC.presence_of_element_located((By.CLASS_NAME, "theme__content"))
    )
except TimeoutException:
    print("blad na stronie wyboru rodzaju bloga")
else:
    pickBtn = driver.find_element_by_class_name("theme__content")
    pickBtnActionChain = ActionChains(driver) #Action Chain przemieszczajacy kursor nad pierwszy theme + klik
    pickBtnActionChain.move_to_element(pickBtn)
    pickBtnActionChain.click()
    pickBtnActionChain.perform()


#----------SPRAWDZANIE DOSTEPNOSCI DOMEN----------

try:
    wait = WebDriverWait(driver, 15).until( #czekamy az searchbox sie pojawi
        EC.presence_of_element_located((By.ID, "search-component-1"))
    )
except TimeoutException:
    print("blad na stronie sprawdzania domen")
else:   #jeśli searchbox jest na stronie
    domainsChecked = []
    for domain in domainsToCheck:
        driver.find_element_by_id("search-component-1").clear()
        #wpisujemy text
        #jesli skrypt dziala za szybko (#sebozadobrzekoduje) czasami wpisuje kilka domen na raz
        #co ciekawe: output skryptu jest poprawny mimo że w przeglądarce jest sprawdzana np: "domena1domena2"
        #nie mam pojecia dlaczego to dziala
        driver.find_element_by_id("search-component-1").send_keys(domain)
        try:
            wait = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "domain-suggestion__content"))
            )
            wait2 = WebDriverWait(driver, 15).until(
                EC.text_to_be_present_in_element((By.CLASS_NAME, "domain-suggestion__content"), "wordpress")
            )
        except TimeoutException:
            print("blad przy wyswietlaniu sugestii")
        else:
            try:
                domainSuggestion = driver.find_element_by_xpath("//*[contains(text(), '{}.wordpress.com')]".format(domain))
            except NoSuchElementException:
                pass
            else:
                domainsChecked.append(domain + "\n")

with open("wordpress-available-checked.csv", "w") as file:
    file.writelines(domainsChecked)





