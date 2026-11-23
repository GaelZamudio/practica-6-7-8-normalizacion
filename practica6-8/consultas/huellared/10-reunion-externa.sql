-- Ejercicio 2.2. Ejecutar primero ../../relax/muestra.sql en esta misma sesión.
-- Los resultados describen exclusivamente la muestra compartida.
-- Pregunta: ¿Qué registros de adopción tiene cada animal de la muestra, incluidos aquellos sin registros?
-- Álgebra: π id_animal, nombre, id_persona, fecha_adopcion (animal ⟕ adopcion)
-- Demuestra: Conserva todos los animales: los animales sin registros de adopción en la muestra salen con NULL en id_persona y fecha_adopcion. Contrasta con la consulta 08, que los pierde.

SELECT a.id_animal, a.nombre, d.id_persona, d.fecha_adopcion
FROM animal a
LEFT JOIN adopcion d ON a.id_animal = d.id_animal;
