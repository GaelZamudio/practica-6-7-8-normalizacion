# Consultas originales para el ejercicio 2.3

**Responsable:** Alejandro. **Integración:** Gael. SQL, análisis y resultados documentados en algebra-sismos.md.
Origen: https://github.com/GaelZamudio/Seismic-Data-Visualization-System, HEAD local `8569667cf4f46fab640dba3f82a7b324ca7efaf7`. Se extrajeron solo las cadenas SQL de los archivos PHP locales;
no se copiaron sus credenciales. La selección puede revisarse justificando cualquier cambio.

## Consulta 01

**Pregunta:** ¿Qué población total, femenina y masculina tiene cada entidad con código distinto de cero?
**Fuente:** [src/std2.php, líneas 260–268](https://github.com/GaelZamudio/Seismic-Data-Visualization-System/blob/8569667cf4f46fab640dba3f82a7b324ca7efaf7/src/std2.php#L260-L268).
**Archivo ejecutable:** [01-consulta.sql](../../../practica6-8/consultas/sismos/01-consulta.sql).

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

La extracción solo elimina la envoltura PHP y añade el terminador SQL.

## Consulta 02

**Pregunta:** ¿Cuál es la producción bruta total agrupada por nombre de entidad?
**Fuente:** [src/aeconomica.php, líneas 60–64](https://github.com/GaelZamudio/Seismic-Data-Visualization-System/blob/8569667cf4f46fab640dba3f82a7b324ca7efaf7/src/aeconomica.php#L60-L64).
**Archivo ejecutable:** [02-consulta.sql](../../../practica6-8/consultas/sismos/02-consulta.sql).

```sql
SELECT nombre_entidad, SUM(produccion_bruta_total) as total_produccion 
            FROM dim_economia 
            WHERE nombre_entidad IS NOT NULL 
            GROUP BY nombre_entidad 
            ORDER BY nombre_entidad;
```

La extracción solo elimina la envoltura PHP y añade el terminador SQL.

## Consulta 03

**Pregunta:** ¿Qué sismos de magnitud al menos 4 ocurrieron en 2017 y qué impacto tienen registrado?
**Fuente:** [src/std.php, líneas 282–297](https://github.com/GaelZamudio/Seismic-Data-Visualization-System/blob/8569667cf4f46fab640dba3f82a7b324ca7efaf7/src/std.php#L282-L297).
**Archivo ejecutable:** [03-consulta.sql](../../../practica6-8/consultas/sismos/03-consulta.sql).

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
            WHERE ds.magnitud >= $1 
            AND dt.anio = $2
            ORDER BY ds.magnitud DESC;
```

Para el archivo ejecutable se fijaron `$1 = 4.0` y `$2 = 2017`. Mantener esos valores al comparar resultados.

## Análisis y resultados

Las expresiones, árboles y resultados se documentan en [algebra-sismos.md](../../../practica6-8/algebra-sismos.md). Se conservan los filtros, las columnas y la semántica de las consultas originales.
