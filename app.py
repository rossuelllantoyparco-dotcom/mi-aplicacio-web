from pathlib import Path

import joblib
import pandas as pd
from flask import Flask, jsonify, request


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "modelo_abandono.joblib"
MODEL = joblib.load(MODEL_PATH)

app = Flask(__name__)

REQUIRED_FIELDS = {
    "edad": (int, float),
    "ingreso_mensual": (int, float),
    "antiguedad_meses": (int, float),
    "consultas_soporte": (int, float),
    "gasto_mensual": (int, float),
    "tipo_plan": (str,),
    "region": (str,),
}


def validate_payload(payload):
    if not isinstance(payload, dict):
        return "El cuerpo debe ser un objeto JSON."

    missing = [field for field in REQUIRED_FIELDS if field not in payload]
    if missing:
        return f"Faltan campos obligatorios: {', '.join(missing)}."

    for field, expected_types in REQUIRED_FIELDS.items():
        value = payload[field]
        if isinstance(value, bool) or not isinstance(value, expected_types):
            expected = "número" if field not in {"tipo_plan", "region"} else "texto"
            return f"El campo '{field}' debe ser un {expected}."

    if payload["edad"] < 18 or payload["edad"] > 75:
        return "'edad' debe estar entre 18 y 75."
    if payload["ingreso_mensual"] < 0 or payload["gasto_mensual"] < 0:
        return "Los importes no pueden ser negativos."
    if payload["antiguedad_meses"] < 0 or payload["consultas_soporte"] < 0:
        return "La antigüedad y las consultas no pueden ser negativas."

    return None


@app.get("/health")
def health():
    return jsonify({"status": "ok", "modelo": MODEL_PATH.name})


@app.post("/predict")
def predict():
    payload = request.get_json(silent=True)
    error = validate_payload(payload)
    if error:
        return jsonify({"error": error}), 400

    features = pd.DataFrame([payload])
    prediction = int(MODEL.predict(features)[0])
    probability = float(MODEL.predict_proba(features)[0, 1])

    return jsonify(
        {
            "abandono": prediction,
            "etiqueta": "Abandona" if prediction else "Se queda",
            "probabilidad_abandono": round(probability, 4),
            "probabilidad_permanencia": round(1 - probability, 4),
        }
    )


@app.errorhandler(404)
def not_found(_error):
    return jsonify({"error": "Ruta no encontrada."}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
