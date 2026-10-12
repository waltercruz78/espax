# espa/nativas.py

import math
import os
import random
import time
import shutil
import subprocess
import copy as _copy

from espa.errores import ErrorTipo, ErrorValor


def _num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def _entero(x):
    return isinstance(x, int) and not isinstance(x, bool)


def _txt(x):
    return isinstance(x, str)


def _lista(x):
    return isinstance(x, list)


def _mapa(x):
    return isinstance(x, dict) and "__campos__" not in x


def _tipo(x):
    if x is None:
        return "nulo"
    if isinstance(x, bool):
        return "logico"
    if isinstance(x, (int, float)):
        return "numero"
    if isinstance(x, str):
        return "texto"
    if isinstance(x, list):
        return "lista"
    if isinstance(x, dict) and "__campos__" in x:
        return "objeto"
    if isinstance(x, dict):
        return "mapa"
    if callable(x):
        return "funcion"
    return "desconocido"


# ---------- pila de rutas (para archivos relativos) ----------

_ruta_stack = []


def empujar_ruta(r):
    _ruta_stack.append(r)


def sacar_ruta():
    if _ruta_stack:
        _ruta_stack.pop()


def ruta_actual():
    return _ruta_stack[-1] if _ruta_stack else os.getcwd()


def _ruta_completa(ruta):
    if not _txt(ruta):
        raise ErrorTipo("la ruta debe ser un texto.")
    if os.path.isabs(ruta):
        return ruta
    return os.path.join(ruta_actual(), ruta)


# ============================================================
# TEXTO
# ============================================================

def n_longitud(x):
    if isinstance(x, (str, list, dict)):
        return len(x)
    raise ErrorTipo(f"longitud espera texto, lista o mapa, pero recibí {_tipo(x)}.")


def n_mayus(x):
    if _txt(x):
        return x.upper()
    raise ErrorTipo(f"mayus espera texto, pero recibí {_tipo(x)}.")


def n_minus(x):
    if _txt(x):
        return x.lower()
    raise ErrorTipo(f"minus espera texto, pero recibí {_tipo(x)}.")


def n_capitalizar(x):
    if _txt(x):
        return x.capitalize()
    raise ErrorTipo(f"capitalizar espera texto, pero recibí {_tipo(x)}.")


def n_recortar(x):
    if _txt(x):
        return x.strip()
    raise ErrorTipo(f"recortar espera texto, pero recibí {_tipo(x)}.")


def n_reemplazar(texto, viejo, nuevo):
    if _txt(texto) and _txt(viejo) and _txt(nuevo):
        return texto.replace(viejo, nuevo)
    raise ErrorTipo("reemplazar espera tres textos.")


def n_contiene(contenedor, cosa):
    if _txt(contenedor) or _lista(contenedor):
        return cosa in contenedor
    if _mapa(contenedor):
        return cosa in contenedor
    raise ErrorTipo(f"contiene espera texto, lista o mapa, pero recibí {_tipo(contenedor)}.")


def n_empieza(texto, prefijo):
    if _txt(texto) and _txt(prefijo):
        return texto.startswith(prefijo)
    raise ErrorTipo("empieza espera dos textos.")


def n_termina(texto, sufijo):
    if _txt(texto) and _txt(sufijo):
        return texto.endswith(sufijo)
    raise ErrorTipo("termina espera dos textos.")


def n_separar(texto, separador=" "):
    if _txt(texto) and _txt(separador):
        return texto.split(separador)
    raise ErrorTipo("separar espera dos textos.")


def n_unir(lista, separador=""):
    if _lista(lista) and _txt(separador):
        return separador.join(n_a_texto(e) for e in lista)
    raise ErrorTipo("unir espera una lista y un texto.")


def n_cortar(texto, inicio, fin=None):
    if not _txt(texto):
        raise ErrorTipo("cortar espera un texto.")
    if not _entero(inicio):
        raise ErrorTipo("cortar espera un número entero como inicio.")
    if fin is None:
        return texto[inicio:]
    if not _entero(fin):
        raise ErrorTipo("cortar espera un número entero como fin.")
    return texto[inicio:fin]


