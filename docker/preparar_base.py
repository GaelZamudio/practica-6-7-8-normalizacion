# Responsable: Gael
# Ejercicio: Parte 3: entorno reproducible
# Qué completar: Mantener este archivo coherente con las rutas, dependencias y el arranque final. Documentar únicamente resultados comprobados.

"""Load the inherited baseline and apply the numbered normalization migrations."""
import hashlib
import os
import re
from pathlib import Path
import subprocess
import sys
import psycopg
from inicializar import preparar

ROOT = Path(__file__).resolve().parents[1]

def migrar_normalizacion():
    with psycopg.connect(host=os.environ['PGHOST'], port=os.environ['POSTGRES_PORT'],
                        dbname=os.environ['POSTGRES_DB'], user=os.environ['POSTGRES_USER'],
                        password=os.environ['POSTGRES_PASSWORD']) as conn:
        conn.add_notice_handler(lambda notice: print(notice.message_primary))
        conn.execute('SELECT pg_advisory_xact_lock(6082027)')
        for filename in ['002-ejemplo-desnormalizado.sql', '003-normalizar-rescates.sql']:
            path = ROOT / 'practica6-8' / 'migraciones' / filename
            name = path.relative_to(ROOT).as_posix()
            content = path.read_text(encoding='utf-8-sig').replace('\r\n', '\n')
            digest = hashlib.sha256(content.encode()).hexdigest()
            previous = conn.execute(
                'SELECT sha256 FROM huellared_control.migraciones WHERE archivo=%s',
                (name,)).fetchone()
            if previous:
                if previous[0] != digest:
                    raise ValueError(f'{name} changed after application; create a new migration.')
                print(f'Already applied: {name}')
                continue
            # Both files and their registration commit together; SQL also supports manual execution.
            sql = re.sub(r'(?m)^\s*(BEGIN|COMMIT);\s*$', '', content)
            conn.execute(sql)
            conn.execute(
                'INSERT INTO huellared_control.migraciones(archivo, sha256) VALUES (%s,%s)',
                (name, digest))
            print(f'Applied: {name}')


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
    migrar_normalizacion()
    print('HuellaRed ready; normalization example migrated. Queries and RelaX export are pending.')

if __name__ == '__main__':
    main()
