# Organización y colaboración — Prácticas 6, 7 y 8

## Reparto

| Responsable | Trabajo |
|---|---|
| **Gael** | Todo HuellaRed: 1.1, 1.2, 1.3, 2.1 y las 13 consultas de 2.2. Carga de ambas bases, migraciones, integración Docker y README final. |
| **José** | Proyecto asignado: **1.4**, formas normales de las dimensiones de sismos. Prueba final desde un clon limpio. |
| **Alejandro** | Proyecto asignado: **2.3**, tres consultas existentes de sismos traducidas a álgebra con sus árboles y explicación.|
| **Cada integrante** | Tres consultas individuales propias y explicación personal de una descomposición de la Parte 1. |

Para el trabajo individual de José y Alejandro: se preparará sobre HuellaRed cuando Gael entregue el esquema y grupo de RelaX definitivos.

## Ramas y Pull Requests — obligatorio

**Todos los cambios de José y Alejandro se trabajan en `proyecto-asignado`. Al terminar abren PR hacia `practica6-8`. Nunca hacia `main` ni `master`.**

En GitHub, comprobar antes de crear el PR:

```text
base: practica6-8  ←  compare: proyecto-asignado
```

- Antes de editar, guardar o confirmar el trabajo local y actualizar la rama compartida con `git pull --ff-only origin proyecto-asignado`.
- Trabajar solo en los archivos asignados y hacer commits propios. Antes de subir, volver a actualizar; si la rama divergió, coordinar la integración. No usar push forzado ni reescribir commits del compañero.
- Como comparten rama, el PR incluye todos los cambios de ambos. Coordinar un PR conjunto cuando sus entregables estén listos; si hay entregas parciales, acordar con Gael su alcance.
- El PR debe explicar ejercicios terminados, archivos relevantes, qué se ejecutó y qué falta comprobar. Gael revisa su integración.
- Solo Gael coordina posteriormente el PR de `practica6-8` hacia la principal, con revisión de otro integrante.
- Cada integrante debe tener sus propios commits en días distintos. No atribuirse trabajo ajeno ni alterar fechas.

Estos son acuerdos de trabajo; este documento no crea ramas ni publica cambios.

## Estándar de commits

Formato obligatorio: **`tipo(alcance): descripción breve en inglés`**. La descripción expresa la acción, sin mensajes genéricos como Update files. Un commit debe representar un cambio coherente.

| Tipo | Cuándo usarlo |
|---|---|
| `feat` | Consulta o funcionalidad nueva. |
| `docs` | Análisis, explicación, árboles, resultados o evidencias documentales. |
| `fix` | Corregir una consulta, error o comportamiento existente. |
| `chore` | Organización o configuración sin funcionalidad nueva. |
| `refactor` | Reorganizar código conservando el comportamiento. |

Alcances: `1.4`, `2.3`, `individual-jose`, `individual-alejandro`, `sismos`, `docker` o el ejercicio correspondiente. Por ejemplo:

```text
docs(1.4): analyze seismic warehouse dimensions
feat(2.3): add seismic activity query
fix(2.3): preserve the original query filters
docs(individual-jose): explain lossless decomposition
docs(individual-alejandro): add relational algebra results
```

Preparar en stage solo los archivos del cambio. No subir `.env`, contraseñas reales, archivos de PostgreSQL, entornos virtuales, logs ni ZIP del sistema original.

## Material de sismos disponible

Los originales ya están incluidos. **No necesitan volver a buscarlos ni transcribirlos.**

| Ubicación | Contenido |
|---|---|
| `base/sismos/sql/00-datawarehouse_tables.sql` | Esquema original: cuatro dimensiones y una tabla de hechos. |
| `base/sismos/sql/01-dim_zonas.sql` | Datos completos de zonas. |
| `base/sismos/sql/02-dim_tiempo.sql` | Datos completos de tiempo. |
| `base/sismos/sql/03-dim_sismos.sql` | Datos completos de eventos sísmicos. |
| `base/sismos/sql/04-dim_economia.sql` | Datos económicos. |
| `base/sismos/sql/05-fact_impacto_sismos_imputed.sql` | Datos de la tabla de hechos. |
| [Procedencia](base/sismos/procedencia.json) | Repo, HEAD local, tamaño y SHA-256 de las copias. |
| [Licencia](base/sismos/LICENSE) | MIT, copyright 2025 Gabriel Hurtado. Conservarla. |
| [Consultas originales](base/sismos/referencias/consultas-origen.md) | Fragmentos del backend, rutas, líneas y parámetros de las tres consultas elegidas. |
| `practica6-8/consultas/sismos/01-consulta.sql` a `03-consulta.sql` | SQL real extraído; falta ejecución y análisis. |

Origen: https://github.com/GaelZamudio/Seismic-Data-Visualization-System, HEAD local `8569667cf4f46fab640dba3f82a7b324ca7efaf7`.
Se copiaron los archivos del árbol local; las huellas identifican su contenido exacto. El proyecto original declara fuentes SSN/INEGI y cita el artículo DOI 10.24275/AZC2026E1004.

El alcance inicial es el almacén 00–05. Las variantes históricas de anomalías del fork no forman parte de esta carga.
Si la base de prácticas 4–5 utilizada por el equipo incluía alguna extensión, comunicarlo a Gael para acordar su incorporación; no ejecutar dos versiones que crean los mismos objetos.
La tabla de hechos original no declara PK ni UNIQUE: analizar ese hecho, no inventar una clave a partir de unas filas.

## José — ejercicio 1.4

**Editar:** `practica6-8/almacen-y-formas-normales.md`.

