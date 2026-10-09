# API DataExpert en Docker

Esta API expone el pipeline final de Regresión Logística entrenado en `Trabajo_Final_IA_DataExpert.ipynb`.

El contenedor usa Gunicorn para servir la API de forma adecuada para un despliegue y acepta el puerto `PORT` que asigne la nube.

## Levantar el contenedor

Desde esta carpeta:

```bash
docker compose up -d --build
```

Comprobar el estado:

```bash
curl http://localhost:5000/health
```

## Probar una predicción

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "edad": 35,
    "ingreso_mensual": 3200,
    "antiguedad_meses": 24,
    "consultas_soporte": 3,
    "gasto_mensual": 180,
    "tipo_plan": "Estandar",
    "region": "Costa"
  }'
```

Detenerlo:

```bash
docker compose down
```

## Probar con Postman

Importa el archivo `DataExpert_Docker.postman_collection.json` en Postman.
La colección incluye:

- `GET /health` para verificar que el contenedor está activo.
- `POST /predict` con un ejemplo completo de entrada.

La variable `base_url` ya está configurada como `http://localhost:5000`.

## Endpoints

- `GET /health`: confirma que la API y el modelo están disponibles.
- `POST /predict`: devuelve la predicción, la etiqueta y ambas probabilidades.
