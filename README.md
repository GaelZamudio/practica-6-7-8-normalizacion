# HuellaRed — Practices 6, 7 and 8

```sh
docker compose run --build --rm consultas
```

Run this command from a fresh clone with Docker Desktop running (Linux containers). No local Python, PostgreSQL installation or `.env` file is required. It prepares PostgreSQL 17, loads both databases, applies the HuellaRed normalization migrations, prints each implemented query's question, relational algebra and complete SQL result, and regenerates a RelaX group. The query job exits on completion; PostgreSQL stays available in the background.

The final line is `PARTE 3: ... consultas ejecutadas; ... pendientes de integración. Fin sin errores SQL.` A nonzero exit code indicates a failed operation. Pending teammate documents are reported explicitly: they are not represented as completed work. In the current branch, 19 queries are executable (13 team queries, Gael's 3 individual queries and 3 seismic queries). The 3 seismic algebra expressions and the other two individual submissions await branch integration.

## Requirements and connections

Docker Compose v2 is required. The first build downloads Python dependencies; the initial seismic load can take several minutes. The original SQL inputs total roughly 177 MB. Allow enough disk space for the images, PostgreSQL volume and generated output.

Both databases use the same PostgreSQL service and separate database names:

| Setting | Default |
| --- | --- |
| Host / port | `127.0.0.1:5434` |
| Own project database | `huellared` |
| Assigned project database | `sismos` |
| Read-only account | `huellared_consulta` |
| Read-only password | `p678_consulta_demo` |

All credentials are public demonstration values in [.env.example](.env.example). Compose supplies matching defaults. Copying that file to `.env` is optional; never commit real credentials. `POSTGRES_DB` and `SISMOS_DB` must be different. Both databases persist in the named `postgres_data` volume. Changing credentials in an existing installation may require updating the database credentials as well.

To keep all services in detached mode instead, use `docker compose up -d --build`; inspect the query output with `docker compose logs consultas` and initialization with `docker compose logs inicializar`. These are optional diagnostic commands, not extra setup steps. `docker compose down` stops the services without removing the database volume.

## Automatic workflow

1. `postgres` becomes healthy.
2. `inicializar` prepares HuellaRed's schema, domains and roles; loads the 7,205 synthetic baseline rows once; and applies migrations 002 and 003. The normalized demonstration in schema `normalizacion` reconstructs all 420 rescues with no differences, while the 23 operational tables remain in `public`.
3. The initializer loads the six original seismic SQL files into `sismos`, in order and in one transaction. File hashes and completion records prevent duplicate loads. A failed load rolls back; a changed input or an untracked existing seismic schema causes an explicit error instead of overwriting data.
4. `consultas` waits for successful initialization, opens the versioned HuellaRed sample in temporary tables, and executes the 13 team queries followed by implemented individual submissions. It then executes the 3 assigned-project queries against the full seismic database. Query connections use a read-only account and read-only transactions after creating the temporary sample.
5. Questions and algebra are read from the Markdown documents; SQL runs from the corresponding `.sql` files. Individual files are discovered automatically. Keep their documented query order synchronized with SQL order. Unimplemented individual templates are reported, not executed. Missing algebra is visibly flagged.
6. The exporter reads PostgreSQL and regenerates a 10–30-row-per-table RelaX sample with valid foreign keys. Outputs go to `salida/relax/`, preserving the versioned group used by the screenshots.

Running the command again reuses database rows and migrations, reruns the queries and refreshes the generated reports. Reports from a failed attempt must not be treated as a successful run: `salida/resultados.json` is created only after the whole query/export job succeeds.

## Results and shared sample

The console displays all result rows; no preview limit is applied. Generated files under `salida/` are ignored by Git:

- One CSV per executed query, including headers; SQL NULL is represented as `NULL`.
- `resultados.json`: executed query names, questions, algebra, row counts, CSV paths, outstanding integrations and group hashes.
- `relax/grupo.txt`, `relax/muestra.sql`, `relax/resumen.json`: regenerated export.

The versioned [group](practica6-8/relax/grupo.txt) and [SQL sample](practica6-8/relax/muestra.sql) are the shared data behind the current query results and screenshots. Automatic queries intentionally use that versioned sample. The regenerated group is also produced from the database as required, but is not substituted silently: the selection algorithm can choose another valid sample. The job reports whether both groups match. Adopting a different group requires updating query comparisons and screenshots together.

For manual SQL checks, load `muestra.sql` in a new pgAdmin session, then execute the HuellaRed queries in that same session without a `public.` prefix. Seismic queries use the separate `sismos` database.

## Deliverables

- [Functional dependencies and normalization, 1.1–1.3](practica6-8/normalizacion.md).
- [Assigned warehouse analysis, 1.4](practica6-8/almacen-y-formas-normales.md), maintained by José.
- [RelaX export, 2.1](practica6-8/relax/README.md).
- [Team queries and screenshots, 2.2](practica6-8/algebra.md).
- [Assigned-project algebra, 2.3](practica6-8/algebra-sismos.md), maintained by Alejandro.
- Individual work: [Gael](practica6-8/integrantes/GaelZamudio.md), [Alejandro](practica6-8/integrantes/alejandro-rojas.md), [José](practica6-8/integrantes/jose.md).
- [Contribution rules and branch workflow](CONTRIBUTING.md).

The external dependency-set exchange in exercise 1.2 remains pending and is outside this implementation. Teammate placeholders will be replaced through their branch merges; their status is not evidence that they have not completed work elsewhere.

## Validation

The original HuellaRed Docker initialization was previously run successfully on PostgreSQL 17. The extended Part 3 workflow has a separate validation status; see the final integration record below.

| Check | Status |
| --- | --- |
| Compose configuration | Validated |
| Extended SQL workflow and repeated execution on isolated PostgreSQL 18.6 | Passed on 2026-11-22: 19 queries in both runs; unchanged table counts |
| Extended workflow in Docker PostgreSQL 17 | Passed on 2026-11-22 in Gael's working copy: 19 queries, no SQL errors; 23 exported tables and 29 verified foreign keys; regenerated group identical to the versioned group |
| Fresh clone by another teammate | Pending after final integration |

The isolated runs loaded 7,205 HuellaRed rows and, in sismos, 32 zones, 319,592 time rows, 319,592 seismic events, 32 economy rows and 196,576 fact rows. The 13 team queries and Gael's 3 queries matched their documented row counts. A failed seismic load was rolled back before a corrected retry. The three seismic queries returned 32, 32 and 2,880 rows respectively.

Gael ran `docker compose run --build --rm consultas` and provided the final console output. The job returned to the terminal after reporting 19 executed queries and five integration notices (two individual SQL submissions and three seismic algebra expressions). This validates the current Docker workflow, not a fresh clone or the still-pending teammate content. The tested working-tree changes had not yet been committed; no commit SHA is claimed for this run.

Before submission, another teammate must replace the last pending entry with their name, test date, exact commit SHA, command and observed result. Do not record a successful clean-clone test before performing it.

## Data provenance and AI assistance

HuellaRed's data are synthetic, generated with seed 20261105; they are not real animal-rescue observations. The inherited project is [Practices 4–5](https://github.com/GaelZamudio/practica-4-y-5-implementacion). Seismic source attribution and query locations are documented in [consultas-origen.md](base/sismos/referencias/consultas-origen.md); its original license is preserved in [base/sismos/LICENSE](base/sismos/LICENSE).