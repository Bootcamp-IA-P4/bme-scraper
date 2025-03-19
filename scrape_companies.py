import os
from dotenv import load_dotenv
load_dotenv()
DEBUG_MODE = False
DEBUG_MODE = os.getenv("DEBUG_MODE")
import sqlite3
import datetime
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
import time
from random import randint
from scrape_handlers import *
import logging
logger = logging.getLogger(__name__)

def main():

    logging.basicConfig(filename='myapp.log', level=logging.INFO)
    logger.info('Started')

    #Set options for headless browsing
    options = Options()
    options.add_argument("--headless") #True: closed browser, False: opened browser

    #Initialize firefox driver and set target url
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
    url = "https://www.bolsasymercados.es/bme-exchange/es/Mercados-y-Cotizaciones/Acciones/Mercado-Continuo/Precios/mercado-continuo"
      
    driver.get(url)

    #Wait for page to load  completely
    time.sleep(randint(2, 4)) # Random sleep between 2 and 4 seconds to avoid detection 
    accept_consent(driver)
    wait_for_body(driver)
    view_all(driver)
    wait_for_table(driver)
    browse_companies(driver,links=get_urls(driver))
    
    save_companies(db_connect())
    driver.quit()
    logger.info('Finished')

if __name__ == '__main__':
    main()
