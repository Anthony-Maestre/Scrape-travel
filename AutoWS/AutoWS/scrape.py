import pandas as pd
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--headless')

driver = webdriver.Chrome('chromedriver.exe', options=options)
driver.get("https://www.pricetravel.co/paquetes")
driver.set_window_size(1920, 1080)

actions = ActionChains(driver)
driver.implicitly_wait(10)

def fetch(values, valuesh, valuesm, hab):
    soup = BeautifulSoup(driver.page_source, 'lxml')
    anio = soup.find('span', class_='ui-datepicker-year').get_text().strip("\n'' ")

    driver.find_element_by_xpath("//input[@id='ap_origin_flightPackage']").send_keys(values[0])
    driver.find_element_by_xpath("//ul[@id='ui-id-1']").click()
    driver.find_element_by_xpath("//input[@id='ap_dest_flightPackage']").send_keys(values[1])
    driver.find_element_by_xpath("//ul[@id='ui-id-2']").click()
    driver.find_element_by_xpath("//input[@id='ap_flightPackage_start']").clear()
    driver.find_element_by_xpath("//input[@id='ap_flightPackage_start']").send_keys(f"{values[3]}/{values[2]}/2021")
    driver.find_element_by_xpath("//input[@id='ap_flightPackage_end']").clear()
    driver.find_element_by_xpath("//input[@id='ap_flightPackage_end']").send_keys(f"{values[5]}/{values[4]}/2021")
    driver.find_element_by_xpath(f"//select[@id='ap_booker_FlightPackage_rooms']/child::option[contains(text(),{values[6]})]").click()
    
    n = 0
    while n <= int(values[6]) - 1:
        driver.find_element_by_xpath(f"//select[@id='ap_booker_FlightPackage_adults{n}']/child::option[contains(text(),{valuesh[n]})]").click()
        driver.find_element_by_xpath(f"//select[@id='ap_booker_FlightPackage_minors{n}']/child::option[contains(text(),{valuesh[f'm{n}']})]").click()
        n += 1

    n = 0
    while n <= int(values[6]) - 1:
        a = 0
        while a <= len(hab[n]) - 1:
            b = hab[n][a]
            driver.find_element_by_xpath(f"//select[@name='HotelRooms[{n}].MinorsAges[{a}].Years']/child::option[contains(text(),{b})]").click()
            a += 1
        n += 1

    driver.find_element_by_xpath("//input[@type='submit']").click()
    WebDriverWait(driver1, 120).until(EC.element_to_be_clickable((By.CLASS_NAME, "text-arrow")))
    sg.popup_no_wait('Extrayendo información...', non_blocking = True, auto_close = True, button_type = 5)
    habitacion = driver1.find_elements_by_xpath("//span[contains(text(),'Elegir habitación')]")
    page_source = driver1.page_source
    soup = BeautifulSoup(page_source, 'lxml')
    precio = soup.find_all('span', class_='product-rate-final', limit = 5)
    hotel = [i.find_previous('div', class_='list-product-title') for i in precio]
    hotel = [i.find('a', class_='list-product-name') for i in hotel]
    precios = [i.get_text().strip("\n'' ") for i in precio]
    hoteles = [i.get_text().strip("\n'' ") for i in hotel]

    a= 0
    for i in habitacion:
        i.click()
        a += 1
        if a == 5:
            break
    allwindo = driver1.window_handles;

    habitacion = []
    for i in allwindo:
        if i != allwindo[0]:
            driver1.switch_to.window(i)
            try:
                WebDriverWait(driver1, 120).until(EC.element_to_be_clickable((By.XPATH, "//strong[contains(text(),'Reservar')]")))
            except:
                 return habi == 'No hay habitaciones disponibles';
            opage = driver1.page_source
            soup = BeautifulSoup(opage, 'lxml')
            habi = soup.find(class_='room-title')
            if habi is not None:
                habitacion.append(habi.get_text().replace('\n',' '))
            else:
                driver1.switch_to.window(i)

    hora = datetime.today().strftime('%Y-%m-%d  %H:%M:%S')
    resultados = {
        "Fecha del viaje": f'{values[3]}/{values[2]}/{anio}',
        "Ciudad": f'{values[0]}',
        "Destino": f'{values[1]}',
        "Precios": precios,
        "Hotel": hoteles,
        "Tipo de acomodacion": habitacion,
        "hora de solicitud": hora
        }
