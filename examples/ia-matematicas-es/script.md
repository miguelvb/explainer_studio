## 0 · Gancho

**0a** (pausa 2.4) Las matemáticas se aceleran: setecientos veintidós teoremas de una IA.
> Pantalla de título sobre fondo oscuro con el sello de Arkinos; el título se escribe a máquina y suena una campanilla.

**0b** En octubre de 2025, un directivo de OpenAI anunció que su modelo había resuelto diez problemas matemáticos abiertos. Era falso: solo había encontrado soluciones que ya estaban publicadas.
> Aparece un agente con la etiqueta «GPT-5». Diez banderas verdes se encienden sobre él y, de golpe, se vuelven rojas, tachadas una a una; al lado, una hoja con la nota «ya estaba publicado».

**0c** Un año después, el seis de octubre de 2026, la misma empresa publicó setecientos veintidós manuscritos matemáticos escritos por un modelo interno.
> Un reloj marca 06 octubre 2026. Una carpeta se abre y de ella salen documentos que se apilan en una torre; un contador sube hasta 722.

**0d** ¿Qué ha cambiado en doce meses? Y, sobre todo: ¿cómo se comprueba tanta matemática?
> La torre de documentos queda en el centro; un agente verificador pequeño la mira desde un lado, con un signo de interrogación sobre él.

## 1 · La aceleración

**1a** Para entender el salto, hay que mirar un sitio concreto: erdosproblems.com. Es una web que recoge más de mil problemas que dejó planteados el matemático húngaro Paul Erdős.
> Aparece una ventana de carpetas «erdosproblems.com» con una lista de problemas numerados; al decir «Erdős» se dibuja una persona de pie junto a la ventana.

**1b** Entre diciembre de 2025 y enero de 2026, algunos aficionados empezaron a probar GPT-5.2 con esos problemas. Resolvieron el número 728, y lo comprobaron con un programa de verificación formal.
> Una persona y un agente «GPT-5.2» a la izquierda; una bandera junto al número 728 de la lista se pone verde, y un sello «verificado» la acompaña.

**1c** En enero, un equipo de Google DeepMind resolvió cuatro más y rescató nueve soluciones olvidadas, entre unas setecientas conjeturas. En mayo, otro equipo resolvió nueve de trescientas cincuenta y tres, a unos cientos de dólares por problema.
> Línea de tiempo horizontal con un agente «DeepMind» que recorre las fechas «enero 2026» y «mayo 2026»; en cada parada, banderas verdes se encienden sobre la lista: 4, y luego 9 de 353.

**1d** El veinte de mayo llegó el salto cualitativo: OpenAI anunció que su modelo había refutado una conjetura de Erdős de 1946. Matemáticos como Noga Alon, Melanie Wood y Thomas Bloom revisaron el resultado y lo avalaron.
> Fecha 20 mayo 2026 en el reloj. Un agente «OpenAI» emite un mensaje hacia tres personas con etiquetas «Alon», «Wood», «Bloom», y cada una responde con un sello de aprobado.

**1e** En agosto, un modelo llamado Astra anunció diez avances más. Y en septiembre, OpenAI afirmó que ya eran más de cien los problemas abiertos resueltos, e incluyó una variante del problema de Navier-Stokes, sobre cómo se mueven los fluidos: uno de los más buscados de las matemáticas, con un millón de dólares de premio. OpenAI dice que no reclamará ese premio, y el resultado todavía se está revisando.
> La línea de tiempo continúa: «agosto 2026», «septiembre 2026». El contador sube a 100+. Aparece una ficha «Navier–Stokes · 1.000.000 $ de premio»; después, una nota «OpenAI renuncia al premio». Una bandera de la lista queda amarilla con el rótulo «en revisión».

**1f** (pausa 1.6) Y el seis de octubre, setecientos veintidós manuscritos. En doce meses se pasó de no resolver nada, a resolver cientos.
> Zoom a toda la línea de tiempo; el contador salta de 10 a 100 y a 722, y el agente crece en tamaño.

## 2 · Qué se ha publicado

**2a** OpenAI lo ha dejado todo en un repositorio público de GitHub: setecientos veintidós manuscritos, agrupados en trescientas setenta y dos familias de resultados.
> Una carpeta grande «openai/math» con una torre de 722 documentos que se agrupan en 372 paquetes pequeños.

