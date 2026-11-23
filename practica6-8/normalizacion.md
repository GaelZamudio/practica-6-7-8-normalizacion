# Normalización de HuellaRed

**Responsable:** Gael Zamudio.  
**Ejercicios:** 1.1, 1.2 y 1.3 de las prácticas 6–8.  
**Estado:** 1.1 y análisis formal 1.2–1.3 documentados. Estado de ejecución al final.

## 1.1. Pautas informales de diseño

### Alcance y criterios

Se analiza el esquema lógico resultante de aplicar [esquema.sql](../base/huellared/esquema.sql) y después [001-dominios.sql](../base/huellared/migraciones/001-dominios.sql). Se consideran sus 23 tablas, restricciones y unicidades parciales. Este es un análisis documental: no se presentan conteos de datos ni resultados de ejecución.

Las cuatro pautas son: semántica clara de cada fila; ausencia de anomalías de inserción, actualización y eliminación por redundancia; nulos limitados y justificados; y ausencia de tuplas espurias al reunir información. Repetir una FK no implica redundancia perjudicial. Las políticas CASCADE, RESTRICT y SET NULL no son por sí mismas anomalías de normalización.

Para la cuarta pauta se identifican las condiciones correctas de reunión. La existencia de FK no demuestra que cualquier descomposición sea sin pérdida; esa prueba corresponde al 1.3. Tampoco se certifica aquí 3FN o BCNF: se necesitan las dependencias funcionales del 1.2.

Cada diagnóstico toma una decisión explícita de interpretación, justificada por las reglas del negocio de las prácticas 3 a 5 y no por datos de muestra. Donde había dos lecturas posibles se elige una, se anota por qué y se indica qué cambiaría con la otra. Al final de la sección se resume qué tabla falla qué pauta.

### Análisis por tabla

#### 1. `zona`

**Cada fila representa** una zona identificada por colonia, municipio y entidad.

| Pauta | Evaluación |
| --- | --- |
| Semántica clara | Los atributos describen una ubicación; 001 impide repetir la combinación de los tres nombres. |
| Anomalías de inserción, actualización y eliminación | Los nombres geográficos se repiten entre zonas. Cambiar el nombre de un municipio podría exigir varias actualizaciones. No se debe inferir municipio → entidad por nombres, pues puede haber homónimos. La zona puede registrarse sin hogares o rescates. |
| Nulos | Ningún atributo admite NULL. |
| Tuplas espurias y reuniones | Hogares y rescates se enlazan por id_zona; unir solo por colonia o municipio podría combinar ubicaciones diferentes. |

**Diagnóstico:** Falla la pauta 2 en sentido informal: municipio y entidad se repiten en cada colonia, y renombrar un municipio exige varias actualizaciones. No es una violación de forma normal, porque `municipio → entidad` no es una dependencia del negocio (hay municipios homónimos en entidades distintas). La solución completa sería un catálogo de municipios; se descarta porque ninguna dependencia de F lo exige.

#### 2. `persona`

**Cada fila representa** una persona registrada, independientemente de sus roles.

| Pauta | Evaluación |
| --- | --- |
| Semántica clara | Nombre, contacto y fecha de registro describen a la persona. |
| Anomalías de inserción, actualización y eliminación | Puede registrarse sin roles. Sus datos se actualizan una sola vez aunque desempeñe varios; retirar un rol no obliga a borrar persona. El correo tiene unicidad, pero es opcional. |
| Nulos | ap_materno y correo pueden no estar disponibles. No hay columnas vacías para atributos de cada rol. |
| Tuplas espurias y reuniones | Los subtipos se enlazan por id_persona, PK en ambos extremos; nombre y teléfono no identifican inequívocamente personas. |

**Diagnóstico:** No se identifica una infracción de las pautas bajo esta interpretación.

#### 3. `rescatista`

**Cada fila representa** el rol de rescatista de una persona.

| Pauta | Evaluación |
| --- | --- |
| Semántica clara | vehiculo_propio y disponibilidad describen características operativas generales del rescatista. |
| Anomalías de inserción, actualización y eliminación | No copia nombre ni contacto. Puede existir antes de participar en un rescate. Retirar el rol, cuando las referencias lo permitan, no requiere eliminar persona. |
| Nulos | disponibilidad admite información no registrada; vehiculo_propio exige una respuesta explícita. |
| Tuplas espurias y reuniones | id_persona identifica una única persona; las participaciones se conservan en rescate_rescatista. |

**Diagnóstico:** Coherente si disponibilidad es una descripción general, no un historial de turnos.

#### 4. `adoptante`

**Cada fila representa** el perfil actual de una persona que puede adoptar.

| Pauta | Evaluación |
| --- | --- |
| Semántica clara | Vivienda, patio y otras mascotas describen al adoptante, no un episodio de adopción. |
| Anomalías de inserción, actualización y eliminación | Puede existir sin adopciones; su perfil se actualiza una sola vez. Eliminar una solicitud no elimina el perfil. No se conserva aquí el historial de viviendas. |
| Nulos | No admite NULL; las tres características son obligatorias. |
| Tuplas espurias y reuniones | id_persona enlaza con persona; solicitudes y adopciones conservan sus propias claves de evento. |

**Diagnóstico:** Coherente para un perfil actual. Conservar condiciones históricas sería un requisito distinto.

#### 5. `veterinario`

**Cada fila representa** el rol profesional de una persona veterinaria voluntaria.

| Pauta | Evaluación |
| --- | --- |
| Semántica clara | La cédula y especialidad pertenecen al profesional; cedula es obligatoria y única. |
| Anomalías de inserción, actualización y eliminación | No copia datos personales por atención. Puede existir antes de atender y permanece aunque se elimine una atención. |
| Nulos | especialidad permite información desconocida; NULL no afirma ausencia de especialidad. |
| Tuplas espurias y reuniones | id_persona enlaza con persona y es la referencia que usan las atenciones; especialidad no sirve como clave. |

