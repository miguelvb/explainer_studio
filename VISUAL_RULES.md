# Regla visual nº 1 (la más importante)

**Las películas son una novela gráfica de lo que ocurre, no pantallas de texto que se limitan a repetir lo que dice la voz.**

- Lo principal es la imagen de lo que pasa. Una pantalla que solo copia la frase que se oye no aporta nada: para eso ya están los subtítulos.
- **A veces sí se puede repetir** en pantalla texto de la voz: una frase clave, una cita o un dato que refuerce la idea. Siempre como apoyo de la escena, no en lugar de ella.
- Si la voz habla de un agente, **se ve un agente**. Si un agente manda un mensaje, **se ve a ese agente mandándolo** (el mensaje viajando hacia donde llega), no el texto del mensaje en una pantalla nueva.
- Las letras solo son etiquetas pequeñas (un nombre, una fecha, un identificador largo en letra pequeña). Los números clave sí pueden ser grandes.
- Los contenedores que agrupan varias cosas pueden ser grandes; el texto, no.
- Se mantiene la identidad visual de las primeras películas (tarjetas, secuencias, terminal, jerarquía, banderas, cajas aisladas, campo de puntos, contadores).
- Método: **primero** se escribe, por cada frase del guion, qué se ve en pantalla (storyboard en texto); se aprueba; **después** se construye.

## Composición (aprobada con la escena 0 de `examples/hf-swarm-vivido-es`)

- Se cuenta **qué ha pasado** y se deja **espacio** para las cosas: conexiones, assets, acciones. Nada de pantallas llenas.
- Los agentes son **pequeños** (no pasa nada); lo que importa es el conjunto.
- **Cuántos** se muestra con un contenedor **abierto por arriba**: las filas de agentes suben y se desvanecen por el borde superior. Las filas de abajo **no se mueven** al añadir más.
- Contenedor grande = rectángulo **vertical** en rojo punteado; **Artifactory** (caja ámbar con su nombre) **abajo**; los agentes arriba, en filas ordenadas, cada uno en su cajita.
- Los enlaces son **curvos**, con bolita que va y viene (petición/respuesta).
- Una rotura del contenedor es un **hueco** en la pared, y los enlaces pasan por él (no una X).
- Hugging Face = caja roja con su nombre, fuera del contenedor, con mucho aire alrededor.
- Se empieza con **zoom** al agente solo y la cámara se aleja al mostrar el contexto.

## Assets guardados (studio/worldkit.py)

`agent_named` (agente con su nombre) · `agent` (agente sin nombre, en su cajita) · `agent_group` (conjunto: contenedor abierto por arriba con filas que se desvanecen; admite un hueco en la pared) · `hugging_face` (estructura + agujeros) · `counter` (número blanco que cuenta, con texto debajo) · `clock` (reloj UTC tipo máquina de escribir, que puede avanzar) · `link` (enlace con bolita). La escena 0 de `examples/hf-swarm-vivido-es/scenes/s00.py` ya los usa.