def n_repetir_texto(texto, veces):
    if not _txt(texto):
        raise ErrorTipo("repetir_texto espera un texto.")
    if not _entero(veces):
        raise ErrorTipo("repetir_texto espera un número entero.")
    if veces < 0:
        raise ErrorValor("repetir_texto no acepta números negativos.")
    return texto * veces


def n_al_reves(x):
    if _txt(x):
        return x[::-1]
    if _lista(x):
        return list(reversed(x))
    raise ErrorTipo(f"al_reves espera texto o lista, pero recibí {_tipo(x)}.")


def n_contar_palabras(texto):
    if not _txt(texto):
        raise ErrorTipo("contar_palabras espera un texto.")
    return len(texto.split())


def n_indice_texto(texto, subtexto):
    if not _txt(texto) or not _txt(subtexto):
        raise ErrorTipo("indice_texto espera dos textos.")
    return texto.find(subtexto)


# ============================================================
# NÚMEROS
# ============================================================

def n_absoluto(x):
    if _num(x):
        return abs(x)
    raise ErrorTipo(f"absoluto espera un número, pero recibí {_tipo(x)}.")


def n_signo(x):
    if not _num(x):
        raise ErrorTipo(f"signo espera un número, pero recibí {_tipo(x)}.")
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


def n_redondear(x, decimales=0):
    if not _num(x):
        raise ErrorTipo(f"redondear espera un número, pero recibí {_tipo(x)}.")
    if not _entero(decimales):
        raise ErrorTipo("redondear espera un entero como decimales.")
    if decimales == 0:
        return round(x)
    return round(x, decimales)


def n_techo(x):
    if _num(x):
        return math.ceil(x)
    raise ErrorTipo(f"techo espera un número, pero recibí {_tipo(x)}.")


def n_piso(x):
    if _num(x):
        return math.floor(x)
    raise ErrorTipo(f"piso espera un número, pero recibí {_tipo(x)}.")


def n_raiz(x):
    if not _num(x):
        raise ErrorTipo("raiz espera un número.")
    if x < 0:
        raise ErrorValor("no se puede calcular la raíz de un número negativo.")
    return math.sqrt(x)


def n_potencia(base, exponente):
    if _num(base) and _num(exponente):
        return base ** exponente
    raise ErrorTipo("potencia espera dos números.")


def n_maximo(*args):
    if len(args) == 1 and _lista(args[0]):
        args = args[0]
    if len(args) == 0:
        raise ErrorValor("maximo necesita al menos un valor.")
    if not all(_num(x) for x in args):
        raise ErrorTipo("maximo solo funciona con números.")
    return max(args)


def n_minimo(*args):
    if len(args) == 1 and _lista(args[0]):
        args = args[0]
    if len(args) == 0:
        raise ErrorValor("minimo necesita al menos un valor.")
    if not all(_num(x) for x in args):
        raise ErrorTipo("minimo solo funciona con números.")
    return min(args)


def n_suma(lista):
    if not _lista(lista):
        raise ErrorTipo("suma espera una lista de números.")
    total = 0
    for x in lista:
        if not _num(x):
            raise ErrorTipo(f"suma espera solo números, pero encontré {_tipo(x)}.")
        total += x
    return total


def n_promedio(lista):
    if not _lista(lista):
        raise ErrorTipo("promedio espera una lista de números.")
    if len(lista) == 0:
        raise ErrorValor("no se puede calcular el promedio de una lista vacía.")
    return n_suma(lista) / len(lista)


def n_aleatorio(inicio, fin):
    if not _entero(inicio) or not _entero(fin):
        raise ErrorTipo("aleatorio espera dos números enteros.")
    if inicio > fin:
        raise ErrorValor("aleatorio: el inicio no puede ser mayor que el fin.")
    return random.randint(inicio, fin)


def n_decimal_aleatorio():
    return random.random()


def n_entre(x, a, b):
    if not _num(x) or not _num(a) or not _num(b):
        raise ErrorTipo("entre espera tres números.")
    return a <= x <= b


def n_es_primo(x):
    if not _entero(x):
        raise ErrorTipo("es_primo espera un número entero.")
    if x < 2:
        return False
    if x == 2:
        return True
    if x % 2 == 0:
        return False
    i = 3
    while i * i <= x:
        if x % i == 0:
            return False
        i += 2
    return True