**Diagnóstico:** No se identifica redundancia; se registra una descripción de especialidad por profesional.

#### 6. `hogar_temporal`

**Cada fila representa** un hogar temporal con dirección, capacidad y responsable actuales.

| Pauta | Evaluación |
| --- | --- |
| Semántica clara | Los datos propios describen el hogar; id_persona e id_zona identifican responsable y ubicación. No almacena lugares_disponibles. |
| Anomalías de inserción, actualización y eliminación | No copia los datos personales ni los nombres geográficos. Puede existir sin estancias; cambiar capacidad no exige actualizar cada estancia. Debe validarse cualquier dependencia entre cp y zona. |
| Nulos | Solo alias es opcional; los datos operativos y referencias son obligatorios. |
| Tuplas espurias y reuniones | Las FK enlazan con PK de persona y zona. Varias filas al unir especies aceptadas son multiplicidad legítima. |

**Diagnóstico:** Cumple las pautas. `cp` e `id_zona` guardan información geográfica relacionada, pero no se declara `cp → id_zona`: un código postal puede cubrir varias colonias y una colonia puede tener varios códigos. Se trata como dato capturado, no derivable.

#### 7. `hogar_especie`

**Cada fila representa** la aceptación de una especie por un hogar.

| Pauta | Evaluación |
| --- | --- |
| Semántica clara | La pareja (id_hogar, especie) representa una aceptación, no la ficha del hogar. |
| Anomalías de inserción, actualización y eliminación | No copia dirección ni capacidad. Agregar o quitar una aceptación no altera otras ni elimina el hogar. Repetir id_hogar expresa múltiples aceptaciones. |
| Nulos | Los dos atributos integran la PK y no admiten NULL. |
| Tuplas espurias y reuniones | id_hogar apunta a un único hogar; la PK evita repetir la misma aceptación. Una fila por especie en la unión es correcta. |

**Diagnóstico:** Cumple las pautas. Exigir al menos una especie por hogar es una regla adicional de participación.

#### 8. `rescate`

**Cada fila representa** un evento de rescate o ingreso en una zona y momento determinados.

| Pauta | Evaluación |
| --- | --- |
| Semántica clara | Lugar, fecha y tipo de ingreso describen el evento. condicion_inicial se interpreta como descripción general del evento; si fuera la salud individual, su ubicación sería ambigua para rescates con varios animales. |
| Anomalías de inserción, actualización y eliminación | No repite nombres de zona ni crea un evento por participante. Puede registrarse antes de asociar participantes. Guardar condiciones individuales mezcladas en un texto introduciría hechos de distinto nivel. |
| Nulos | Todos los atributos son obligatorios. |
| Tuplas espurias y reuniones | Zona se enlaza por id_zona; animales y participantes mediante sus FK, no por coincidencia de fecha. |

**Diagnóstico:** Decisión de diseño: `condicion_inicial` describe el rescate como evento (la situación al ingreso), no la salud de cada animal, que se registra en `atencion_medica`. Con esa lectura cumple la pauta 1. Si se usara por animal estaría en la tabla equivocada, porque un rescate puede incluir varios animales.

#### 9. `animal`

**Cada fila representa** un animal individual con características y estado actuales.

| Pauta | Evaluación |
| --- | --- |
| Semántica clara | Las referencias identifican su rescate de ingreso y madre registrada. Los detalles médicos se conservan aparte. |
| Anomalías de inserción, actualización y eliminación | No copia datos del rescate; cambiar nombre no obliga a modificar atenciones. La coherencia de estado_actual con adopciones necesita reglas de integridad, pero no demuestra por sí sola una dependencia interna problemática. |
| Nulos | nombre, fecha_nacimiento_aprox, color, senas e id_madre permiten información desconocida o no registrada. id_madre también queda NULL si se elimina la madre. |
| Tuplas espurias y reuniones | id_rescate enlaza con un rescate. La reunión recursiva correcta es cria.id_madre = madre.id_animal usando alias distintos. |

**Diagnóstico:** Existe riesgo de inconsistencia entre el estado actual y los eventos registrados: una adopción puede requerir actualizar también animal. Sin embargo, estancia y adopcion no determinan todo el estado, que incluye valores como fallecido y en_atencion. No se afirma una derivación completa ni que ya exista un trigger de sincronización. Los nulos están justificados; la compatibilidad de especie y subtipo y los ciclos maternos son asuntos adicionales de integridad.

#### 10. `perro`

**Cada fila representa** los atributos específicos de un animal clasificado como perro.

| Pauta | Evaluación |
| --- | --- |
| Semántica clara | Tamaño, energía y aptitud con niños describen el animal identificado por id_animal. |
| Anomalías de inserción, actualización y eliminación | No copia datos generales. Estos se actualizan en animal; la existencia dependiente del subtipo es intencional. |
| Nulos | No admite NULL; evita columnas caninas vacías en gatos y otros animales. |
| Tuplas espurias y reuniones | La PK/FK id_animal enlaza con un único animal, aunque no valida que su especie sea perro. |

**Diagnóstico:** Separación adecuada; compatibilidad del subtipo pendiente de una regla cruzada.

#### 11. `gato`

**Cada fila representa** los resultados registrados de FIV y FeLV de un gato.

| Pauta | Evaluación |
| --- | --- |
| Semántica clara | Son resultados disponibles del animal; esta tabla no representa un historial de pruebas fechado. |
| Anomalías de inserción, actualización y eliminación | No copia datos generales. Cambiar un resultado sustituye al anterior; un historial requeriría otra entidad si fuera necesario. |
| Nulos | resultado_fiv y resultado_felv permiten desconocimiento. FALSE representa negativo y no equivale a NULL. |
| Tuplas espurias y reuniones | id_animal enlaza con un animal; no debe asociarse por resultados iguales. |

