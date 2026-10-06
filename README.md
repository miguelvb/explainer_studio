# Explainer Studio

Convierte un PDF, un texto o un guion en un **vídeo explicativo animado**. Todo lo que se ve en pantalla son *assets* de movimiento deterministas (`studio/player/assets.js`): nada de imágenes de archivo ni clips de IA. Cada asset es una función pura del tiempo, así que los fotogramas salen exactos y **la película se reajusta sola cuando se genera la voz real**.

```
fuente ──ingest (LLM)──► story.json ──validate──► build/ (horario, subtítulos, reproductor)
                              │                        │
           tts (voz) ─────────┴─ tiempos reales ─► build ─► render ─► video_silent.mp4 ─► mux (+música, ducking) ─► final.mp4
```

Firma: *Arkinos · Explainer Studio*.

---

## 1. Instalación

```bash
pip install -r requirements.txt            # playwright, numpy, Pillow, openai (solo tts), pypdf…
playwright install chromium
# ffmpeg y ffprobe deben estar en el PATH
```

### Configuración (`.env`)

Copia `.env.example` a `.env` junto a `explainer.py` (solo se lee ahí; las variables de la shell tienen prioridad). Pon tus claves **solo en tu `.env`**, nunca en el repositorio.

| Variable | Para qué |
|---|---|
| `ELEVENLABS_API_KEY` | Voz con ElevenLabs (la que usamos) |
| `OPENAI_API_KEY` | Voz OpenAI y/o paso LLM |
| `ANTHROPIC_API_KEY` / `OPENROUTER_API_KEY` | Paso LLM (`ingest`, `verify`) |
| `TTS_PROVIDER`, `OPENAI_TTS_*` | Proveedor y ajustes de voz globales |
| `STUDIO_LLM_PROVIDER`, `STUDIO_LLM_MODEL` | Proveedor/modelo del paso LLM |

Precedencia: línea de comandos > `meta` de `story.json` > `.env` > valores por defecto. Así una película puede tener su voz propia sin tocar el `.env`.

---

## 2. Flujo de trabajo

El método que seguimos (ver `VISUAL_RULES.md`): **primero** el guion, **después** qué se ve en cada frase (storyboard en texto, se aprueba), **después** se construye.

```bash
python explainer.py validate -p examples/test            # comprobaciones estáticas + cada cue en un navegador real
python explainer.py build    -p examples/test --estimate # horario con tiempos estimados (necesario antes de preview)
python explainer.py preview  -p examples/test --scene 3  # hoja de contactos en build/preview/sheet.png
python explainer.py voices   -p examples/test            # probar voces y pronunciaciones
python explainer.py all      -p examples/test            # build → voz → reajuste → música → render → mux
```

Variantes de `all`:

| Opción | Efecto |
|---|---|
| `--from A --to B` / `--scene N` | solo ese rango de escenas (`final_scenes_A-B.mp4`) |
| `--draft` | render rápido: 854 px, 20 fps, ultrarrápido (revisar ritmo y contenido) |
| `--skip-tts` | usa la voz ya generada, o tiempos estimados con solo música |
| `--workers N` | escenas renderizadas en paralelo (por defecto: núcleos − 2, mínimo 2) |
| `--burn` | incrusta subtítulos en el vídeo |
| `--force-render` | rehace también las escenas sin cambios |

Otros comandos: `new · ingest · prompt · catalog · script · music · render · mux · verify · mark`.

### Qué hay entre `video_range.mp4` y `final`

`video_range.mp4` (o `video_silent.mp4` para la película entera) es **solo imagen**: las escenas ya renderizadas, pegadas sin recodificar. `final*.mp4` es esa misma imagen con el sonido montado: cada frase de voz en su instante exacto, la música bajando cuando habla la voz, volumen normalizado y fundido final. Puedes rehacer el audio sin volver a renderizar la imagen.

### Rendimiento

- El render captura cada fotograma con Chromium y lo manda a ffmpeg.
- **Fotogramas idénticos:** si el estado visual no cambia entre dos fotogramas, se reutiliza la imagen anterior (firma del DOM). El resultado es idéntico; el aviso "N/M frames reused" lo indica. Las escenas con `canvas` no se saltan fotogramas. Desactivar: `NODEDUP=1`.
- **Caché por escena:** una escena solo se rehace si cambian sus cues, el reproductor (`assets.js`, `style.css`) o el tamaño/fps. Tocar el motor invalida todas: haz el render final de una vez, y revisa antes con `preview` y `--draft`.

---

## 3. `story.json`

Escenas → `beats` (frases de voz, ids automáticos `3a`, `3b`…) y `cues` (qué se ve). Un cue lleva `a` (asset), `at`/`until` (anclas) y `p` (propiedades). La descripción completa de assets está en `prompts/script_from_doc.md` (se genera desde `studio/catalog.py`, así que siempre está al día; `python explainer.py catalog`).

**Anclas de tiempo** (los cues cuelgan de palabras y frases, así que cambiar la voz o el texto no rompe la sincronía):

| Ancla | Significa |
|---|---|
| `"3c"` | inicio de la frase 3c |
| `">3c"` | final de la frase 3c |
| `"3c#palabra"` | el instante en que se dice esa palabra (sin distinguir mayúsculas) |
| `S3` / `E3` | inicio / fin de la escena 3 |
| `+1.5` / `-0.5` | desplazamiento en segundos |

**Frases**: pueden ser texto o `{text, pause}`; `pause` añade segundos de silencio detrás de la frase.

