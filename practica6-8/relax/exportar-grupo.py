#!/usr/bin/env python3
"""Ejercicio 2.1 — Gael Zamudio. Exporta una muestra real de HuellaRed a RelaX.
No modifica PostgreSQL: selecciona filas y comprueba límites, PK y todas las FK.
"""
import argparse
import hashlib
import json
import math
import os
from datetime import datetime
from decimal import Decimal
from pathlib import Path
import re

import numpy as np
import psycopg
from psycopg import sql
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_matrix
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]


def read_database(conn):
    tables = {}
    for (name,) in conn.execute("SELECT tablename FROM pg_tables WHERE schemaname='public' ORDER BY tablename"):
        if not re.fullmatch(r'[a-z_][a-z_0-9]*', name):
            raise ValueError(f'Nombre de tabla no compatible: {name}')
        columns = conn.execute("""
            SELECT a.attname, COALESCE(b.typname,t.typname), t.typcategory
            FROM pg_attribute a JOIN pg_type t ON t.oid=a.atttypid
            LEFT JOIN pg_type b ON b.oid=NULLIF(t.typbasetype,0)
            WHERE a.attrelid=%s::regclass AND a.attnum>0 AND NOT a.attisdropped
            ORDER BY a.attnum
        """, (f'public.{name}',)).fetchall()
        pk = conn.execute("""
            SELECT a.attname FROM pg_constraint c
            CROSS JOIN LATERAL unnest(c.conkey) WITH ORDINALITY k(attnum,ord)
            JOIN pg_attribute a ON a.attrelid=c.conrelid AND a.attnum=k.attnum
            WHERE c.conrelid=%s::regclass AND c.contype='p' ORDER BY k.ord
        """, (f'public.{name}',)).fetchall()
        if not pk:
            raise ValueError(f'{name} necesita PK para ordenar e identificar la muestra.')
        pk = [x[0] for x in pk]
        names = [c[0] for c in columns]
        types = []
        for col, typ, category in columns:
            if not re.fullmatch(r'[a-z_][a-z_0-9]*', col):
                raise ValueError(f'Nombre de columna no compatible: {name}.{col}')
            if typ in ('int2','int4','int8','float4','float8','numeric'): kind = 'number'
            elif typ == 'bool': kind = 'boolean'
            elif typ == 'date': kind = 'date'
            elif typ in ('text','varchar','bpchar','timestamp','timestamptz') or category == 'E': kind = 'string'
            else: raise ValueError(f'Tipo sin conversión definida: {name}.{col} ({typ})')
            types.append(kind)
        query = sql.SQL('SELECT {} FROM public.{} ORDER BY {}').format(
            sql.SQL(',').join(map(sql.Identifier,names)), sql.Identifier(name),
            sql.SQL(',').join(map(sql.Identifier,pk)))
        rows = conn.execute(query).fetchall()
        tables[name] = {'columns': names, 'types': types, 'pk': pk, 'rows': rows}
    fks = conn.execute("""
        SELECT c.conname, child.relname, pn.nspname, parent.relname,
            ARRAY(SELECT a.attname FROM unnest(c.conkey) WITH ORDINALITY k(n,o)
                  JOIN pg_attribute a ON a.attrelid=c.conrelid AND a.attnum=k.n ORDER BY k.o),
            ARRAY(SELECT a.attname FROM unnest(c.confkey) WITH ORDINALITY k(n,o)
                  JOIN pg_attribute a ON a.attrelid=c.confrelid AND a.attnum=k.n ORDER BY k.o)
        FROM pg_constraint c JOIN pg_class child ON child.oid=c.conrelid
        JOIN pg_namespace cn ON cn.oid=child.relnamespace
        JOIN pg_class parent ON parent.oid=c.confrelid
        JOIN pg_namespace pn ON pn.oid=parent.relnamespace
        WHERE c.contype='f' AND cn.nspname='public' ORDER BY c.conname
    """).fetchall()
    return tables, fks


