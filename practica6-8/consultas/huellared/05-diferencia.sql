-- Ejercicio 2.2. Ejecutar primero ../../relax/muestra.sql en esta misma sesión.
-- Los resultados describen exclusivamente la muestra compartida.
-- Pregunta: ¿Qué adoptantes no tienen adopciones registradas en la muestra?
-- Álgebra: π id_persona (adoptante) - π id_persona (adopcion)
-- Demuestra: Se resta adopción de adoptante. El orden importa: adopción - adoptante daría vacío, porque toda adopción pertenece a un adoptante (llave foránea).

SELECT id_persona FROM adoptante
EXCEPT
SELECT id_persona FROM adopcion;
