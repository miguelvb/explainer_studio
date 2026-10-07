# Prompt de arranque para una IA que continúa este proyecto

> Léelo entero antes de tocar nada. Está escrito para una IA (Claude u otra) que empieza una sesión nueva y debe seguir produciendo películas explicativas con **Explainer Studio** exactamente como se ha hecho hasta ahora. Complementa a `README.md` (manual técnico) y `VISUAL_RULES.md` (regla visual nº 1). Si algo de aquí contradice una orden directa del usuario, manda el usuario.

## 1. Quién es el usuario y cómo trabaja

- Se hace llamar **Arkinos** (científico, músico, astrofísico, divulgador). Habla **español**; responde siempre en español, de forma concisa y directa, sin florituras.
- **Él ejecuta el audio y el render** en su propio ordenador/VPS (6 vCores, 12 GB, sin GPU) con su `.env`. **Nunca pidas claves de API.** Tu trabajo es dejar el proyecto listo en el repositorio (`git push` a `main`) y decirle qué regenerar tras `git pull`.
- Revisa los vídeos renderizados y te manda **capturas con el minuto** y una frase corta ("aquí el enlace debe ser de segmentos rectos", "no se oye la agitación"). Cada mensaje suele ser **una corrección puntual**: localiza la escena, arréglala, comprueba con una vista previa, valida, haz commit y push, y contesta en pocas líneas.
- Método base: **primero** guion, **después** qué se ve en cada frase (storyboard en texto, se aprueba), **después** se construye y se retoca escena a escena. Quiere ver PNG antes de renderizar vídeo.
- Si algo no se entiende de lo que dice, pregunta **una** cosa corta; si es una corrección clara, hazla.
- Marca de la casa: las películas se firman *Arkinos · Explainer Studio*; cierre con sello "Arkinos @ oct 2026".

## 2. Qué es el proyecto

Programa (Python + Chromium/Playwright + ffmpeg) que convierte un guion en un vídeo explicativo animado. Todo lo que se ve son *assets* de movimiento deterministas (`studio/player/assets.js`), sin imágenes de archivo ni clips de IA. La voz es ElevenLabs; la película se reajusta sola a los tiempos reales de la voz porque todo cuelga de **anclas de palabra** (`"3c#palabra+0.4"`).

Mapa del código:

| Dónde | Qué |
|---|---|
| `explainer.py` | CLI: `validate · build · preview · voices · all · music · render · mux …` |
| `studio/player/assets.js`, `style.css` | assets, motor de enlaces, fondo, cámara |
| `studio/storykit.py` | helpers genéricos de escena, cargador (`gen`), lint y `newfilm` |
| `studio/worldkit.py` | constructores del asset `world` (`agent_named`, `link`, `counter`, `msg_feed`, `judge`, `console`, `folder_view`, `sheet`, `article`, `seal`…) y `classify_links` |
| `studio/spec.py` | resolución de anclas y horario (gemelo Python del resolvedor JS) |
| `studio/render.py` | render por escenas, caché, sondas de aviso |
| `studio/sound.py`, `studio/audio.py` | música por capítulo, ambiente, efectos, mezcla, ducking |
| `examples/hf-swarm-vivido-es/` | **película activa** (ver §3) |
| `bible/`, `brand/`, `prompts/` | material de marca y prompts de partida |

## 3. Estado de las películas

- **`examples/hf-swarm-vivido-es`** — *"El primer ataque de un enjambre de agentes"*, versión "como vivido": 21 escenas (0–20), la última con créditos. **Es la buena y la que se sigue puliendo.** Viene del antiguo proyecto `test`.
- **Rama `antiguo-video`** — el antiguo `hf-swarm-vivido-es` descartado. No tocar.
- **`hf-rob-es`** (resumen en español del vídeo de Rob Wiblin, 80,000 Hours, ~10 min) — **en espera** hasta que el usuario diga adelante. Cuando toque: primero guion y storyboard en texto, luego PNG, luego render.
- Otros proyectos de `examples/` (`hf-swarm-es`, `hf-incident*`, `mars-orbiter`, `cinematic-demo`, `opts`) son anteriores; no los des por abiertos sin preguntar.

