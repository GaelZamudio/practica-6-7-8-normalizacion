-- Responsable: Gael Zamudio. Ejercicio 1.3: descomposición sin pérdida a BCNF.
-- Entrada: normalizacion.rescate_zona creada por 002; nunca recarga public.
BEGIN;
LOCK TABLE normalizacion.rescate_zona IN ACCESS EXCLUSIVE MODE;
CREATE TABLE normalizacion.zona (
    LIKE public.zona INCLUDING DEFAULTS INCLUDING CONSTRAINTS INCLUDING INDEXES
);
CREATE TABLE normalizacion.rescate (
    LIKE public.rescate INCLUDING DEFAULTS INCLUDING CONSTRAINTS INCLUDING INDEXES,
    CONSTRAINT fk_rescate_zona_normalizada FOREIGN KEY (id_zona)
        REFERENCES normalizacion.zona (id_zona)
        ON DELETE RESTRICT ON UPDATE CASCADE
);
INSERT INTO normalizacion.zona (id_zona, colonia, municipio, entidad)
SELECT DISTINCT id_zona, colonia, municipio, entidad
FROM normalizacion.rescate_zona;
INSERT INTO normalizacion.rescate
    (id_rescate, descripcion_lugar, fecha_hora, condicion_inicial, tipo_ingreso, id_zona)
SELECT id_rescate, descripcion_lugar, fecha_hora, condicion_inicial, tipo_ingreso, id_zona
FROM normalizacion.rescate_zona;

-- EXCEPT ALL detecta diferencias de valores y de multiplicidad en ambos sentidos.
-- Las columnas se listan una por una: no depende del orden físico de la tabla.
DO $$
DECLARE origen bigint; reconstruidas bigint; diferencias bigint;
BEGIN
    WITH instantanea AS (
        SELECT id_rescate, descripcion_lugar, fecha_hora, condicion_inicial,
               tipo_ingreso, id_zona, colonia, municipio, entidad
        FROM normalizacion.rescate_zona
    ), reconstruccion AS (
        SELECT r.id_rescate, r.descripcion_lugar, r.fecha_hora, r.condicion_inicial,
               r.tipo_ingreso, r.id_zona, z.colonia, z.municipio, z.entidad
        FROM normalizacion.rescate r JOIN normalizacion.zona z USING (id_zona)
    ), faltantes AS (
        SELECT * FROM instantanea
        EXCEPT ALL SELECT * FROM reconstruccion
    ), sobrantes AS (
        SELECT * FROM reconstruccion
        EXCEPT ALL SELECT * FROM instantanea
    )
    SELECT (SELECT count(*) FROM instantanea),
           (SELECT count(*) FROM reconstruccion),
           (SELECT count(*) FROM faltantes) + (SELECT count(*) FROM sobrantes)
    INTO origen, reconstruidas, diferencias;
    IF origen = 0 OR diferencias <> 0 THEN
        RAISE EXCEPTION 'Migración cancelada: origen %, reconstruidas %, diferencias %',
            origen, reconstruidas, diferencias;
    END IF;
    RAISE NOTICE '003: origen=%, reconstruidas=%, diferencias=%; reunión sin pérdida verificada',
        origen, reconstruidas, diferencias;
END $$;

-- Eliminar solo la copia redundante, después de comprobar toda su información.
DROP TABLE normalizacion.rescate_zona;
CREATE VIEW normalizacion.rescate_zona AS
SELECT r.id_rescate, r.descripcion_lugar, r.fecha_hora, r.condicion_inicial,
       r.tipo_ingreso, r.id_zona, z.colonia, z.municipio, z.entidad
FROM normalizacion.rescate r JOIN normalizacion.zona z USING (id_zona);
COMMENT ON VIEW normalizacion.rescate_zona IS
    'Reconstrucción de la instantánea desnormalizada del ejercicio 1.3, sin almacenar redundancia.';
GRANT USAGE ON SCHEMA normalizacion TO hr_admin, hr_app, hr_consulta;
GRANT SELECT ON ALL TABLES IN SCHEMA normalizacion TO hr_admin, hr_app, hr_consulta;
COMMIT;