**Diagnóstico:** Nulos justificados; coherente para resultados sin historial y sujeto a compatibilidad del subtipo.

#### 12. `otro`

**Cada fila representa** los detalles de un animal de la categoría general otro.

| Pauta | Evaluación |
| --- | --- |
| Semántica clara | descripcion_especie precisa la especie; cuidados_especiales se interpreta como necesidad individual. |
| Anomalías de inserción, actualización y eliminación | No copia datos generales. Si los cuidados fueran determinados exclusivamente por la especie, repetirlos por animal introduciría anomalías y habría que analizar un catálogo. Esa dependencia no está establecida. |
| Nulos | Solo cuidados_especiales permite información no registrada. |
| Tuplas espurias y reuniones | id_animal identifica al individuo; compartir texto de especie no significa compartir identidad. |

**Diagnóstico:** Coherente para cuidados individuales; confirmar si describen al individuo o a una especie del catálogo.

#### 13. `rescate_rescatista`

**Cada fila representa** la participación de un rescatista en un rescate.

| Pauta | Evaluación |
| --- | --- |
| Semántica clara | La pareja de identificadores representa el hecho completo. |
| Anomalías de inserción, actualización y eliminación | No copia descripciones. Agregar o quitar una participación no modifica las demás ni elimina los registros padre. |
| Nulos | No admite NULL. |
| Tuplas espurias y reuniones | Cada FK identifica un extremo. Separar la asociación en dos listas y combinarlas produciría participaciones inexistentes. |

**Diagnóstico:** Cumple las pautas; exigir al menos un rescatista por rescate necesita otra regla de integridad.

#### 14. `estancia`

**Cada fila representa** un periodo de alojamiento de un animal en un hogar asociado a un rescatista.

| Pauta | Evaluación |
| --- | --- |
| Semántica clara | La PK es (id_animal, id_hogar, id_persona, fecha_inicio); fecha_fin y motivo_salida describen el episodio. |
| Anomalías de inserción, actualización y eliminación | No copia datos del hogar ni rescatista. Puede insertarse abierta y cerrarse en una fila. La unicidad parcial impide dos estancias abiertas, pero no todos los solapamientos entre periodos cerrados. |
| Nulos | fecha_fin permite una estancia abierta; motivo_salida es opcional y solo puede existir cuando hay fecha_fin. |
| Tuplas espurias y reuniones | Las tres FK preservan los participantes. Descomponer la asociación ternaria en parejas sin prueba podría recombinar participantes incorrectos. |

**Diagnóstico:** La identidad conserva la combinación animal–hogar–rescatista–fecha inicial del esquema heredado. Una sola estancia abierta no implica una sola estancia iniciada por día. No se ha establecido una regla que permita eliminar hogar o rescatista de la clave; se conserva completa en 1.2.

#### 15. `solicitud_adopcion`

**Cada fila representa** una solicitud de un adoptante para un animal en una fecha.

| Pauta | Evaluación |
| --- | --- |
| Semántica clara | La PK incluye id_animal, id_persona y fecha_solicitud. estado es el de la solicitud. |
| Anomalías de inserción, actualización y eliminación | No copia perfiles; puede existir sin adopción. Eliminarla no elimina al solicitante ni al animal. |
| Nulos | Solo observaciones es opcional. |
| Tuplas espurias y reuniones | Las FK identifican animal y adoptante. Compartir ambos con una adopción no demuestra qué solicitud la originó: no existe ese enlace explícito. |

**Diagnóstico:** Coherente para una solicitud por pareja y día; no se identifica redundancia descriptiva.

#### 16. `adopcion`

**Cada fila representa** un episodio de adopción de un animal por una persona en una fecha.

| Pauta | Evaluación |
| --- | --- |
| Semántica clara | La PK es (id_animal, id_persona, fecha_adopcion); devolución y motivo describen su cierre. |
| Anomalías de inserción, actualización y eliminación | No copia datos del adoptante o animal. Se registra sin devolución y se cierra en una fila. La unicidad parcial de adopciones vigentes no hace a id_animal clave de todo el historial. |
| Nulos | fecha_devolucion permite una adopción sin devolución registrada; motivo es opcional y exige fecha si se proporciona. |
| Tuplas espurias y reuniones | Los seguimientos se enlazan por los tres componentes de la PK; solo animal mezclaría episodios distintos. |

**Diagnóstico:** Coherente para episodios identificados por animal, adoptante y fecha. La unicidad de la adopción vigente no implica que animal y fecha identifiquen todo el historial; se conserva la clave completa en 1.2.

#### 17. `seguimiento`

**Cada fila representa** una revisión numerada de una adopción concreta.

| Pauta | Evaluación |
| --- | --- |
| Semántica clara | La PK combina la clave completa de adopción con num_seguimiento. Fecha, medio y estado observado describen la revisión. |
| Anomalías de inserción, actualización y eliminación | No copia el perfil del adoptante. estado_del_animal es observación histórica, distinta del estado actual. Borrar una revisión no borra la adopción. |
| Nulos | Solo observaciones admite NULL. |
| Tuplas espurias y reuniones | La FK compuesta se usa completa. num_seguimiento no identifica una revisión globalmente. |

**Diagnóstico:** Buena separación entre observaciones históricas y datos actuales.

#### 18. `clinica`

**Cada fila representa** un establecimiento clínico con sus datos de contacto.

