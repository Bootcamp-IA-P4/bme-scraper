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
options.headless = False  # Cambia a True para ejecución en segundo plano

# Inicializar WebDriver de Firefox
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)

# URL del IBEX 35 en Bolsas y Mercados Españoles (BME)
url = "https://www.bolsasymercados.es/bme-exchange/es/Mercados-y-Cotizaciones/Acciones/Mercado-Continuo/Precios/ibex-35-ES0SI0000005"
driver.get(url)

# Esperar que la tabla cargue
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//table[contains(@class, "table")]'))
)
print("Tabla encontrada.")

# Extraer todos los enlaces dentro de la tabla
links = driver.find_elements(By.XPATH, '//table[contains(@class, "table")]/tbody/tr/td[1]/a')

# Recorrer los enlaces y hacer clic en cada uno
for i in range(len(links)):
    try:
        # Recolectar los enlaces de nuevo en cada iteración (la página cambia después de cada click)
        links = driver.find_elements(By.XPATH, '//table[contains(@class, "table")]/tbody/tr/td[1]/a')

        # Obtener el texto y la URL del enlace
        link_text = links[i].text
        link_href = links[i].get_attribute("href")

        print(f"\nHaciendo clic en: {link_text} ({link_href})")

        # Abrir el enlace en la misma pestaña
        driver.execute_script("arguments[0].click();", links[i])

        # Esperar a que cargue la nueva página
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # Extraer datos de la nueva página (ejemplo: título de la acción)
        titulo = driver.find_element(By.TAG_NAME, "h1").text
        print(f"Título de la página: {titulo}")

        # Volver atrás a la tabla
        driver.back()

        # Esperar que la tabla recargue antes de seguir con el siguiente enlace
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//table[contains(@class, "table")]'))
        )
        print("Volviendo a la tabla...")

    except Exception as e:
        print(f"Error con el enlace {link_text}: {e}")

# Cerrar el navegador
driver.quit()

print("\nScraping completado.")