def n_factorial(x):
    if not _entero(x):
        raise ErrorTipo("factorial espera un número entero.")
    if x < 0:
        raise ErrorValor("factorial no acepta números negativos.")
    return math.factorial(x)


def n_fibonacci(x):
    if not _entero(x):
        raise ErrorTipo("fibonacci espera un número entero.")
    if x < 0:
        raise ErrorValor("fibonacci no acepta números negativos.")
    if x == 0:
        return 0
    if x == 1:
        return 1
    a, b = 0, 1
    for _ in range(x - 1):
        a, b = b, a + b
    return b


# ============================================================
# LISTAS
# ============================================================

def n_agregar(lista, valor):
    if not _lista(lista):
        raise ErrorTipo("agregar espera una lista.")
    lista.append(valor)
    return lista


def n_quitar(lista, valor=None):
    if not _lista(lista):
        raise ErrorTipo("quitar espera una lista.")
    if valor is None:
        if not lista:
            raise ErrorValor("no se puede quitar de una lista vacía.")
        return lista.pop()
    if valor not in lista:
        raise ErrorValor(f"el valor {valor!r} no está en la lista.")
    lista.remove(valor)
    return lista


def n_insertar(lista, posicion, valor):
    if not _lista(lista):
        raise ErrorTipo("insertar espera una lista.")
    if not _entero(posicion):
        raise ErrorTipo("insertar espera un número entero como posición.")
    lista.insert(posicion, valor)
    return lista


def n_ordenar(lista):
    if not _lista(lista):
        raise ErrorTipo("ordenar espera una lista.")
    return sorted(lista)


def n_invertir(lista):
    if _lista(lista):
        return list(reversed(lista))
    if _txt(lista):
        return lista[::-1]
    raise ErrorTipo("invertir espera una lista o un texto.")


def n_repetir(lista, veces):
    if not _lista(lista):
        raise ErrorTipo("repetir espera una lista.")
    if not _entero(veces):
        raise ErrorTipo("repetir espera un número entero.")
    return lista * veces


def n_rango(inicio, fin=None, paso=1):
    if not _entero(inicio) or not _entero(paso):
        raise ErrorTipo("rango espera números enteros.")
    if fin is None:
        return list(range(inicio))
    if not _entero(fin):
        raise ErrorTipo("rango espera un entero como fin.")
    return list(range(inicio, fin, paso))


def n_filtrar(lista, funcion):
    if not _lista(lista):
        raise ErrorTipo("filtrar espera una lista como primer argumento.")
    if not callable(funcion):
        raise ErrorTipo(f"filtrar espera una función como segundo argumento, pero recibí {_tipo(funcion)}.")
    resultado = []
    for x in lista:
        if funcion(x):
            resultado.append(x)
    return resultado


def n_mapear(lista, funcion):
    if not _lista(lista):
        raise ErrorTipo("mapear espera una lista como primer argumento.")
    if not callable(funcion):
        raise ErrorTipo(f"mapear espera una función como segundo argumento, pero recibí {_tipo(funcion)}.")
    return [funcion(x) for x in lista]


def n_reducir(lista, funcion, inicial=None):
    if not _lista(lista):
        raise ErrorTipo("reducir espera una lista como primer argumento.")
    if not callable(funcion):
        raise ErrorTipo(f"reducir espera una función como segundo argumento, pero recibí {_tipo(funcion)}.")
    if len(lista) == 0:
        if inicial is None:
            raise ErrorValor("no se puede reducir una lista vacía sin valor inicial.")
        return inicial
    if inicial is None:
        acumulador = lista[0]
        resto = lista[1:]
    else:
        acumulador = inicial
        resto = lista
    for x in resto:
        acumulador = funcion(acumulador, x)
    return acumulador


def n_buscar(lista, valor):
    if not _lista(lista):
        raise ErrorTipo("buscar espera una lista.")
    try:
        return lista.index(valor)
    except ValueError:
        return -1


def n_contar(lista, valor):
    if not _lista(lista):
        raise ErrorTipo("contar espera una lista.")
    return lista.count(valor)


