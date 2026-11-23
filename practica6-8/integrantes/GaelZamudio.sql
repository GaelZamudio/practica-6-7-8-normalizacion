-- Trabajo individual — Gael Zamudio
-- Ejecutar primero ../relax/muestra.sql en la misma sesión de pgAdmin.
-- Consultas de lectura sobre la muestra compartida, no sobre todo public.
-- Preguntas, álgebra, resultados y espacios de evidencia en GaelZamudio.md.

-- Consulta 1: ¿Qué clínicas no tienen atenciones médicas registradas en la muestra?
SELECT c.id_clinica, c.nombre
FROM clinica c
LEFT JOIN atencion_medica am ON am.id_clinica = c.id_clinica
WHERE am.id_animal IS NULL
ORDER BY c.id_clinica;

-- Consulta 2: ¿Qué animales tienen tanto vacunaciones como cirugías registradas en la muestra?
SELECT a.id_animal, a.nombre, a.especie
FROM animal a
JOIN (
    SELECT id_animal FROM vacunacion
    INTERSECT
    SELECT id_animal FROM cirugia
) ambas ON ambas.id_animal = a.id_animal
ORDER BY a.id_animal;

-- Consulta 3: ¿Qué rescatistas participaron en al menos dos rescates de la muestra y en cuántos?
SELECT p.id_persona, p.nombres, p.ap_paterno, c.total_rescates
FROM (
    SELECT id_persona, COUNT(*) AS total_rescates
    FROM rescate_rescatista
    GROUP BY id_persona
    HAVING COUNT(*) >= 2
) c
JOIN persona p ON p.id_persona = c.id_persona
ORDER BY p.id_persona;