### Cómo se genera `story.json` (importante)

**No edites `story.json` a mano:** lo escribe `studio/storykit.py` (`python explainer.py gen -p <película>`; `validate`/`build`/`all` lo regeneran solos).

- La carpeta de la película tiene `film.py` (META y PRONUNCIATION), `narration.md` (la narración: **fuente de verdad**; `script.md` lo genera `build` solo para leer) y `scenes/sNN.py` (un script por escena).
- Un script de escena define `cues` y, opcionalmente, `MUSIC`, `MOOD`, `INTENSITY`, `SFX` y `PROFILE` (`'house'` por defecto, y lo usan todas las escenas; `'raw'` solo para casos excepcionales). Corre en un espacio de nombres compartido con los helpers de `storykit` y `worldkit`.
- La numeración de escenas y frases (`9c`, `17e`…) sale de `narration.md`: una línea `**9c** texto` por frase; `(pausa 2.4)` tras el id añade silencio.
- Película nueva: `python explainer.py newfilm -p examples/<nombre> --title "…"`.
- Tras cualquier cambio: `python explainer.py validate -p examples/hf-swarm-vivido-es` (debe dar **0 errores**; hay ~26 avisos conocidos). Si has refactorizado, comprueba que `story.json` no cambia (`git diff --stat`).
- Si cambias el texto de una frase, avisa al usuario de que debe **regenerar la narración de esa escena**; los tiempos de las demás se recalculan solos.
- `build/` y `audio/` están en `.gitignore`: viven solo en la máquina de cada uno.

Vista previa de escenas (hoja de contactos en `build/preview/sheet.png`):

```python
from pathlib import Path; from studio import render
render.preview(Path('examples/hf-swarm-vivido-es'), times=[...segundos...], w=640)
```

(Requiere `build --estimate` antes.) Mira siempre la imagen antes de decir que está arreglado.

## 4. Reglas visuales (no negociables)

1. **Novela gráfica de lo que ocurre, nunca pantallas de texto que repiten la voz.** Si se habla de un agente, se ve un agente; si manda un mensaje, se ve viajar el mensaje. Las letras son solo etiquetas pequeñas; los números clave pueden ser grandes.
2. Un "agente" es el **icono de OpenAI**, no una persona. Personajes simples; las acciones deben verse.
3. **Composición con aire:** contenedores pequeños, agentes pequeños, mucho espacio vacío. "Cuántos" = contenedor abierto por arriba con filas que se desvanecen.
4. **Fechas siempre con el mes escrito** ("08 julio 2026").
5. **Tipografía:** *Press Start 2P* para citas y nombres de agentes; *Share Tech Mono* para títulos y textos de Arkinos; el resto, monoespaciada. El sonido de tecleo antiguo está **apagado** (`typing_sound` off): lo sustituye el teclado suave de `sound.py`.
6. **Enlaces** (reglas del motor, ya implementadas; respétalas al añadir enlaces):
   - *Relación* (pertenece a, secuencia, lo tiene): segmentos **rectilíneos y continuos** con esquinas redondeadas, sin diagonales, sin bolitas.
   - *Comunicación* (viaja información): curva suave **sin arcos grandes**, sale y llega a **90° de la superficie**, con bolitas; si hay algo en medio, baja a recorrido rectilíneo/zigzag elegante que esquiva obstáculos. **Nunca salen por arriba salvo que el destino esté arriba o abajo.**
   - Un enlace no aparece antes que sus dos extremos. Las relaciones se asignan solas con `classify_links`; fuerza una con `OR(...)`/`orth` o `rel`.
7. Cuando el usuario dice "enlace de segmentos rectos y no discontinuo": usa un enlace `orth` con `solid=True`.
8. Fondo: capa cinematográfica oscura azul (`meta.background`; actualmente `poly`; alternativas `fluid`, `sand`, `network`, `diamonds`, `cubes`, `grid`, `none`). Vira a rojo con la tensión.
9. Narración: **explicativa, no descriptiva**; cada concepto se explica la primera vez con palabras sencillas (lector lego/adolescente). Los términos en inglés se pronuncian bien: tabla `el_pronunciation` en `meta`.
10. Voz: ElevenLabs **Cristina**, modelo `eleven_v4`, velocidad 0,95, estabilidad 0,5.

