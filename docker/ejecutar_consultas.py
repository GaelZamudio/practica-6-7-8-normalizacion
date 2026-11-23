"""Parte 3: preguntas, álgebra y resultados completos, en orden y solo lectura."""
import csv
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import psycopg

ROOT = Path(__file__).resolve().parents[1]
PRACTICA = ROOT / "practica6-8"
OUTPUT = Path(os.getenv("OUTPUT_DIR", str(ROOT / "salida")))


def metadata(path):
    records = []
    text = path.read_text(encoding="utf-8-sig")
    for part in re.split(r"(?m)^## ", text)[1:]:
        title = part.splitlines()[0]
        sql_blocks = re.findall(r"```sql\s*\n(.*?)```", part, re.S)
        if not sql_blocks:
            continue
        question = re.search(r"\*\*Pregunta(?: del dominio)?:\*\*\s*([^\n]+)", part)
        if not question:
            question_text = re.sub(r"^Consulta \d+\s*[—–-]\s*", "", title)
        else:
            question_text = question.group(1).strip()
        algebra = re.findall(r"```(?:text|relalg)?[ \t]*\n(.*?)```", part, re.S)
        records.append(dict(pregunta=question_text, algebra=algebra[0].strip() if algebra else None))
    return records


def has_sql(path):
    return bool(re.sub(r"(?m)--[^\n]*", "", path.read_text(encoding="utf-8-sig")).strip())


def connect(database):
    return psycopg.connect(host=os.environ["PGHOST"], port=os.environ["POSTGRES_PORT"],
                          dbname=database, user="huellared_consulta",
                          password=os.environ["HUELLARED_CONSULTA_PASSWORD"], autocommit=True)


def run_file(conn, path, records, label, report):
    if not has_sql(path):
        return
    cur = conn.execute(path.read_text(encoding="utf-8-sig"))
    index = 0
    while True:
        if cur.description is not None:
            index += 1
            if index > len(records):
                raise ValueError(f"{path.name}: falta pregunta/documentación para el resultado {index}")
            entry = dict(records[index-1])
            entry.update(archivo=path.relative_to(ROOT).as_posix(), consulta=index)
            if not entry["algebra"]:
                raise ValueError(f"{path.name}: cada consulta ejecutable debe incluir una expresión algebraica")
            print(f"\n=== {label} / {index} ===\nPregunta: {entry['pregunta']}\nÁlgebra:\n{entry['algebra']}", flush=True)
            columns = [c.name for c in cur.description]
            print(" | ".join(columns), flush=True)
            name = label.replace("/", "-") + f"-{index:02d}.csv"
            count = 0
            with (OUTPUT / name).open("w",encoding="utf-8",newline="") as f:
                writer = csv.writer(f); writer.writerow(columns)
                for row in cur:
                    writer.writerow(["NULL" if v is None else v for v in row])
                    print(" | ".join("NULL" if v is None else str(v) for v in row))
                    count += 1
            print(f"Filas: {count} | CSV: salida/{name}", flush=True)
            entry.update(filas=count,columnas=columns,csv=name)
            report.append(entry)
        if not cur.nextset():
            break
    if index != len(records):
        raise ValueError(f"{path.name}: número de resultados distinto al documento")


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    # Un fallo no debe dejar un resumen anterior que parezca corresponder a esta ejecución.
    summary = OUTPUT / "resultados.json"
    summary.unlink(missing_ok=True)
    report = []
    with connect(os.environ["POSTGRES_DB"]) as conn:
        conn.execute((PRACTICA / "relax/muestra.sql").read_text(encoding="utf-8-sig"))
        conn.execute("SET default_transaction_read_only = on")
        records = metadata(PRACTICA / "algebra.md")
        files = sorted((PRACTICA / "consultas/huellared").glob("*.sql"))
        if len(files) != 13 or len(records) != 13:
            raise ValueError("Se requieren las 13 consultas documentadas del ejercicio 2.2")
        for path, record in zip(files, records):
            run_file(conn,path,[record],"huellared/"+path.stem,report)
        for path in sorted((PRACTICA / "integrantes").glob("*.sql"), key=lambda p: p.name.casefold()):
            records = metadata(path.with_suffix(".md"))
            if has_sql(path) and len(records) != 3:
                raise ValueError(f"{path.name}: se requieren tres consultas documentadas")
            run_file(conn,path,records,"individual/"+path.stem,report)
    with connect(os.getenv("SISMOS_DB", "sismos")) as conn:
        conn.execute("SET default_transaction_read_only = on")
        records = metadata(PRACTICA / "algebra-sismos.md")
        files = sorted((PRACTICA / "consultas/sismos").glob("*.sql"))
        if len(files) != 3 or len(records) != 3:
            raise ValueError("Se requieren las tres consultas documentadas de sismos")
        for path, record in zip(files, records):
            run_file(conn,path,[record],"sismos/"+path.stem,report)
    subprocess.run([sys.executable, str(PRACTICA / "relax/exportar-grupo.py"),
                    "--destino", str(OUTPUT / "relax")], check=True)
    original = (PRACTICA / "relax/grupo.txt").read_text(encoding="utf-8-sig").encode("utf-8")
    generated = (OUTPUT / "relax/grupo.txt").read_text(encoding="utf-8-sig").encode("utf-8")
    matches = original == generated
    print(f"Grupo regenerado desde PostgreSQL: salida/relax/grupo.txt. Igual al versionado: {matches}")
    if not matches:
        print("La selección regenerada difiere; las consultas usaron la muestra versionada de las capturas, que no se sobrescribió.")
    result = dict(consultas=report,
                  grupo_consultado_sha256=hashlib.sha256(original).hexdigest(),
                  grupo_regenerado_sha256=hashlib.sha256(generated).hexdigest())
    summary.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"PARTE 3: {len(report)} consultas ejecutadas. Fin sin errores SQL.")


if __name__ == "__main__":
    main()
