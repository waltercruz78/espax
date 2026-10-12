# Manual de Espa+

Lenguaje de programación en español, basado en pseudocódigo ejecutable.

---

## Índice

1. Introducción
2. Instalación y uso
3. Hola mundo
4. Comentarios
5. Variables y constantes
6. Tipos de datos
7. Operadores
8. Condicionales
9. Bucles
10. Funciones
11. Patrones (sello único de Espa+)
12. Clases y objetos
13. Errores
14. Módulos
15. Biblioteca estándar
16. Ejemplos completos
17. Errores que enseñan

---

## 1. Introducción

Espa+ es un lenguaje de programación en español cuyo objetivo es que el pseudocódigo que se enseña en las escuelas hispanas pueda ejecutarse de verdad.

**Filosofía:**
- Todo en español, sin acentos en palabras clave.
- Palabras claras e intuitivas.
- Basado en los fundamentos de la programación y el pensamiento computacional.
- Errores que enseñan el concepto, no solo el fallo.
- Simple pero potente.

**Diferencias con otros lenguajes:**
- Bloques con palabras de cierre (`fin si`, `fin mientras`).
- Sin punto y coma.
- Sin llaves para bloques (solo para mapas).
- Case-insensitive (acepta mayúsculas, las trata igual).
- Palabra reservada `patron` única en el mundo.

---

## 2. Instalación y uso

**Requisitos:**
- Python 3.10 o superior.

**Comandos:**

```bash
corre programa.wal       # ejecuta un archivo
corre                    # abre el REPL
corre --ayuda            # muestra la ayuda
corre --version          # muestra la versión
```

**Extensión de archivos:** `.wal`

---

## 3. Hola mundo

```text
algoritmo hola
  escribir "hola, mundo"
fin algoritmo
```

---

## 4. Comentarios

```text
# esto es un comentario de una línea

/*
  esto es un comentario
  de varias líneas
*/
```

---

## 5. Variables y constantes

**Variable:**
```text
variable x = 5
variable nombre = "ana"
variable lista = [1, 2, 3]
```

**Constante:**
```text
constante PI = 3.14159
```

**Anotación de tipo (opcional):**
```text
variable x: numero = 5
variable nombre: texto = "ana"
variable activo: logico = verdadero
```

Los tipos válidos son: `numero`, `texto`, `logico`, `lista`, `mapa`.

**Reasignar:**
```text
variable x = 5
x = 10
```

---

## 6. Tipos de datos

| Tipo | Ejemplo |
|---|---|
| número entero | `5`, `-3`, `0` |
| número decimal | `3.14`, `-0.5` |
| texto | `"hola"`, `"con \"comillas\""` |
| lógico | `verdadero`, `falso` |
| nulo | `nulo` |
| lista | `[1, 2, 3]`, `["a", "b"]` |
| mapa | `{"a": 1, "b": 2}` |

**Escapes en textos:**

| Escape | Significa |
|---|---|
| `\n` | salto de línea |
| `\t` | tabulador |
| `\"` | comilla doble |
| `\\` | barra invertida |

---

## 7. Operadores

**Matemáticos:**
```text
+   suma
-   resta
*   multiplicación
/   división
**  potencia
residuo   resto de división
```

**Comparación:**
```text
==   igual
!=   distinto
<    menor
<=   menor o igual
>    mayor
>=   mayor o igual
```

**Lógicos:**
```text
y    conjunción
o    disyunción
no   negación
```

**Precedencia (de menor a mayor):**
1. `o`
2. `y`
3. `no`
4. `==`, `!=`, `<`, `<=`, `>`, `>=`
5. `+`, `-`
6. `*`, `/`, `residuo`, `**`

**Ejemplo:**
```text
variable x = 2 + 3 * 4      # 14
variable y = (2 + 3) * 4    # 20
variable z = no verdadero   # falso
variable w = 5 > 3 y 2 < 4  # verdadero
```

---

## 8. Condicionales

**Si / sino:**
```text
si x > 0 entonces
  escribir "positivo"
sino
  escribir "no positivo"
fin si
```

La palabra `entonces` es opcional.

