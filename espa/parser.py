# espa/parser.py

from espa.tokens import (
    Token, PALABRA, IDENT, NUMERO, TEXTO, OPERADOR,
    PAREN_IZQ, PAREN_DER, COMA, DOS_PUNTOS, PUNTO,
    CORCHETE_IZQ, CORCHETE_DER, LLAVE_IZQ, LLAVE_DER,
    FIN_LINEA, FIN_ARCHIVO,
)
from espa import ast
from espa.errores import ErrorSintaxis


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def actual(self):
        return self.tokens[self.pos]

    def anterior(self):
        return self.tokens[self.pos - 1]

    def en_fin(self):
        return self.actual().tipo == FIN_ARCHIVO

    def avanzar(self):
        if not self.en_fin():
            self.pos += 1
        return self.anterior()

    def mirar(self, offset=1):
        p = self.pos + offset
        if p >= len(self.tokens):
            return self.tokens[-1]
        return self.tokens[p]

    def error(self, mensaje):
        t = self.actual()
        raise ErrorSintaxis(mensaje, t.linea, t.columna)

    def comprobar(self, tipo, valor=None):
        t = self.actual()
        if t.tipo != tipo:
            return False
        if valor is not None and t.valor != valor:
            return False
        return True

    def aceptar(self, tipo, valor=None):
        if self.comprobar(tipo, valor):
            return self.avanzar()
        return None

    def esperar(self, tipo, valor=None, mensaje=None):
        if self.comprobar(tipo, valor):
            return self.avanzar()
        if mensaje is None:
            mensaje = f"esperaba {tipo}"
            if valor:
                mensaje += f" '{valor}'"
            mensaje += f", pero encontré '{self.actual().valor}'"
        self.error(mensaje)

    def saltar_fin_linea(self):
        while self.comprobar(FIN_LINEA):
            self.avanzar()

    # ---------- expresiones ----------

    def expresion(self):
        return self.exp_o()

    def exp_o(self):
        izq = self.exp_y()
        while self.comprobar(PALABRA, "o"):
            op = self.avanzar().valor
            der = self.exp_y()
            izq = ast.Binaria(izq=izq, op=op, der=der,
                              linea=izq.linea, columna=izq.columna)
        return izq

    def exp_y(self):
        izq = self.exp_no()
        while self.comprobar(PALABRA, "y"):
            op = self.avanzar().valor
            der = self.exp_no()
            izq = ast.Binaria(izq=izq, op=op, der=der,
                              linea=izq.linea, columna=izq.columna)
        return izq

    def exp_no(self):
        if self.comprobar(PALABRA, "no"):
            t = self.avanzar()
            valor = self.exp_no()
            return ast.Unaria(op="no", valor=valor,
                              linea=t.linea, columna=t.columna)
        return self.exp_comparacion()

    def exp_comparacion(self):
        izq = self.exp_suma()
        while self.comprobar(OPERADOR) and self.actual().valor in (
            "==", "!=", "<", "<=", ">", ">="
        ):
            op = self.avanzar().valor
            der = self.exp_suma()
            izq = ast.Binaria(izq=izq, op=op, der=der,
                              linea=izq.linea, columna=izq.columna)
        return izq

    def exp_suma(self):
        izq = self.exp_producto()
        while self.comprobar(OPERADOR) and self.actual().valor in ("+", "-"):
            op = self.avanzar().valor
            der = self.exp_producto()
            izq = ast.Binaria(izq=izq, op=op, der=der,
                              linea=izq.linea, columna=izq.columna)
        return izq

    def exp_producto(self):
        izq = self.exp_unaria()
        while (
            (self.comprobar(OPERADOR) and self.actual().valor in ("*", "/", "**"))
            or self.comprobar(PALABRA, "residuo")
        ):
            op = self.avanzar().valor
            der = self.exp_unaria()
            izq = ast.Binaria(izq=izq, op=op, der=der,
                              linea=izq.linea, columna=izq.columna)
        return izq

    def exp_unaria(self):
        if self.comprobar(OPERADOR, "-"):
            t = self.avanzar()
            valor = self.exp_unaria()
            return ast.Unaria(op="-", valor=valor,
                              linea=t.linea, columna=t.columna)
        if self.comprobar(OPERADOR, "+"):
            t = self.avanzar()
            valor = self.exp_unaria()
            return ast.Unaria(op="+", valor=valor,
                              linea=t.linea, columna=t.columna)
        return self.exp_llamada()

    def exp_llamada(self):
        expr = self.exp_primaria()

        while True:
            if self.comprobar(PAREN_IZQ):
                self.avanzar()
                args = []
                if not self.comprobar(PAREN_DER):
                    args.append(self.expresion())
                    while self.aceptar(COMA):
                        args.append(self.expresion())
                self.esperar(PAREN_DER, mensaje="falta ')' en la llamada.")
                if isinstance(expr, ast.Identificador):
                    expr = ast.Llamada(nombre=expr.nombre, argumentos=args,
                                       linea=expr.linea, columna=expr.columna)
                else:
                    self.error("solo se pueden llamar funciones o métodos.")
                continue

            if self.comprobar(CORCHETE_IZQ):
                self.avanzar()
                idx = self.expresion()
                self.esperar(CORCHETE_DER, mensaje="falta ']' en el índice.")
                expr = ast.Indice(objeto=expr, indice=idx,
                                  linea=expr.linea, columna=expr.columna)
                continue

            if self.comprobar(PUNTO):
                self.avanzar()
                nombre = self.esperar(
                    IDENT,
                    mensaje="esperaba un nombre tras '.'.",
                ).valor
                if self.comprobar(PAREN_IZQ):
                    self.avanzar()
                    args = []
                    if not self.comprobar(PAREN_DER):
                        args.append(self.expresion())
                        while self.aceptar(COMA):
                            args.append(self.expresion())
                    self.esperar(PAREN_DER,
                                 mensaje="falta ')' en la llamada al método.")
                    expr = ast.LlamadaMetodo(objeto=expr, metodo=nombre,
                                             argumentos=args,
                                             linea=expr.linea,
                                             columna=expr.columna)
                else:
                    expr = ast.Acceso(objeto=expr, nombre=nombre,
                                      linea=expr.linea, columna=expr.columna)
                continue

            break

        return expr

    def exp_primaria(self):
        t = self.actual()

        if t.tipo == NUMERO:
            self.avanzar()
            if "." in t.valor:
                return ast.Numero(valor=float(t.valor), linea=t.linea, columna=t.columna)
            return ast.Numero(valor=int(t.valor), linea=t.linea, columna=t.columna)

        if t.tipo == TEXTO:
            self.avanzar()
            return ast.Texto(valor=t.valor, linea=t.linea, columna=t.columna)

        if t.tipo == PALABRA and t.valor == "verdadero":
            self.avanzar()
            return ast.Booleano(valor=True, linea=t.linea, columna=t.columna)

        if t.tipo == PALABRA and t.valor == "falso":
            self.avanzar()
            return ast.Booleano(valor=False, linea=t.linea, columna=t.columna)

        if t.tipo == PALABRA and t.valor == "nulo":
            self.avanzar()
            return ast.Nulo(linea=t.linea, columna=t.columna)

        if t.tipo == PALABRA and t.valor == "esto":
            self.avanzar()
            return ast.Esto(linea=t.linea, columna=t.columna)

        if t.tipo == PALABRA and t.valor == "nuevo":
            self.avanzar()
            nombre = self.esperar(
                IDENT,
                mensaje="esperaba el nombre de la clase tras 'nuevo'.",
            ).valor
            self.esperar(PAREN_IZQ, mensaje="falta '(' tras el nombre de la clase.")
            args = []
            if not self.comprobar(PAREN_DER):
                args.append(self.expresion())
                while self.aceptar(COMA):
                    args.append(self.expresion())
            self.esperar(PAREN_DER, mensaje="falta ')' al crear el objeto.")
            return ast.Nuevo(clase=nombre, argumentos=args,
                             linea=t.linea, columna=t.columna)

        if t.tipo == PALABRA and t.valor == "patron":
            self.avanzar()
            nombre = self.esperar(
                IDENT,
                mensaje="esperaba el nombre del patrón.",
            ).valor
            self.esperar(
                PALABRA, "con",
                mensaje="esperaba 'con' tras el nombre del patrón.",
            )
            args = [self.expresion()]
            while self.aceptar(COMA):
                args.append(self.expresion())
            return ast.UsarPatron(nombre=nombre, argumentos=args,
                                  linea=t.linea, columna=t.columna)

        if t.tipo == IDENT:
            self.avanzar()
            return ast.Identificador(nombre=t.valor, linea=t.linea, columna=t.columna)

        if t.tipo == PAREN_IZQ:
            self.avanzar()
            expr = self.expresion()
            self.esperar(PAREN_DER, mensaje="falta ')' para cerrar la agrupación.")
            return expr

        if t.tipo == CORCHETE_IZQ:
            self.avanzar()
            elementos = []
            if not self.comprobar(CORCHETE_DER):
                elementos.append(self.expresion())
                while self.aceptar(COMA):
                    elementos.append(self.expresion())
            self.esperar(CORCHETE_DER, mensaje="falta ']' para cerrar la lista.")
            return ast.Lista(elementos=elementos, linea=t.linea, columna=t.columna)

        if t.tipo == LLAVE_IZQ:
            self.avanzar()
            pares = []
            if not self.comprobar(LLAVE_DER):
                while True:
                    clave = self.expresion()
                    self.esperar(DOS_PUNTOS,
                                 mensaje="falta ':' entre clave y valor en el mapa.")
                    valor = self.expresion()
                    pares.append((clave, valor))
                    if not self.aceptar(COMA):
                        break
            self.esperar(LLAVE_DER, mensaje="falta '}' para cerrar el mapa.")
            return ast.Mapa(pares=pares, linea=t.linea, columna=t.columna)

        self.error(f"expresión inesperada: '{t.valor}'")

    # ---------- sentencias simples ----------

    def sentencia(self):
        self.saltar_fin_linea()
        t = self.actual()

        if t.tipo == PALABRA:
            if t.valor in ("variable", "constante"):
                return self.sent_declaracion()
            if t.valor == "escribir":
                return self.sent_escribir()
            if t.valor == "leer":
                return self.sent_leer()
            if t.valor == "retornar":
                return self.sent_retornar()
            if t.valor == "romper":
                self.avanzar()
                self.saltar_fin_linea()
                return ast.Romper(linea=t.linea, columna=t.columna)
            if t.valor == "saltar":
                self.avanzar()
                self.saltar_fin_linea()
                return ast.Saltar(linea=t.linea, columna=t.columna)
            if t.valor == "lanzar":
                return self.sent_lanzar()

        return self.sent_asignacion_o_expresion()

    def sent_declaracion(self):
        t = self.avanzar()
        es_constante = (t.valor == "constante")

        nombre = self.esperar(
            IDENT,
            mensaje=f"esperaba un nombre tras '{t.valor}'.",
        ).valor

        tipo = None
        if self.aceptar(DOS_PUNTOS):
            tipo = self.esperar(
                IDENT,
                mensaje="esperaba un tipo tras ':'.",
            ).valor

        valor = None
        if self.aceptar(OPERADOR, "="):
            valor = self.expresion()

        self.saltar_fin_linea()

        return ast.Declaracion(
            nombre=nombre, valor=valor, constante=es_constante, tipo=tipo,
            linea=t.linea, columna=t.columna,
        )

    def sent_escribir(self):
        t = self.avanzar()
        valores = [self.expresion()]
        while self.aceptar(COMA):
            valores.append(self.expresion())
        self.saltar_fin_linea()
        return ast.Escribir(valores=valores, linea=t.linea, columna=t.columna)

    def sent_leer(self):
        t = self.avanzar()
        destino = self.expresion()
        if not isinstance(destino, (ast.Identificador, ast.Indice, ast.Acceso)):
            raise ErrorSintaxis(
                "'leer' necesita una variable donde guardar el valor.",
                t.linea, t.columna,
            )
        self.saltar_fin_linea()
        return ast.Leer(destino=destino, linea=t.linea, columna=t.columna)

    def sent_retornar(self):
        t = self.avanzar()
        valor = None
        if not self.comprobar(FIN_LINEA) and not self.comprobar(FIN_ARCHIVO):
            valor = self.expresion()
        self.saltar_fin_linea()
        return ast.Retornar(valor=valor, linea=t.linea, columna=t.columna)

    def sent_lanzar(self):
        t = self.avanzar()
        valor = self.expresion()
        self.saltar_fin_linea()
        return ast.Lanzar(valor=valor, linea=t.linea, columna=t.columna)

    def sent_importar(self):
        t = self.avanzar()
        nombre = self.esperar(IDENT, mensaje="esperaba el nombre del módulo.").valor
        self.saltar_fin_linea()
        return ast.Importar(nombre=nombre, linea=t.linea, columna=t.columna)

    def sent_paquete(self):
        t = self.avanzar()
        nombre = self.esperar(IDENT, mensaje="esperaba el nombre del paquete.").valor
        self.saltar_fin_linea()
        return ast.Paquete(nombre=nombre, linea=t.linea, columna=t.columna)

    def sent_asignacion_o_expresion(self):
        t = self.actual()
        expr = self.expresion()

        if self.comprobar(OPERADOR, "="):
            self.avanzar()
            valor = self.expresion()
            self.saltar_fin_linea()
            return ast.Asignacion(destino=expr, valor=valor,
                                  linea=t.linea, columna=t.columna)

        if self.comprobar(OPERADOR) and self.actual().valor in ("+=", "-=", "*=", "/="):
            op_token = self.avanzar()
            op = op_token.valor[0]
            valor = self.expresion()
            self.saltar_fin_linea()
            binaria = ast.Binaria(izq=expr, op=op, der=valor,
                                  linea=op_token.linea, columna=op_token.columna)
            return ast.Asignacion(destino=expr, valor=binaria,
                                  linea=t.linea, columna=t.columna)

        self.saltar_fin_linea()
        return expr

    # ---------- bloques ----------

    def bloque(self, cierres, nombre_apertura=""):
        cuerpo = []
        self.saltar_fin_linea()
        while not self.en_fin():
            if self.es_cierre(cierres):
                return cuerpo
            cuerpo.append(self.sentencia_completa())
            self.saltar_fin_linea()

        if nombre_apertura:
            t = self.actual()
            raise ErrorSintaxis(
                f"falta 'fin {nombre_apertura}' para el bloque abierto.",
                t.linea, t.columna,
            )
        return cuerpo

    def es_cierre(self, cierres):
        t = self.actual()
        if t.tipo != PALABRA:
            return False
        for c in cierres:
            if len(c) == 1 and t.valor == c[0]:
                return True
        if t.valor == "fin" and self.mirar(1).tipo == PALABRA:
            par = ("fin", self.mirar(1).valor)
            if par in cierres:
                return True
        return False

    def consumir_cierre(self, par):
        for p in par:
            self.esperar(PALABRA, p, mensaje=f"esperaba '{p}'.")
        self.saltar_fin_linea()

    def sentencia_completa(self):
        self.saltar_fin_linea()
        t = self.actual()

        if t.tipo == PALABRA:
            if t.valor == "algoritmo":
                return self.bloque_algoritmo()
            if t.valor == "si":
                return self.bloque_si()
            if t.valor == "segun":
                return self.bloque_segun()
            if t.valor == "mientras":
                return self.bloque_mientras()
            if t.valor == "para":
                return self.bloque_para()
            if t.valor == "funcion":
                return self.bloque_funcion()
            if t.valor == "patron":
                return self.bloque_patron()
            if t.valor == "clase":
                return self.bloque_clase()
            if t.valor == "intentar":
                return self.bloque_intentar()

        return self.sentencia()

    def bloque_algoritmo(self):
        t = self.avanzar()
        nombre = self.esperar(IDENT, mensaje="esperaba el nombre del algoritmo.").valor
        self.saltar_fin_linea()
        cuerpo = self.bloque({("fin", "algoritmo")}, "algoritmo")
        self.consumir_cierre(("fin", "algoritmo"))
        return ast.Programa(nombre=nombre, cuerpo=cuerpo,
                            linea=t.linea, columna=t.columna)

    def bloque_si(self):
        t = self.avanzar()
        condicion = self.expresion()
        self.aceptar(PALABRA, "entonces")
        self.saltar_fin_linea()

        entonces = self.bloque({("sino",), ("fin", "si")}, "si")

        sino = []
        if self.comprobar(PALABRA, "sino"):
            self.avanzar()
            self.saltar_fin_linea()
            sino = self.bloque({("fin", "si")}, "si")

        self.consumir_cierre(("fin", "si"))
        return ast.Si(condicion=condicion, entonces=entonces, sino=sino,
                      linea=t.linea, columna=t.columna)

    def bloque_segun(self):
        t = self.avanzar()
        valor = self.expresion()
        self.aceptar(PALABRA, "entonces")
        self.saltar_fin_linea()

        casos = []
        defecto = []

        while not self.es_cierre({("fin", "segun")}):
            self.saltar_fin_linea()
            if self.comprobar(PALABRA, "caso"):
                self.avanzar()
                v = self.expresion()
                self.saltar_fin_linea()
                cuerpo = self.bloque(
                    {("caso",), ("defecto",), ("fin", "segun")}, "segun"
                )
                casos.append((v, cuerpo))
            elif self.comprobar(PALABRA, "defecto"):
                self.avanzar()
                self.saltar_fin_linea()
                defecto = self.bloque({("fin", "segun")}, "segun")
            else:
                self.error("esperaba 'caso', 'defecto' o 'fin segun'.")

        self.consumir_cierre(("fin", "segun"))
        return ast.Segun(valor=valor, casos=casos, defecto=defecto,
                         linea=t.linea, columna=t.columna)

    def bloque_mientras(self):
        t = self.avanzar()
        condicion = self.expresion()
        self.aceptar(PALABRA, "hacer")
        self.saltar_fin_linea()
        cuerpo = self.bloque({("fin", "mientras")}, "mientras")
        self.consumir_cierre(("fin", "mientras"))
        return ast.Mientras(condicion=condicion, cuerpo=cuerpo,
                            linea=t.linea, columna=t.columna)

    def bloque_para(self):
        t = self.avanzar()  # para

        # forma 1: para cada x en lista
        if self.comprobar(PALABRA, "cada"):
            self.avanzar()
            variable = self.esperar(IDENT, mensaje="esperaba la variable del bucle.").valor
            self.esperar(PALABRA, "en", mensaje="esperaba 'en' tras la variable.")
            coleccion = self.expresion()
            self.aceptar(PALABRA, "hacer")
            self.saltar_fin_linea()
            cuerpo = self.bloque({("fin", "para")}, "para")
            self.consumir_cierre(("fin", "para"))
            return ast.ParaCada(variable=variable, coleccion=coleccion,
                                cuerpo=cuerpo, linea=t.linea, columna=t.columna)

        # forma 2: para i desde a hasta b [paso c]
        variable = self.esperar(
            IDENT,
            mensaje="esperaba 'cada' o un nombre de variable tras 'para'.",
        ).valor
        self.esperar(PALABRA, "desde",
                     mensaje="esperaba 'desde' tras la variable del bucle.")
        inicio = self.expresion()
        self.esperar(PALABRA, "hasta",
                     mensaje="esperaba 'hasta' tras el valor inicial.")
        fin = self.expresion()

        paso = None
        if self.aceptar(PALABRA, "paso"):
            paso = self.expresion()

        self.aceptar(PALABRA, "hacer")
        self.saltar_fin_linea()
        cuerpo = self.bloque({("fin", "para")}, "para")
        self.consumir_cierre(("fin", "para"))
        return ast.ParaNumerico(variable=variable, inicio=inicio, fin=fin,
                                paso=paso, cuerpo=cuerpo,
                                linea=t.linea, columna=t.columna)

    def bloque_funcion(self):
        t = self.avanzar()
        nombre = self.esperar(IDENT, mensaje="esperaba el nombre de la función.").valor
        self.esperar(PAREN_IZQ, mensaje="falta '(' tras el nombre de la función.")

        parametros = []
        if not self.comprobar(PAREN_DER):
            parametros.append(self.esperar(IDENT, mensaje="esperaba un parámetro.").valor)
            while self.aceptar(COMA):
                parametros.append(self.esperar(IDENT, mensaje="esperaba un parámetro.").valor)

        self.esperar(PAREN_DER, mensaje="falta ')' en los parámetros.")
        self.saltar_fin_linea()
        cuerpo = self.bloque({("fin", "funcion")}, "funcion")
        self.consumir_cierre(("fin", "funcion"))
        return ast.Funcion(nombre=nombre, parametros=parametros, cuerpo=cuerpo,
                           linea=t.linea, columna=t.columna)

    def bloque_patron(self):
        t = self.avanzar()
        nombre = self.esperar(
            IDENT,
            mensaje="esperaba el nombre del patrón.",
        ).valor

        parametros = []
        if self.comprobar(PALABRA, "con"):
            self.avanzar()
            parametros.append(self.esperar(
                IDENT,
                mensaje="esperaba el nombre de un parámetro tras 'con'.",
            ).valor)
            while self.aceptar(COMA):
                parametros.append(self.esperar(
                    IDENT,
                    mensaje="esperaba otro parámetro.",
                ).valor)

        self.saltar_fin_linea()
        cuerpo = self.bloque({("fin", "patron")}, "patron")
        self.consumir_cierre(("fin", "patron"))
        return ast.Patron(nombre=nombre, parametros=parametros, cuerpo=cuerpo,
                          linea=t.linea, columna=t.columna)

    def bloque_clase(self):
        t = self.avanzar()
        nombre = self.esperar(IDENT, mensaje="esperaba el nombre de la clase.").valor

        base = None
        if self.comprobar(PALABRA, "herea"):
            self.avanzar()
            base = self.esperar(IDENT, mensaje="esperaba la clase base.").valor

        self.saltar_fin_linea()
        cuerpo = self.bloque({("fin", "clase")}, "clase")
        self.consumir_cierre(("fin", "clase"))
        return ast.Clase(nombre=nombre, base=base, cuerpo=cuerpo,
                         linea=t.linea, columna=t.columna)

    def bloque_intentar(self):
        t = self.avanzar()  # intentar
        self.saltar_fin_linea()

        cuerpo = self.bloque({("capturar",), ("finalmente",)}, "intentar")

        nombre_error = ""
        captura = []
        if self.comprobar(PALABRA, "capturar"):
            self.avanzar()
            nombre_error = self.esperar(
                IDENT,
                mensaje="esperaba el nombre del error tras 'capturar'.",
            ).valor
            self.saltar_fin_linea()
            captura = self.bloque({("finalmente",), ("fin", "intentar")}, "intentar")

        finalmente = []
        if self.comprobar(PALABRA, "finalmente"):
            self.avanzar()
            self.saltar_fin_linea()
            finalmente = self.bloque({("fin", "intentar")}, "intentar")

        if not captura and not finalmente:
            self.error("'intentar' necesita al menos un 'capturar' o un 'finalmente'.")

        self.consumir_cierre(("fin", "intentar"))
        return ast.Intentar(cuerpo=cuerpo, nombre_error=nombre_error,
                            captura=captura, finalmente=finalmente,
                            linea=t.linea, columna=t.columna)

    # ---------- punto de entrada ----------

    def analizar(self):
        self.saltar_fin_linea()
        declaraciones = []

        while not self.en_fin():
            t = self.actual()
            if t.tipo == PALABRA and t.valor == "paquete":
                declaraciones.append(self.sent_paquete())
                continue
            if t.tipo == PALABRA and t.valor == "importar":
                declaraciones.append(self.sent_importar())
                continue
            break

        self.saltar_fin_linea()

        while not self.en_fin():
            self.saltar_fin_linea()
            if self.en_fin():
                break

            t = self.actual()
            if t.tipo == PALABRA and t.valor == "algoritmo":
                prog = self.bloque_algoritmo()
                declaraciones.extend(prog.cuerpo)
                continue
            if t.tipo == PALABRA and t.valor == "funcion":
                declaraciones.append(self.bloque_funcion())
                continue
            if t.tipo == PALABRA and t.valor == "patron":
                declaraciones.append(self.bloque_patron())
                continue
            if t.tipo == PALABRA and t.valor == "clase":
                declaraciones.append(self.bloque_clase())
                continue
            declaraciones.append(self.sentencia_completa())

        return ast.Programa(
            nombre="",
            cuerpo=declaraciones,
            linea=1,
            columna=1,
        )