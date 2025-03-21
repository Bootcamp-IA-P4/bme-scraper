# Accept consent window
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from random import randint
from entities import Company, StockValue
from db_manager import db_connect, save_company, save_stock_value
from arguments import argument_parser
from utils import parse_money, parse_updated, progress_bar
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename='myapp.log', level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s",)

arguments =argument_parser()


def accept_consent(driver):
    try:
        accept_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Aceptar")]'))
        )
        accept_button.click()
    except Exception as e:
        print(f'Error accepting consent: {e}')
        logger.error(f'Error accepting consent: {e}')
        driver.quit()
        exit()

def wait_for_table(driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//table[contains(@class, "table")]'))
        )
    except Exception as e:
        print("Table not found:", e)
        logger.error(f"Table not found: {e}")
        driver.quit()
        exit()

def wait_for_body(driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//body'))
        )
    except Exception as e:
        print("BODY not found at:", e)
        logger.error(f"BODY not found at: {e}")
        driver.quit()
        exit()

def get_urls(driver):
    # Instance links
    links = driver.find_elements(By.XPATH, '//table[contains(@class, "table")]/tbody/tr/td[1]/a')
    # Browse and get links
    link_list = []
    try:
            if arguments.verbose:
                print(">> Scraping links")
            for i in range(len(links)):
                if not arguments.verbose:
                    progress_bar(i+1, len(links),title="Scraping HREFS ")
                # Get text and href
                link_text = links[i].text
                link_href = links[i].get_attribute("href")
                link = [link_text,link_href]
                link_list.append(link)
                if arguments.verbose:
                    print(f"Link {i}: {link_text} - {link_href}")
            if arguments.verbose:
                print("\n>> Scraping links finished\n")
    except Exception as e:
        print(f"Error with link {link_text}: {e}")
        logger.error(f"Error with link {link_text}: {e}")
        driver.quit()
        exit()
    return link_list

def view_all(driver):
    try:
        ver_todas = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "Ver todas")]'))
        )
        driver.execute_script("arguments[0].click();", ver_todas)
    except Exception as e:
        print(f'Error clicking "Ver todas": {e}')
        logger.error(f'Error clicking "Ver todas": {e}')
        driver.quit()
        exit()

def scrape_companies(driver):
    if arguments.verbose:
        print(">> Scraping companies")
    url = "https://www.bolsasymercados.es/bme-exchange/es/Mercados-y-Cotizaciones/Acciones/Mercado-Continuo/Precios/mercado-continuo"
    driver.get(url)
    #Wait for page to load  completely
    time.sleep(randint(1, 4)) # Random sleep to avoid detection 
    accept_consent(driver)
    wait_for_body(driver)
    view_all(driver)
    wait_for_table(driver)
    links = get_urls(driver)
    # Connect to db
    connection = db_connect()
    for i in range(len(links)):
        if not arguments.verbose:
            progress_bar(i+1, len(links),title="Scraping companies ")
        url = links[i][1]
        driver.get(url)
        save_company(scrape_company_data_by_id(driver),connection)
        driver.back()
        time.sleep(randint(1, 4)) # Random sleep detection
    connection.close()
    if arguments.verbose:
        print(f">> Finished scraping of {i+1} companies\n")
    logger.info(f"Finished scraping of {i+1} companies")
    return

def scrape_company_data_by_id(driver):
    # Wait for the divs to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "details-table.horizontalCompanyInfo")))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "details-table.horizontal")))
    # Get the divs
    company_info = driver.find_element(By.CLASS_NAME, "details-table.horizontalCompanyInfo")
    company_details = driver.find_element(By.CLASS_NAME, "details-table.horizontal")
    # Get the labels
    info_labels = company_info.find_elements(By.TAG_NAME, "label")
    details_labels = company_details.find_elements(By.TAG_NAME, "label")
    company_dict = {}
    for label in info_labels:
        if label.text.strip() == "Domicilio:":
            details_labels.append(label)
            break
    for label in details_labels:
         field_id = label.get_attribute("for")  # Return example: lbl-details-2-1
         span_element = driver.find_element(By.ID, field_id)
         if label.text.strip() in ("Capital Admitido","Nominal"):
             field_value = parse_money(span_element.text.strip())
         else:
             field_value = span_element.text.strip()
         company_dict[label.text.strip().replace(":","")] = field_value
    company = Company(
    company_dict.get("Nombre", None),
    company_dict.get("ISIN", None),
    company_dict.get("Ticker", None),
    company_dict.get("Nominal", None),
    company_dict.get("Mercado", None),
    company_dict.get("Domicilio", None),
    company_dict.get("Capital Admitido", None)
    )
    if arguments.verbose:
        print(f'Company scrapped: {company}')
    return company


def scrape_stock_values(driver):
    if arguments.verbose:
        print(">> Scraping stock values <<")
    url = "https://www.bolsasymercados.es/bme-exchange/es/Mercados-y-Cotizaciones/Acciones/Mercado-Continuo/Precios/mercado-continuo"
    driver.get(url)
    #Wait for page to load  completely
    time.sleep(randint(1, 4)) # Random sleep to avoid detection 
    accept_consent(driver)
    wait_for_body(driver)
    view_all(driver)
    wait_for_table(driver)
    rows = driver.find_elements(By.XPATH, '//table[contains(@class, "table")]/tbody/tr')
    connection = db_connect()
    i = 0
    for row in rows:
        if not arguments.verbose:
            progress_bar(i, len(rows),title="Scraping stock values ")
        i += 1
        columns = row.find_elements(By.TAG_NAME, "td")
        data_row = []
        for col in columns:
            href_element = col.find_element(By.TAG_NAME, "a") if col.find_elements(By.TAG_NAME, "a") else None

            if href_element:
                href = href_element.get_attribute("href")  # URL
                data_row.insert(0,href[-12:])  # Insert ISIN at the beginning
            else:
                data_row.append(col.text.strip())  # Si no hay enlace, guardar solo el texto
        if len(data_row) == 8:
            stock = StockValue(
                data_row[0],
                parse_money(data_row[1]),
                parse_money(data_row[2].replace("%","")),
                parse_money(data_row[3]),
                parse_money(data_row[4]),
                parse_money(data_row[5]),
                parse_money(data_row[6])
            )
        else:
            stock = StockValue(
                data_row[0],
                parse_money(data_row[1]),
                parse_money(data_row[2].replace("%","")),
                parse_money(data_row[3]),
                parse_money(data_row[4]),
                parse_money(data_row[5]),
                parse_money(data_row[6]),
                parse_updated(data_row[7],data_row[8]),
        )
        if arguments.verbose:
            print(f'Stock scrapped: {stock.__str__()}')
        # Save stock value to db
        save_stock_value(stock,connection)
        time.sleep(randint(1, 4)) # Random sleep to avoid detection 
    connection.close()
    print(f">> Finished scraping of {i} stock values\n")
    logger.info(f"Finished scraping of {i} stock values")
    return