| Pauta | Evaluación |
| --- | --- |
| Semántica clara | Nombre, dirección, teléfono y tipo describen la clínica. 001 hace única la pareja nombre y dirección. |
| Anomalías de inserción, actualización y eliminación | Puede existir sin atenciones y su teléfono se actualiza una vez. Una dirección textual no prueba por sí sola una violación de atomicidad: depende del uso del atributo. |
| Nulos | No admite NULL, incluido telefono. |
| Tuplas espurias y reuniones | Las atenciones se enlazan por id_clinica; el nombre solo puede repetirse en establecimientos diferentes. |

**Diagnóstico:** Coherente para una dirección y un teléfono por clínica. direccion se utiliza como descripción unitaria; su distinta granularidad respecto a hogar_temporal no demuestra una falla semántica ni de 1FN.

#### 19. `vacuna`

**Cada fila representa** una entrada del catálogo de vacunas para una especie destino.

| Pauta | Evaluación |
| --- | --- |
| Semántica clara | El nombre, especie e intervalo describen el catálogo, no una aplicación. La pareja nombre y especie es única. |
| Anomalías de inserción, actualización y eliminación | Puede registrarse sin aplicaciones; corregir su intervalo requiere una fila y no cada vacunación. |
| Nulos | intervalo_refuerzo_dias permite una pauta desconocida; NULL no equivale a cero. |
| Tuplas espurias y reuniones | La aplicación enlaza por id_vacuna; el nombre sin especie podría asociar entradas distintas. |

**Diagnóstico:** No se identifica redundancia entre catálogo y aplicaciones.

#### 20. `atencion_medica`

**Cada fila representa** una atención numerada dentro del historial de un animal.

| Pauta | Evaluación |
| --- | --- |
| Semántica clara | La PK es (id_animal, num_atencion). Fecha y observaciones describen el evento; id_persona referencia al veterinario. |
| Anomalías de inserción, actualización y eliminación | No copia datos de clínica ni profesional. Los detalles específicos se separan; el tipo consulta puede existir sin subtipo. Debe mantenerse coherencia entre tipo y detalle. |
| Nulos | observaciones, id_persona e id_clinica son opcionales. Las dos FK también pueden quedar NULL por SET NULL; no se distingue ausencia original de referencia eliminada. |
| Tuplas espurias y reuniones | Los subtipos se enlazan por la pareja completa; solo num_atencion mezclaría animales distintos. |

**Diagnóstico:** Hay riesgo de inconsistencia entre tipo y el detalle de vacunación, cirugía o tratamiento, porque falta comprobar su correspondencia; consulta no exige uno de esos subtipos. Los NULL de las referencias son justificables, aunque no distinguen un dato nunca registrado de una referencia eliminada. Se documentan como límites de integridad y trazabilidad, sin afirmar que la mera presencia de NULL viole la pauta 3 ni que estas observaciones cambien la forma normal.

#### 21. `vacunacion`

**Cada fila representa** el detalle de una atención en que se aplica una dosis de una vacuna.

| Pauta | Evaluación |
| --- | --- |
| Semántica clara | Hereda la identidad compuesta de atención. 001 también hace única la terna (id_animal, id_vacuna, dosis_num). |
| Anomalías de inserción, actualización y eliminación | No copia nombre de vacuna ni fecha de atención. fecha_proxima_dosis se interpreta como programación individual. Si debiera calcularse siempre con un intervalo fijo, habría que revisar su almacenamiento. |
| Nulos | Solo fecha_proxima_dosis es opcional cuando no hay siguiente fecha programada. |
| Tuplas espurias y reuniones | Enlaza con atención por ambos componentes de su PK y con vacuna por id_vacuna. |

**Diagnóstico:** Coherente bajo la decisión de que `fecha_proxima_dosis` es una programación individual que el veterinario puede ajustar. Si siempre fuera la fecha de la atención más `intervalo_refuerzo_dias`, sería un atributo derivado entre tablas y convendría calcularlo en una consulta en vez de almacenarlo. La unicidad `(id_animal, id_vacuna, dosis_num)` obliga a numerar de forma continua los ciclos repetidos de una misma vacuna.

#### 22. `cirugia`

**Cada fila representa** el detalle quirúrgico de una atención.

| Pauta | Evaluación |
| --- | --- |
| Semántica clara | Tipo y complicaciones pertenecen a la intervención identificada por la clave de atención. |
| Anomalías de inserción, actualización y eliminación | No copia fecha, clínica ni profesional. Los datos comunes se modifican en atención; la dependencia de existencia es intencional. |
| Nulos | complicaciones permite información no registrada; NULL no afirma ausencia clínica de complicaciones. |
| Tuplas espurias y reuniones | La FK (id_animal, num_atencion) identifica una única atención. |

**Diagnóstico:** Cumple las pautas, sujeto a la compatibilidad del subtipo.

#### 23. `tratamiento`

**Cada fila representa** el diagnóstico y duración de un tratamiento asociado a una atención.

| Pauta | Evaluación |
| --- | --- |
| Semántica clara | Los atributos describen ese tratamiento, no un catálogo de enfermedades. |
| Anomalías de inserción, actualización y eliminación | No duplica datos comunes. No se presume que diagnóstico determine siempre la duración: esta se interpreta como decisión individual. |
| Nulos | No admite NULL; duracion_dias es obligatoria y positiva. |
| Tuplas espurias y reuniones | La FK compuesta enlaza con una única atención; diagnóstico o num_atencion solos podrían mezclar tratamientos. |

**Diagnóstico:** Coherente para tratamientos con duración conocida; requiere compatibilidad del subtipo.

### Resumen de hallazgos y observaciones

