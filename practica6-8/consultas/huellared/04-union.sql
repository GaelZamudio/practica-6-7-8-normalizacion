-- Ejercicio 2.2. Ejecutar primero ../../relax/muestra.sql en esta misma sesión.
-- Los resultados describen exclusivamente la muestra compartida.
-- Pregunta: ¿Qué personas participan en la red como rescatistas o como adoptantes?
-- Álgebra: π id_persona (rescatista) ∪ π id_persona (adoptante)
-- Demuestra: Compatibilidad de unión: ambas relaciones quedan con un solo atributo id_persona del mismo dominio (numérico). La persona 85 está en las dos y aparece una sola vez.

SELECT id_persona FROM rescatista
UNION
SELECT id_persona FROM adoptante;
