import sqlite3
import datetime
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
import time

# Configurar Firefox
options = Options()
options.headless = False  # Si quieres ejecutarlo sin abrir navegador, cambia a True

# Inicializar WebDriver de Firefox
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)

# URL del IBEX 35 en Bolsas y Mercados Españoles (BME)
url = "https://www.bolsasymercados.es/bme-exchange/es/Mercados-y-Cotizaciones/Acciones/Mercado-Continuo/Precios/ibex-35-ES0SI0000005"
driver.get(url)

# Esperar a que la página cargue completamente
time.sleep(3)






# # Conectar a SQLite y crear la tabla si no existe
# conn = sqlite3.connect("ibex35.db")  # Base de datos local SQLite
# cursor = conn.cursor()

# cursor.execute("""
# CREATE TABLE IF NOT EXISTS ibex35 (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     nombre TEXT,
#     precio REAL,
#     variacion REAL,
#     porcentaje REAL,
#     volumen INTEGER,
#     fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# )
# """)

# # Extraer todas las filas de la tabla de cotizaciones
# rows = driver.find_elements(By.XPATH, '//table[contains(@class, "table")]/tbody/tr')

# # Insertar datos en SQLite
# for row in rows:
#     try:
#         nombre = row.find_element(By.XPATH, './td[1]').text  # Nombre de la empresa
#         precio = float(row.find_element(By.XPATH, './td[2]').text.replace(',', '.'))  # Último precio
#         variacion = float(row.find_element(By.XPATH, './td[3]').text.replace(',', '.').replace('%', ''))  # Variación absoluta
#         porcentaje = float(row.find_element(By.XPATH, './td[4]').text.replace('%', '').replace(',', '.'))  # Variación %
#         volumen = int(row.find_element(By.XPATH, './td[5]').text.replace('.', ''))  # Volumen sin puntos

#         cursor.execute("""
#         INSERT INTO ibex35 (nombre, precio, variacion, porcentaje, volumen) 
#         VALUES (?, ?, ?, ?, ?)""", (nombre, precio, variacion, porcentaje, volumen))

#     except Exception as e:
#         print("Error extrayendo datos de una fila:", e)

# # Guardar cambios y cerrar la conexión con la BD
# conn.commit()
# conn.close()
# Cerrar el navegador
# driver.quit()

# print("Datos guardados en SQLite correctamente.")






# Extraer todas las filas de la tabla de cotizaciones
rows = driver.find_elements(By.XPATH, '//table[contains(@class, "table")]/tbody/tr')

# Iterar sobre las filas y extraer información de cada acción
data = []
for row in rows:
    try:
        # Extraer cada celda
        # nombre = row.find_element(By.XPATH, './td[1]').text  # Nombre de la empresa
        # precio = row.find_element(By.XPATH, './td[2]').text  # Último precio
        # variacion = row.find_element(By.XPATH, './td[3]').text  # Variación absoluta
        # porcentaje = row.find_element(By.XPATH, './td[4]').text  # Variación porcentual
        # volumen = row.find_element(By.XPATH, './td[5]').text  # Volumen negociado
        name = row.find_element(By.CLASS_NAME,'text-nowrap ').text  # Nombre de la empresa
        last_val = row.find_element(By.XPATH, './td[2]').text  # Último precio
        # Guardar en lista
        #data.append(name, last_val)
        # Imprimir en consola
        # print(f"Empresa: {nombre}, Precio: {precio}, Variación: {variacion}, %: {porcentaje}, Volumen: {volumen}")
        print(f"Empresa: {name}, Último: {last_val}")
    except Exception as e:
        print("Error extrayendo datos de una fila:", e)

# Cerrar el navegador
driver.quit()