**2b** Según la propia empresa, el modelo recibió unos cuatro mil problemas. Cada resultado costó, de media, unas tres horas de «pensamiento» de ChatGPT Pro. De ahí salieron los resultados que se consideraron suficientemente importantes.
> Un embudo: arriba 4.000 puntos pequeños; el embudo los reduce y de abajo caen los paquetes. Un reloj en una esquina marca «3 h» por resultado.

**2c** (pausa 1.6) Cubren casi todo: teoría de números, geometría, análisis, informática teórica, combinatoria, física matemática, topología…
> Los paquetes se reparten en columnas rotuladas con áreas de las matemáticas; las columnas de informática y combinatoria son las más altas.

**2d** Entre los títulos hay nombres enormes: una región sin ceros para la función zeta de Riemann, el décimo problema de Hilbert sobre los racionales, la fórmula de Birch y Swinnerton-Dyer en varios casos. Son afirmaciones de OpenAI, y no todas tienen aún prueba comprobada.
> Una hoja con la lista de títulos famosos, cada uno con una bandera: unas verdes con sello Lean, otras grises con interrogante.

## 3 · El problema de las distancias unitarias

**3a** Vamos a ver dos de estos problemas con calma. El primero lo planteó Erdős en 1946, y se puede explicar con un folio. Dados n puntos en un plano, ¿cuántas parejas pueden estar a distancia exactamente uno?
> Aparece un plano con puntos; al decir «distancia uno», se dibuja una pareja de puntos unidos por un segmento con la etiqueta «1».

**3b** Si pones los puntos en línea, consigues n menos uno parejas. Si los colocas en una cuadrícula, bastantes más.
> Una fila de puntos con segmentos unitarios: «n−1». Debajo, una cuadrícula de puntos con muchos segmentos unitarios entre vecinos.

**3c** Erdős demostró que con una cuadrícula bien escalada se consigue algo un poco mejor que n, y conjeturó que eso era casi lo máximo posible: que no se podía mejorar de forma apreciable.
> La cuadrícula se escala y aparece una curva casi plana pegada al eje; sobre ella, un cartel «Erdős: casi n».

**3d** Durante casi ochenta años nadie lo refutó. Lo mejor que se sabía, en el otro sentido, era que no podía ser mayor que n elevado a cuatro tercios.
> Una barra con dos marcas: «casi n» abajo y «n^(4/3)» arriba, con una franja enorme entre las dos; un reloj pasa de 1946 a 2026.

**3e** (pausa 1.2) El modelo de OpenAI lo refutó. Encontró configuraciones de puntos con n elevado a uno más delta parejas, para un delta fijo mayor que cero. Un refinamiento posterior de Will Sawin, de Princeton, lo concreta en cero coma cero catorce.
> La franja entre las dos marcas se llena: aparece una nueva marca por encima de la anterior, «n^(1,014)», y se enciende una bandera verde.

**3f** La idea no vino de la geometría. Los números de la cuadrícula de Erdős son enteros gaussianos, que tienen un par de simetrías. El modelo los sustituyó por cuerpos numéricos con muchas más simetrías, y usó resultados de teoría algebraica de números que nadie había aplicado a este problema.
> Una cuadrícula pequeña se transforma en una malla muchísimo más densa, con muchas más conexiones unitarias; al decir «teoría algebraica de números» aparece una caja con ese rótulo que alimenta la malla.

**3g** Tim Gowers dijo que, si lo hubiera escrito un humano, habría recomendado aceptarlo en los Annals of Mathematics sin dudar. Y Jacob Tsimerman, medalla Fields, contó que él había intentado construir un contraejemplo y había fracasado.
> Dos citas aparecen una tras otra sobre dos personas: «Lo habría aceptado en Annals» y «Lo intenté y fracasé».

## 4 · El número pi

**4a** El segundo problema es sobre el número pi. Pi es irracional: no se puede escribir como fracción. Pero se puede aproximar muy bien con fracciones, como veintidós séptimos o trescientos cincuenta y cinco ciento trece.
> Aparece un círculo y el símbolo π; debajo, dos fracciones «22/7» y «355/113» con segmentos que se acercan al punto del número π en una recta.

**4b** La pregunta es cuán buenas pueden ser esas aproximaciones. Se mide con un número que se llama exponente de irracionalidad. Cuanto más grande, mejor se deja aproximar el número por fracciones.
> En la recta numérica, una banda alrededor de π se estrecha mientras se prueban fracciones con denominador cada vez mayor; un medidor etiquetado «exponente» sube y baja.

