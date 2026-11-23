# Catequesis de novios

Proyecto personal de Pablo para preparar la catequesis mensual de novios de su parroquia. Las sesiones las llevan matrimonios acompañantes junto al sacerdote (Juanan). Todo en español.

## Material de referencia

- **Juntos en Camino +Q2** es el itinerario base (libro del acompañante, 12 temas, 32 sesiones). Antes de preparar una catequesis, localizar su sesión en [fuentes/juntos-en-camino/INDICE.md](fuentes/juntos-en-camino/INDICE.md) y leer esas páginas en `juntos-en-camino.md` (buscar `<!-- página N -->`). El número de página coincide con el impreso.
- Las catequesis ya hechas están en `catequesis/` y son la referencia de estilo y estructura.

## Cómo preparar una catequesis nueva

1. Elegir tema y sesión del itinerario con Pablo, y revisar qué se ha dado ya en `catequesis/README.md`.
2. Leer la sesión del libro y las catequesis anteriores.
3. Partir de [plantillas/plantilla-catequesis.md](plantillas/plantilla-catequesis.md). Estructura habitual: objetivo, idea central y pregunta sembrada; oración inicial; bloques con *Idea fuerza*, *Palabra de Dios* (cita + "Para fijarnos"), *Ideas para explicar* y *Preguntas para los novios*; cierre con un recorrido de pasos; dinámica final con tiempos y un compromiso ante Dios.
4. Guardarla en `catequesis/AAAA-MM-tema/` como `tema.md` y añadir la fila en `catequesis/README.md`.
5. Pablo la pasa a Notion y la exporta a PDF; el PDF final se guarda en la misma carpeta.

## Criterios de contenido

- Citas bíblicas con referencia exacta (libro, capítulo, versículos). Citas del Magisterio con documento, número, autor y año (p. ej. *Familiaris Consortio* 11, San Juan Pablo II, 1981). No inventar citas: si no se puede verificar el texto literal, citar solo la referencia y marcarlo.
- Tono cercano y concreto, dirigido a novios. Preguntas abiertas, ejemplos de la vida de pareja.
- Sin emojis ni rayas largas en los textos nuevos.

## Páginas públicas

El repo es público y la web sale de `docs/` con GitHub Pages: https://pablorenedolastra.github.io/catequesis-novios/. El PDF y el texto de Juntos en Camino están en `.gitignore` y solo existen en local; no subirlos nunca.

La web es la app del curso: la fuente es `app/catequesis.html` (también publicada como artefacto de Claude) y `python3 scripts/publicar.py` genera `docs/index.html`, el calendario `docs/catequesis.ics` y los ficheros PWA. Los datos (plan, casas, parejas, realizadas) están solo en el bloque JSON `datos` de la app. Tras cambiarlos: ejecutar el script, republicar el artefacto y subir.

Estas páginas son de la parroquia: estilo propio, sobrio y legible (también en móvil), **sin branding de Sapira** ni la skill `ux-sapira`. Decisión de Pablo del 20 nov 2026, excepción a su regla general.
