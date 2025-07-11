from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
import re
import time

app = Flask(__name__)

def extraer_productos(palabra):
    url = f"https://listado.mercadolibre.com.mx/{palabra.replace(' ', '-')}"

    chrome_options = Options()
    chrome_options.add_argument("--headless")  # sin ventana
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(2)  # espera carga de JS

    productos = []
    tarjetas = driver.find_elements(By.CSS_SELECTOR, "div.ui-search-result__content-wrapper")

    for tarjeta in tarjetas:
        try:
            titulo = tarjeta.find_element(By.CSS_SELECTOR, "h2.ui-search-item__title").text
            precio = tarjeta.find_element(By.CSS_SELECTOR, "span.andes-money-amount__fraction").text
            link = tarjeta.find_element(By.CSS_SELECTOR, "a.ui-search-link").get_attribute("href")
        except:
            continue

        try:
            descuento = tarjeta.find_element(By.CSS_SELECTOR, "span.andes-money-amount__discount").text
        except:
            descuento = "0% OFF"

        match = re.search(r"(\d+)", descuento)
        porcentaje = int(match.group(1)) if match else 0

        if porcentaje >= 30:
            productos.append(f"📱 {titulo}\n💰 ${precio}\n🎯 {descuento}\n🔗 {link}")

    driver.quit()
    return productos

@app.route('/buscar', methods=['POST'])
def buscar():
    data = request.get_json()
    palabra = data.get("busqueda", "iphone")
    resultados = extraer_productos(palabra)
    return jsonify({"resultados": resultados})

@app.route('/')
def home():
    return "Servidor con Selenium funcionando"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