**Elección múltiple:**
```text
segun x
  caso 1
    escribir "uno"
  caso 2
    escribir "dos"
  defecto
    escribir "otro"
fin segun
```

---

## 9. Bucles

**Mientras:**
```text
variable i = 0
mientras i < 10 hacer
  escribir i
  i = i + 1
fin mientras
```

La palabra `hacer` es opcional.

**Para cada:**
```text
para cada nombre en ["ana", "luis", "sofia"] hacer
  escribir nombre
fin para
```

**Romper y saltar:**
```text
mientras verdadero
  leer linea
  si linea == "salir"
    romper
  fin si
  si linea == ""
    saltar
  fin si
  escribir linea
fin mientras
```

---

## 10. Funciones

```text
funcion area(r)
  retornar 3.14159 * r * r
fin funcion

funcion saludar(nombre)
  escribir "hola, ", nombre
fin funcion

escribir area(5)
saludar("ana")
```

**Funciones como valores:**
```text
funcion es_par(x)
  retornar x residuo 2 == 0
fin funcion

variable nums = [1, 2, 3, 4, 5, 6]
escribir filtrar(nums, es_par)   # [2, 4, 6]
```

---

## 11. Patrones (sello único de Espa+)

Un **patrón** es una receta reutilizable. Le pones nombre a una forma de resolver algo, y después la aplicas a distintos datos.

Ningún otro lenguaje tiene esto.

**Definir:**
```text
patron sumar_lista con lista
  variable total = 0
  para cada x en lista
    total = total + x
  fin para
  retornar total
fin patron
```

**Usar:**
```text
variable notas = [7, 8, 6, 9]
escribir patron sumar_lista con notas
```

**Diferencia con `funcion`:**

| | `funcion` | `patron` |
|---|---|---|
| Enfoque | Cálculo | Forma de resolver |
| Se llama | `area(5)` | `patron sumar_lista con notas` |
| Fundamento | Álgebra | Reconocimiento de patrones |

---

## 12. Clases y objetos

```text
clase persona
  funcion iniciar(nombre, edad)
    esto.nombre = nombre
    esto.edad = edad
  fin funcion

  funcion saludar()
    escribir "hola, soy ", esto.nombre
  fin funcion
fin clase

variable ana = nuevo persona("ana", 25)
ana.saludar()
```

**Herencia:**
```text
clase animal
  funcion iniciar(nombre)
    esto.nombre = nombre
  fin funcion
fin clase

clase perro herea animal
  funcion ladra()
    escribir esto.nombre, " dice guau"
  fin funcion
fin clase
```

**Método especial `iniciar`:** es el constructor. Se llama automáticamente cuando escribes `nuevo`.

---

## 13. Errores

**Lanzar:**
```text
lanzar "algo salió mal"
```

**Intentar y capturar:**
```text
intentar
  variable x = 10 / 0
capturar fallo
  escribir "atrapado: ", fallo
fin intentar
```

**Errores que enseñan:** cada mensaje de error explica **qué pasó** y **cómo arreglarlo**.

```text
línea 3, columna 5: la variable 'x' no existe. ¿la declaraste antes de usarla?
línea 7, columna 10: no puedes sumar texto con número. convierte uno primero.
línea 4, columna 1: falta 'fin mientras' para el bloque abierto.
```

---

## 14. Módulos

**Importar:**
```text
paquete geometria
importar matematicas
```

**Estructura típica:**

`matematicas.wal`:
```text
paquete matematicas

constante PI = 3.14159

funcion sumar(a, b)
  retornar a + b
fin funcion

patron sumar_lista con lista
  variable total = 0
  para cada x en lista
    total = total + x
  fin para
  retornar total
fin patron
```

`principal.wal`:
```text
paquete principal

importar matematicas

algoritmo main
  escribir sumar(2, 3)
  escribir PI
  escribir patron sumar_lista con [1, 2, 3]
fin algoritmo
```

**Lo que se importa:** variables, constantes, funciones, patrones y clases del módulo quedan disponibles en el archivo que lo importa.

**Rutas:** los módulos se buscan en la misma carpeta del archivo que los importa.

