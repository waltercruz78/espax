# espa/cli.py

import sys
import os

from espa.lexer import Lexer
from espa.parser import Parser
from espa.interprete import Interprete
from espa.errores import ErrorEspa
from espa.nativas import es_salir_programa, codigo_salida


def _soportan_colores():
    return sys.stdout.isatty()


class Color:
    ROJO = "\033[31m"
    GRIS = "\033[90m"
    FIN = "\033[0m"


def rojo(texto):
    if _soportan_colores():
        return f"{Color.ROJO}{texto}{Color.FIN}"
    return texto


def gris(texto):
    if _soportan_colores():
        return f"{Color.GRIS}{texto}{Color.FIN}"
    return texto


def ejecutar_archivo(ruta):
    if not os.path.exists(ruta):
        print(rojo(f"error: no encuentro el archivo '{ruta}'."))
        return 1

    if not ruta.endswith(".wal"):
        print(rojo(f"error: '{ruta}' no termina en '.wal'."))
        print(gris("los archivos de espa+ usan la extensión .wal"))
        return 1

    try:
        with open(ruta, "r", encoding="utf-8") as f:
            codigo = f.read()
    except OSError as e:
        print(rojo(f"error al leer el archivo: {e}"))
        return 1

    ruta_abs = os.path.abspath(ruta)
    ruta_base = os.path.dirname(ruta_abs)
    return ejecutar_codigo(codigo, nombre_archivo=ruta, ruta_base=ruta_base)


def ejecutar_codigo(codigo, nombre_archivo="<wal>", ruta_base=None):
    if ruta_base is None:
        ruta_base = os.getcwd()
    try:
        tokens = Lexer(codigo).tokenizar()
        arbol = Parser(tokens).analizar()
        Interprete(ruta_base=ruta_base).ejecutar(arbol)
        return 0
    except ErrorEspa as e:
        ubicacion = ""
        if e.linea > 0:
            ubicacion = f"{nombre_archivo}:{e.linea}:{e.columna}: "
        print(rojo(f"{ubicacion}{e.mensaje}"))
        return 1
    except RecursionError:
        print(rojo("error: el programa es demasiado profundo. "
                   "¿hay una función que se llama a sí misma sin parar?"))
        return 1
    except KeyboardInterrupt:
        print()
        print(gris("interrumpido."))
        return 130
    except Exception as e:
        if es_salir_programa(e):
            return codigo_salida(e)
        print(rojo(f"error interno del motor: {type(e).__name__}: {e}"))
        print(gris("esto no debería pasar. es un fallo de espa+, no de tu código."))
        return 2


def repl():
    print(gris("espa+ v0.4 — escribí 'salir' para terminar."))
    print(gris("cada línea se ejecuta al presionar enter."))
    print()

    interprete = Interprete(ruta_base=os.getcwd())

    while True:
        try:
            linea = input("espa+> ")
        except (EOFError, KeyboardInterrupt):
            print()
            print(gris("hasta luego."))
            return 0

        if linea.strip() in ("salir", "terminar", "exit", "quit"):
            print(gris("hasta luego."))
            return 0

        if not linea.strip():
            continue

        try:
            tokens = Lexer(linea).tokenizar()
            arbol = Parser(tokens).analizar()
            interprete.ejecutar(arbol)
        except ErrorEspa as e:
            ubicacion = ""
            if e.linea > 0:
                ubicacion = f"línea {e.linea}: "
            print(rojo(f"{ubicacion}{e.mensaje}"))
        except KeyboardInterrupt:
            print()
            print(gris("interrumpido."))
        except Exception as e:
            if es_salir_programa(e):
                print(gris("hasta luego."))
                return codigo_salida(e)
            print(rojo(f"error interno: {type(e).__name__}: {e}"))


def mostrar_ayuda():
    print("uso: corre [archivo.wal]")
    print()
    print("  corre programa.wal   ejecuta un archivo espa+")
    print("  corre                abre la consola interactiva (repl)")
    print("  corre --ayuda        muestra esta ayuda")
    print("  corre --version      muestra la versión")
    print()
    print("los archivos de espa+ usan la extensión .wal")


def mostrar_version():
    print("espa+ v0.4")


def main():
    args = sys.argv[1:]

    if not args:
        return repl()

    if args[0] in ("--ayuda", "-h", "-?"):
        mostrar_ayuda()
        return 0

    if args[0] in ("--version", "-v"):
        mostrar_version()
        return 0

    if len(args) > 1:
        print(rojo("error: demasiados argumentos."))
        print(gris("uso: corre [archivo.wal]"))
        return 1

    return ejecutar_archivo(args[0])


if __name__ == "__main__":
    sys.exit(main())