def n_indice(lista, posicion):
    if not _lista(lista):
        raise ErrorTipo("indice espera una lista.")
    if not _entero(posicion):
        raise ErrorTipo("indice espera un número entero.")
    if posicion < 0 or posicion >= len(lista):
        raise ErrorValor(f"la posición {posicion} está fuera de la lista.")
    return lista[posicion]


def n_primeros(lista, n):
    if not _lista(lista):
        raise ErrorTipo("primeros espera una lista.")
    if not _entero(n):
        raise ErrorTipo("primeros espera un número entero.")
    return lista[:n]


def n_ultimos(lista, n):
    if not _lista(lista):
        raise ErrorTipo("ultimos espera una lista.")
    if not _entero(n):
        raise ErrorTipo("ultimos espera un número entero.")
    if n == 0:
        return []
    return lista[-n:]


def n_unicos(lista):
    if not _lista(lista):
        raise ErrorTipo("unicos espera una lista.")
    vistos = []
    for x in lista:
        if x not in vistos:
            vistos.append(x)
    return vistos


def n_vacio(x):
    if isinstance(x, (str, list, dict)):
        return len(x) == 0
    if x is None:
        return True
    raise ErrorTipo(f"vacio espera texto, lista o mapa, pero recibí {_tipo(x)}.")


def n_lleno(x):
    if isinstance(x, (str, list, dict)):
        return len(x) > 0
    if x is None:
        return False
    raise ErrorTipo(f"lleno espera texto, lista o mapa, pero recibí {_tipo(x)}.")


def n_concatenar(a, b):
    if _lista(a) and _lista(b):
        return a + b
    if _txt(a) and _txt(b):
        return a + b
    raise ErrorTipo("concatenar espera dos listas o dos textos.")


# ============================================================
# CONVERSIÓN
# ============================================================

def n_a_texto(x):
    if x is None:
        return "nulo"
    if isinstance(x, bool):
        return "verdadero" if x else "falso"
    if callable(x) and not isinstance(x, type):
        return repr(x)
    if isinstance(x, float):
        if x.is_integer():
            return str(int(x))
        return f"{x:.10f}".rstrip("0").rstrip(".")
    if isinstance(x, list):
        return "[" + ", ".join(n_a_texto(e) for e in x) + "]"
    if isinstance(x, dict):
        return "{" + ", ".join(
            f"{n_a_texto(k)}: {n_a_texto(v)}" for k, v in x.items()
        ) + "}"
    return str(x)


def n_a_numero(x):
    if _num(x):
        return x
    if _txt(x):
        try:
            if "." in x:
                return float(x)
            return int(x)
        except ValueError:
            raise ErrorValor(f"no puedo convertir '{x}' a número.")
    if isinstance(x, bool):
        return 1 if x else 0
    raise ErrorTipo(f"no puedo convertir {_tipo(x)} a número.")


def n_a_logico(x):
    if isinstance(x, bool):
        return x
    if _num(x):
        return x != 0
    if _txt(x):
        minus = x.lower()
        if minus in ("verdadero", "si", "sí", "true", "1"):
            return True
        if minus in ("falso", "no", "false", "0", ""):
            return False
        raise ErrorValor(f"no puedo convertir '{x}' a lógico.")
    raise ErrorTipo(f"no puedo convertir {_tipo(x)} a lógico.")


# ============================================================
# SISTEMA
# ============================================================

def n_tiempo():
    return time.time()


def n_tipo(x):
    return _tipo(x)


def n_copiar(x):
    return _copy.deepcopy(x)


def n_claves(mapa):
    if not _mapa(mapa):
        raise ErrorTipo(f"claves espera un mapa, pero recibí {_tipo(mapa)}.")
    return list(mapa.keys())


def n_valores(mapa):
    if not _mapa(mapa):
        raise ErrorTipo(f"valores espera un mapa, pero recibí {_tipo(mapa)}.")
    return list(mapa.values())


# ============================================================
# ARCHIVOS
# ============================================================

def n_leer_archivo(ruta):
    r = _ruta_completa(ruta)
    if not os.path.exists(r):
        raise ErrorValor(f"no existe el archivo '{ruta}'.")
    if not os.path.isfile(r):
        raise ErrorValor(f"'{ruta}' no es un archivo.")
    try:
        with open(r, "r", encoding="utf-8") as f:
            return f.read()
    except OSError as e:
        raise ErrorValor(f"no puedo leer '{ruta}': {e}")


