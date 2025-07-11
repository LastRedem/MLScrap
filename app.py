from flask import Flask, request, jsonify
import re

app = Flask(__name__)

@app.route('/buscar', methods=['POST'])
def buscar():
    data = request.get_json()
    palabra = data.get('busqueda', 'iphone')
    resultados = [
        f"📱 {palabra} 1 - $24,999 - 35% OFF",
        f"📱 {palabra} 2 - $19,499 - 40% OFF"
    ]
    return jsonify({"resultados": resultados})

@app.route('/')
def home():
    return 'Servidor funcionando'

if __name__ == '__main__':
    app.run()
