-- Ejercicio 2.2. Ejecutar primero ../../relax/muestra.sql en esta misma sesión.
-- Los resultados describen exclusivamente la muestra compartida.
-- Pregunta: ¿Qué adopciones se han registrado, con el animal y la persona que adoptó?
-- Álgebra: π id_animal, especie, nombres, ap_paterno, fecha_adopcion (adopcion ⨝ animal ⨝ persona)
-- Demuestra: Se conservan solo las filas que coinciden en id_animal e id_persona. Se pierden los 21 animales sin adopción y las personas sin adopciones en la muestra.

SELECT DISTINCT d.id_animal, a.especie, p.nombres, p.ap_paterno, d.fecha_adopcion
FROM adopcion d
JOIN animal a ON a.id_animal = d.id_animal
JOIN persona p ON p.id_persona = d.id_persona;