def n_escribir_archivo(ruta, contenido):
    r = _ruta_completa(ruta)
    if not _txt(contenido):
        contenido = n_a_texto(contenido)
    try:
        with open(r, "w", encoding="utf-8") as f:
            f.write(contenido)
    except OSError as e:
        raise ErrorValor(f"no puedo escribir '{ruta}': {e}")
    return None


def n_agregar_archivo(ruta, contenido):
    r = _ruta_completa(ruta)
    if not _txt(contenido):
        contenido = n_a_texto(contenido)
    try:
        with open(r, "a", encoding="utf-8") as f:
            f.write(contenido)
    except OSError as e:
        raise ErrorValor(f"no puedo escribir en '{ruta}': {e}")
    return None


def n_existe_archivo(ruta):
    r = _ruta_completa(ruta)
    return os.path.isfile(r)


def n_borrar_archivo(ruta):
    r = _ruta_completa(ruta)
    if not os.path.exists(r):
        raise ErrorValor(f"no existe el archivo '{ruta}'.")
    if not os.path.isfile(r):
        raise ErrorValor(f"'{ruta}' no es un archivo.")
    try:
        os.remove(r)
    except OSError as e:
        raise ErrorValor(f"no puedo borrar '{ruta}': {e}")
    return None


def n_listar_archivos(carpeta="."):
    r = _ruta_completa(carpeta)
    if not os.path.exists(r):
        raise ErrorValor(f"no existe la carpeta '{carpeta}'.")
    if not os.path.isdir(r):
        raise ErrorValor(f"'{carpeta}' no es una carpeta.")
    try:
        return sorted(os.listdir(r))
    except OSError as e:
        raise ErrorValor(f"no puedo listar '{carpeta}': {e}")


def n_crear_carpeta(ruta):
    r = _ruta_completa(ruta)
    try:
        os.makedirs(r, exist_ok=True)
    except OSError as e:
        raise ErrorValor(f"no puedo crear la carpeta '{ruta}': {e}")
    return None


def n_existe_carpeta(ruta):
    r = _ruta_completa(ruta)
    return os.path.isdir(r)


def n_leer_lineas(ruta):
    contenido = n_leer_archivo(ruta)
    if contenido == "":
        return []
    lineas = contenido.split("\n")
    if lineas and lineas[-1] == "":
        lineas = lineas[:-1]
    return lineas


def n_escribir_lineas(ruta, lineas):
    if not _lista(lineas):
        raise ErrorTipo("escribir_lineas espera una lista de líneas.")
    texto = "\n".join(n_a_texto(x) for x in lineas)
    if lineas:
        texto += "\n"
    return n_escribir_archivo(ruta, texto)


# ============================================================
# CSV
# ============================================================

def _parsear_campo_csv(campo):
    campo = campo.strip()
    if campo == "":
        return ""
    try:
        return int(campo)
    except ValueError:
        pass
    try:
        return float(campo)
    except ValueError:
        pass
    return campo


def n_separar_csv(texto):
    if not _txt(texto):
        raise ErrorTipo("separar_csv espera un texto.")
    lineas = texto.split("\n")
    filas = []
    for linea in lineas:
        if linea.strip() == "":
            continue
        campos = [c.strip().strip('"') for c in linea.split(",")]
        filas.append([_parsear_campo_csv(c) for c in campos])
    return filas


def n_unir_csv(filas):
    if not _lista(filas):
        raise ErrorTipo("unir_csv espera una lista de listas.")
    lineas = []
    for fila in filas:
        if not _lista(fila):
            raise ErrorTipo("unir_csv espera que cada fila sea una lista.")
        campos = []
        for campo in fila:
            texto = n_a_texto(campo)
            if "," in texto or '"' in texto or "\n" in texto:
                texto = '"' + texto.replace('"', '""') + '"'
            campos.append(texto)
        lineas.append(",".join(campos))
    return "\n".join(lineas)


# ============================================================
# ARCHIVOS EXTRA
# ============================================================

