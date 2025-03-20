# Description: Main script to scrape data from the spanish stock market website
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from arguments import argument_parser
from random import randint
from scrape_handlers import *
import logging
logger = logging.getLogger(__name__)



def main():
    arguments =argument_parser()
    #Check if any argument is provided
    if not any(vars(arguments).values()):
        print("No arguments provided. Use -h for help")
        exit()

    logging.basicConfig(filename='myapp.log', level=logging.INFO)
    logger.info('Started')

    #Selenium Options
    options = Options()
    options.add_argument("--headless") #True: closed browser, False: opened browser
    options.add_argument("--lang=es")  #Set brwoser language to spanish

    #Initialize firefox driver
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)

    #Scrape companies
    if arguments.all or arguments.companies: 
        scrape_companies(driver)
    else:
        print("Companies data not scraped")
    #Scrape stock values
    if arguments.all or arguments.stock_values:
        True
        #scrape_stock_values(driver)
    else:
        print("Stock values not scraped")
    driver.quit() #Close browser
    logger.info('Finished')

if __name__ == '__main__':
    main()

