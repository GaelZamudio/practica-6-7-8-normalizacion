-- Ejercicio 2.2. Ejecutar primero ../../relax/muestra.sql en esta misma sesión.
-- Los resultados describen exclusivamente la muestra compartida.
-- Pregunta: ¿Qué animales están disponibles para adopción?
-- Álgebra: σ estado_actual = 'disponible_adopcion' (animal)
-- Demuestra: La selección filtra filas y conserva todas las columnas.

SELECT *
FROM animal
WHERE estado_actual = 'disponible_adopcion';
