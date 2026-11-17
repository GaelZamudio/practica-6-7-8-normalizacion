-- Responsable: Alejandro (análisis 2.3); Gael (integración).
-- Ejercicio: 2.3 y Parte 3.
-- Estado: SQL extraído del backend; ejecutado en sismos (2,880 filas); álgebra y árbol completos.
-- Origen: https://github.com/GaelZamudio/Seismic-Data-Visualization-System/blob/8569667cf4f46fab640dba3f82a7b324ca7efaf7/src/std.php#L282-L297
-- Pregunta: ¿Qué sismos de magnitud al menos 4 ocurrieron en 2017 y qué impacto tienen registrado?
-- Álgebra: completa en practica6-8/algebra-sismos.md, Consulta 03.
-- Base de ejecución: sismos; no la muestra de HuellaRed.
-- Adaptación: $1 = 4.0 y $2 = 2017; parámetros explícitos de demostración, no resultados observados.

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
