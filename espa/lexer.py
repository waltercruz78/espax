# espa/lexer.py

from espa.tokens import (
    Token, PALABRA, IDENT, NUMERO, TEXTO, OPERADOR,
    PAREN_IZQ, PAREN_DER, COMA, DOS_PUNTOS, PUNTO,
    CORCHETE_IZQ, CORCHETE_DER, LLAVE_IZQ, LLAVE_DER,
    FIN_LINEA, FIN_ARCHIVO,
)
from espa.errores import ErrorLexico

PALABRAS = {
    "algoritmo", "funcion", "si", "sino", "segun",
    "mientras", "para", "cada", "en",
    "intentar", "capturar", "clase", "fin",
    "variable", "constante", "retornar", "romper", "saltar",
    "escribir", "leer",
    "verdadero", "falso", "nulo",
    "y", "o", "no", "residuo",
    "importar", "paquete",
    "caso", "defecto",
    "lanzar",
    "esto", "herea", "nuevo",
    "asincrono", "esperar",
    "entonces", "hacer",
    "patron", "con",
    "desde", "hasta", "paso", "finalmente",
}


class Lexer:
    def __init__(self, texto):
        self.texto = texto
        self.pos = 0
        self.linea = 1
        self.columna = 1
        self.tokens = []

    def error(self, mensaje):
        raise ErrorLexico(mensaje, self.linea, self.columna)

    def actual(self):
        if self.pos >= len(self.texto):
            return None
        return self.texto[self.pos]

    def mirar(self, offset=1):
        p = self.pos + offset
        if p >= len(self.texto):
            return None
        return self.texto[p]

    def avanzar(self):
        c = self.texto[self.pos]
        self.pos += 1
        if c == "\n":
            self.linea += 1
            self.columna = 1
        else:
            self.columna += 1
        return c

    def agregar(self, tipo, valor, linea, columna):
        self.tokens.append(Token(tipo, valor, linea, columna))

    def tokenizar(self):
        while self.pos < len(self.texto):
            c = self.actual()

            if c in " \t\r":
                self.avanzar()
                continue

            if c == "\n":
                l, col = self.linea, self.columna
                self.avanzar()
                self.agregar(FIN_LINEA, "\n", l, col)
                continue

            if c == "#":
                while self.actual() is not None and self.actual() != "\n":
                    self.avanzar()
                continue

            if c == "/" and self.mirar() == "*":
                self.avanzar()
                self.avanzar()
                while True:
                    if self.actual() is None:
                        self.error("comentario '/*' sin cerrar. falta '*/'.")
                    if self.actual() == "*" and self.mirar() == "/":
                        self.avanzar()
                        self.avanzar()
                        break
                    self.avanzar()
                continue

            if c.isdigit():
                self.leer_numero()
                continue

            if c == '"':
                self.leer_texto()
                continue

            if c.isalpha() or c == "_":
                self.leer_identificador()
                continue

            self.leer_simbolo()

        self.agregar(FIN_ARCHIVO, "", self.linea, self.columna)
        return self.tokens

    def leer_numero(self):
        l, col = self.linea, self.columna
        inicio = self.pos
        tiene_punto = False
        while self.actual() is not None and (self.actual().isdigit() or self.actual() == "."):
            if self.actual() == ".":
                if tiene_punto:
                    self.error("número con dos puntos decimales.")
                tiene_punto = True
            self.avanzar()
        valor = self.texto[inicio:self.pos]
        self.agregar(NUMERO, valor, l, col)

    def leer_texto(self):
        l, col = self.linea, self.columna
        self.avanzar()
        resultado = []
        escapes = {"n": "\n", "t": "\t", '"': '"', "\\": "\\"}
        while True:
            c = self.actual()
            if c is None:
                self.error("texto sin cerrar. falta '\"'.")
            if c == "\n":
                self.error("texto sin cerrar. falta '\"'.")
            if c == "\\":
                self.avanzar()
                e = self.actual()
                if e is None:
                    self.error("escape incompleto al final del archivo.")
                if e not in escapes:
                    self.error(f"escape desconocido: '\\{e}'.")
                resultado.append(escapes[e])
                self.avanzar()
                continue
            if c == '"':
                self.avanzar()
                break
            resultado.append(c)
            self.avanzar()
        self.agregar(TEXTO, "".join(resultado), l, col)

    def leer_identificador(self):
        l, col = self.linea, self.columna
        inicio = self.pos
        while self.actual() is not None and (
            self.actual().isalnum()
            or self.actual() == "_"
            or ord(self.actual()) > 127
        ):
            self.avanzar()
        valor = self.texto[inicio:self.pos]
        minus = valor.lower()
        if minus in PALABRAS:
            self.agregar(PALABRA, minus, l, col)
        else:
            self.agregar(IDENT, minus, l, col)

    def leer_simbolo(self):
        l, col = self.linea, self.columna
        c = self.actual()

        dos = self.texto[self.pos:self.pos + 2]
        if dos in ("==", "<=", ">=", "!=", "**", "+=", "-=", "*=", "/="):
            self.avanzar()
            self.avanzar()
            self.agregar(OPERADOR, dos, l, col)
            return

        simples = {
            "+": OPERADOR, "-": OPERADOR, "*": OPERADOR, "/": OPERADOR,
            "=": OPERADOR, "<": OPERADOR, ">": OPERADOR,
            "(": PAREN_IZQ, ")": PAREN_DER,
            ",": COMA, ":": DOS_PUNTOS, ".": PUNTO,
            "[": CORCHETE_IZQ, "]": CORCHETE_DER,
            "{": LLAVE_IZQ, "}": LLAVE_DER,
        }
        if c in simples:
            self.avanzar()
            self.agregar(simples[c], c, l, col)
            return

        self.error(f"carácter desconocido: {c!r}")