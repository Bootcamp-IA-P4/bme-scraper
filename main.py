# Description: Main script to scrape data from the spanish stock market website
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from arguments import argument_parser, validate_arguments
from random import randint
from scrape_handlers import *
from db_manager import db_connect, db_dump, db_file_delete, db_delete
import logging
from utils import clear_console
logger = logging.getLogger(__name__)
from dotenv import load_dotenv
import os
load_dotenv()
db_file = os.getenv("DB_NAME")


def main():
    clear_console()
    arguments =argument_parser()
    validate_arguments(arguments)
    logging.basicConfig(filename='myapp.log', level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s",)
    logger.info('START of main program')
    print('*** Wellcome to BME Exchange scraper ***\n')
    try:
        if arguments.verbose: #Verbose mode
            logger.info('VERBOSE mode activated')

        if arguments.database: #Database mode
            logger.info('DB mode activated')

            if arguments.dump:#Dump database
                logger.info('DB DUMP mode activated')
                db_dump(db_connect())
                logger.info('DB DUMP finished')
                logger.info('END of main program')
                exit()

            if arguments.delete_file:#Delete database
                logger.info('DB DELETE mode activated')
                db_file_delete(db_file)
                print(f'Database {db_file} file deleted')
                logger.info(f'Database {db_file} file deleted')
                logger.info('END of main program')
                exit()
            
            if arguments.delete_db:#Delete all rows from all tables
                logger.info('DB TABLES delete started')
                db_delete(db_connect())
                print(f'Tables from {db_file} database deleted')
                logger.info(f'Tables from {db_file} database deleted')
                logger.info('DB TABLES delete finished')
                logger.info('END of main program')
                exit()

        if arguments.scrape: #Scrape data
                print('>> SCRAPING DATA FROM BME EXCHANGE\n')
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
        print('\n>> Process finished\n')
        logger.info('END of main program')
    except KeyboardInterrupt:
        print('\n>> Process interrupted by user !!!\n')
        logger.info('KeyboardInterrupt')
        exit()
    except Exception as e:
        logger.error(f'Error: {e}')
        exit()

if __name__ == '__main__':
    main()