**4c** (pausa 0.6) Y si eres una persona con mucha curiosidad matemática, te voy a explicar qué es ese exponente. Es más sencillo de lo que parece.
> Un rótulo «para curiosos» y una letra μ grande con un signo de interrogación: el exponente, todavía sin explicar.

**4d** Una fracción tiene arriba un numerador y abajo un denominador. Con denominador siete, las fracciones caen como marcas de una regla, una cada séptimo. Pi cae entre dos marcas, y la más cercana, veintidós séptimos, falla por poco más de un milésimo.
> Aparece «p sobre q» con sus dos partes señaladas; debajo, una regla de 3,0 a 3,3 con marcas cada 1/7; el punto de π cae junto a la marca 22/7, con un pequeño tramo de error.

**4e** Si usamos una regla más fina, con denominador ciento trece, las marcas están mucho más juntas, y trescientos cincuenta y cinco ciento trece falla por menos de una millonésima.
> Una segunda regla con 34 marcas muy juntas; el punto 355/113 casi se superpone al de π; rótulo «error < 0,000001».

**4f** Para medir cuán buena es una aproximación hay que compararla con el denominador. Siempre se pueden encontrar fracciones que fallan menos que uno partido por el denominador al cuadrado. Esa es la línea del dos: el suelo que alcanza cualquier número irracional.
> Las reglas desaparecen y aparece una gráfica: eje horizontal, tamaño del denominador (escala logarítmica); eje vertical, precisión. Los puntos de las fracciones de π (22/7, 355/113…) aparecen y se traza la línea «2», con todos los puntos sobre ella o por encima.

**4g** Pero ¿y si hay fracciones que lo hacen mejor, que fallan menos que uno partido por el denominador al cubo, o a la cuarta? El exponente es la potencia más alta que consiguen infinitas fracciones a la vez. Una sola fracción afortunada no cuenta: tienen que ser infinitas.
> Se trazan las líneas «3» y «4». El punto 355/113 queda por encima de la «3» y se rodea con un círculo: «una sola, no cuenta». Después una hilera de puntos por encima de la «3» que sigue y sigue hacia la derecha, con el símbolo ∞.

**4h** Para pi, las fracciones que se conocen se quedan pegadas a la línea del dos. Lo difícil es demostrar que, más arriba, no hay infinitas.
> Un halo ámbar rodea los puntos pegados a la línea «2»; en la zona de arriba aparece un signo de interrogación «¿infinitas?».

**4i** Un exponente de dos significa que pi no tiene trucos: se aproxima como cualquier otro número. Y con esto ya puedes seguir la historia.
> La línea «2» se ilumina y aparece el rótulo «2 = sin trucos».

**4j** Para casi cualquier número, ese exponente es dos. Es el mínimo posible, como si fuera un número «sin trucos». También ocurre con los números algebraicos, como la raíz de dos.
> Un medidor con una marca «2» en el mínimo; una nube de puntos «casi todos» se queda en 2; la raíz de dos aparece con la etiqueta «2».

**4k** Pero nadie había podido demostrarlo. Lo único que se sabía es que el exponente de pi no podía ser mayor que siete coma uno: podía valer cualquier cosa entre dos y siete coma uno.
> El medidor de π sube hasta el 7,1 con el rótulo «se sabía: ≤ 7,1», y después queda flotando en mitad del rango con un signo de interrogación (valor desconocido entre 2 y 7,1).

**4l** (pausa 1.2) El modelo de OpenAI afirma haber demostrado que el exponente de pi es exactamente dos. Es decir, que pi se comporta como un número corriente a la hora de aproximarlo.
> El medidor baja de golpe y se clava en 2; una bandera verde se enciende junto al símbolo π.

**4m** De regalo, esa cota demuestra que converge una suma infinita que lleva años sin resolverse: la serie de Flint Hills. La suma es uno partido por n al cubo por el seno de n al cuadrado, para n igual a uno, dos, tres, y así sin parar. Que converja quiere decir que, sumando y sumando, el total deja de crecer y se acerca a un valor fijo.
> Se escribe la fórmula Σ 1/(n³·sen²n) término a término. Debajo, una gráfica (n en escala logarítmica) donde la suma acumulada sube a escalones hasta 4,8, da un salto enorme en n = 355 (el seno casi se anula), sube a 29,4 y después se aplana en una línea de ≈ 30,3: converge.

**4n** Además, el resumen de razonamiento que publican muestra al modelo probando una vía tras otra, y descartándolas. No es una chispa: es una búsqueda larga, con muchos callejones sin salida.
> Una consola muestra líneas de intentos que van apareciendo y tachándose; un agente tachando caminos de un laberinto hasta llegar a una bandera.

