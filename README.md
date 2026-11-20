# Catequesis de novios

Espacio de trabajo para preparar la catequesis mensual de novios, a partir del itinerario *Juntos en Camino +Q2*.

Web pública: https://pablorenedolastra.github.io/catequesis-novios/

## Estructura

```
catequesis/            una carpeta por sesión (AAAA-MM-tema): PDF + texto .md
  README.md            calendario de lo que se ha dado
fuentes/
  juntos-en-camino/    INDICE.md con temas, sesiones y páginas del libro
                       (el PDF y su texto solo en local, ver .gitignore)
plantillas/            plantilla-catequesis.md, estructura de una sesión
docs/                  web pública (GitHub Pages)
CLAUDE.md              contexto y forma de trabajar para Claude
```

## Preparar la siguiente catequesis

1. Elegir tema en [fuentes/juntos-en-camino/INDICE.md](fuentes/juntos-en-camino/INDICE.md).
2. Crear `catequesis/AAAA-MM-tema/` partiendo de [plantillas/plantilla-catequesis.md](plantillas/plantilla-catequesis.md).
3. Añadirla a [catequesis/README.md](catequesis/README.md) y, si se quiere compartir, a `docs/index.html`.
