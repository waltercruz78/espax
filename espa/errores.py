# espa/errores.py


class ErrorEspa(Exception):
    """Base de todos los errores de Espa+.

    Siempre lleva línea y columna para que el mensaje enseñe
    exactamente dónde pasó.
    """

    def __init__(self, mensaje, linea=0, columna=0):
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.linea = linea
        self.columna = columna

    def ubicacion(self):
        if self.linea > 0:
            return f"línea {self.linea}, columna {self.columna}: "
        return ""

    def __str__(self):
        return f"{self.ubicacion()}{self.mensaje}"


class ErrorLexico(ErrorEspa):
    pass


class ErrorSintaxis(ErrorEspa):
    pass


class ErrorEjecucion(ErrorEspa):
    pass


class ErrorNombre(ErrorEjecucion):
    pass


class ErrorTipo(ErrorEjecucion):
    pass


class ErrorValor(ErrorEjecucion):
    pass


class ErrorLogico(ErrorEjecucion):
    pass


class ErrorControl(ErrorEjecucion):
    pass