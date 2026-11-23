"""Carga transaccional de los SQL originales en una base separada; no duplica datos."""
import hashlib
import os
from pathlib import Path
import psycopg
from psycopg import sql

ROOT = Path(__file__).resolve().parents[1]
TABLES = ["dim_zonas", "dim_tiempo", "dim_sismos", "dim_economia", "fact_impacto_sismos_imputed"]


def connection_args(database=None):
    return dict(host=os.environ["PGHOST"], port=os.environ["POSTGRES_PORT"],
                dbname=database or os.environ["POSTGRES_DB"],
                user=os.environ["POSTGRES_USER"], password=os.environ["POSTGRES_PASSWORD"])


def main():
    database = os.getenv("SISMOS_DB", "sismos")
    if database == os.environ["POSTGRES_DB"]:
        raise ValueError("SISMOS_DB debe ser distinta de POSTGRES_DB")
    with psycopg.connect(**connection_args(), autocommit=True) as conn:
        conn.execute("SELECT pg_advisory_lock(6082030)")
        try:
            if not conn.execute("SELECT 1 FROM pg_database WHERE datname=%s", (database,)).fetchone():
                conn.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(database)))
        finally:
            conn.execute("SELECT pg_advisory_unlock(6082030)")
    files = sorted((ROOT / "base/sismos/sql").glob("*.sql"))
    if len(files) != 6:
        raise ValueError("Se requieren los seis SQL originales de sismos")
    with psycopg.connect(**connection_args(database)) as conn:
        conn.execute("SELECT pg_advisory_xact_lock(6082031)")
        conn.execute("CREATE SCHEMA IF NOT EXISTS practica_control")
        conn.execute("REVOKE ALL ON SCHEMA practica_control FROM PUBLIC")
        conn.execute("""CREATE TABLE IF NOT EXISTS practica_control.cargas (
            archivo text PRIMARY KEY, sha256 text NOT NULL,
            terminado_en timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP)""")
        recorded = dict(conn.execute("SELECT archivo, sha256 FROM practica_control.cargas").fetchall())
        if not recorded and any(conn.execute("SELECT to_regclass(%s)", ("public."+t,)).fetchone()[0] for t in TABLES):
            raise ValueError("Sismos contiene tablas sin registro de carga; no se sobrescriben ni se duplican")
        for path in files:
            content = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
            digest = hashlib.sha256(content.encode()).hexdigest()
            if path.name in recorded:
                if recorded[path.name] != digest:
                    raise ValueError(f"{path.name} cambió tras cargarse; se requiere una migración")
                print(f"Sismos: ya registrado {path.name}", flush=True)
                continue
            if len(content) < 1_000_000:
                conn.execute(content)
            else:
                # Los archivos heredados contienen un INSERT completo por línea.
                batch = []
                for line in content.splitlines():
                    if not line.strip() or line.lstrip().startswith("--"):
                        continue
                    if not line.lstrip().upper().startswith("INSERT INTO ") or not line.rstrip().endswith(";"):
                        raise ValueError(f"Formato inesperado en {path.name}; se revierte la carga")
                    batch.append(line)
                    if len(batch) == 500:
                        conn.execute("\n".join(batch)); batch.clear()
                if batch:
                    conn.execute("\n".join(batch))
            conn.execute("INSERT INTO practica_control.cargas(archivo,sha256) VALUES (%s,%s)", (path.name,digest))
            print(f"Sismos: aplicado {path.name}", flush=True)
        for table in TABLES:
            count = conn.execute(sql.SQL("SELECT count(*) FROM {}").format(sql.Identifier(table))).fetchone()[0]
            if count == 0:
                raise ValueError(f"Sismos: {table} quedó vacía")
            print(f"Sismos: {table} = {count} filas", flush=True)
        conn.execute("GRANT CONNECT ON DATABASE {} TO huellared_consulta".format(sql.Identifier(database).as_string(conn)))
        conn.execute("GRANT USAGE ON SCHEMA public TO huellared_consulta")
        conn.execute("GRANT SELECT ON ALL TABLES IN SCHEMA public TO huellared_consulta")
    print("Sismos: carga confirmada.", flush=True)


if __name__ == "__main__":
    main()
