-- Ejercicio 2.2. Ejecutar primero ../../relax/muestra.sql en esta misma sesión.
-- Los resultados describen exclusivamente la muestra compartida.
-- Pregunta: ¿Cómo se llaman y de qué sexo son los perros que están en atención médica?
-- Álgebra: perros_en_atencion = σ especie = 'perro' and estado_actual = 'en_atencion' (animal)
-- Álgebra: π nombre, sexo (perros_en_atencion)
-- Demuestra: Primero se filtra y luego se proyecta: si se proyectara antes, especie y estado_actual ya no existirían para filtrar.

SELECT DISTINCT nombre, sexo
FROM animal
WHERE especie = 'perro' AND estado_actual = 'en_atencion';
