# Accept consent window
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from random import randint
from entities import Company
from db_manager import db_connect, save_company



def parse_money(money:str):
    return float(money.replace("€","").replace(".","").replace(",",".").replace(" ","").upper().replace("EUROS",""))

def accept_consent(driver):
    try:
        accept_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Aceptar")]'))
        )
        accept_button.click()
    except Exception as e:
        print(f'Error accepting consent: {e}')

def wait_for_table(driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//table[contains(@class, "table")]'))
        )
    except Exception as e:
        print("Table not found:", e)
        driver.quit()
        exit()

def wait_for_body(driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//body'))
        )
    except Exception as e:
        print("BODY not found at:", e)
        driver.quit()
        exit()

def get_urls(driver):
    # Instance links
    links = driver.find_elements(By.XPATH, '//table[contains(@class, "table")]/tbody/tr/td[1]/a')
    # Browse and get links
    link_list = []
    try:
            for i in range(len(links)):
                # Get text and href
                link_text = links[i].text
                link_href = links[i].get_attribute("href")
                link = [link_text,link_href]
                link_list.append(link)
    except Exception as e:
        print(f"Error with link {link_text}: {e}")
    
                      
    return link_list

def view_all(driver):
    try:
        ver_todas = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "Ver todas")]'))
        )
        driver.execute_script("arguments[0].click();", ver_todas)
    except Exception as e:
        print(f'Error clicking "Ver todas": {e}')
        driver.quit()
        exit()

def scrape_companies(driver,links:list):
    # Connect to db
    connection = db_connect()
    for i in range(len(links)):
        url = links[i][1]
        driver.get(url)
        save_company(scrape_company_data_by_id(driver),connection)
        driver.back()
        time.sleep(randint(2, 4)) # Random sleep between 2 and 4 seconds to avoid detection
    connection.close()

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
    return company


