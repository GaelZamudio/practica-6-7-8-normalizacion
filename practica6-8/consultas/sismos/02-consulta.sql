-- Responsable: Alejandro (análisis 2.3); Gael (integración).
-- Ejercicio: 2.3 y Parte 3.
-- Estado: SQL extraído del backend; ejecución, álgebra y árbol pendientes.
-- Origen: https://github.com/GaelZamudio/Seismic-Data-Visualization-System/blob/8569667cf4f46fab640dba3f82a7b324ca7efaf7/src/aeconomica.php#L60-L64
-- Pregunta: ¿Cuál es la producción bruta total agrupada por nombre de entidad?
-- Álgebra: PENDIENTE, completar en practica6-8/algebra-sismos.md.
-- Base de ejecución: sismos; no la muestra de HuellaRed.
-- Adaptación: extracción de la cadena PHP y terminador SQL; misma consulta.

SELECT nombre_entidad, SUM(produccion_bruta_total) as total_produccion
FROM dim_economia
WHERE nombre_entidad IS NOT NULL
GROUP BY nombre_entidad
ORDER BY nombre_entidad;
