-- Ejercicio 2.2. Ejecutar primero ../../relax/muestra.sql en esta misma sesión.
-- Los resultados describen exclusivamente la muestra compartida.
-- Pregunta: ¿Qué combinaciones distintas de especie y color existen entre los animales?
-- Álgebra: π especie, color (animal)
-- Demuestra: La proyección filtra columnas y elimina duplicados: 30 animales dan 20 combinaciones. En SQL hace falta DISTINCT para igualar el álgebra.

SELECT DISTINCT especie, color
FROM animal;