| Tabla | Evaluación | Tratamiento |
| --- | --- | --- |
| zona | Pauta 2: renombrar un municipio puede exigir actualizar varias colonias. Esto no demuestra municipio → entidad ni una violación de forma normal. | Se documenta la repetición de nombres; no se incorpora un catálogo adicional sin nuevas reglas. |
| animal | Riesgo de inconsistencia del estado con eventos; no es completamente derivable de estancia y adopcion. | Coordinación entre actualizaciones pendiente; no se afirma un control ya implementado. |
| atencion_medica | Riesgo de inconsistencia entre tipo y subtipo; referencias nulas con procedencia indistinguible. | Documentar integridad cruzada y límite de trazabilidad; no clasificar automáticamente los NULL como falla. |
| estancia, adopcion, seguimiento | No se demuestra que sus claves completas contengan atributos sobrantes. | Conservar las claves del modelo; los índices parciales no imponen un episodio por día. |
| clinica | Dirección tratada como un valor descriptivo unitario. | No se identifica falla por tener distinta granularidad que hogar_temporal. |
| rescate, otro, vacunacion | Semántica delimitada: condición del evento, cuidados individuales y fecha programada individual. | No se consideran fallos hipótesis descartadas por esa interpretación. |
| Subtipos de animal y atencion_medica | Falta comprobar compatibilidad entre categoría y subtipo. | Es una regla de integridad; no demuestra por sí sola tuplas espurias de una descomposición. |

En las demás tablas no se identifican infracciones bajo las interpretaciones documentadas. La forma normal se determina con F y sus cierres en 1.2–1.3, no solo a partir de estas observaciones informales.

En las reuniones deben conservarse las claves completas. Por ejemplo, unir `seguimiento` con `adopcion` solo por animal puede asociar una revisión con otro episodio; deben incluirse también `id_persona` y `fecha_adopcion`. Es un ejemplo del riesgo de perder el contexto de una asociación, no una prueba formal de descomposición.

## 1.2. Dependencias funcionales, claves y cubierta mínima

### Reglas y notación

El análisis usa las reglas de identificación del modelo heredado y las unicidades de 001, no coincidencias de los datos sintéticos. Se adopta el siguiente alcance para resolver las ambigüedades del 1.1: `condicion_inicial` describe el rescate completo; los cuidados de `otro` y la duración del tratamiento son individuales; la próxima dosis es una programación individual. No se supone que los nombres geográficos o el código postal determinen una zona. **Alcance temporal:** los índices ux_estancia_abierta y ux_adopcion_vigente impiden, respectivamente, más de una estancia abierta y más de una adopción vigente por animal. No implican una sola estancia o adopción iniciada por día ni impiden todos los solapamientos históricos. No se añade esa regla al negocio. Se conservan las combinaciones completas del esquema para identificar episodios y revisiones; no se deduce animal–fecha → hogar o adoptante.

Estas son interpretaciones explícitas del dominio para esta entrega, no nuevas restricciones comprobadas con una muestra. Si cambian, debe recalcularse F. El análisis es por relación: una FK es una dependencia de inclusión y no agrega automáticamente una DF entre atributos de tablas diferentes.

En cada fila de la tabla siguiente, **U** es el conjunto completo de columnas de esa tabla, **K** la PK y **L**, cuando existe, la otra clave. `X → U−X` abrevia una DF por cada atributo de U que no está en X. Así se especifica F de forma exhaustiva sin repetir todas las columnas. En las dos asociaciones sin atributos adicionales, F es vacío salvo dependencias triviales.

`correo` no se considera clave candidata de persona: UNIQUE permite varios NULL y no identifica obligatoriamente a todas las personas. Tampoco los índices parciales de estancia y adopcion hacen de id_animal una clave de todo el historial. Las formas normales se analizan en el modelo relacional por las reglas de identificación; los campos opcionales SQL no se usan como determinantes alternativos.

### F, justificación y cierres de cada tabla

Para cada cierre: se inicia con X, se aplican las DF indicadas y se repite hasta que no aparezcan atributos nuevos. Las flechas de la columna de cierres muestran esos pasos; **U** significa que se alcanzó toda la relación.

