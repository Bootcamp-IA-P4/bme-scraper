# Accept consent window
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from load_dotenv import load_dotenv
import time
from random import randint
import os
import json
import sqlite3

load_dotenv()
DEBUG_MODE = False
DEBUG_MODE = os.getenv("DEBUG_MODE")

company_dict = {
"name":"lbl-details-2-1",
"isin":"lbl-details-2-2",
"ticker":"lbl-details-2-3",
"nominal":"lbl-details-2-4",
"market":"lbl-details-2-5",
"admitted_capital":"lbl-details-2-6",
"address":"lbl-details-1-2"
}

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
            #for i in range(len(links)):
            for i in range(5): # For testing purposes
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

def browse_companies(driver,links:list):
    # Browse companies
    data = []
    #for i in range(len(links)):
    for i in range(5): # For testing purposes
        url = links[i][1]
        driver.get(url)
        data.append(get_company_data_by_id(driver))
        driver.back()
        time.sleep(randint(2, 4)) # Random sleep between 2 and 4 seconds to avoid detection
    with open("company_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
def get_company_data_by_id(driver):
    elements = []
    for field, value in company_dict.items():
        try:
            WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, value)))
            element = driver.find_element(By.ID, value)
            elements.append([field,element.text])
        except Exception as e:
            print(f'\nError {e} with field:\n {field} : {value}')
            return None
    return elements

def db_connect():
    # Connect to database
    try:
        connection = sqlite3.connect("bme.db")
        return connection
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def save_companies(connection):
    cursor = connection.cursor()
    # Create table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS company (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name varchar(50),
            isin char(12),
            ticker varchar(4),
            nominal float,
            market varchar(50),
            addmited_capital float
        )
    """)
    connection.commit()