**Ciclos:** si A importa B y B importa A, no se cuelga. El segundo import se ignora.

---

## 15. Biblioteca estándar

Espa+ trae **72 funciones nativas** organizadas por categoría.

### Texto

| Función | Qué hace |
|---|---|
| `longitud(x)` | Cuántos caracteres o elementos |
| `mayus(texto)` | A mayúsculas |
| `minus(texto)` | A minúsculas |
| `capitalizar(texto)` | Primera letra mayúscula |
| `recortar(texto)` | Quita espacios al inicio y final |
| `reemplazar(t, viejo, nuevo)` | Reemplaza |
| `contiene(x, cosa)` | Verdadero si lo contiene |
| `empieza(texto, prefijo)` | Verdadero si empieza con |
| `termina(texto, sufijo)` | Verdadero si termina con |
| `separar(texto, sep)` | Divide en lista |
| `unir(lista, sep)` | Junta en texto |
| `cortar(texto, inicio, fin)` | Subcadena |
| `repetir_texto(t, n)` | Repite n veces |
| `al_reves(x)` | Invierte |
| `contar_palabras(texto)` | Cuenta palabras |
| `indice_texto(texto, sub)` | Posición de subcadena |

### Números

| Función | Qué hace |
|---|---|
| `absoluto(x)` | Valor sin signo |
| `signo(x)` | -1, 0 o 1 |
| `redondear(x, dec)` | Redondea |
| `techo(x)` | Entero mayor |
| `piso(x)` | Entero menor |
| `raiz(x)` | Raíz cuadrada |
| `potencia(b, e)` | b elevado a e |
| `maximo(...)` | El mayor |
| `minimo(...)` | El menor |
| `suma(lista)` | Suma total |
| `promedio(lista)` | Promedio |
| `aleatorio(a, b)` | Entero al azar |
| `decimal_aleatorio()` | Decimal al azar |
| `entre(x, a, b)` | ¿a ≤ x ≤ b? |
| `es_primo(x)` | ¿Es primo? |
| `factorial(x)` | Factorial |
| `fibonacci(x)` | n-ésimo Fibonacci |

### Listas

| Función | Qué hace |
|---|---|
| `agregar(lista, valor)` | Añade al final |
| `quitar(lista, valor)` | Quita |
| `insertar(lista, pos, v)` | Inserta en posición |
| `ordenar(lista)` | Ordena |
| `invertir(lista)` | Invierte |
| `repetir(lista, n)` | Repite |
| `rango(a, b, paso)` | Lista de números |
| `filtrar(lista, func)` | Filtra con función |
| `mapear(lista, func)` | Transforma con función |
| `reducir(lista, func, ini)` | Reduce con función |
| `buscar(lista, valor)` | Posición o -1 |
| `contar(lista, valor)` | Cuántas veces aparece |
| `indice(lista, pos)` | Elemento en posición |
| `primeros(lista, n)` | Primeros n |
| `ultimos(lista, n)` | Últimos n |
| `unicos(lista)` | Sin repetidos |
| `vacio(x)` | ¿Está vacío? |
| `lleno(x)` | ¿Tiene contenido? |
| `concatenar(a, b)` | Une listas o textos |

### Conversión

| Función | Qué hace |
|---|---|
| `a_texto(x)` | Convierte a texto |
| `a_numero(x)` | Convierte a número |
| `a_logico(x)` | Convierte a lógico |

### Sistema

| Función | Qué hace |
|---|---|
| `tiempo()` | Segundos desde 1970 |
| `tipo(x)` | Devuelve el tipo |
| `copiar(x)` | Copia profunda |
| `claves(mapa)` | Lista de claves |
| `valores(mapa)` | Lista de valores |

### Archivos

