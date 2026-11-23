-- Ejercicio 2.2. Ejecutar primero ../../relax/muestra.sql en esta misma sesión.
-- Los resultados describen exclusivamente la muestra compartida.
-- Pregunta: ¿A qué hogares temporales podría pasar cada animal en atención, según las especies que el hogar acepta?
-- Álgebra: hogares = ρ especie_hogar ← especie (hogar_especie)
-- Álgebra: en_atencion = σ estado_actual = 'en_atencion' (animal)
-- Álgebra: π id_animal, nombre, especie, id_hogar (en_atencion ⨝ especie = especie_hogar hogares)
-- Demuestra: Se especifica explícitamente la condición especie = especie_hogar: es una reunión theta de igualdad. La reunión natural compara todos los atributos homónimos y no requiere una FK. Se renombra especie para hacer explícita la comparación. Un animal en atención cuya especie ningún hogar acepta no aparecería; en esta muestra los 6 tienen al menos un hogar compatible.

SELECT DISTINCT a.id_animal, a.nombre, a.especie, he.id_hogar
FROM animal a
JOIN hogar_especie he ON a.especie = he.especie
WHERE a.estado_actual = 'en_atencion';