def n_mover_archivo(origen, destino):
    o = _ruta_completa(origen)
    d = _ruta_completa(destino)
    if not os.path.exists(o):
        raise ErrorValor(f"no existe '{origen}'.")
    if os.path.exists(d):
        raise ErrorValor(f"ya existe '{destino}'. elige otro nombre.")
    try:
        os.rename(o, d)
    except OSError as e:
        raise ErrorValor(f"no puedo mover '{origen}' a '{destino}': {e}")
    return None


def n_copiar_archivo(origen, destino):
    o = _ruta_completa(origen)
    d = _ruta_completa(destino)
    if not os.path.exists(o):
        raise ErrorValor(f"no existe '{origen}'.")
    if os.path.isdir(o):
        raise ErrorValor(f"'{origen}' es una carpeta, no un archivo.")
    try:
        shutil.copy2(o, d)
    except OSError as e:
        raise ErrorValor(f"no puedo copiar '{origen}' a '{destino}': {e}")
    return None


def n_renombrar_archivo(viejo, nuevo):
    return n_mover_archivo(viejo, nuevo)


def n_borrar_carpeta(ruta):
    r = _ruta_completa(ruta)
    if not os.path.exists(r):
        raise ErrorValor(f"no existe la carpeta '{ruta}'.")
    if not os.path.isdir(r):
        raise ErrorValor(f"'{ruta}' no es una carpeta.")
    try:
        shutil.rmtree(r)
    except OSError as e:
        raise ErrorValor(f"no puedo borrar '{ruta}': {e}")
    return None


def n_ruta_absoluta(ruta):
    return os.path.abspath(_ruta_completa(ruta))


def n_carpeta_actual():
    return ruta_actual()


def n_listar_todo(carpeta="."):
    r = _ruta_completa(carpeta)
    if not os.path.exists(r):
        raise ErrorValor(f"no existe la carpeta '{carpeta}'.")
    if not os.path.isdir(r):
        raise ErrorValor(f"'{carpeta}' no es una carpeta.")
    try:
        return sorted(os.listdir(r))
    except OSError as e:
        raise ErrorValor(f"no puedo listar '{carpeta}': {e}")


def n_es_carpeta(ruta):
    return os.path.isdir(_ruta_completa(ruta))


# ============================================================
# ENTRADA INTERACTIVA
# ============================================================

def n_pedir(texto=""):
    if not _txt(texto):
        texto = n_a_texto(texto)
    try:
        return input(texto)
    except EOFError:
        return ""


def n_pedir_numero(texto=""):
    entrada = n_pedir(texto)
    if not _txt(entrada):
        raise ErrorValor("no se pudo leer un número.")
    try:
        if "." in entrada:
            return float(entrada)
        return int(entrada)
    except ValueError:
        raise ErrorValor(f"'{entrada}' no es un número válido.")


def n_pedir_logico(texto=""):
    entrada = n_pedir(texto)
    minus = entrada.lower().strip()
    if minus in ("verdadero", "si", "sí", "s", "y", "yes", "true", "1"):
        return True
    if minus in ("falso", "no", "n", "false", "0"):
        return False
    raise ErrorValor(f"'{entrada}' no es un valor lógico (verdadero/falso).")


# ============================================================
# SISTEMA AVANZADO
# ============================================================

class _SalirPrograma(Exception):
    def __init__(self, codigo=0):
        self.codigo = codigo


def n_salir(codigo=0):
    if not _entero(codigo):
        codigo = 0
    raise _SalirPrograma(codigo)


def n_variable_entorno(nombre):
    if not _txt(nombre):
        raise ErrorTipo("variable_entorno espera un texto.")
    return os.environ.get(nombre, "")


def n_dormir(segundos):
    if not _num(segundos):
        raise ErrorTipo("dormir espera un número.")
    if segundos < 0:
        raise ErrorValor("dormir no acepta números negativos.")
    time.sleep(segundos)
    return None


def n_ejecutar_comando(cmd):
    if not _txt(cmd):
        raise ErrorTipo("ejecutar_comando espera un texto.")
    try:
        resultado = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30,
        )
        return {
            "codigo": resultado.returncode,
            "salida": resultado.stdout,
            "error": resultado.stderr,
        }
    except subprocess.TimeoutExpired:
        raise ErrorValor("el comando tardó demasiado (más de 30 segundos).")
    except Exception as e:
        raise ErrorValor(f"no puedo ejecutar el comando: {e}")


