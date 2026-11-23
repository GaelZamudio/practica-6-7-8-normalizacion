# Ejercicio 2.1 — Grupo de RelaX de HuellaRed

**Responsable:** Gael Zamudio.

El grupo contiene una muestra de las 23 tablas operativas de `public`, de 10 a 30 filas por tabla, tomada de PostgreSQL. Los datos son sintéticos del generador heredado; no son observaciones reales. No se exportan las tablas administrativas de huellared_control ni la instantánea didáctica de normalizacion del ejercicio 1.3.

## Archivos

| Archivo | Uso |
| --- | --- |
| [exportar-grupo.py](exportar-grupo.py) | Lee la base y selecciona filas conservando todas las FK; no escribe en la base. |
| [grupo.txt](grupo.txt) | Grupo para cargar en RelaX y compartir entre los integrantes. |
| [muestra.sql](muestra.sql) | La misma muestra para comparar las consultas SQL en pgAdmin. |
| [resumen.json](resumen.json) | Conteos por tabla, número de FK comprobadas y SHA-256 del grupo. No contiene contraseñas. |

## Usar en RelaX

1. Abrir [RelaX](https://dbis-uibk.github.io/relax/).
2. Entrar a **Group Editor / Editor de grupo** y pegar el contenido completo de grupo.txt.
3. Elegir **Use group in editor**. Las tablas aparecen con sus nombres originales en minúsculas.
4. Para comprobar la carga, ejecutar `animal`. Después escribir las consultas del equipo o las individuales y capturar su árbol y resultado.

Todos los integrantes deben usar la misma versión de grupo.txt. Registrar el commit utilizado; el SHA-256 de resumen.json identifica su contenido. No modificar filas a mano. La muestra permite comenzar las consultas individuales; deben reservarse las preguntas para que no coincidan con las del equipo.

## Comparar con SQL

Abrir una sesión **nueva** del Query Tool de pgAdmin en HuellaRed, con un usuario que pueda crear tablas temporales (por ejemplo huellared_admin), y ejecutar muestra.sql completo. Luego ejecutar las consultas en esa misma sesión usando `animal`, `adopcion`, etc., **sin el prefijo public.** Esos nombres apuntan a las tablas temporales con exactamente las filas del grupo; `public.animal` seguiría consultando la base completa.

El archivo no modifica public. Las tablas temporales desaparecen al cerrar la conexión; para volver a cargarlo se abre una sesión nueva. Las columnas usan los mismos tipos representados en RelaX. Para comparar álgebra de conjuntos con SQL, tratar los duplicados deliberadamente (por ejemplo SELECT DISTINCT en proyecciones) y no asumir que ambos ordenan el resultado igual. La igualdad del resultado de cada consulta debe comprobarse en 2.2 o en el trabajo individual.

## Regenerar

El comando completo de la Parte 3 es:

```powershell
docker compose run --build --rm consultas
```

Prepara las bases, ejecuta las consultas y exporta el grupo desde PostgreSQL a `salida/relax/`. El grupo versionado de esta carpeta se conserva para que las consultas y capturas sigan usando la misma muestra. El resultado informa si la selección regenerada coincide con la versionada. No reemplazar la muestra compartida sin actualizar conjuntamente comparaciones y evidencias.

Con la base ya preparada, para exportar únicamente el grupo:

```powershell
docker compose run --rm --no-deps consultas python practica6-8/relax/exportar-grupo.py --destino /app/salida/relax
```


## Selección y representación

Tomar LIMIT 10 de cada tabla independientemente podría romper las referencias. Se selecciona una variable binaria por fila y se imponen simultáneamente: 10–30 filas por tabla y, para cada fila hija elegida, su fila padre elegida. SciPy resuelve estas restricciones buscando una muestra pequeña; incluye las FK compuestas y animal.id_madre. No es una muestra aleatoria ni estadísticamente representativa.

Se ordenan las filas por PK y se lee una instantánea consistente en una transacción de solo lectura. Antes de escribir se comprueban nuevamente los límites, la unicidad de las PK y todas las FK. Si faltan datos o no se encuentra una solución en 60 segundos, se informa el problema: no se inventan filas ni se cortan referencias. Los archivos solo se reemplazan después de generar y validar su contenido. La selección válida no es necesariamente única. Cambios de datos, versión del solucionador o el tiempo disponible pueden cambiarla; se comparte siempre el archivo versionado y se coordina cualquier regeneración mientras se elaboran las consultas.

| PostgreSQL | RelaX |
| --- | --- |
| Enteros | number |
| BOOLEAN | boolean (true / false) |
| DATE | date, AAAA-MM-DD |
| Texto, teléfono, código postal y enumerados | string, conservando ceros iniciales |
| TIMESTAMP de rescate.fecha_hora | string ISO con fecha y hora, sin truncar a fecha |
| NULL | null, distinto de texto vacío o FALSE |

RelaX no tiene un tipo timestamp en sus tablas inline. Para operaciones sobre fecha_hora se debe considerar su representación textual; muestra.sql conserva esa misma representación. Su gramática tampoco permite escapes arbitrarios en texto inline: si aparece un texto con saltos de línea o ambas clases de comillas, el exportador informa el caso en vez de alterar el dato.

Formato contrastado con el [repositorio oficial](https://github.com/dbis-uibk/relax) y su [gramática de grupos y relaciones](https://github.com/dbis-uibk/relax/blob/development/src/db/parser/grammar_ra.pegjs).

## Validación

El 20 de noviembre de 2026 se generó la muestra desde la copia aislada huellared_revision (PostgreSQL 18.6), poblada con el generador heredado: 23 tablas, 348 filas en total, todas entre 10 y 30 y las 29 FK conservadas. La base operativa no fue modificada por el exportador.

La gramática oficial de RelaX aceptó el grupo. Se comparó cada valor de sus 23 relaciones con las tablas temporales creadas por muestra.sql en PostgreSQL: igualdad completa, incluidos NULL, fechas, booleanos y textos. Se verificaron nuevamente las 29 FK sobre esas tablas temporales, así como el rechazo de una tabla con menos de diez filas y de textos no representables sin transformación. Las claves compuestas y la FK recursiva están incluidas.

Compose valida como configuración. Falta confirmar la ejecución integrada con PostgreSQL 17 en Docker; la prueba anterior no se presenta como ejecución del contenedor. Los conteos vigentes de cualquier regeneración posterior están en resumen.json. La carga visual en el editor puede hacerse siguiendo los pasos anteriores.
