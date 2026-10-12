# espa/interprete.py

import os

from espa import ast
from espa.entorno import Entorno
from espa.errores import (
    ErrorEjecucion, ErrorNombre, ErrorTipo, ErrorValor,
    ErrorLogico, ErrorControl, ErrorEspa,
)
from espa import nativas
from espa.nativas import NATIVAS


class _Retorno(Exception):
    def __init__(self, valor):
        self.valor = valor


class _Romper(Exception):
    pass


class _Saltar(Exception):
    pass


class _NodoFalso:
    linea = 0
    columna = 0


class Callable:
    def __init__(self, interprete, nombre, entorno):
        self.interprete = interprete
        self.nombre = nombre
        self.entorno = entorno

    def __call__(self, *args):
        return self.interprete.llamar_por_nombre(
            self.nombre, list(args), self.entorno, _NodoFalso()
        )

    def __repr__(self):
        return f"<funcion {self.nombre}>"


class Interprete:
    def __init__(self, ruta_base=None, importados=None):
        self.global_ = Entorno(nombre="global")
        self.ruta_base = ruta_base if ruta_base is not None else os.getcwd()
        self.importados = importados if importados is not None else set()

    # ---------- entrada ----------

    def ejecutar(self, programa, entorno=None):
        if entorno is None:
            entorno = self.global_

        for nodo in programa.cuerpo:
            if isinstance(nodo, ast.Funcion):
                entorno.definir_funcion(nodo.nombre, nodo)
            elif isinstance(nodo, ast.Patron):
                entorno.definir_patron(nodo.nombre, nodo)
            elif isinstance(nodo, ast.Clase):
                entorno.definir_clase(nodo.nombre, nodo)

        nativas.empujar_ruta(self.ruta_base)
        try:
            for nodo in programa.cuerpo:
                if isinstance(nodo, (ast.Funcion, ast.Patron, ast.Clase)):
                    continue
                try:
                    self.ejecutar_nodo(nodo, entorno)
                except _Retorno:
                    raise ErrorControl(
                        "'retornar' solo funciona dentro de una función o patrón.",
                        nodo.linea, nodo.columna,
                    )
                except _Romper:
                    raise ErrorControl(
                        "'romper' solo funciona dentro de un bucle.",
                        nodo.linea, nodo.columna,
                    )
                except _Saltar:
                    raise ErrorControl(
                        "'saltar' solo funciona dentro de un bucle.",
                        nodo.linea, nodo.columna,
                    )
        finally:
            nativas.sacar_ruta()

    # ---------- despacho ----------

    def ejecutar_nodo(self, nodo, entorno):
        if isinstance(nodo, (
            ast.Numero, ast.Texto, ast.Booleano, ast.Nulo,
            ast.Identificador, ast.Binaria, ast.Unaria,
            ast.Lista, ast.Mapa, ast.Indice, ast.Acceso,
            ast.Llamada, ast.UsarPatron, ast.LlamadaMetodo,
            ast.Nuevo, ast.Esto,
        )):
            self.evaluar(nodo, entorno)
            return

        if isinstance(nodo, ast.Paquete):
            return
        if isinstance(nodo, ast.Importar):
            return self.ej_importar(nodo, entorno)
        if isinstance(nodo, ast.Declaracion):
            return self.ej_declaracion(nodo, entorno)
        if isinstance(nodo, ast.Asignacion):
            return self.ej_asignacion(nodo, entorno)
        if isinstance(nodo, ast.Escribir):
            return self.ej_escribir(nodo, entorno)
        if isinstance(nodo, ast.Leer):
            return self.ej_leer(nodo, entorno)
        if isinstance(nodo, ast.Retornar):
            return self.ej_retornar(nodo, entorno)
        if isinstance(nodo, ast.Romper):
            raise _Romper()
        if isinstance(nodo, ast.Saltar):
            raise _Saltar()
        if isinstance(nodo, ast.Lanzar):
            return self.ej_lanzar(nodo, entorno)
        if isinstance(nodo, ast.Programa):
            return self.ejecutar(nodo, entorno)

        if isinstance(nodo, (ast.Si, ast.Segun, ast.Mientras,
                             ast.ParaCada, ast.ParaNumerico, ast.Intentar)):
            return self.ejecutar_bloque(nodo, entorno)

        raise ErrorEjecucion(
            f"no sé ejecutar '{type(nodo).__name__}'.",
            nodo.linea, nodo.columna,
        )

    # ---------- importar ----------

    def ej_importar(self, nodo, entorno):
        nombre = nodo.nombre

        if nombre.endswith(".wal"):
            archivo = nombre
        else:
            archivo = nombre + ".wal"

        ruta = os.path.abspath(os.path.join(self.ruta_base, archivo))

        if ruta in self.importados:
            return

        if not os.path.exists(ruta):
            raise ErrorEjecucion(
                f"no encuentro el módulo '{nombre}'. "
                f"esperaba el archivo '{ruta}'.",
                nodo.linea, nodo.columna,
            )

        self.importados.add(ruta)

        try:
            with open(ruta, "r", encoding="utf-8") as f:
                codigo = f.read()
        except OSError as e:
            raise ErrorEjecucion(
                f"no puedo leer el módulo '{nombre}': {e}",
                nodo.linea, nodo.columna,
            )

        from espa.lexer import Lexer
        from espa.parser import Parser

        try:
            tokens = Lexer(codigo).tokenizar()
            arbol = Parser(tokens).analizar()
        except ErrorEspa as e:
            raise ErrorEjecucion(
                f"error al cargar el módulo '{nombre}': {e.mensaje}",
                nodo.linea, nodo.columna,
            )

        nuevo_interprete = Interprete(
            ruta_base=os.path.dirname(ruta),
            importados=self.importados,
        )
        try:
            nuevo_interprete.ejecutar(arbol)
        except ErrorEspa as e:
            raise ErrorEjecucion(
                f"error al ejecutar el módulo '{nombre}': {e.mensaje}",
                nodo.linea, nodo.columna,
            )

        entorno.absorber(nuevo_interprete.global_)

    # ---------- sentencias simples ----------

    def ej_declaracion(self, nodo, entorno):
        valor = None
        if nodo.valor is not None:
            valor = self.evaluar(nodo.valor, entorno)

        if nodo.tipo is not None and valor is not None:
            self.verificar_tipo(valor, nodo.tipo, nodo)

        entorno.definir_variable(
            nodo.nombre, valor,
            constante=nodo.constante,
            tipo=nodo.tipo,
            linea=nodo.linea, columna=nodo.columna,
        )

    def verificar_tipo(self, valor, tipo, nodo):
        mapa = {
            "numero":  self.es_numero,
            "texto":   self.es_texto,
            "logico":  self.es_logico,
            "lista":   lambda v: isinstance(v, list),
            "mapa":    lambda v: isinstance(v, dict),
            "funcion": callable,
        }
        if tipo not in mapa:
            raise ErrorTipo(
                f"tipo desconocido: '{tipo}'. "
                f"los tipos válidos son: numero, texto, logico, lista, mapa, funcion.",
                nodo.linea, nodo.columna,
            )
        if not mapa[tipo](valor):
            raise ErrorTipo(
                f"esperaba un {tipo}, pero recibí {self.tipo_de(valor)}.",
                nodo.linea, nodo.columna,
            )

    def ej_asignacion(self, nodo, entorno):
        valor = self.evaluar(nodo.valor, entorno)
        destino = nodo.destino

        if isinstance(destino, ast.Identificador):
            entorno.asignar_variable(destino.nombre, valor,
                                     destino.linea, destino.columna)
            return

        if isinstance(destino, ast.Indice):
            contenedor = self.evaluar(destino.objeto, entorno)
            indice = self.evaluar(destino.indice, entorno)
            if not isinstance(contenedor, (list, dict)):
                raise ErrorTipo(
                    f"solo puedes indexar listas o mapas, "
                    f"pero recibí {self.tipo_de(contenedor)}.",
                    nodo.linea, nodo.columna,
                )
            try:
                contenedor[indice] = valor
            except (IndexError, KeyError):
                raise ErrorValor(
                    f"el índice {indice!r} no existe en el contenedor.",
                    nodo.linea, nodo.columna,
                )
            return

        if isinstance(destino, ast.Acceso):
            objeto = self.evaluar(destino.objeto, entorno)
            if isinstance(objeto, dict) and "__campos__" in objeto:
                objeto["__campos__"][destino.nombre] = valor
                return
            if isinstance(objeto, dict):
                objeto[destino.nombre] = valor
                return
            raise ErrorTipo(
                f"solo puedes asignar a campos de objetos o mapas, "
                f"pero recibí {self.tipo_de(objeto)}.",
                nodo.linea, nodo.columna,
            )

        raise ErrorEjecucion(
            "no puedes asignar a esa expresión.",
            nodo.linea, nodo.columna,
        )

    def ej_escribir(self, nodo, entorno):
        partes = [self.a_texto(self.evaluar(v, entorno)) for v in nodo.valores]
        print("".join(partes))

    def ej_leer(self, nodo, entorno):
        try:
            linea = input()
        except EOFError:
            linea = ""
        destino = nodo.destino
        if isinstance(destino, ast.Identificador):
            if entorno.existe_variable(destino.nombre):
                entorno.asignar_variable(destino.nombre, linea,
                                         destino.linea, destino.columna)
            else:
                entorno.definir_variable(destino.nombre, linea,
                                         linea=destino.linea,
                                         columna=destino.columna)
            return
        raise ErrorEjecucion(
            "'leer' necesita una variable simple.",
            nodo.linea, nodo.columna,
        )

    def ej_retornar(self, nodo, entorno):
        valor = None
        if nodo.valor is not None:
            valor = self.evaluar(nodo.valor, entorno)
        raise _Retorno(valor)

    def ej_lanzar(self, nodo, entorno):
        valor = self.evaluar(nodo.valor, entorno)
        raise ErrorEjecucion(
            self.a_texto(valor),
            nodo.linea, nodo.columna,
        )

    # ---------- evaluación ----------

    def evaluar(self, nodo, entorno):
        if isinstance(nodo, ast.Numero):
            return nodo.valor
        if isinstance(nodo, ast.Texto):
            return nodo.valor
        if isinstance(nodo, ast.Booleano):
            return nodo.valor
        if isinstance(nodo, ast.Nulo):
            return None
        if isinstance(nodo, ast.Identificador):
            return self.ev_identificador(nodo, entorno)
        if isinstance(nodo, ast.Binaria):
            return self.ev_binaria(nodo, entorno)
        if isinstance(nodo, ast.Unaria):
            return self.ev_unaria(nodo, entorno)
        if isinstance(nodo, ast.Lista):
            return [self.evaluar(e, entorno) for e in nodo.elementos]
        if isinstance(nodo, ast.Mapa):
            return {
                self.evaluar(k, entorno): self.evaluar(v, entorno)
                for k, v in nodo.pares
            }
        if isinstance(nodo, ast.Indice):
            return self.ev_indice(nodo, entorno)
        if isinstance(nodo, ast.Acceso):
            return self.ev_acceso(nodo, entorno)
        if isinstance(nodo, ast.Llamada):
            return self.ev_llamada(nodo, entorno)
        if isinstance(nodo, ast.UsarPatron):
            return self.ev_usar_patron(nodo, entorno)
        if isinstance(nodo, ast.LlamadaMetodo):
            return self.ev_metodo(nodo, entorno)
        if isinstance(nodo, ast.Nuevo):
            return self.ev_nuevo(nodo, entorno)
        if isinstance(nodo, ast.Esto):
            return entorno.obtener_variable("esto", nodo.linea, nodo.columna)

        raise ErrorEjecucion(
            f"no sé evaluar '{type(nodo).__name__}'.",
            nodo.linea, nodo.columna,
        )

    def ev_identificador(self, nodo, entorno):
        if entorno.existe_variable(nodo.nombre):
            return entorno.obtener_variable(nodo.nombre, nodo.linea, nodo.columna)

        if self._es_callable(nodo.nombre, entorno):
            return Callable(self, nodo.nombre, entorno)

        raise ErrorNombre(
            f"la variable '{nodo.nombre}' no existe. "
            f"¿la declaraste antes de usarla?",
            nodo.linea, nodo.columna,
        )

    def _es_callable(self, nombre, entorno):
        if nombre in NATIVAS:
            return True
        e = entorno
        while e is not None:
            if nombre in e.funciones or nombre in e.patrones:
                return True
            e = e.padre
        return False

    # ---------- operadores ----------

    def ev_binaria(self, nodo, entorno):
        op = nodo.op

        if op == "y":
            izq = self.evaluar(nodo.izq, entorno)
            self.exigir_logico(izq, nodo, "'y'")
            if not izq:
                return False
            der = self.evaluar(nodo.der, entorno)
            self.exigir_logico(der, nodo, "'y'")
            return der

        if op == "o":
            izq = self.evaluar(nodo.izq, entorno)
            self.exigir_logico(izq, nodo, "'o'")
            if izq:
                return True
            der = self.evaluar(nodo.der, entorno)
            self.exigir_logico(der, nodo, "'o'")
            return der

        izq = self.evaluar(nodo.izq, entorno)
        der = self.evaluar(nodo.der, entorno)

        if op == "+":
            return self.sumar(izq, der, nodo)
        if op == "-":
            return self.op_num(izq, der, op, nodo)
        if op == "*":
            return self.op_num(izq, der, op, nodo)
        if op == "/":
            if self.es_numero(der) and der == 0:
                raise ErrorValor(
                    "no se puede dividir entre cero. "
                    "verifica el divisor antes de dividir.",
                    nodo.linea, nodo.columna,
                )
            return self.op_num(izq, der, op, nodo)
        if op == "**":
            return self.op_num(izq, der, op, nodo)
        if op == "residuo":
            if self.es_numero(der) and der == 0:
                raise ErrorValor(
                    "no se puede calcular el residuo entre cero. "
                    "verifica el divisor antes de calcular.",
                    nodo.linea, nodo.columna,
                )
            return self.op_num(izq, der, op, nodo)
        if op in ("==", "!="):
            if isinstance(izq, bool) != isinstance(der, bool):
                return (op == "!=")
            return (izq == der) if op == "==" else (izq != der)
        if op in ("<", "<=", ">", ">="):
            return self.comparar(izq, der, op, nodo)

        raise ErrorEjecucion(
            f"operador desconocido: '{op}'.",
            nodo.linea, nodo.columna,
        )

    def ev_unaria(self, nodo, entorno):
        valor = self.evaluar(nodo.valor, entorno)
        if nodo.op == "no":
            self.exigir_logico(valor, nodo, "'no'")
            return not valor
        if nodo.op == "-":
            self.exigir_numero(valor, nodo, "'-'")
            return -valor
        if nodo.op == "+":
            self.exigir_numero(valor, nodo, "'+'")
            return valor
        raise ErrorEjecucion(
            f"operador unario desconocido: '{nodo.op}'.",
            nodo.linea, nodo.columna,
        )

    def ev_indice(self, nodo, entorno):
        contenedor = self.evaluar(nodo.objeto, entorno)
        indice = self.evaluar(nodo.indice, entorno)
        try:
            return contenedor[indice]
        except (IndexError, KeyError):
            raise ErrorValor(
                f"el índice {indice!r} no existe.",
                nodo.linea, nodo.columna,
            )
        except TypeError:
            raise ErrorTipo(
                f"no puedes indexar {self.tipo_de(contenedor)}.",
                nodo.linea, nodo.columna,
            )

    def ev_acceso(self, nodo, entorno):
        objeto = self.evaluar(nodo.objeto, entorno)

        if isinstance(objeto, dict) and "__campos__" in objeto:
            if nodo.nombre not in objeto["__campos__"]:
                raise ErrorNombre(
                    f"el campo '{nodo.nombre}' no existe en el objeto "
                    f"de la clase '{objeto['__clase__']}'.",
                    nodo.linea, nodo.columna,
                )
            return objeto["__campos__"][nodo.nombre]

        if isinstance(objeto, dict):
            if nodo.nombre not in objeto:
                raise ErrorNombre(
                    f"la clave '{nodo.nombre}' no existe en el mapa.",
                    nodo.linea, nodo.columna,
                )
            return objeto[nodo.nombre]

        raise ErrorTipo(
            f"solo puedes acceder a campos de objetos o mapas, "
            f"pero recibí {self.tipo_de(objeto)}.",
            nodo.linea, nodo.columna,
        )

    # ---------- llamadas ----------

    def ev_llamada(self, nodo, entorno):
        funcion = self._buscar_funcion(nodo.nombre, entorno)
        if funcion is not None:
            args = [self.evaluar(a, entorno) for a in nodo.argumentos]
            return self.llamar_funcion(funcion, args, nodo, entorno)

        if nodo.nombre in NATIVAS:
            return self.llamar_nativa(nodo, entorno)

        raise ErrorNombre(
            f"la función '{nodo.nombre}' no existe. "
            f"¿la definiste antes de llamarla?",
            nodo.linea, nodo.columna,
        )

    def _buscar_funcion(self, nombre, entorno):
        e = entorno
        while e is not None:
            if nombre in e.funciones:
                return e.funciones[nombre]
            e = e.padre
        return None

    def llamar_nativa(self, nodo, entorno):
        args = [self.evaluar(a, entorno) for a in nodo.argumentos]
        return self._aplicar_nativa(nodo.nombre, args, nodo)

    def _aplicar_nativa(self, nombre, args, nodo):
        fn = NATIVAS[nombre]
        try:
            return fn(*args)
        except ErrorEspa:
            raise
        except TypeError as e:
            raise ErrorValor(
                f"la función nativa '{nombre}' recibió mal sus argumentos: {e}",
                nodo.linea, nodo.columna,
            )
        except Exception as e:
            raise ErrorEjecucion(
                f"error en la función nativa '{nombre}': {e}",
                nodo.linea, nodo.columna,
            )

    def llamar_por_nombre(self, nombre, args, entorno, nodo):
        if nombre in NATIVAS:
            return self._aplicar_nativa(nombre, args, nodo)

        e = entorno
        while e is not None:
            if nombre in e.funciones:
                return self.llamar_funcion(e.funciones[nombre], args, nodo, entorno)
            if nombre in e.patrones:
                return self.usar_patron(e.patrones[nombre], args, nodo, entorno)
            e = e.padre

        raise ErrorNombre(
            f"la función '{nombre}' no existe.",
            nodo.linea, nodo.columna,
        )

    def llamar_funcion(self, funcion, args, nodo_llamada, entorno_llamador):
        if len(args) != len(funcion.parametros):
            raise ErrorValor(
                f"la función '{funcion.nombre}' espera "
                f"{len(funcion.parametros)} argumento(s), "
                f"pero recibí {len(args)}.",
                nodo_llamada.linea, nodo_llamada.columna,
            )
        local = entorno_llamador.hijo(nombre=funcion.nombre)
        for nombre, valor in zip(funcion.parametros, args):
            local.definir_variable(nombre, valor)
        try:
            for sent in funcion.cuerpo:
                self.ejecutar_nodo(sent, local)
        except _Retorno as r:
            return r.valor
        return None

    # ---------- patrones ----------

    def ev_usar_patron(self, nodo, entorno):
        patron = entorno.obtener_patron(nodo.nombre, nodo.linea, nodo.columna)
        args = [self.evaluar(a, entorno) for a in nodo.argumentos]
        return self.usar_patron(patron, args, nodo, entorno)

    def usar_patron(self, patron, args, nodo_uso, entorno_usador):
        if len(args) != len(patron.parametros):
            raise ErrorValor(
                f"el patrón '{patron.nombre}' espera "
                f"{len(patron.parametros)} argumento(s), "
                f"pero recibí {len(args)}.",
                nodo_uso.linea, nodo_uso.columna,
            )
        local = entorno_usador.hijo(nombre=f"patron {patron.nombre}")
        for nombre, valor in zip(patron.parametros, args):
            local.definir_variable(nombre, valor)
        try:
            for sent in patron.cuerpo:
                self.ejecutar_nodo(sent, local)
        except _Retorno as r:
            return r.valor
        return None

    # ---------- objetos ----------

    def ev_nuevo(self, nodo, entorno):
        clase = entorno.obtener_clase(nodo.clase, nodo.linea, nodo.columna)
        args = [self.evaluar(a, entorno) for a in nodo.argumentos]
        objeto = {
            "__clase__": nodo.clase,
            "__campos__": {},
        }
        constructor = self.buscar_metodo(clase, "iniciar")
        if constructor is not None:
            self.llamar_metodo(objeto, constructor, args, nodo, entorno)
        elif args:
            raise ErrorValor(
                f"la clase '{nodo.clase}' no tiene un método 'iniciar' "
                f"que reciba argumentos.",
                nodo.linea, nodo.columna,
            )
        return objeto

    def ev_metodo(self, nodo, entorno):
        objeto = self.evaluar(nodo.objeto, entorno)
        if not isinstance(objeto, dict) or "__clase__" not in objeto:
            raise ErrorTipo(
                f"solo puedes llamar métodos de objetos, "
                f"pero recibí {self.tipo_de(objeto)}.",
                nodo.linea, nodo.columna,
            )
        clase = entorno.obtener_clase(objeto["__clase__"],
                                      nodo.linea, nodo.columna)
        metodo = self.buscar_metodo(clase, nodo.metodo)
        if metodo is None:
            raise ErrorNombre(
                f"el método '{nodo.metodo}' no existe en la clase "
                f"'{objeto['__clase__']}'.",
                nodo.linea, nodo.columna,
            )
        args = [self.evaluar(a, entorno) for a in nodo.argumentos]
        return self.llamar_metodo(objeto, metodo, args, nodo, entorno)

    def buscar_metodo(self, clase, nombre):
        while clase is not None:
            for item in clase.cuerpo:
                if isinstance(item, ast.Funcion) and item.nombre == nombre:
                    return item
            if clase.base:
                clase = self.global_.obtener_clase(clase.base)
            else:
                clase = None
        return None

    def llamar_metodo(self, objeto, metodo, args, nodo_llamada, entorno):
        if len(args) != len(metodo.parametros):
            raise ErrorValor(
                f"el método '{metodo.nombre}' espera "
                f"{len(metodo.parametros)} argumento(s), "
                f"pero recibí {len(args)}.",
                nodo_llamada.linea, nodo_llamada.columna,
            )
        local = entorno.hijo(nombre=f"{objeto['__clase__']}.{metodo.nombre}")
        local.definir_variable("esto", objeto)
        for nombre, valor in zip(metodo.parametros, args):
            local.definir_variable(nombre, valor)
        try:
            for sent in metodo.cuerpo:
                self.ejecutar_nodo(sent, local)
        except _Retorno as r:
            return r.valor
        return None

    # ---------- bloques ----------

    def ejecutar_bloque(self, nodo, entorno):
        if isinstance(nodo, ast.Si):
            return self.bloque_si(nodo, entorno)
        if isinstance(nodo, ast.Segun):
            return self.bloque_segun(nodo, entorno)
        if isinstance(nodo, ast.Mientras):
            return self.bloque_mientras(nodo, entorno)
        if isinstance(nodo, ast.ParaCada):
            return self.bloque_para(nodo, entorno)
        if isinstance(nodo, ast.ParaNumerico):
            return self.bloque_para_numerico(nodo, entorno)
        if isinstance(nodo, ast.Intentar):
            return self.bloque_intentar(nodo, entorno)
        raise ErrorEjecucion(
            f"bloque desconocido: '{type(nodo).__name__}'.",
            nodo.linea, nodo.columna,
        )

    def bloque_si(self, nodo, entorno):
        cond = self.evaluar(nodo.condicion, entorno)
        self.exigir_logico(cond, nodo, "'si'")
        rama = nodo.entonces if cond else nodo.sino
        local = entorno.hijo(nombre="si")
        for sent in rama:
            self.ejecutar_nodo(sent, local)

    def bloque_segun(self, nodo, entorno):
        valor = self.evaluar(nodo.valor, entorno)
        local = entorno.hijo(nombre="segun")
        for caso_valor, cuerpo in nodo.casos:
            if self.evaluar(caso_valor, entorno) == valor:
                for sent in cuerpo:
                    self.ejecutar_nodo(sent, local)
                return
        for sent in nodo.defecto:
            self.ejecutar_nodo(sent, local)

    def bloque_mientras(self, nodo, entorno):
        while True:
            cond = self.evaluar(nodo.condicion, entorno)
            self.exigir_logico(cond, nodo, "'mientras'")
            if not cond:
                break
            local = entorno.hijo(nombre="mientras")
            try:
                for sent in nodo.cuerpo:
                    self.ejecutar_nodo(sent, local)
            except _Romper:
                break
            except _Saltar:
                continue

    def bloque_para(self, nodo, entorno):
        coleccion = self.evaluar(nodo.coleccion, entorno)
        if not isinstance(coleccion, (list, dict, str)):
            raise ErrorTipo(
                f"'para cada' necesita una lista, un mapa o un texto, "
                f"pero recibí {self.tipo_de(coleccion)}.",
                nodo.linea, nodo.columna,
            )
        iterable = coleccion.keys() if isinstance(coleccion, dict) else coleccion
        for item in iterable:
            local = entorno.hijo(nombre="para")
            local.definir_variable(nodo.variable, item)
            try:
                for sent in nodo.cuerpo:
                    self.ejecutar_nodo(sent, local)
            except _Romper:
                break
            except _Saltar:
                continue

    def bloque_para_numerico(self, nodo, entorno):
        inicio = self.evaluar(nodo.inicio, entorno)
        fin = self.evaluar(nodo.fin, entorno)
        self.exigir_numero(inicio, nodo, "'para desde'")
        self.exigir_numero(fin, nodo, "'para hasta'")

        if nodo.paso is not None:
            paso = self.evaluar(nodo.paso, entorno)
            self.exigir_numero(paso, nodo, "'para paso'")
            if paso == 0:
                raise ErrorValor(
                    "el paso no puede ser cero.",
                    nodo.linea, nodo.columna,
                )
        else:
            paso = 1

        i = inicio
        while True:
            if paso > 0 and i > fin:
                break
            if paso < 0 and i < fin:
                break

            local = entorno.hijo(nombre=f"para {nodo.variable}")
            local.definir_variable(nodo.variable, i)

            try:
                for sent in nodo.cuerpo:
                    self.ejecutar_nodo(sent, local)
            except _Romper:
                break
            except _Saltar:
                pass

            i = i + paso

    def bloque_intentar(self, nodo, entorno):
        local = entorno.hijo(nombre="intentar")
        try:
            for sent in nodo.cuerpo:
                self.ejecutar_nodo(sent, local)
        except ErrorEjecucion as e:
            if not nodo.captura:
                raise
            if local.existe_variable(nodo.nombre_error):
                local.asignar_variable(nodo.nombre_error, str(e),
                                       nodo.linea, nodo.columna)
            else:
                local.definir_variable(nodo.nombre_error, str(e))
            for sent in nodo.captura:
                self.ejecutar_nodo(sent, local)
        finally:
            if nodo.finalmente:
                for sent in nodo.finalmente:
                    self.ejecutar_nodo(sent, local)

    # ---------- auxiliares ----------

    def es_numero(self, x):
        return isinstance(x, (int, float)) and not isinstance(x, bool)

    def es_texto(self, x):
        return isinstance(x, str)

    def es_logico(self, x):
        return isinstance(x, bool)

    def tipo_de(self, x):
        if x is None:
            return "nulo"
        if isinstance(x, bool):
            return "lógico"
        if isinstance(x, (int, float)):
            return "número"
        if isinstance(x, str):
            return "texto"
        if isinstance(x, list):
            return "lista"
        if isinstance(x, dict):
            return "mapa"
        if isinstance(x, Callable):
            return "función"
        return type(x).__name__

    def exigir_numero(self, x, nodo, contexto):
        if not self.es_numero(x):
            raise ErrorTipo(
                f"{contexto} necesita números, pero recibí {self.tipo_de(x)}.",
                nodo.linea, nodo.columna,
            )

    def exigir_logico(self, x, nodo, contexto):
        if not self.es_logico(x):
            raise ErrorLogico(
                f"{contexto} necesita valores lógicos (verdadero o falso), "
                f"pero recibí {self.tipo_de(x)}.",
                nodo.linea, nodo.columna,
            )

    def sumar(self, izq, der, nodo):
        if self.es_numero(izq) and self.es_numero(der):
            return izq + der
        if self.es_texto(izq) and self.es_texto(der):
            return izq + der
        if isinstance(izq, list) and isinstance(der, list):
            return izq + der
        if self.es_texto(izq) or self.es_texto(der):
            raise ErrorTipo(
                "no puedes sumar texto con número. "
                "convierte el número a texto o el texto a número primero.",
                nodo.linea, nodo.columna,
            )
        raise ErrorTipo(
            f"no puedes sumar {self.tipo_de(izq)} con {self.tipo_de(der)}.",
            nodo.linea, nodo.columna,
        )

    def op_num(self, izq, der, op, nodo):
        self.exigir_numero(izq, nodo, f"'{op}'")
        self.exigir_numero(der, nodo, f"'{op}'")
        if op == "-":
            return izq - der
        if op == "*":
            return izq * der
        if op == "/":
            return izq / der
        if op == "**":
            return izq ** der
        if op == "residuo":
            return izq % der
        raise ErrorEjecucion(
            f"operador numérico desconocido: '{op}'.",
            nodo.linea, nodo.columna,
        )

    def comparar(self, izq, der, op, nodo):
        if self.es_numero(izq) and self.es_numero(der):
            pass
        elif self.es_texto(izq) and self.es_texto(der):
            pass
        else:
            raise ErrorTipo(
                f"no puedes comparar {self.tipo_de(izq)} con {self.tipo_de(der)}.",
                nodo.linea, nodo.columna,
            )
        if op == "<":
            return izq < der
        if op == "<=":
            return izq <= der
        if op == ">":
            return izq > der
        if op == ">=":
            return izq >= der
        raise ErrorEjecucion(
            f"comparador desconocido: '{op}'.",
            nodo.linea, nodo.columna,
        )

    def a_texto(self, x):
        if x is None:
            return "nulo"
        if isinstance(x, bool):
            return "verdadero" if x else "falso"
        if isinstance(x, Callable):
            return repr(x)
        if isinstance(x, int):
            return str(x)
        if isinstance(x, float):
            if x.is_integer():
                return str(int(x))
            texto = f"{x:.10f}".rstrip("0").rstrip(".")
            return texto
        if isinstance(x, str):
            return x
        if isinstance(x, list):
            return "[" + ", ".join(self.a_texto(e) for e in x) + "]"
        if isinstance(x, dict) and "__campos__" in x:
            partes = [f"{k}: {self.a_texto(v)}"
                      for k, v in x["__campos__"].items()]
            return f"{x['__clase__']}{{" + ", ".join(partes) + "}"
        if isinstance(x, dict):
            return "{" + ", ".join(
                f"{self.a_texto(k)}: {self.a_texto(v)}" for k, v in x.items()
            ) + "}"
        return str(x)