def sample(tables, fks, minimum, maximum):
    if not tables: raise ValueError('No hay tablas en public. Ejecuta primero la carga.')
    offset, total = {}, 0
    for name,t in tables.items():
        if len(t['rows']) < minimum:
            raise ValueError(f'{name}: solo hay {len(t["rows"])} filas; se requieren {minimum}. No se inventarán datos.')
        offset[name], total = total, total + len(t['rows'])
    rowidx, colidx, values, lower, upper = [], [], [], [], []
    def constraint(terms, lo, hi):
        row = len(lower)
        for col,val in terms:
            rowidx.append(row); colidx.append(col); values.append(val)
        lower.append(lo); upper.append(hi)
    for name,t in tables.items():
        constraint(((offset[name]+i,1) for i in range(len(t['rows']))),minimum,maximum)
    edges = []
    for fk, child, schema, parent, ccols, pcols in fks:
        if schema != 'public' or parent not in tables:
            raise ValueError(f'{fk} referencia fuera de la muestra: {schema}.{parent}')
        ct,pt = tables[child],tables[parent]
        ci = [ct['columns'].index(c) for c in ccols]
        pi = [pt['columns'].index(c) for c in pcols]
        lookup = {tuple(r[j] for j in pi):offset[parent]+i for i,r in enumerate(pt['rows'])}
        for i,r in enumerate(ct['rows']):
            key = tuple(r[j] for j in ci)
            if any(v is None for v in key): continue  # MATCH SIMPLE: referencia opcional.
            if key not in lookup: raise ValueError(f'FK inválida en origen: {fk}, {key}')
            a,b = offset[child]+i, lookup[key]
            edges.append((a,b,fk))
            if a != b: constraint(((a,1),(b,-1)),-np.inf,0)
    # Una variable 0/1 por fila. Hija seleccionada implica padre seleccionado.
    matrix = coo_matrix((values,(rowidx,colidx)),shape=(len(lower),total)).tocsc()
    result = milp(c=1+np.arange(total)/max(total,1)*0.001,
                  integrality=np.ones(total), bounds=Bounds(0,1),
                  constraints=LinearConstraint(matrix,lower,upper),
                  options={'time_limit':60,'mip_rel_gap':0.01})
    if result.x is None:
        raise ValueError('No se obtuvo una muestra con esos límites y todas las FK. '
                         'Puede ser inviable o agotarse el límite de 60 s; no se escribió una muestra incompleta.')
    chosen = result.x > 0.5
    for a,b,fk in edges:
        if chosen[a] and not chosen[b]: raise ValueError(f'El resultado viola {fk}')
    output = {}
    for name,t in tables.items():
        rows = [r for i,r in enumerate(t['rows']) if chosen[offset[name]+i]]
        if not minimum <= len(rows) <= maximum: raise ValueError(f'Límite incumplido: {name}')
        pkidx = [t['columns'].index(c) for c in t['pk']]
        if len({tuple(r[j] for j in pkidx) for r in rows}) != len(rows):
            raise ValueError(f'PK duplicada: {name}')
        output[name] = {**t, 'rows': rows}
    return output


def text_value(value):
    return value.isoformat(sep=' ') if isinstance(value,datetime) else str(value)


def relax_literal(value, kind):
    if value is None: return 'null'
    if kind == 'boolean': return 'true' if value else 'false'
    if kind == 'date': return value.isoformat()
    if kind == 'number':
        if not math.isfinite(float(value)) or abs(value)>2**53-1:
            raise ValueError(f'Número fuera del rango seguro de RelaX: {value}')
        return format(Decimal(str(value)),'f') if not isinstance(value,int) else str(value)
    text = text_value(value)
    # La gramática oficial no interpreta escapes dentro de tablas inline.
    if '\n' in text or '\r' in text or ("'" in text and '"' in text):
        raise ValueError('RelaX no admite sin transformación un texto con saltos de línea o ambos tipos de comillas. No se alteró el dato.')
    quote = '"' if "'" in text else "'"
    return quote+text+quote