Usar el esquema de `base/sismos/sql/00-datawarehouse_tables.sql`, los datos y las reglas del proyecto. Para cada una de las cuatro dimensiones:

1. Explicar qué representa cada fila.
2. Identificar claves y dependencias funcionales justificadas por el negocio.
3. Determinar su forma normal con justificación.
4. Identificar las dependencias transitivas que conserve, si existen; no asumir que todas las dimensiones están fuera de 3FN.
5. Explicar el beneficio y el costo de mantener la desnormalización.
6. Terminar con un párrafo sobre cuándo conviene desnormalizar y qué se vigilaría al hacerlo en HuellaRed.

Firmar el documento y citar el esquema/versión analizados. No modificar los SQL originales ni la configuración Docker.
Si necesita imágenes, agregarlas en `practica6-8/evidencias/proyecto-asignado/1.4/` y enlazarlas desde su documento; no crear imágenes vacías.

## Alejandro — ejercicio 2.3

**Editar:** `practica6-8/algebra-sismos.md`.

**Revisar y completar, conservando estos nombres:**

| Archivo | Consulta de origen |
|---|---|
| `practica6-8/consultas/sismos/01-consulta.sql` | Población por entidad, `src/std2.php`. |
| `practica6-8/consultas/sismos/02-consulta.sql` | Producción agrupada por entidad, `src/aeconomica.php`. |
| `practica6-8/consultas/sismos/03-consulta.sql` | Sismos con impacto por magnitud y año, `src/std.php`. |

Para cada consulta documentar pregunta, origen verificable, SQL en bloque, expresión algebraica, árbol dibujado y operador que realiza el trabajo pesado, con explicación. Ejecutar el SQL en sismos y registrar su resultado real para la integración.

La consulta 03 fija magnitud mínima 4.0 y año 2017. Mantener esos parámetros al comprobar resultados, o documentar el cambio. Explicar COALESCE, agrupación, renombramientos y el papel de ORDER BY cuando aparezcan. No alterar duplicados o filtros sin justificarlo.

Guardar árboles e imágenes en `practica6-8/evidencias/sismos/2.3/` con nombres `01-arbol`, `02-arbol`, `03-arbol` y extensión real, o incluir los árboles directamente en Markdown con Mermaid. Las capturas de resultados pueden llamarse `01-resultado.png`, etc.
No es necesario desplegar PHP ni modificar las tablas para traducir estas consultas.

## Trabajo individual de los tres integrantes

Cada persona escribe su propia entrega cuando esté disponible la muestra definitiva de HuellaRed. Se entrega dentro de la misma rama de trabajo de cada responsable; José y Alejandro usan `proyecto-asignado` también para estos archivos.

| Autor | Documento | SQL |
|---|---|---|
| Gael | `practica6-8/integrantes/GaelZamudio.md` | `practica6-8/integrantes/GaelZamudio.sql` |
| Alejandro | `practica6-8/integrantes/alejandro-rojas.md` | `practica6-8/integrantes/alejandro-rojas.sql` |
| José | `practica6-8/integrantes/jose.md` | `practica6-8/integrantes/jose.sql` |

Cada entrega contiene tres consultas propias, distintas de las del equipo, al menos una con división o reunión externa. Cada consulta incluye pregunta, álgebra, captura de RelaX con árbol y resultado, SQL y comprobación sobre los mismos datos. Reservar las preguntas con Gael para evitar repeticiones.
Además, explicar con palabras propias una descomposición de la Parte 1. Firmar el documento y prepararse para modificar una consulta en clase.
Capturas en `practica6-8/evidencias/integrantes/<nombre-del-archivo-sin-extension>/`, enlazadas con rutas relativas.

## Base heredada y trabajo de Gael

HuellaRed procede de https://github.com/GaelZamudio/practica-4-y-5-implementacion,
`base/huellared/` conserva esquema, migración 001, generador, cargadores y roles. Los cambios nuevos al modelo se harán mediante migraciones numeradas después de cargar los datos, no reescribiendo el esquema inicial.

Gael creará los entregables cuando exista contenido real: `practica6-8/normalizacion.md`, `practica6-8/algebra.md`, migraciones justificadas, consultas de HuellaRed, exportador y grupo RelaX. 
También implementará la carga automática de sismos y la ejecución final de consultas. El análisis formal de equivalencia de F con otro equipo pertenece al 1.2 de Gael.

## Arranque básico disponible

```powershell
docker compose up -d --build
docker compose ps -a
docker compose logs inicializar
```

Actualmente Compose solo prepara HuellaRed: esquema, 001, roles y carga sintética con marca de finalización. Usa PostgreSQL 17, base `huellared`, puerto local 5434 y volumen nombrado separado. Las credenciales públicas de prueba están en `.env.example`; no se necesita crear `.env` para los valores por defecto.
`inicializar` debe terminar con código 0 y PostgreSQL permanecer saludable. Este arranque aún no está validado en un clon limpio; las comprobaciones realizadas hasta ahora son de configuración y sintaxis.
Los SQL originales de sismos son entradas para su futura carga: no ejecutarlos repetidamente sobre una base ya poblada, porque pueden duplicar registros o fallar.

## Cierre de la entrega

- Gael debe volver a crear el **README en inglés** antes de entregar: comando único y salida esperada al inicio, instrucciones y declaración del uso de IA. Se retiró temporalmente durante la limpieza.
- José hará la prueba desde un clon nuevo una vez completada la integración; registrará fecha, commit exacto, comando y resultado real en el README final.

- Uso de IA hasta ahora: Codex ayudó a preparar la estructura, la automatización inicial y la extracción de consultas. 
