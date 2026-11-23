-- Ejercicio 2.2. Ejecutar primero ../../relax/muestra.sql en esta misma sesión.
-- Los resultados describen exclusivamente la muestra compartida.
-- Pregunta: ¿Cuántos animales hay en cada estado del proceso de rescate?
-- Álgebra: γ estado_actual; count(*) -> total (animal)
-- Demuestra: Un resumen por grupo: cinco grupos (uno por estado), con 12 animales adoptados como el grupo mayor.

SELECT estado_actual, COUNT(*) AS total
FROM animal
GROUP BY estado_actual
ORDER BY total DESC;
