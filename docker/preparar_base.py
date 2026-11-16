# Responsable: Gael
# Ejercicio: Parte 3: entorno reproducible
# Qué completar: Mantener este archivo coherente con las rutas, dependencias y el arranque final. Documentar únicamente resultados comprobados.

"""Prepare the inherited HuellaRed baseline; new exercises are not applied yet."""
import os
from pathlib import Path
import subprocess
import sys
import psycopg
from inicializar import preparar

ROOT = Path(__file__).resolve().parents[1]

def main():
    preparar()
    with psycopg.connect(host=os.environ['PGHOST'], port=os.environ['POSTGRES_PORT'],
                        dbname=os.environ['POSTGRES_DB'], user=os.environ['POSTGRES_USER'],
                        password=os.environ['POSTGRES_PASSWORD']) as conn:
        conn.execute('SELECT pg_advisory_xact_lock(6082026)')
        conn.execute("""CREATE TABLE IF NOT EXISTS huellared_control.cargas (
            nombre text PRIMARY KEY, terminado_en timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP
        )""")
        loaded = conn.execute("SELECT 1 FROM huellared_control.cargas WHERE nombre = %s",
                              ('huellared_p45',)).fetchone()
        if loaded:
            print('Baseline load already recorded; skipping the old loader.')
        else:
            subprocess.run([sys.executable, str(ROOT / 'base/huellared/poblar/poblar.py'),
                            '--regenerar'], check=True)
            conn.execute('INSERT INTO huellared_control.cargas(nombre) VALUES (%s)',
                         ('huellared_p45',))
            print('Baseline load recorded.')
    print('HuellaRed baseline ready. Practices 6-8 migrations, queries and export are pending.')

if __name__ == '__main__':
    main()
