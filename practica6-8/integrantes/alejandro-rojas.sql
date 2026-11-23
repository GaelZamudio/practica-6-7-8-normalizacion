-- Trabajo individual — Alejandro Rojas
-- Base: muestra compartida de HuellaRed. Ejecutar primero ../relax/muestra.sql en la misma sesión.
-- Tres consultas de lectura. La consulta 2 usa reunión externa izquierda.
-- Expresiones, resultados y evidencias en alejandro-rojas.md.

-- Consulta 1
-- Pregunta: ¿Qué perros de tamaño chico están disponibles para adopción?
-- Álgebra: π id_animal, nombre (σ estado_actual = 'disponible_adopcion' ∧ tamano = 'chico' (animal ⋈ perro))
SELECT a.id_animal, a.nombre
FROM animal a
JOIN perro p ON p.id_animal = a.id_animal
WHERE a.estado_actual = 'disponible_adopcion'
  AND p.tamano = 'chico'
ORDER BY a.id_animal;

-- Consulta 2
-- Pregunta: ¿Qué perros no tienen vacunas registradas en la muestra?
-- Álgebra: π id_animal, nombre, tamano ((π id_animal, tamano (σ id_vacuna = null (perro ⟕ vacunacion))) ⋈ animal)
SELECT a.id_animal, a.nombre, p.tamano
FROM perro p
LEFT JOIN vacunacion v ON v.id_animal = p.id_animal
JOIN animal a ON a.id_animal = p.id_animal
WHERE v.id_vacuna IS NULL
ORDER BY a.id_animal;

-- Consulta 3
-- Pregunta: ¿Qué adoptantes tienen patio en su casa?
-- Álgebra: π id_persona, nombres, ap_paterno, tipo_vivienda (σ tiene_patio = true (adoptante) ⋈ persona)
SELECT p.id_persona, p.nombres, p.ap_paterno, d.tipo_vivienda
FROM adoptante d
JOIN persona p ON p.id_persona = d.id_persona
WHERE d.tiene_patio = TRUE
ORDER BY p.id_persona;