def es_salir_programa(e):
    return isinstance(e, _SalirPrograma)


def codigo_salida(e):
    return e.codigo


# ============================================================
# REGISTRO
# ============================================================

NATIVAS = {
    # texto
    "longitud":        n_longitud,
    "mayus":           n_mayus,
    "minus":           n_minus,
    "capitalizar":     n_capitalizar,
    "recortar":        n_recortar,
    "reemplazar":      n_reemplazar,
    "contiene":        n_contiene,
    "empieza":         n_empieza,
    "termina":         n_termina,
    "separar":         n_separar,
    "unir":            n_unir,
    "cortar":          n_cortar,
    "repetir_texto":   n_repetir_texto,
    "al_reves":        n_al_reves,
    "contar_palabras": n_contar_palabras,
    "indice_texto":    n_indice_texto,
    # números
    "absoluto":          n_absoluto,
    "signo":             n_signo,
    "redondear":         n_redondear,
    "techo":             n_techo,
    "piso":              n_piso,
    "raiz":              n_raiz,
    "potencia":          n_potencia,
    "maximo":            n_maximo,
    "minimo":            n_minimo,
    "suma":              n_suma,
    "promedio":          n_promedio,
    "aleatorio":         n_aleatorio,
    "decimal_aleatorio": n_decimal_aleatorio,
    "entre":             n_entre,
    "es_primo":          n_es_primo,
    "factorial":         n_factorial,
    "fibonacci":         n_fibonacci,
    # listas
    "agregar":    n_agregar,
    "quitar":     n_quitar,
    "insertar":   n_insertar,
    "ordenar":    n_ordenar,
    "invertir":   n_invertir,
    "repetir":    n_repetir,
    "rango":      n_rango,
    "filtrar":    n_filtrar,
    "mapear":     n_mapear,
    "reducir":    n_reducir,
    "buscar":     n_buscar,
    "contar":     n_contar,
    "indice":     n_indice,
    "primeros":   n_primeros,
    "ultimos":    n_ultimos,
    "unicos":     n_unicos,
    "vacio":      n_vacio,
    "lleno":      n_lleno,
    "concatenar": n_concatenar,
    # conversión
    "a_texto":   n_a_texto,
    "a_numero":  n_a_numero,
    "a_logico":  n_a_logico,
    # sistema
    "tiempo":  n_tiempo,
    "tipo":    n_tipo,
    "copiar":  n_copiar,
    "claves":  n_claves,
    "valores": n_valores,
    # archivos
    "leer_archivo":     n_leer_archivo,
    "escribir_archivo": n_escribir_archivo,
    "agregar_archivo":  n_agregar_archivo,
    "existe_archivo":   n_existe_archivo,
    "borrar_archivo":   n_borrar_archivo,
    "listar_archivos":  n_listar_archivos,
    "crear_carpeta":    n_crear_carpeta,
    "existe_carpeta":   n_existe_carpeta,
    "leer_lineas":      n_leer_lineas,
    "escribir_lineas":  n_escribir_lineas,
    # csv
    "separar_csv": n_separar_csv,
    "unir_csv":    n_unir_csv,
    # archivos extra
    "mover_archivo":     n_mover_archivo,
    "copiar_archivo":    n_copiar_archivo,
    "renombrar_archivo": n_renombrar_archivo,
    "borrar_carpeta":    n_borrar_carpeta,
    "ruta_absoluta":     n_ruta_absoluta,
    "carpeta_actual":    n_carpeta_actual,
    "listar_todo":       n_listar_todo,
    "es_carpeta":        n_es_carpeta,
    # entrada interactiva
    "pedir":         n_pedir,
    "pedir_numero":  n_pedir_numero,
    "pedir_logico":  n_pedir_logico,
    # sistema avanzado
    "salir":             n_salir,
    "variable_entorno":  n_variable_entorno,
    "dormir":            n_dormir,
    "ejecutar_comando":  n_ejecutar_comando,
}