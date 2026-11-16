-- Responsable: Alejandro (análisis 2.3); Gael (integración).
-- Ejercicio: 2.3 y Parte 3.
-- Estado: SQL extraído del backend; ejecución, álgebra y árbol pendientes.
-- Origen: https://github.com/GaelZamudio/Seismic-Data-Visualization-System/blob/8569667cf4f46fab640dba3f82a7b324ca7efaf7/src/std2.php#L260-L268
-- Pregunta: ¿Qué población total, femenina y masculina tiene cada entidad con código distinto de cero?
-- Álgebra: PENDIENTE, completar en practica6-8/algebra-sismos.md.
-- Base de ejecución: sismos; no la muestra de HuellaRed.
-- Adaptación: extracción de la cadena PHP y terminador SQL; misma consulta.

SELECT
entidad,
nom_ent AS nombre,
pobtot AS poblacion_total,
pobfem AS poblacion_femenina,
pobmas AS poblacion_masculina
FROM dim_zonas
WHERE entidad != 0
ORDER BY entidad;
