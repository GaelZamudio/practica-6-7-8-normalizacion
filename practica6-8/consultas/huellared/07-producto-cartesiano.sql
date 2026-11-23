-- Ejercicio 2.2. Ejecutar primero ../../relax/muestra.sql en esta misma sesión.
-- Los resultados describen exclusivamente la muestra compartida.
-- Pregunta: ¿Qué parejas animal disponible–adoptante con patio podrían formarse?
-- Álgebra: disponibles = σ estado_actual = 'disponible_adopcion' (animal)
-- Álgebra: con_patio = σ tiene_patio = true (adoptante)
-- Álgebra: π id_animal, nombre, id_persona (disponibles cross join con_patio)
-- Demuestra: Cada animal se empareja con cada adoptante: 5 cross join 6 = 30 filas. Sin una condición que relacione a las dos (una solicitud, compatibilidad de tamaño) las parejas no significan nada, por eso casi siempre se combina con una selección y se convierte en reunión.

SELECT a.id_animal, a.nombre, d.id_persona
FROM animal a CROSS JOIN adoptante d
WHERE a.estado_actual = 'disponible_adopcion' AND d.tiene_patio;