| Tabla | Identificadores | F y regla que lo justifica | Cierres y claves candidatas |
| --- | --- | --- | --- |
| `zona` | K = `{id_zona}`; L = `{colonia, municipio, entidad}` | K → U−K; L → U−L. Una zona tiene una ubicación descriptiva; la combinación colonia–municipio–entidad identifica una sola entrada del catálogo. | K₀ = K; K₁ = K ∪ (U−K) = U; K₂ = K₁. L₀ = L; L₁ = L ∪ (U−L) = U; L₂ = L₁. Claves: K y L. |
| `persona` | K = `{id_persona}` | K → U−K. Una persona tiene una ficha actual de nombre, contacto y registro; el correo es opcional. | K₀ = K; K₁ = K ∪ (U−K) = U; K₂ = K₁. Única clave: K. |
| `rescatista` | K = `{id_persona}` | K → U−K. Una persona tiene como máximo un perfil actual de rescatista. | K₀ = K; K₁ = K ∪ (U−K) = U; K₂ = K₁. Única clave: K. |
| `adoptante` | K = `{id_persona}` | K → U−K. Una persona tiene como máximo un perfil actual de adoptante. | K₀ = K; K₁ = K ∪ (U−K) = U; K₂ = K₁. Única clave: K. |
| `veterinario` | K = `{id_persona}`; L = `{cedula}` | K → U−K; L → U−L. Un profesional tiene un perfil y una cédula; cada cédula identifica un solo profesional. | K₀ = K; K₁ = K ∪ (U−K) = U; K₂ = K₁. L₀ = L; L₁ = L ∪ (U−L) = U; L₂ = L₁. Claves: K y L. |
| `hogar_temporal` | K = `{id_hogar}` | K → U−K. Cada hogar tiene una ficha actual de dirección, capacidad, responsable y zona. | K₀ = K; K₁ = K ∪ (U−K) = U; K₂ = K₁. Única clave: K. |
| `hogar_especie` | K = `{id_hogar, especie}` | F = ∅. Cada pareja hogar–especie representa una aceptación única; no tiene atributos descriptivos adicionales. | K₀ = K = U; sin DF que aplicar. Única clave: K. |
| `rescate` | K = `{id_rescate}` | K → U−K. Cada evento tiene una fecha, ubicación, vía de ingreso y condición general. | K₀ = K; K₁ = K ∪ (U−K) = U; K₂ = K₁. Única clave: K. |
| `animal` | K = `{id_animal}` | K → U−K. Cada animal tiene una ficha actual, un rescate de ingreso y como máximo una madre registrada. | K₀ = K; K₁ = K ∪ (U−K) = U; K₂ = K₁. Única clave: K. |
| `perro` | K = `{id_animal}` | K → U−K. Cada perro tiene una sola descripción actual de tamaño, energía y aptitud. | K₀ = K; K₁ = K ∪ (U−K) = U; K₂ = K₁. Única clave: K. |
| `gato` | K = `{id_animal}` | K → U−K. Cada gato tiene un par de resultados registrados, sin historial de pruebas en esta tabla. | K₀ = K; K₁ = K ∪ (U−K) = U; K₂ = K₁. Única clave: K. |
| `otro` | K = `{id_animal}` | K → U−K. Cada animal de categoría otro tiene una descripción y cuidados individuales. | K₀ = K; K₁ = K ∪ (U−K) = U; K₂ = K₁. Única clave: K. |
| `rescate_rescatista` | K = `{id_rescate, id_persona}` | F = ∅. Cada pareja rescate–rescatista representa una participación; no tiene otros atributos. | K₀ = K = U; sin DF que aplicar. Única clave: K. |
| `estancia` | K = `{id_animal, id_hogar, id_persona, fecha_inicio}` | K → U−K. La combinación animal–hogar–rescatista–fecha inicial identifica un episodio con cierre y motivo propios. | K₀ = K; K₁ = K ∪ (U−K) = U; K₂ = K₁. Única clave: K. |
| `solicitud_adopcion` | K = `{id_animal, id_persona, fecha_solicitud}` | K → U−K. Una pareja animal–adoptante presenta como máximo una solicitud por fecha; esta tiene estado y observaciones. | K₀ = K; K₁ = K ∪ (U−K) = U; K₂ = K₁. Única clave: K. |
| `adopcion` | K = `{id_animal, id_persona, fecha_adopcion}` | K → U−K. Una pareja animal–adoptante registra como máximo una adopción por fecha, con devolución propia. | K₀ = K; K₁ = K ∪ (U−K) = U; K₂ = K₁. Única clave: K. |
| `seguimiento` | K = `{id_animal, id_persona, fecha_adopcion, num_seguimiento}` | K → U−K. Cada adopción identificada por su clave completa numera sus revisiones; cada revisión tiene una ficha propia. | K₀ = K; K₁ = K ∪ (U−K) = U; K₂ = K₁. Única clave: K. |
| `clinica` | K = `{id_clinica}`; L = `{nombre, direccion}` | K → U−K; L → U−L. Cada establecimiento tiene una ficha; la combinación nombre–dirección identifica una clínica. | K₀ = K; K₁ = K ∪ (U−K) = U; K₂ = K₁. L₀ = L; L₁ = L ∪ (U−L) = U; L₂ = L₁. Claves: K y L. |
| `vacuna` | K = `{id_vacuna}`; L = `{nombre, especie_destino}` | K → U−K; L → U−L. Cada entrada de vacuna tiene especie e intervalo; nombre–especie identifica una entrada. | K₀ = K; K₁ = K ∪ (U−K) = U; K₂ = K₁. L₀ = L; L₁ = L ∪ (U−L) = U; L₂ = L₁. Claves: K y L. |
| `atencion_medica` | K = `{id_animal, num_atencion}` | K → U−K. Cada animal numera sus atenciones; cada número dentro del animal identifica una ficha de atención. | K₀ = K; K₁ = K ∪ (U−K) = U; K₂ = K₁. Única clave: K. |
| `vacunacion` | K = `{id_animal, num_atencion}`; L = `{id_animal, id_vacuna, dosis_num}` | K → U−K; L → U−L. Cada atención de vacunación tiene vacuna, dosis y programación; la misma dosis de la misma vacuna no se registra dos veces para un animal. | K₀ = K; K₁ = K ∪ (U−K) = U; K₂ = K₁. L₀ = L; L₁ = L ∪ (U−L) = U; L₂ = L₁. Claves: K y L. |
| `cirugia` | K = `{id_animal, num_atencion}` | K → U−K. Cada atención quirúrgica tiene un detalle de tipo y complicaciones. | K₀ = K; K₁ = K ∪ (U−K) = U; K₂ = K₁. Única clave: K. |
| `tratamiento` | K = `{id_animal, num_atencion}` | K → U−K. Cada atención de tratamiento tiene un diagnóstico y duración individuales. | K₀ = K; K₁ = K ∪ (U−K) = U; K₂ = K₁. Única clave: K. |

**Minimalidad y exhaustividad de las claves.** En F todos los determinantes no triviales son K o L. Si X no contiene completo ninguno, no se dispara ninguna DF: X⁺ = X. Por tanto, ningún subconjunto propio de K o L alcanza U; tampoco existe una tercera clave que no contenga una de ellas. En las asociaciones con F vacío solo U se cierra a U. Esta prueba cubre también las claves compuestas, no solo las simples.

