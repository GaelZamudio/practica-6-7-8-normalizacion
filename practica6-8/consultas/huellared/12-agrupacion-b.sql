-- Ejercicio 2.2. Ejecutar primero ../../relax/muestra.sql en esta misma sesión.
-- Los resultados describen exclusivamente la muestra compartida.
-- Pregunta: ¿Cuántos casos, días totales y duración máxima de tratamiento hay por diagnóstico?
-- Álgebra: γ diagnostico; count(*) -> casos, sum(duracion_dias) -> dias_total, max(duracion_dias) -> mas_largo (tratamiento)
-- Demuestra: Cuatro grupos. La sarna sarcóptica es la más frecuente (4 casos); la desnutrición tiene los tratamientos más largos (hasta 60 días).

SELECT diagnostico, COUNT(*) AS casos, SUM(duracion_dias) AS dias_total, MAX(duracion_dias) AS mas_largo
FROM tratamiento
GROUP BY diagnostico
ORDER BY casos DESC, diagnostico;
