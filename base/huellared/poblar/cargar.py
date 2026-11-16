# Responsable: Gael
# Ejercicio: Base heredada de prácticas 4–5; entrada para 1.1–1.3 y Parte 3
# Qué completar: Conservar las reglas y datos de origen. No resolver la normalización editando esta base; implementar cambios en practica6-8/migraciones. Revisar rutas y compatibilidad al integrar. Este encabezado es documentación nueva; el cuerpo es heredado.

"""Entrada de carga SQL con el usuario de aplicación (ejercicio 1.6)."""
import argparse
import os
from pathlib import Path

import psycopg


def conectar():
    # Las credenciales del administrador nunca se usan para cargar datos.
    return psycopg.connect(
        host=os.environ.get("PGHOST", "localhost"),
        port=os.environ["POSTGRES_PORT"],
        dbname=os.environ["POSTGRES_DB"],
        user="huellared_app",
        password=os.environ["HUELLARED_APP_PASSWORD"],
    )


def cargar(archivo, prueba=False):
    contenido = Path(archivo).read_text(encoding="utf-8-sig")
    with conectar() as conn:
        identidad = conn.execute("SELECT current_user, session_user").fetchone()
        print(f"Carga: current_user={identidad[0]}, session_user={identidad[1]}")
        cursor = conn.execute(contenido)
        while True:
            print(cursor.statusmessage)
            if not cursor.nextset():
                break
        if prueba:
            conn.rollback()
            print("ROLLBACK: carga de prueba revertida.")
    if not prueba:
        print("COMMIT: carga confirmada.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archivo", help="SQL de datos, sin BEGIN/COMMIT/ROLLBACK ni órdenes de psql")
    parser.add_argument("--prueba", action="store_true", help="Ejecutar y revertir la carga")
    args = parser.parse_args()
    try:
        cargar(args.archivo, args.prueba)
    except KeyError as exc:
        raise SystemExit(f"Falta la variable de entorno {exc.args[0]}") from None
    except psycopg.Error as exc:
        raise SystemExit(f"Carga revertida. SQLSTATE={exc.sqlstate}; "
                         f"{exc.diag.message_primary or 'No se pudo conectar'}") from None
