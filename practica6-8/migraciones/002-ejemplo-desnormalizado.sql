-- Responsable: Gael Zamudio. Ejercicio 1.3 (alternativa para esquema ya en BCNF).
-- Ejecutar después de la carga heredada. Instantánea didáctica, no datos manuales.
-- El inicializador registra esta migración y controla la transacción al automatizarla.
BEGIN;
CREATE SCHEMA normalizacion;
REVOKE ALL ON SCHEMA normalizacion FROM PUBLIC;
COMMENT ON SCHEMA normalizacion IS
    'Ejercicio 1.3: instantánea didáctica de rescates y zonas; public es el modelo operativo.';

-- LIKE copia columnas, CHECK, valores iniciales y PK; no copia las FK.
CREATE TABLE normalizacion.rescate_zona (
    LIKE public.rescate INCLUDING DEFAULTS INCLUDING CONSTRAINTS INCLUDING INDEXES,
    colonia VARCHAR(80) NOT NULL,
    municipio VARCHAR(80) NOT NULL,
    entidad VARCHAR(50) NOT NULL
);
INSERT INTO normalizacion.rescate_zona
    (id_rescate, descripcion_lugar, fecha_hora, condicion_inicial, tipo_ingreso,
     id_zona, colonia, municipio, entidad)
SELECT r.id_rescate, r.descripcion_lugar, r.fecha_hora, r.condicion_inicial,
       r.tipo_ingreso, r.id_zona, z.colonia, z.municipio, z.entidad
FROM public.rescate AS r JOIN public.zona AS z USING (id_zona);
DO $$
DECLARE n bigint;
BEGIN
    SELECT count(*) INTO n FROM normalizacion.rescate_zona;
    IF n = 0 THEN
        RAISE EXCEPTION 'Primero cargar HuellaRed: el ejemplo requiere rescates existentes';
    END IF;
    RAISE NOTICE '002: relación desnormalizada poblada con % rescates', n;
END $$;
COMMIT;
