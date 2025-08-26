from flask import Flask, render_template, request, jsonify
import secrets
import string
import re

app = Flask(__name__)


def generar_contraseña(longitud=12, incluir_mayus=True, incluir_numeros=True, incluir_simbolos=True):
    caracteres = string.ascii_lowercase
    if incluir_mayus:
        caracteres += string.ascii_uppercase
    if incluir_numeros:
        caracteres += string.digits
    if incluir_simbolos:
        caracteres += string.punctuation

    return ''.join(secrets.choice(caracteres) for _ in range(longitud))


def evaluar_fuerza(password):
    puntuacion = 0
    detalles = []

    # Longitud
    if len(password) >= 12:
        puntuacion += 30
    elif len(password) >= 8:
        puntuacion += 20
    else:
        puntuacion += 10
        detalles.append("Aumenta la longitud a al menos 12 caracteres.")

    # Mayúsculas
    if re.search(r"[A-Z]", password):
        puntuacion += 15
    else:
        detalles.append("Agrega al menos una mayúscula.")

    # Minúsculas
    if re.search(r"[a-z]", password):
        puntuacion += 15
    else:
        detalles.append("Agrega al menos una minúscula.")

    # Números
    if re.search(r"[0-9]", password):
        puntuacion += 15
    else:
        detalles.append("Agrega al menos un número.")

    # Símbolos
    if re.search(r"[^A-Za-z0-9]", password):
        puntuacion += 25
    else:
        detalles.append("Agrega al menos un símbolo.")

    # Clasificación
    if puntuacion >= 80:
        fuerza = "fuerte"
    elif puntuacion >= 50:
        fuerza = "media"
    else:
        fuerza = "débil"

    return {"fuerza": fuerza, "puntuacion": puntuacion, "detalles": detalles}


@app.route("/", methods=["GET", "POST"])
def home():
    password = None
    if request.method == "POST":
        longitud = int(request.form.get("longitud", 12))
        incluir_mayus = "mayus" in request.form
        incluir_numeros = "numeros" in request.form
        incluir_simbolos = "simbolos" in request.form

        password = generar_contraseña(longitud, incluir_mayus, incluir_numeros, incluir_simbolos)

    return render_template("index.html", password=password)


# 🔹 API para validar fuerza de contraseña
@app.route("/api/fuerza", methods=["GET"])
def api_fuerza():
    password = request.args.get("password", "")
    if not password:
        return jsonify({"error": "Debes enviar el parámetro 'password'"}), 400

    resultado = evaluar_fuerza(password)
    return jsonify(resultado)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8090, debug=True)

