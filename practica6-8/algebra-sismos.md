# Ejercicio 2.3 — Álgebra del proyecto asignado

**Responsable y autor:** Alejandro Rojas.  
**Estado:** SQL extraído del backend; álgebra, árboles y resultados pendientes.

## Fuentes y ejecución

Consultar los [fragmentos originales y su procedencia](../base/sismos/referencias/consultas-origen.md)
y el [esquema de sismos](../base/sismos/sql/00-datawarehouse_tables.sql).
Ejecutar las consultas en la base de sismos, no en HuellaRed. Mantener los bloques SQL de este documento
sincronizados con los archivos ejecutables si se modifica alguna consulta.

## Consulta 01 — Población por entidad

**Pregunta:** ¿Qué población total, femenina y masculina tiene cada entidad con código distinto de cero?

**SQL ejecutable:** [01-consulta.sql](consultas/sismos/01-consulta.sql).

```sql
SELECT
entidad,
nom_ent AS nombre,
pobtot AS poblacion_total,
pobfem AS poblacion_femenina,
pobmas AS poblacion_masculina
FROM dim_zonas
WHERE entidad != 0
ORDER BY entidad;
```

### Expresión algebraica

Pendiente: escribir la expresión, usando asignaciones intermedias si es larga. Explicar renombramientos
y cualquier extensión necesaria para representar el SQL.

### Árbol

Pendiente: dibujarlo con Mermaid aquí o enlazar una imagen real en `evidencias/sismos/2.3/01-arbol.png`.

### Operador principal

Pendiente: identificar el operador que realiza el trabajo pesado y justificarlo. No presentar una suposición
sobre costo como una medición de rendimiento.

### Resultado y observaciones

Pendiente: ejecutar en PostgreSQL y registrar el resultado observado, los parámetros y cualquier adaptación.
Si se adjunta captura, usar `evidencias/sismos/2.3/01-resultado.png` y enlazarla cuando exista.

## Consulta 02 — Producción por entidad

**Pregunta:** ¿Cuál es la producción bruta total agrupada por nombre de entidad?

**SQL ejecutable:** [02-consulta.sql](consultas/sismos/02-consulta.sql).

```sql
SELECT nombre_entidad, SUM(produccion_bruta_total) as total_produccion
FROM dim_economia
WHERE nombre_entidad IS NOT NULL
GROUP BY nombre_entidad
ORDER BY nombre_entidad;
```

### Expresión algebraica

Pendiente: escribir la expresión, usando asignaciones intermedias si es larga. Explicar renombramientos
y cualquier extensión necesaria para representar el SQL.

### Árbol

Pendiente: dibujarlo con Mermaid aquí o enlazar una imagen real en `evidencias/sismos/2.3/02-arbol.png`.

### Operador principal

Pendiente: identificar el operador que realiza el trabajo pesado y justificarlo. No presentar una suposición
sobre costo como una medición de rendimiento.

### Resultado y observaciones

Pendiente: ejecutar en PostgreSQL y registrar el resultado observado, los parámetros y cualquier adaptación.
Si se adjunta captura, usar `evidencias/sismos/2.3/02-resultado.png` y enlazarla cuando exista.

## Consulta 03 — Sismos e impacto

**Pregunta:** ¿Qué sismos de magnitud al menos 4 ocurrieron en 2017 y qué impacto tienen registrado?

**SQL ejecutable:** [03-consulta.sql](consultas/sismos/03-consulta.sql).

```sql
SELECT
ds.id_sismo,
ds.latitud,
ds.longitud,
ds.magnitud,
ds.profundidad,
ds.referencia_de_localizacion AS referencia_localizacion,
dt.fecha,
COALESCE(fis.poblacion_afectada, 0) AS poblacion_afectada,
COALESCE(fis.impacto_economico, 0) AS impacto_economico
FROM dim_sismos ds
JOIN fact_impacto_sismos_imputed fis ON ds.id_sismo = fis.id_sismo
JOIN dim_tiempo dt ON fis.id_tiempo = dt.id_tiempo
WHERE ds.magnitud >= 4.0
AND dt.anio = 2017
ORDER BY ds.magnitud DESC;
```

### Expresión algebraica

Pendiente: escribir la expresión, usando asignaciones intermedias si es larga. Explicar renombramientos
y cualquier extensión necesaria para representar el SQL.

### Árbol

Pendiente: dibujarlo con Mermaid aquí o enlazar una imagen real en `evidencias/sismos/2.3/03-arbol.png`.

### Operador principal

Pendiente: identificar el operador que realiza el trabajo pesado y justificarlo. No presentar una suposición
sobre costo como una medición de rendimiento.

### Resultado y observaciones

Pendiente: ejecutar en PostgreSQL y registrar el resultado observado, los parámetros y cualquier adaptación.
Si se adjunta captura, usar `evidencias/sismos/2.3/03-resultado.png` y enlazarla cuando exista.

## Revisión final

- [ ] Las tres consultas conservan su origen verificable.
- [ ] Cada una tiene álgebra, árbol y explicación del operador principal.
- [ ] Se explican agrupación, renombramientos, COALESCE y ORDER BY cuando aparecen.
- [ ] Los resultados corresponden a ejecuciones reales; no se alteraron filtros o duplicados sin documentarlo.