**`meta`** (por película): `title`, `lang`, `provider`, `el_voice`, `el_model`, `el_speed`, `el_pronunciation` (tabla de pronunciación), `pre`/`post`/`gap` (silencios), `lead` (silencio antes de la primera frase), `fadein` (entrada de la música, s), `fadeout` (salida), `mark` (logo vectorizado), `typing_sound` (sonido de teclas; apagado en nuestras películas).

---

## 4. El asset `world` y `worldkit.py`

La mayoría de escenas nuevas usan `world`: un diagrama persistente de 960×540 cuyos **nodos** aparecen y desaparecen con anclas, con **enlaces** entre ellos y una **cámara** (`cam`) que vuela entre nodos. `studio/worldkit.py` tiene los constructores: `agent_named`, `agent`, `agent_group`, `hugging_face`, `counter`, `clock`, `link`, `msg_feed`, `sheet`, `article`, `judge`, `console`, `folder_view`, `bulb`…

Reglas del motor (valen para todas las escenas):

- **Un enlace nunca aparece antes que sus dos extremos.**
- **Dos tipos de enlace.** *Relación* (pertenece a, es parte de, lo tiene, secuencia): segmento **recto y continuo**, sin bolitas (`rel: true`; se asigna solo a enlaces con `chip`, `key`, `person`, `exam`, discontinuos y `sandbox→sheet`, ver `classify_links` en `worldkit.py`). *Comunicación* (viaja información): curva **en S** (dos curvaturas) con bolitas, que **rodea los demás nodos**; si no encuentra paso libre, `validate` avisa.
- **Enlaces ortogonales** (`orth`): tramos rectos con giros de 90° y esquinas redondeadas, sin bolitas; los enlaces de comunicación son curvos, con bolita.
- **Parpadeo** (`blink`, `bf`, `bat`) y **apagado dramático** (`flick`: se apaga varias veces y termina en `off`/`dim`/`on`).
- **Barras** (`bar`) para presupuestos; **iconos** de línea (`ok*`, `ko*`, `sig*`, `fl*`, `idea*`, `sc*`, `orb`…).
- **Guardia anti-overflow:** todo texto dentro de un contenedor se mide y, si no cabe, se reduce (mínimo 60 %) o se comprime; si queda fuera por abajo, se oculta. `validate` avisa de cada ajuste ("text shrunk to fit…"), y de cada texto oculto como error.
- **Fuentes por elemento** (`font` en el nodo): *Press Start 2P* por defecto en las citas (`quote`) y en los nombres de agentes (`acard`, `judge`, `agent`); el resto, monoespaciada; sello en *Share Tech Mono*. Las fuentes viajan en `studio/player/fonts/` (licencia OFL), así que el render no depende de internet.

### Sello de Arkinos (`seal`)

Marca A-constelación con doble anillo y envolvente de puntos, más créditos. Propiedades: `text` (`|` salta de línea), `sub`, `links` (lista de enlaces que aparecen al final), `type` (letras por segundo: máquina de escribir), `scale`, `cy`, `ty`, `tfs`, `small` (firma en la esquina), `black` (fundido a negro). Se usa como intro (la voz lee el título) y como cierre.

---

## 5. Reglas visuales

Resumen de `VISUAL_RULES.md` (léelo antes de diseñar una escena):

1. **La película es una novela gráfica de lo que ocurre**, no pantallas de texto que repiten la voz.
2. Agente = icono de OpenAI. Los mensajes se ven como **enlaces con bolitas** que viajan.
3. El texto son **etiquetas pequeñas**; solo los números clave pueden ser grandes.
4. **Espacio para respirar**, agentes pequeños, estética oscura/transparente.
5. Fechas siempre con el mes escrito. Artifactory = ventana de lista de carpetas.
6. Palabras en inglés: añadir `el_pronunciation` y comprobar con `voices`.

---

## 6. Estructura del repositorio

```
explainer.py        línea de comandos
studio/             motor: spec (horario), audio (voz, música, mux), render, worldkit, catalog
studio/player/      reproductor web: assets.js, style.css, fonts/
examples/           películas y pruebas (hf-swarm-vivido-es, hf-rob-es, test, opts…)
prompts/ bible/     prompts del paso LLM y material de fuente
brand/              marca Arkinos (svg/png)
VISUAL_RULES.md     reglas visuales
```

Un proyecto contiene `story.json`, `script.md` (guion generado), `audio/`, `build/` y, opcionalmente, `mark.txt`. En `examples/test`, `story.json` **se genera** con `python examples/test/gen_test.py` (y `gen_8_17.py`): edita esos scripts, no el JSON.

---

## 7. Cómo añadir un asset

1. En `assets.js`: `A.miasset=(host,props,C)=>{ …DOM…; return t=>{ …actualizar para el tiempo local t… } }` (`C.T(x)` convierte un ancla o número en segundos desde el inicio del cue).
2. Descríbelo en `catalog.py` (tipo, uso, propiedades, ejemplo): el validador y el prompt lo recogen solos.
3. Si es un icono de `world`, añádelo a `ICON` y úsalo como `kind` del nodo.

---

## 8. Límites y problemas habituales

- Colores y tema oscuro fijos; solo la marca es personalizable.
- Máximo 26 frases por escena.
- El paso LLM puede malinterpretar una fuente: ejecuta `verify` y revisa la hoja de contactos.
- Si cambias frases o su orden, las pistas de voz de esos ids se regeneran (la caché es por texto + voz).
- Si `validate` avisa de un texto ajustado, acórtalo o amplía su contenedor.
- La demo `examples/mars-orbiter` está escrita de memoria: revísala antes de publicarla.
