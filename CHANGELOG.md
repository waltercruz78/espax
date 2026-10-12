# Historial de cambios

Todos los cambios notables de Espa+ se documentan en este archivo.

El formato sigue [Keep a Changelog](https://keepachangelog.com/es/1.0.0/).

---

## [0.3.0] — 2026-10-12

### Añadido

- **Motor completo**: lexer, parser, intérprete, entorno, errores.
- **72 funciones nativas** organizadas en 6 categorías.
- **Patrones** (`patron`): sello único de Espa+. Nombrar recetas reutilizables.
- **Funciones como valores**: `filtrar`, `mapear`, `reducir` funcionan con funciones, patrones y nativas.
- **Clases y objetos**: `clase`, `nuevo`, `esto`, `herea`. Constructor `iniciar`.
- **Módulos**: `importar` y `paquete`. Detección de ciclos.
- **Archivos**: leer, escribir, agregar, borrar, listar, crear carpetas.
- **CSV**: `separar_csv` y `unir_csv` con conversión automática de números.
- **Errores que enseñan**: cada mensaje explica qué pasó y cómo arreglarlo.
- **Comando `corre`** instalable globalmente.
- **REPL interactivo**: escribir Espa+ línea a línea.
- **Manual completo** en `docs/manual.md`.

### Cambiado

- `leer` ahora crea la variable si no existe.
- Los identificadores son case-insensitive.

### Corregido

- Los decimales ya no muestran ceros de más (`3.3333333333` en vez de `3.333333333333333`).
- Los enteros se muestran sin `.0`.

---

## [0.2.0] — anterior

### Añadido

- Especificación inicial del lenguaje.
- Glosario de palabras clave.

---

## [0.1.0] — inicial

### Añadido

- Idea del proyecto.
- Filosofía: pseudocódigo ejecutable en español.