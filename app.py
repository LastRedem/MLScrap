from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import re
import os

app = Flask(__name__)

def extraer_productos(palabra):
    url = f"https://listado.mercadolibre.com.mx/{palabra.replace(' ', '-')}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    productos_html = soup.select("li.ui-search-layout__item")

    productos = []

    for producto in productos_html:
        try:
            titulo = producto.select_one("a.ui-search-item__group__element").text.strip()
            url_producto = producto.select_one("a.ui-search-item__group__element")["href"]
        except:
            continue

        try:
            precio = producto.select_one("span.andes-money-amount__fraction").text.strip()
        except:
            precio = "No disponible"

        try:
            descuento_raw = producto.select_one("span.andes-money-amount__discount")
            descuento = descuento_raw.text.strip() if descuento_raw else "0% OFF"
        except:
            descuento = "0% OFF"

        # Extraer número del descuento
        match = re.search(r"(\d+)", descuento)
        porcentaje = int(match.group(1)) if match else 0

        if porcentaje > 30:
            productos.append(f"📱 {titulo}\n💰 ${precio}\n🎯 {descuento}\n🔗 {url_producto}")

    return productos

@app.route('/buscar', methods=['POST'])
def buscar():
    data = request.get_json()
    palabra = data.get("busqueda", "iphone")
    resultados = extraer_productos(palabra)
    return jsonify({"resultados": resultados})

@app.route('/')
def home():
    return "Servidor funcionando con BeautifulSoup"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
