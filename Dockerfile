# Responsable: Gael
# Ejercicio: Parte 3: entorno reproducible
# Qué completar: Mantener este archivo coherente con las rutas, dependencias y el arranque final. Documentar únicamente resultados comprobados.

FROM python:3.13-slim
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY base/huellared ./base/huellared
COPY docker ./docker

COPY practica6-8/migraciones ./practica6-8/migraciones
