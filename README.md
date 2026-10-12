# Espa+

**Lenguaje de programación en español, basado en pseudocódigo ejecutable.**

Espa+ es un lenguaje de programación cuyo objetivo es que el pseudocódigo
que se enseña en las escuelas hispanas pueda **ejecutarse de verdad**.

Cada palabra clave corresponde a un concepto real de la lógica de
programación o del pensamiento computacional. Nada decorativo. Nada
inventado.

---

## Características

- **Todo en español**: variables, funciones, clases, errores.
- **Pseudocódigo ejecutable**: lo que aprendiste a escribir en papel, ahora corre.
- **Sello único**: `patron`, una palabra reservada para nombrar recetas reutilizables.
  Ningún otro lenguaje tiene esto.
- **Errores que enseñan**: cada error explica qué pasó y cómo arreglarlo.
- **72 funciones nativas**: texto, números, listas, archivos, CSV.
- **Módulos**: divide tu código en varios archivos `.wal`.
- **Sin símbolos raros**: bloques con palabras (`fin si`, `fin mientras`).
- **Case-insensitive**: acepta mayúsculas, las trata igual.

---

## Instalación

**Requisitos:** Python 3.10 o superior.

```bash
git clone https://github.com/TU_USUARIO/espax.git
cd espax
pip install -e .
```

Después de instalar, el comando `corre` queda disponible en cualquier carpeta.

---

## Uso

```bash
corre programa.wal       # ejecuta un archivo
corre                    # abre la consola interactiva (REPL)
corre --ayuda            # muestra la ayuda
corre --version          # muestra la versión
```

---

## Ejemplo

```text
algoritmo hola
  variable nombre = "ana"
  escribir "hola, ", nombre
fin algoritmo
```

Guarda como `hola.wal` y ejecuta:

```bash
corre hola.wal
```

---

## Ejemplo con patrón (sello único)

```text
patron sumar_lista con lista
  variable total = 0
  para cada x en lista
    total = total + x
  fin para
  retornar total
fin patron

algoritmo principal
  variable notas = [7, 8, 6, 9]
  escribir "suma: ", patron sumar_lista con notas
fin algoritmo
```

Los **patrones** permiten nombrar una forma de resolver algo y reutilizarla.
Es el pilar del pensamiento computacional llamado *reconocimiento de patrones*,
convertido en palabra clave.

---

## Sintaxis rápida

### Variables y constantes

```text
variable x = 5
constante PI = 3.14159
```

### Condicionales

```text
si x > 0 entonces
  escribir "positivo"
sino
  escribir "no positivo"
fin si
```

### Bucles

```text
mientras i < 10
  escribir i
  i = i + 1
fin mientras

para cada nombre en ["ana", "luis"]
  escribir nombre
fin para
```

### Funciones

```text
funcion area(r)
  retornar 3.14159 * r * r
fin funcion
```

### Clases

```text
clase perro
  funcion iniciar(nombre)
    esto.nombre = nombre
  fin funcion

  funcion ladra()
    escribir esto.nombre, " dice guau"
  fin funcion
fin clase

variable p = nuevo perro("firulais")
p.ladra()
```

### Módulos

```text
importar matematicas
escribir sumar(2, 3)
```

### Archivos

```text
variable contenido = leer_archivo("datos.csv")
variable filas = separar_csv(contenido)
escribir filas[0]
```

---

## Biblioteca estándar

Espa+ trae **72 funciones nativas** organizadas en 6 categorías:

| Categoría | Ejemplos |
|---|---|
| Texto | `mayus`, `minus`, `separar`, `unir`, `reemplazar` |
| Números | `absoluto`, `raiz`, `maximo`, `promedio`, `aleatorio` |
| Listas | `ordenar`, `filtrar`, `mapear`, `reducir`, `unicos` |
| Conversión | `a_texto`, `a_numero`, `a_logico` |
| Sistema | `tiempo`, `tipo`, `copiar`, `claves` |
| Archivos | `leer_archivo`, `escribir_archivo`, `separar_csv` |

Ver el [manual completo](docs/manual.md) para la lista entera.

---

## Documentación

- [Manual completo](docs/manual.md) — 17 secciones, todo el lenguaje.
- [Especificación](docs/especificacion.md) — diseño técnico.

---

## Filosofía

Espa+ no pretende reemplazar a Python, JavaScript o Rust. Pretende
**enseñar a programar en español**, con las palabras que ya se usan en
las aulas, y que ese código funcione de verdad.

Los errores no son castigos: son oportunidades para aprender. Cada
mensaje de error explica **qué pasó** y **cómo arreglarlo**.

---

## Estado del proyecto

**v0.3.0 (alpha)** — núcleo funcional completo.

Lo que está:
- Motor completo (lexer, parser, intérprete).
- 72 funciones nativas.
- Patrones, funciones como valores.
- Clases, objetos, herencia.
- Módulos con `importar`.
- Archivos y CSV.
- Comando `corre` global.
- REPL interactivo.

Lo que viene:
- Bucle `para i desde a hasta b`.
- Operadores `+=`, `-=`.
- Funciones anónimas.
- Resaltado de sintaxis para VS Code.
- Más funciones de sistema.

Ver [CHANGELOG.md](CHANGELOG.md) para el historial.

---

## Contribuir

Ver [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Licencia

MIT. Ver [LICENSE](LICENSE).

---

## Créditos

Creado por la comunidad hispanohablante que quiere programar en su idioma.