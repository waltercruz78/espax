# espa/entorno.py

from espa.errores import ErrorNombre, ErrorValor


class Entorno:
    def __init__(self, padre=None, nombre=""):
        self.padre = padre
        self.nombre = nombre
        self.variables = {}
        self.funciones = {}
        self.patrones = {}
        self.clases = {}

    def hijo(self, nombre=""):
        return Entorno(padre=self, nombre=nombre)

    def absorber(self, otro):
        """Copia las definiciones de otro entorno a este.

        Si un nombre ya existe en este entorno, se conserva el actual.
        Así el archivo que importa puede sobrescribir lo importado.
        """
        for nombre, info in otro.variables.items():
            if nombre not in self.variables:
                self.variables[nombre] = info
        for nombre, nodo in otro.funciones.items():
            if nombre not in self.funciones:
                self.funciones[nombre] = nodo
        for nombre, nodo in otro.patrones.items():
            if nombre not in self.patrones:
                self.patrones[nombre] = nodo
        for nombre, nodo in otro.clases.items():
            if nombre not in self.clases:
                self.clases[nombre] = nodo

    # ---------- variables ----------

    def definir_variable(self, nombre, valor, constante=False, tipo=None,
                         linea=0, columna=0):
        if nombre in self.variables:
            raise ErrorNombre(
                f"la variable '{nombre}' ya existe en este bloque. "
                f"elige otro nombre o asígnala sin 'variable'.",
                linea, columna,
            )
        self.variables[nombre] = {
            "valor": valor,
            "constante": constante,
            "tipo": tipo,
        }

    def obtener_variable(self, nombre, linea=0, columna=0):
        entorno = self.buscar(nombre)
        if entorno is None:
            raise ErrorNombre(
                f"la variable '{nombre}' no existe. "
                f"¿la declaraste antes de usarla?",
                linea, columna,
            )
        return entorno.variables[nombre]["valor"]

    def asignar_variable(self, nombre, valor, linea=0, columna=0):
        entorno = self.buscar(nombre)
        if entorno is None:
            raise ErrorNombre(
                f"la variable '{nombre}' no existe. "
                f"declárala con 'variable {nombre} = ...' primero.",
                linea, columna,
            )
        info = entorno.variables[nombre]
        if info["constante"]:
            raise ErrorValor(
                f"'{nombre}' es una constante y no se puede cambiar. "
                f"si necesitas modificarla, usa 'variable' en su lugar.",
                linea, columna,
            )
        info["valor"] = valor

    def existe_variable(self, nombre):
        return self.buscar(nombre) is not None

    def buscar(self, nombre):
        entorno = self
        while entorno is not None:
            if nombre in entorno.variables:
                return entorno
            entorno = entorno.padre
        return None

    # ---------- funciones ----------

    def definir_funcion(self, nombre, nodo_funcion):
        if nombre in self.funciones:
            raise ErrorNombre(
                f"la función '{nombre}' ya existe. elige otro nombre.",
                nodo_funcion.linea, nodo_funcion.columna,
            )
        self.funciones[nombre] = nodo_funcion

    def obtener_funcion(self, nombre, linea=0, columna=0):
        entorno = self
        while entorno is not None:
            if nombre in entorno.funciones:
                return entorno.funciones[nombre]
            entorno = entorno.padre
        raise ErrorNombre(
            f"la función '{nombre}' no existe. "
            f"¿la definiste antes de llamarla?",
            linea, columna,
        )

    # ---------- patrones ----------

    def definir_patron(self, nombre, nodo_patron):
        if nombre in self.patrones:
            raise ErrorNombre(
                f"el patrón '{nombre}' ya existe. elige otro nombre.",
                nodo_patron.linea, nodo_patron.columna,
            )
        self.patrones[nombre] = nodo_patron

    def obtener_patron(self, nombre, linea=0, columna=0):
        entorno = self
        while entorno is not None:
            if nombre in entorno.patrones:
                return entorno.patrones[nombre]
            entorno = entorno.padre
        raise ErrorNombre(
            f"el patrón '{nombre}' no existe. "
            f"¿lo definiste antes de usarlo?",
            linea, columna,
        )

    # ---------- clases ----------

    def definir_clase(self, nombre, nodo_clase):
        if nombre in self.clases:
            raise ErrorNombre(
                f"la clase '{nombre}' ya existe. elige otro nombre.",
                nodo_clase.linea, nodo_clase.columna,
            )
        self.clases[nombre] = nodo_clase

    def obtener_clase(self, nombre, linea=0, columna=0):
        entorno = self
        while entorno is not None:
            if nombre in entorno.clases:
                return entorno.clases[nombre]
            entorno = entorno.padre
        raise ErrorNombre(
            f"la clase '{nombre}' no existe. "
            f"¿la definiste antes de usarla?",
            linea, columna,
        )