Ejemplos explícitos: en estancia, quitar id_hogar de K deja `{id_animal, id_persona, fecha_inicio}`; ninguna DF se activa y faltan id_hogar, fecha_fin y motivo_salida. En adopcion, `{id_animal, fecha_adopcion}⁺` permanece igual y no obtiene id_persona. En seguimiento, `{id_animal, fecha_adopcion, num_seguimiento}⁺` tampoco obtiene id_persona. En zona, `{colonia, municipio}⁺` permanece igual; falta entidad. En vacunacion, `{id_animal, id_vacuna}⁺` permanece igual; no obtiene dosis_num ni num_atencion. Los otros subconjuntos propios se resuelven por el mismo criterio anterior.

### Reducción a una cubierta mínima G

1. **Derechos simples.** Separar cada `X → U−X` en `X → a`, para cada `a ∈ U−X`. No se incluyen DF triviales. Por ejemplo, rescate produce cinco DF: id_rescate determina, separadamente, descripcion_lugar, fecha_hora, condicion_inicial, tipo_ingreso e id_zona.
2. **Atributos sobrantes a la izquierda.** No se elimina ninguno. Para cualquier atributo b de un determinante compuesto X, `(X−{b})⁺ = X−{b}`: no contiene K ni L completos y no alcanza el atributo del lado derecho. Para determinantes simples, el cierre vacío es vacío. Los ejemplos anteriores ilustran los cierres que justifican conservar los determinantes.
3. **DF redundantes.** Se retiran únicamente las DF de la siguiente tabla. El cierre indicado se calcula después de retirar la DF y conservando las restantes de G; demuestra cada eliminación.

| Tabla | DF que se eliminan, cada una con derecho simple | Cierre que las sigue implicando |
| --- | --- | --- |
| veterinario | cedula → especialidad | `{cedula}` → añadir id_persona → añadir especialidad; se alcanza U. |
| clinica | `{nombre, direccion}` → telefono; `{nombre, direccion}` → tipo | `{nombre, direccion}` → añadir id_clinica → añadir telefono y tipo; se alcanza U sin las dos DF retiradas. |
| vacuna | `{nombre, especie_destino}` → intervalo_refuerzo_dias | Ese par → añadir id_vacuna → añadir intervalo_refuerzo_dias; se alcanza U. |
| vacunacion | `{id_animal, id_vacuna, dosis_num}` → fecha_proxima_dosis | Esa terna → añadir num_atencion → aplicar K → fecha_proxima_dosis; se alcanza U. |

**G completo**, usando siempre derechos simples:

- Para las 23 tablas: conservar `K → a` por cada `a ∈ U−K` (ninguna en las dos asociaciones sin atributos adicionales).
- Añadir en zona: `{colonia, municipio, entidad} → id_zona`.
- Añadir en veterinario: `cedula → id_persona`.
- Añadir en clinica: `{nombre, direccion} → id_clinica`.
- Añadir en vacuna: `{nombre, especie_destino} → id_vacuna`.
- Añadir en vacunacion: `{id_animal, id_vacuna, dosis_num} → num_atencion`.

No quedan DF redundantes: al quitar `K → a`, K no obtiene a; si a forma parte de L tampoco puede completar L para buscar otra ruta, y si no pertenece a L, las DF alternativas solo recuperan identificadores ya presentes. Al quitar `L → b`, L no obtiene el componente b de K y no activa K. No quedan atributos sobrantes por la prueba del paso 2. Así G es mínima.

**Equivalencia F ≡ G.** G ⊆ F tras separar derechos, de modo que F implica G. Las cinco DF retiradas se recuperan mediante los cierres de la tabla; las demás siguen en G. Por tanto G implica F y F⁺ = G⁺.

## 1.3. Formas normales, descomposición y migración

### Diagnóstico formal del esquema actual

**Las 23 tablas están en BCNF respecto a F y a las reglas delimitadas en 1.2**; en consecuencia también satisfacen 3FN, 2FN y 1FN. La conclusión es relativa a ese conjunto de reglas, no a cualquier interpretación posible del dominio.

- **1FN:** cada atributo contiene un valor de su dominio; las especies aceptadas están en filas de hogar_especie. Los textos se usan como descripciones unitarias, no como listas de hechos que deban consultarse separadamente.
- **BCNF:** toda DF no trivial de F tiene como determinante una clave K o L. Para cualquier DF no trivial de F⁺, su determinante debe contener K o L para activar alguna regla; por ello es superclave. No hay dependencias parciales de atributos no primos ni transitivas con determinante que no sea superclave. En las dos asociaciones con F vacío, BCNF se satisface de forma vacía.

| Tablas | Prueba aplicable | Forma máxima comprobada |
| --- | --- | --- |
| persona, rescatista, adoptante, hogar_temporal, rescate, animal, perro, gato, otro, solicitud_adopcion, atencion_medica, cirugia, tratamiento | Única clave K; K⁺ = U y ningún conjunto que omita parte de K activa una DF. | BCNF |
| estancia, adopcion, seguimiento | Única clave K completa; K⁺ = U. No se adopta la regla adicional de un episodio por día. | BCNF |
| zona, veterinario, clinica, vacuna, vacunacion | K y L son claves, con los cierres mostrados en 1.2; todos los determinantes no triviales son superclaves. | BCNF |
| hogar_especie, rescate_rescatista | F sin DF no triviales; la única clave es U. | BCNF |

No es necesario alterar las 23 tablas para cumplir 3FN. Se aplica la alternativa explícita del enunciado: construir una tabla desnormalizada con datos del dominio y normalizarla. Se conserva como ejemplo aislado en el esquema SQL `normalizacion`; `public` sigue siendo el modelo operativo para las consultas de HuellaRed. El ejemplo es una instantánea de datos sintéticos existentes, no otro catálogo operativo que deba mantenerse sincronizado.

### Relación desnormalizada y anomalías

La migración 002 construye `normalizacion.rescate_zona` mediante un SELECT de rescate unido con zona, tomando todos los rescates existentes y sus zonas. Definimos:

