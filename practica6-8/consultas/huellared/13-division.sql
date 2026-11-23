-- Ejercicio 2.2. Ejecutar primero ../../relax/muestra.sql en esta misma sesión.
-- Los resultados describen exclusivamente la muestra compartida.
-- Pregunta: ¿Qué hogares aceptan todas las especies presentes en la muestra de animales?
-- Álgebra: especies = π especie (animal)
-- Álgebra: hogar_especie ÷ especies
-- Demuestra: Divisor = {perro, gato, otro}, derivado de los datos. «Para todo» se expresa con doble NOT EXISTS: no existe una especie del divisor que el hogar no acepte.

SELECT DISTINCT h.id_hogar
FROM hogar_especie h
WHERE NOT EXISTS (
    SELECT 1 FROM (SELECT DISTINCT especie FROM animal) e
    WHERE NOT EXISTS (
        SELECT 1 FROM hogar_especie x
        WHERE x.id_hogar = h.id_hogar AND x.especie = e.especie));
-- Equivalente con conteo:
-- SELECT id_hogar FROM hogar_especie
-- WHERE especie IN (SELECT especie FROM animal)
-- GROUP BY id_hogar
-- HAVING COUNT(DISTINCT especie) = (SELECT COUNT(DISTINCT especie) FROM animal);
