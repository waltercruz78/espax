# espa/ast.py

from dataclasses import dataclass, field
from typing import Any, List, Optional


@dataclass
class Nodo:
    linea: int = 0
    columna: int = 0


# ---------- programa ----------

@dataclass
class Programa(Nodo):
    nombre: str = ""
    cuerpo: List[Nodo] = field(default_factory=list)


@dataclass
class Paquete(Nodo):
    nombre: str = ""


@dataclass
class Importar(Nodo):
    nombre: str = ""


# ---------- declaraciones ----------

@dataclass
class Declaracion(Nodo):
    nombre: str = ""
    valor: Optional[Nodo] = None
    constante: bool = False
    tipo: Optional[str] = None


@dataclass
class Asignacion(Nodo):
    destino: Nodo = None
    valor: Nodo = None


# ---------- funciones y patrones ----------

@dataclass
class Funcion(Nodo):
    nombre: str = ""
    parametros: List[str] = field(default_factory=list)
    cuerpo: List[Nodo] = field(default_factory=list)


@dataclass
class Patron(Nodo):
    nombre: str = ""
    parametros: List[str] = field(default_factory=list)
    cuerpo: List[Nodo] = field(default_factory=list)


@dataclass
class Llamada(Nodo):
    nombre: str = ""
    argumentos: List[Nodo] = field(default_factory=list)


@dataclass
class UsarPatron(Nodo):
    nombre: str = ""
    argumentos: List[Nodo] = field(default_factory=list)


@dataclass
class LlamadaMetodo(Nodo):
    objeto: Nodo = None
    metodo: str = ""
    argumentos: List[Nodo] = field(default_factory=list)


@dataclass
class Retornar(Nodo):
    valor: Optional[Nodo] = None


# ---------- control ----------

@dataclass
class Si(Nodo):
    condicion: Nodo = None
    entonces: List[Nodo] = field(default_factory=list)
    sino: List[Nodo] = field(default_factory=list)


@dataclass
class Segun(Nodo):
    valor: Nodo = None
    casos: List[Any] = field(default_factory=list)
    defecto: List[Nodo] = field(default_factory=list)


@dataclass
class Mientras(Nodo):
    condicion: Nodo = None
    cuerpo: List[Nodo] = field(default_factory=list)


@dataclass
class ParaCada(Nodo):
    variable: str = ""
    coleccion: Nodo = None
    cuerpo: List[Nodo] = field(default_factory=list)


@dataclass
class ParaNumerico(Nodo):
    variable: str = ""
    inicio: Nodo = None
    fin: Nodo = None
    paso: Optional[Nodo] = None
    cuerpo: List[Nodo] = field(default_factory=list)


@dataclass
class Romper(Nodo):
    pass


@dataclass
class Saltar(Nodo):
    pass


# ---------- entrada/salida ----------

@dataclass
class Escribir(Nodo):
    valores: List[Nodo] = field(default_factory=list)


@dataclass
class Leer(Nodo):
    destino: Nodo = None


# ---------- errores ----------

@dataclass
class Intentar(Nodo):
    cuerpo: List[Nodo] = field(default_factory=list)
    nombre_error: str = ""
    captura: List[Nodo] = field(default_factory=list)
    finalmente: List[Nodo] = field(default_factory=list)


@dataclass
class Lanzar(Nodo):
    valor: Nodo = None


# ---------- objetos ----------

@dataclass
class Clase(Nodo):
    nombre: str = ""
    base: Optional[str] = None
    cuerpo: List[Nodo] = field(default_factory=list)


@dataclass
class Nuevo(Nodo):
    clase: str = ""
    argumentos: List[Nodo] = field(default_factory=list)


@dataclass
class Esto(Nodo):
    pass


# ---------- expresiones ----------

@dataclass
class Binaria(Nodo):
    izq: Nodo = None
    op: str = ""
    der: Nodo = None


@dataclass
class Unaria(Nodo):
    op: str = ""
    valor: Nodo = None


@dataclass
class Identificador(Nodo):
    nombre: str = ""


@dataclass
class Numero(Nodo):
    valor: float = 0


@dataclass
class Texto(Nodo):
    valor: str = ""


@dataclass
class Booleano(Nodo):
    valor: bool = False


@dataclass
class Nulo(Nodo):
    pass


@dataclass
class Lista(Nodo):
    elementos: List[Nodo] = field(default_factory=list)


@dataclass
class Mapa(Nodo):
    pares: List[tuple] = field(default_factory=list)


@dataclass
class Indice(Nodo):
    objeto: Nodo = None
    indice: Nodo = None


@dataclass
class Acceso(Nodo):
    objeto: Nodo = None
    nombre: str = ""