- r = id_rescate; z = id_zona.
- E = {descripcion_lugar, fecha_hora, condicion_inicial, tipo_ingreso}.
- Z = {colonia, municipio, entidad}.
- D = {r, z} ∪ E ∪ Z.
- F_D = {r → E, r → z, z → Z, Z → z}, con derechos separados al aplicar los algoritmos.

Cierres: `r⁺`: {r} → {r}∪E∪{z} → D. `z⁺` = {z}∪Z, y `Z⁺` = Z∪{z}: ninguno obtiene r ni E. Como r no aparece en ningún derecho, toda clave debe contenerlo; **r es la única clave**.

D está en **2FN**: sus valores son atómicos y la única clave es simple. No está en 3FN ni BCNF: `z → colonia` (y los otros nombres) tiene determinante no superclave y derecho no primo; también `Z → z` incumple esos criterios. Los nombres se repiten por cada rescate: corregir una zona exige varias actualizaciones; no puede registrarse una zona sin un rescate en D; eliminar su último rescate pierde su descripción dentro de D. Estas anomalías pertenecen al ejemplo, no a las tablas public ya separadas. Las dos zonas sin rescates no aparecen en D debido al JOIN usado para construirla; eso ilustra que D no representa zonas sin eventos, no una eliminación ejecutada ni una pérdida causada por la descomposición. La anomalía de eliminación descrita es el caso hipotético de borrar el último rescate de una zona en D.

### Descomposición, pérdida y preservación

Se separa D en:

1. **ZONA_N(z, colonia, municipio, entidad)**, con claves z y Z.
2. **RESCATE_N(r, descripcion_lugar, fecha_hora, condicion_inicial, tipo_ingreso, z)**, con clave r y FK a ZONA_N.

El paso elimina de la tabla de eventos la dependencia transitiva `r → z → Z`; la regla `z → Z` se conserva en ZONA_N, no se elimina del negocio. ZONA_N está en BCNF porque z y Z son claves. RESCATE_N está en BCNF porque toda DF no trivial parte de la clave r. No se necesita quedarse solo en 3FN ni sacrificar una dependencia.

**Reunión sin pérdida:** la intersección es {z}. Su cierre incluye todos los atributos de ZONA_N; por tanto la intersección determina una de las relaciones y se cumple el criterio de descomposición binaria sin pérdida. La PK de ZONA_N y la FK obligatoria de RESCATE_N implementan la asociación.

**Preservación:** en RESCATE_N se comprueban `r → E` y `r → z`; en ZONA_N, `z → Z` y `Z → z`. La unión de estas proyecciones contiene todas las DF de F_D y recupera `r → Z` por transitividad, sin reunir tablas para comprobar las DF básicas.

### Migraciones y conservación de datos

Orden después de esquema, 001 y carga heredada:

1. [002-ejemplo-desnormalizado.sql](migraciones/002-ejemplo-desnormalizado.sql): materializa D mediante `INSERT ... SELECT`, sin datos escritos a mano; exige que existan rescates.
2. [003-normalizar-rescates.sql](migraciones/003-normalizar-rescates.sql): copia las proyecciones a `normalizacion.zona` y `normalizacion.rescate`, impone PK, UNIQUE y FK; compara la reconstrucción con D mediante `EXCEPT ALL` en ambos sentidos. Solo si no hay diferencias sustituye la tabla D por una vista de su reunión. Se guardan únicamente las zonas presentes en D, no zonas ajenas al ejemplo.

Las migraciones se ejecutan después de la carga mediante `docker/preparar_base.py`, con transacciones, bloqueo y registro de huellas en huellared_control.migraciones. Un reinicio no vuelve a crear el ejemplo ni recarga public. La vista mantiene accesible el resultado reconstruido sin almacenar los nombres por rescate. No se borra ni se recarga ninguna tabla de public.

La verificación de filas complementa la prueba teórica: comprueba esta ejecución; no sustituye el argumento para cualquier instancia válida. El esquema normalizacion concede lectura a los roles del proyecto; la administración de las migraciones corresponde al usuario de inicialización.

### Verificación realizada

El 17 de noviembre de 2026 se probó la versión inicial de las migraciones en una copia aislada con **PostgreSQL 18.6**, usando el generador y cargador heredados. Los resultados SQL siguientes corresponden a esa ejecución; la modificación posterior que enumera las columnas de la instantánea en 003 se revisó, pero aún no se volvió a ejecutar:

| Comprobación | Resultado observado |
| --- | --- |
| Carga original | 23 tablas, 7,205 filas insertadas y cero rechazos. |
| Ejemplo antes y después | 420 rescates; 92 zonas distintas presentes en esos rescates. Las otras dos zonas del catálogo original no pertenecen a D. |
| Reconstrucción | 420 filas; diferencia simétrica con multiplicidad: 0. |
| Conservación de public | Conteos y huellas de todas las filas de las 23 tablas iguales antes y después. |
| Segunda ejecución del inicializador | Omite carga y migraciones ya registradas; no duplica filas. |
| Consulta del ejemplo | Vista de reconstrucción creada y privilegio SELECT disponible para huellared_consulta. |
| Cierres y cubierta | Claves candidatas y cubierta mínima recalculadas para las 23 tablas con el F documentado, sin la inferencia de un episodio por día: equivalencia F/G, determinantes mínimos y ausencia de DF redundantes comprobadas. |

El arranque previo de HuellaRed se comprobó en Docker con PostgreSQL 17: la salida proporcionada registró la carga de 7,205 filas y las migraciones 002–003 con `diferencias=0`. La Parte 3 amplía ese flujo con sismos, consultas y regeneración del grupo; su comando y validación actual están en el [README](../README.md). Las migraciones ya registradas no se repiten.
