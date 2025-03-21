# Description: Main script to scrape data from the spanish stock market website
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from arguments import argument_parser, validate_arguments
from random import randint
from scrape_handlers import *
from db_manager import db_connect, db_dump
import logging
logger = logging.getLogger(__name__)



def main():
    
    arguments =argument_parser()
    validate_arguments(arguments)
    logging.basicConfig(filename='myapp.log', level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s",)
    logger.info('START of main program')
    try:
        if arguments.verbose: #Verbose mode
            logger.info('VERBOSE mode activated')

        if arguments.dump:#Dump database
            logger.info('DB DUMP mode activated')
            db_dump(db_connect())
            logger.info('DB DUMP finished')
            logger.info('END of main program')
            exit()

        if arguments.scrape: #Scrape data
                logger.info('START of scrape')
                #Selenium Options
                options = Options()
                options.add_argument("--headless") #True: closed browser, False: opened browser
                options.add_argument("--lang=es")  #Set brwoser language to spanish
                #Scrape companies
                if arguments.all or arguments.companies: 
                    logger.info('START of companies scrape')
                    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
                    scrape_companies(driver)
                    driver.quit()
                    logger.info('END of companies scrape')
                #Scrape stock values
                if arguments.all or arguments.stock_values:
                    logger.info('START of stock values scrape')
                    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
                    scrape_stock_values(driver)
                    driver.quit()
                    logger.info('END of stock values scrape')
                logger.info('END of scrape')
        logger.info('END of main program')
    except KeyboardInterrupt:
        print('>> Process interrupted by user !!!')
        logger.info('KeyboardInterrupt')
        exit()
    except Exception as e:
        logger.error(f'Error: {e}')
        exit()

if __name__ == '__main__':
    main()