| Función | Qué hace |
|---|---|
| `leer_archivo(ruta)` | Lee todo el contenido |
| `escribir_archivo(ruta, t)` | Escribe (sobrescribe) |
| `agregar_archivo(ruta, t)` | Añade al final |
| `existe_archivo(ruta)` | ¿Existe? |
| `borrar_archivo(ruta)` | Elimina |
| `listar_archivos(carpeta)` | Lista de nombres |
| `crear_carpeta(ruta)` | Crea carpeta |
| `existe_carpeta(ruta)` | ¿Existe carpeta? |
| `leer_lineas(ruta)` | Lista de líneas |
| `escribir_lineas(ruta, l)` | Escribe lista |
| `separar_csv(texto)` | CSV → matriz |
| `unir_csv(filas)` | Matriz → CSV |

**Rutas relativas:** si escribes `"datos.txt"`, se busca en la carpeta del `.wal` que se ejecuta.

---

## 16. Ejemplos completos

### Calcular promedio de notas

```text
algoritmo promedio
  variable notas = [7, 8, 6, 9, 5]
  escribir "notas: ", notas
  escribir "promedio: ", promedio(notas)
  escribir "mayor: ", maximo(notas)
  escribir "menor: ", minimo(notas)
fin algoritmo
```

### Procesar un CSV

```text
algoritmo analizar_csv
  variable contenido = leer_archivo("datos.csv")
  variable filas = separar_csv(contenido)

  variable total = 0
  variable i = 1
  mientras i < longitud(filas)
    variable edad = filas[i][1]
    total = total + edad
    i = i + 1
  fin mientras

  escribir "promedio de edad: ", total / (longitud(filas) - 1)
fin algoritmo
```

### Patrón reutilizable

```text
patron sumar_lista con lista
  variable total = 0
  para cada x en lista
    total = total + x
  fin para
  retornar total
fin patron

algoritmo main
  escribir patron sumar_lista con [1, 2, 3]
  escribir patron sumar_lista con [10, 20, 30]
fin algoritmo
```

### Clase con herencia

```text
clase animal
  funcion iniciar(nombre)
    esto.nombre = nombre
  fin funcion

  funcion hablar()
    escribir "hace un sonido"
  fin funcion
fin clase

clase perro herea animal
  funcion hablar()
    escribir esto.nombre, " dice guau"
  fin funcion
fin clase

variable p = nuevo perro("firulais")
p.hablar()
```

### Módulos

Ver sección 14.

---

## 17. Errores que enseñan

Cada error de Espa+ explica **qué pasó** y **cómo arreglarlo**.

| Situación | Mensaje |
|---|---|
| Variable no definida | `la variable 'x' no existe. ¿la declaraste antes de usarla?` |
| Variable ya existe | `la variable 'x' ya existe en este bloque. elige otro nombre o asígnala sin 'variable'.` |
| Cambiar constante | `'PI' es una constante y no se puede cambiar. si necesitas modificarla, usa 'variable' en su lugar.` |
| Sumar texto con número | `no puedes sumar texto con número. convierte el número a texto o el texto a número primero.` |
| Dividir entre cero | `no se puede dividir entre cero. verifica el divisor antes de dividir.` |
| Falta cierre | `falta 'fin mientras' para el bloque abierto.` |
| Paréntesis sin cerrar | `falta ')' para cerrar la agrupación.` |
| Argumentos incorrectos | `la función 'area' espera 1 argumento(s), pero recibí 2.` |
| Tipo lógico incorrecto | `'y' necesita valores lógicos (verdadero o falso), pero recibí número.` |
| Campo inexistente | `el campo 'nombre' no existe en el objeto de la clase 'persona'.` |
| `romper` fuera de bucle | `'romper' solo funciona dentro de un bucle.` |
| Función no existe | `la función 'area' no existe. ¿la definiste antes de llamarla?` |
| Patrón no existe | `el patrón 'sumar_lista' no existe. ¿lo definiste antes de usarlo?` |
| Clase no existe | `la clase 'perro' no existe. ¿la definiste antes de usarla?` |
| Archivo no existe | `no existe el archivo 'datos.txt'.` |
| Módulo no existe | `no encuentro el módulo 'mate'. esperaba el archivo 'C:\...\mate.wal'.` |

---

## Fin del manual

Espa+ es un lenguaje en construcción activa. Esta es la versión v0.3.

Para contribuir o reportar problemas: ver el repositorio del proyecto.