## 5. Sonido (`studio/sound.py`)

Todo sintetizado, sin descargas. Se configura en `meta` de la película: `music_style='mix'`, `music_db=-8`, `sfx_db=-12`, `duck_ratio=2.5`, `duck_threshold=0.04`, `ambience=1.0`.

- **Música:** mezcla por capítulo (`music` por escena: estilo o `{estilo: peso}`), con fundidos de 4 s, curva de intensidad por escena y estado `mood:'tense'`.
- **Efectos:** `sfx_events()` los deriva de los nodos de cada cue, **sin tocar la película**. Existen: aparición de agente (`spawn`), creación (`create`), conexión (`connect`), elemento de lista (`tick`), movimiento (`slide`), contador (`count`), scroll/lectura (`scroll`), teclado suave (`keystroke`) y cursor (`cursor`), mensaje de agente (`msg`, buzz robótico), error (`error` + golpe) para cruces/suspensos, validación (`validate`) al juntarse banderas, alarma suave (`alarm`) con bandera parpadeante, motor (`engine`) con agitación (`shake`), apagón dramático (`blackout` + `impact`/`sting`) con `flick`, pregunta/respuesta/info (`ask`/`answer`/`info`), buzz de inspección (`buzz`), whoosh de escena y de ventanas.
- Para añadir sonido a un tipo de nodo: `KIND_SFX` (tabla nodo→efecto) o un bloque nuevo en `sfx_events`; el sonido en sí, en `sfx_sound(kind, rng)`. Los eventos densos se filtran con la tabla `gap`. Un nodo se silencia con `nosfx=True`.
- **Nivel:** los efectos se mezclan *después* del ducking; si un efecto "no se oye", suele ser de ganancia/duración, no de código. Normaliza picos a ~0,8 y usa `tanh` si es muy fuerte.
- **Memoria:** `render_mix` va por disco y en bloques; en una máquina de 8 GB el render de la capa `pad` tarda mucho. No lo repitas sin necesidad.

## 6. Recetas de trabajo

- *"No se oye X"*: localiza el nodo (`grep` en `scenes/`), mira qué eventos genera `sound.sfx_events(root, D)` en esa franja y sube ganancia/duración o añade el evento.
- *"Este enlace…"*: localiza la escena por el texto o el minuto (sumando `S{n}` en `build/data.json['sched']`), cambia el enlace en el generador, vuelve a generar, vista previa, valida.
- *"Quita esta frase"*: edita `narration.md`, regenera y avisa de rehacer la narración de esa escena.
- Convierte "minuto:segundo" del vídeo del usuario en escena con `D['sched']['S{n}']['s']`.
- Los 21 avisos de "link crosses another node" son avisos de la sonda de render (un enlace roza algo), no errores; arréglalos solo si el usuario señala una escena.

## 7. Pendiente conocido

- Enlaces para el sello final (propiedad `links` del `seal`) — los debe dar el usuario.
- Nombres provisionales por confirmar: ZETA417, zzDM_a_b, A/B, LILY, MARB051.
- Prueba de pronunciación de "Hold".
- Elegir fondo definitivo (hoy `poly`).
- Decidir si se retoman `hf-rob-es` (en espera) y el resto de proyectos antiguos.

## 8. Etiqueta de git y de entrega

- Trabaja en `main`; commits pequeños y descriptivos. Si el entorno lo indica, termina el mensaje de commit con las líneas de atribución que te dé el sistema.
- Tras cada cambio relevante: **valida (0 errores) → mira la vista previa → commit → push → di en 2–4 líneas qué cambió y qué debe regenerar** (casi siempre: `git pull`, regenerar sfx/narración de las escenas afectadas y renderizar).
- No inventes claves, no pidas `.env`, no ejecutes la síntesis de voz.