def render(tables, fks, minimum, maximum, dbname):
    group = ['group: HuellaRed - practicas 6-8',
             f'description: Muestra sintetica exportada de PostgreSQL; {len(tables)} tablas operativas, con referencias conservadas. fecha_hora es string ISO.', '']
    sql_lines = ['-- Muestra exacta del grupo de RelaX. Gael Zamudio, ejercicio 2.1.',
                 '-- Ejecutar en una sesión NUEVA de pgAdmin con permiso TEMP.',
                 '-- Crea solo tablas temporales; no cambia public. Consultar nombres sin public.',
                 '-- Cerrar esta sesión elimina la muestra. No repetir en la misma sesión.', 'BEGIN;']
    counts = {}
    for name,t in tables.items():
        counts[name] = len(t['rows'])
        header = ', '.join(f'{c}:{k}' for c,k in zip(t['columns'],t['types']))
        group.append(f'{name} = {{ {header}')
        group.extend('  '+', '.join(relax_literal(v,k) for v,k in zip(row,t['types'])) for row in t['rows'])
        group.extend(['}', ''])
        sqltypes = {'number':'numeric','boolean':'boolean','date':'date','string':'text'}
        definitions = ', '.join(f'"{c}" {sqltypes[k]}' for c,k in zip(t['columns'],t['types']))
        sql_lines.append(f'CREATE TEMP TABLE "{name}" ({definitions}) ON COMMIT PRESERVE ROWS;')
        vals = []
        for row in t['rows']:
            cells = []
            for v,k in zip(row,t['types']):
                if v is None: cell = 'NULL'
                elif k == 'boolean': cell = 'TRUE' if v else 'FALSE'
                elif k == 'number': cell = str(v)
                else: cell = "'"+text_value(v).replace("'","''")+"'"
                cells.append(cell)
            vals.append('('+', '.join(cells)+')')
        sql_lines.append(f'INSERT INTO "{name}" VALUES\n'+',\n'.join(vals)+';')
    sql_lines.append('COMMIT;')
    group = '\n'.join(group)
    manifest = {'database':dbname,'schema':'public','minimum':minimum,'maximum':maximum,
                'rows':counts,'total_rows':sum(counts.values()),'foreign_keys_checked':len(fks),
                'group_sha256':hashlib.sha256(group.encode('utf-8')).hexdigest()}
    return {'grupo.txt':group, 'muestra.sql':'\n'.join(sql_lines)+'\n',
            'resumen.json':json.dumps(manifest,ensure_ascii=False,indent=2)+'\n'}


def main():
    load_dotenv(ROOT/'.env',override=False)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destino',type=Path,default=Path(__file__).resolve().parent)
    parser.add_argument('--minimo',type=int,default=10)
    parser.add_argument('--maximo',type=int,default=30)
    args = parser.parse_args()
    if not 10 <= args.minimo <= args.maximo <= 30:
        raise ValueError('La práctica exige entre 10 y 30 filas por tabla.')
    with psycopg.connect(host=os.getenv('PGHOST','127.0.0.1'),port=os.getenv('POSTGRES_PORT','5434'),
                        dbname=os.getenv('POSTGRES_DB','huellared'),
                        user=os.getenv('PGUSER','huellared_consulta'),
                        password=os.getenv('PGPASSWORD',os.getenv('HUELLARED_CONSULTA_PASSWORD','p678_consulta_demo')),
                        connect_timeout=10) as conn:
        conn.execute('SET TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY')
        tables,fks = read_database(conn)
        selected = sample(tables,fks,args.minimo,args.maximo)
        files = render(selected,fks,args.minimo,args.maximo,conn.info.dbname)
    args.destino.mkdir(parents=True,exist_ok=True)
    for name,content in files.items():
        tmp = args.destino/(name+'.tmp')
        tmp.write_text(content,encoding='utf-8',newline='\n')
        tmp.replace(args.destino/name)
    for name,t in selected.items(): print(f'{name:24s} {len(t["rows"]):2d} filas')
    print(f'Exportadas {len(selected)} tablas; {len(fks)} FK verificadas. Destino: {args.destino}')


if __name__ == '__main__':
    try: main()
    except (ValueError,psycopg.Error,OSError) as exc:
        raise SystemExit(f'Exportación cancelada: {exc}') from None
