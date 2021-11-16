from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from subprocess import CREATE_NO_WINDOW
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import PySimpleGUI as sg
from datetime import datetime

sg.popup_no_wait('Iniciando...', non_blocking = True, auto_close = True, button_type = 5)

def pag_base():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--headless')
    driver = webdriver.Chrome('chromedriver.exe', options=options)
    driver.get("https://www.pricetravel.co/paquetes")
    driver.set_window_size(1920, 1080)
    actions = ActionChains(driver)
    driver.implicitly_wait(10)
    return driver

def parametros():
    layout = [[sg.Text('El número máximo de pasajeros es: 6')],
                [sg.Text('Ciudad de origen'), sg.InputText(size= (20, )), sg.Text('Ciudad de destino'), sg.InputText(size= (20, ))],
               [sg.Text('Mes de Salida'), sg.InputText(size=(10, )), sg.Text('Dia'), sg.InputText(size= (2, )), sg.Text('Mes de Regreso'), sg.InputText(size= (10, )), sg.Text('Dia'), sg.InputText(size= (2, ))],
               [sg.Text('#Habitaciones(Max. 4)'), sg.InputText(size= (2, ))],
               [sg.Button('Ok'), sg.Button('Cancel')] ]
    window = sg.Window('Buscar paquetes de viaje', layout)
    event, values = window.read()
    window.close()
    mes = {
        'enero':'1',
        'febrero':'2',
        'marzo':'3',
        'abril':'4',
        'mayo':'5',
        'junio':'6',
        'julio':'7',
        'agosto':'8',
        'septiembre':'9',
        'octubre':'10',
        'noviembre':'11',
        'diciembre':'12',
        }
    for i in mes:
        if values[2].lower() == i:
            values[2] = mes[i]
        elif values[4].lower() == i:
            values[4] = mes[i]

    n = 0
    habs = []
    while n <= int(values[6]) - 1:
        habs.append([sg.Text('#Adultos(1-6)'), sg.InputText(size= (2, )), sg.Text('#Menores(0-6)'), sg.InputText(size= (2, ), key = f"m{n}")])
        n += 1

    por_hab = [[sg.Text('Recuerda: El número máximo de pasajeros es: 6')], habs, [sg.Button('Ok'), sg.Button('Cancel')]]
    windowh = sg.Window('Buscar paquetes de viaje', por_hab)
    eventh, valuesh = windowh.read()
    print(valuesh)
    windowh.close()
    n = 0
    hab = {}
    while n <= len(valuesh):
        for i in valuesh:
            menores = []
            if valuesh[i] == '0':
                menores.append([sg.Text(f'No hay menores en la habitacion {n}')])
            if i == f'm{n}':
                a = 0
                while a <= int(valuesh[i]) - 1:
                    menores.append([sg.Text(f'Habitacion {n} - Edad del menor (2-17)'), sg.InputText(size= (2, ))])
                    a += 1
                mens_hab = [menores, [sg.Button('Ok'), sg.Button('Cancel')]]
                windowm = sg.Window(f'Habitacion Nro {n}', mens_hab, element_padding = ((20,5),(2,2)))
                eventm, valuesm = windowm.read()
                windowm.close()
                hab[n] = valuesm
        n += 1
    return values, valuesh, valuesm, hab

def buscar(driver, values, valuesh, valuesm, hab):
    sg.popup_no_wait('Buscando paquetes...', non_blocking = True, auto_close = True, button_type = 5)
    
    soup = BeautifulSoup(driver.page_source, 'lxml')
    global anio
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
    return driver

def buscar_res(driver1):
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
            WebDriverWait(driver1, 120).until(EC.element_to_be_clickable((By.XPATH, "//strong[contains(text(),'Reservar')]")))
            opage = driver1.page_source
            soup = BeautifulSoup(opage, 'lxml')
            habi = soup.find(class_='room-title')
            if habi is not None:
                habitacion.append(habi.get_text().replace('\n',' '))
            else:
                driver1.switch_to.window(i)
    return precios, hoteles, habitacion

def guardar_res(precios, hoteles, habitacion):
    sg.popup_no_wait('Guardando...', non_blocking = True, auto_close = True, button_type = 5)
    Lista = pd.DataFrame({
    "Ciudad": f'{values[0]}',
    "Destino": f'{values[1]}',
    "Precios": precios,
    "Hotel": hoteles,
    "Tipo de acomodacion": habitacion
    })
    Lista.columns = pd.MultiIndex.from_product([[f"Vuelos del {values[3]}/{values[2]} al {values[5]}/{values[4]}"], Lista.columns])
    resultado = Lista.to_csv('ListaVuelos.csv', index=False)
    return resultado


if __name__ == '__main__':
    dbname = get_database()
    driver = pag_base()
    values, valuesh, valuesm, hab = parametros()
    driver1 = buscar(driver, values, valuesh, valuesm, hab)
    precios, hoteles, habitacion = buscar_res(driver1)
    resultado = guardar_res(precios, hoteles, habitacion)
    sg.popup('Se han guardado los resultados')
    driver.quit()
