# Responsable: Gael
# Ejercicio: Parte 3: entorno reproducible

FROM python:3.13-slim
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY base/huellared ./base/huellared
COPY docker ./docker

COPY practica6-8/migraciones ./practica6-8/migraciones
COPY practica6-8/relax/exportar-grupo.py ./practica6-8/relax/exportar-grupo.py

COPY base/sismos/sql ./base/sismos/sql
COPY practica6-8/relax/grupo.txt practica6-8/relax/muestra.sql practica6-8/relax/resumen.json ./practica6-8/relax/
COPY practica6-8/consultas ./practica6-8/consultas
COPY practica6-8/integrantes ./practica6-8/integrantes
COPY practica6-8/algebra.md practica6-8/algebra-sismos.md ./practica6-8/