## 5 · Lean

**5a** (pausa 1.6) Un resultado así no puede aceptarse de palabra. Por eso importa Lean.
> Fondo oscuro; aparece una caja con el rótulo «Lean» y un agente verificador al lado, que sostiene una bandera.

**5b** Lean es un lenguaje de programación y, a la vez, un verificador de demostraciones. Escribes la prueba con un formato muy estricto, y el ordenador comprueba cada paso. Si compila, la demostración es correcta.
> Una consola escribe líneas de código; una cinta de pasos avanza y cada paso se marca con un tic verde; al final se enciende «compila».

**5c** No depende de la confianza en quien la escribió, ni de que alguien la lea entera. Solo hay que confiar en un núcleo pequeño que revisa cada paso.
> Una caja pequeña «núcleo» en el centro; muchas demostraciones diferentes pasan por ella y salen con sello verde.

**5d** En el repositorio de OpenAI, doscientas treinta y cinco de las trescientas setenta y dos familias enlazan con alguna formalización en Lean. Es decir, casi dos tercios de los resultados tienen una comprobación hecha por ordenador.
> Un contador muestra «235 / 372»; una barra con dos tercios en verde y el resto en gris.

**5e** Pero hay un matiz. Lean garantiza que la demostración es correcta para el enunciado que se haya escrito. No garantiza que ese enunciado sea el problema que querías resolver. Por eso, en el caso de pi, los humanos pueden leer el enunciado fijado y comprobar que dice lo que debe.
> Dos hojas lado a lado: «enunciado en palabras» y «enunciado en Lean»; una lupa las compara y un cable de dudas pregunta «¿dicen lo mismo?».

**5f** Y hay otro matiz más: la formalización del exponente de pi no incluye la consecuencia sobre la serie de Flint Hills. Cada resultado tiene su propio alcance, y conviene mirar el documento de cada uno.
> En la hoja de pi, la parte del exponente está en verde; la línea de Flint Hills queda fuera del recuadro, en gris.

## 6 · Lo que está en juego

**6a** El propio repositorio lo reconoce. No todos los resultados tienen formalización, y alguno de los que no la tienen podría contener errores.
> El contador 235/372: los 137 restantes aparecen como documentos grises con una advertencia «podrían tener errores».

**6b** Thomas Bloom, que mantiene la web de los problemas de Erdős, avisó de otro riesgo: que haya demostraciones que ningún humano ha leído, ni va a leer.
> Una persona rodeada de una pila de documentos enorme; una cita aparece sobre ella: «ningún humano lo ha leído».

**6c** Noga Alon dijo que dejó de perseguir problemas de Erdős: si la IA los resuelve, ya no tiene sentido. Y veinticinco medallistas Fields firmaron una carta criticando el ritmo al que los laboratorios publican estos resultados.
> Dos citas sobre dos personas; una fila de veinticinco figuras pequeñas con una carta que sale de ellas hacia el agente «OpenAI».

**6d** Para ordenar el debate, OpenAI ha creado un grupo asesor en el Instituto de Estudios Avanzados de Princeton. Su poder es limitado: asesora sobre la importancia y la divulgación, pero no sobre el ritmo del trabajo.
> Una caja «Grupo asesor · IAS» con nueve figuras; una flecha hacia el agente «OpenAI» se corta a medio camino con el rótulo «no decide el ritmo».

## 7 · Cierre

**7a** Entonces, ¿qué sabemos? Que en un año la IA ha pasado de repetir soluciones ajenas a refutar una conjetura de Erdős y a proponer demostraciones sobre pi.
> La línea de tiempo completa de 2025 a 2026 con el agente creciendo y los contadores clave: 10 falsos, 722 manuscritos.

**7b** Lo que no sabemos es cuántos de esos setecientos veintidós resultados resistirán la revisión, y si las matemáticas pueden revisar tan rápido como ahora se produce.
> La torre de manuscritos de nuevo; la barra verde (Lean) y la gris (sin comprobar) conviven, y el verificador pequeño sigue trabajando.

**7c** (pausa 2) El cuello de botella ya no es demostrar. Es entender.
> Todo se atenúa menos el agente verificador y la bandera, que quedan solos en el centro.

## 8 · Créditos

**8a** (pausa 3) Arkinos, Explainer Studio.
> Sello de Arkinos con el texto «Fuentes: openai.com/index/sharing-ai-progress-in-mathematics · github.com/openai/math · Quanta Magazine · Nature».
