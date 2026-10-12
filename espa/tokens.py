# espa/tokens.py

from dataclasses import dataclass

# Tipos de token que existen en Espa+
PALABRA       = "PALABRA"
IDENT         = "IDENT"
NUMERO        = "NUMERO"
TEXTO         = "TEXTO"
OPERADOR      = "OPERADOR"
PAREN_IZQ     = "PAREN_IZQ"
PAREN_DER     = "PAREN_DER"
COMA          = "COMA"
DOS_PUNTOS    = "DOS_PUNTOS"
PUNTO         = "PUNTO"
CORCHETE_IZQ  = "CORCHETE_IZQ"
CORCHETE_DER  = "CORCHETE_DER"
LLAVE_IZQ     = "LLAVE_IZQ"
LLAVE_DER     = "LLAVE_DER"
FIN_LINEA     = "FIN_LINEA"
FIN_ARCHIVO   = "FIN_ARCHIVO"


@dataclass
class Token:
    tipo: str
    valor: str
    linea: int
    columna: int

    def __repr__(self):
        return f"Token({self.tipo}, {self.valor!r}, L{self.linea}:C{self.columna})"