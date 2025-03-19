from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager

# Configurar Firefox
options = Options()
options.headless = False  # Cambia a True si no quieres abrir la ventana del navegador

# Inicializar WebDriver de Firefox
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)

# URL de la página donde está la tabla
url = "https://www.bolsasymercados.es/bme-exchange/es/Mercados-y-Cotizaciones/Acciones/Mercado-Continuo/Precios/ibex-35-ES0SI0000005"
driver.get(url)

# Esperar a que la tabla esté disponible
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "details-table"))
)

# Encontrar la tabla
tabla = driver.find_element(By.CLASS_NAME, "details-table")

# Extraer todas las filas de la tabla
filas = tabla.find_elements(By.TAG_NAME, "tr")

# Guardar los datos en una lista
datos = []

for fila in filas:
    # Obtener todas las celdas de la fila (pueden ser <th> o <td>)
    celdas = fila.find_elements(By.XPATH, ".//td | .//th")

    # Extraer el texto de cada celda
    fila_datos = [celda.text.strip() for celda in celdas]

    # Guardar la fila si no está vacía
    if fila_datos:
        datos.append(fila_datos)

# Imprimir los datos obtenidos
for fila in datos:
    print(fila)

# Cerrar el navegador
driver.quit()
