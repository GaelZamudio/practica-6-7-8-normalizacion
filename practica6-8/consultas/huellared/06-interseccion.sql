-- Ejercicio 2.2. Ejecutar primero ../../relax/muestra.sql en esta misma sesión.
-- Los resultados describen exclusivamente la muestra compartida.
-- Pregunta: ¿Qué personas son a la vez rescatistas y adoptantes?
-- Álgebra: π id_persona (rescatista) ∩ π id_persona (adoptante)
-- Demuestra: Mismos atributos y tipos que la consulta 04. Comprobación: |A ∪ B| = |A| + |B| - |A ∩ B| → 19 = 10 + 10 - 1.

SELECT id_persona FROM rescatista
INTERSECT
SELECT id_persona FROM adoptante;
