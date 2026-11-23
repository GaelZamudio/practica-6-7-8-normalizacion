# HuellaRed — Practices 6, 7 and 8

```sh
docker compose run --build --rm consultas
```

Run this command from a fresh clone with Docker Desktop running (Linux containers). No local Python, PostgreSQL installation or `.env` file is required. It prepares PostgreSQL 17, loads both databases, applies the HuellaRed normalization migrations, prints each implemented query's question, relational algebra and complete SQL result, and regenerates a RelaX group. The query job exits on completion; PostgreSQL stays available in the background.

The final line is `PARTE 3: 22 consultas ejecutadas. Fin sin errores SQL.` The job executes 13 team queries, 6 individual queries and 3 seismic queries, in that order. Each result includes its question and relational algebra. A nonzero exit code indicates a failed operation.

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
5. Questions and algebra are read from the Markdown documents; SQL runs from the corresponding `.sql` files. Individual files are discovered automatically. Keep their documented query order synchronized with SQL order. Files containing only comments produce no queries. Every executable query must have documented algebra; otherwise the job fails.
6. The exporter reads PostgreSQL and regenerates a 10–30-row-per-table RelaX sample with valid foreign keys. Outputs go to `salida/relax/`, preserving the versioned group used by the screenshots.

Running the command again reuses database rows and migrations, reruns the queries and refreshes the generated reports. Reports from a failed attempt must not be treated as a successful run: `salida/resultados.json` is created only after the whole query/export job succeeds.

## Results and shared sample

The console displays all result rows; no preview limit is applied. Generated files under `salida/` are ignored by Git:

- One CSV per executed query, including headers; SQL NULL is represented as `NULL`.
- `resultados.json`: executed query names, questions, algebra, row counts, CSV paths, and group hashes.
- `relax/grupo.txt`, `relax/muestra.sql`, `relax/resumen.json`: regenerated export.

The versioned [group](practica6-8/relax/grupo.txt) and [SQL sample](practica6-8/relax/muestra.sql) are the shared data behind the current query results and screenshots. Automatic queries intentionally use that versioned sample. The regenerated group is also produced from the database as required, but is not substituted silently: the selection algorithm can choose another valid sample. The job compares both groups after normalizing line endings, so Windows CRLF and Linux LF represent the same content. Adopting a different group requires updating query comparisons and screenshots together.

For manual SQL checks, load `muestra.sql` in a new pgAdmin session, then execute the HuellaRed queries in that same session without a `public.` prefix. Seismic queries use the separate `sismos` database.

## Deliverables

- [Functional dependencies and normalization, 1.1–1.3](practica6-8/normalizacion.md).
- [Assigned warehouse analysis, 1.4](practica6-8/almacen-y-formas-normales.md), maintained by José.
- [RelaX export, 2.1](practica6-8/relax/README.md).
- [Team queries and screenshots, 2.2](practica6-8/algebra.md).
- [Assigned-project algebra, 2.3](practica6-8/algebra-sismos.md), maintained by Alejandro.
- Individual work: [Gael](practica6-8/integrantes/GaelZamudio.md), [Alejandro](practica6-8/integrantes/alejandro-rojas.md), [José](practica6-8/integrantes/jose.md).
- [Contribution rules and branch workflow](CONTRIBUTING.md).

## Validation

On 2026-11-22, the integrated SQL workflow was checked in isolated PostgreSQL 18.6. It executed 22 queries with their questions and algebra; repeated initialization retained the same table counts. The regenerated group matched the versioned group, with 23 tables and 29 verified foreign keys.

HuellaRed contains 7,205 baseline rows. The seismic database contains 32 zones, 319,592 time rows, 319,592 seismic events, 32 economy rows and 196,576 fact rows. The three seismic queries return 32, 32 and 2,880 rows. Alejandro's individual queries return 2, 7 and 6 rows on the shared sample.

Gael ran `docker compose run --build --rm consultas` on 2026-11-22 in his working copy with Docker PostgreSQL 17. The integrated version finished with `PARTE 3: 22 consultas ejecutadas. Fin sin errores SQL.`, exported 23 tables, checked 29 foreign keys and regenerated a group identical to the versioned group. This execution was performed before committing the final integration edits.

## Data provenance and AI assistance

HuellaRed's data are synthetic, generated with seed 20261105; they are not real animal-rescue observations. The inherited project is [Practices 4–5](https://github.com/GaelZamudio/practica-4-y-5-implementacion). Seismic source attribution and query locations are documented in [consultas-origen.md](base/sismos/referencias/consultas-origen.md); its original license is preserved in [base/sismos/LICENSE](base/sismos/LICENSE).
AI assistance: Claude contributed an initial repository structure draft. Codex assisted with automation and documentation.
