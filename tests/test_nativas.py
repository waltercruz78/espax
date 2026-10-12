# tests/test_nativas.py
import pytest
from espa.nativas import NATIVAS
from espa.errores import ErrorTipo, ErrorValor


def test_nativas_cargadas():
    assert len(NATIVAS) >= 70


# ---------- TEXTO ----------

def test_longitud_texto():
    assert NATIVAS["longitud"]("hola") == 4


def test_longitud_lista():
    assert NATIVAS["longitud"]([1, 2, 3]) == 3


def test_mayus():
    assert NATIVAS["mayus"]("hola") == "HOLA"


def test_minus():
    assert NATIVAS["minus"]("HOLA") == "hola"


def test_capitalizar():
    assert NATIVAS["capitalizar"]("hola mundo") == "Hola mundo"


def test_recortar():
    assert NATIVAS["recortar"]("  hola  ") == "hola"


def test_reemplazar():
    assert NATIVAS["reemplazar"]("hola mundo", "mundo", "sol") == "hola sol"


def test_contiene():
    assert NATIVAS["contiene"]("hola mundo", "mun") is True
    assert NATIVAS["contiene"]([1, 2, 3], 2) is True


def test_empieza():
    assert NATIVAS["empieza"]("hola", "ho") is True


def test_termina():
    assert NATIVAS["termina"]("hola", "la") is True


def test_separar():
    assert NATIVAS["separar"]("a b c", " ") == ["a", "b", "c"]


def test_unir():
    assert NATIVAS["unir"](["a", "b", "c"], "-") == "a-b-c"


def test_cortar():
    assert NATIVAS["cortar"]("hola mundo", 0, 4) == "hola"


def test_repetir_texto():
    assert NATIVAS["repetir_texto"]("ab", 3) == "ababab"


def test_al_reves():
    assert NATIVAS["al_reves"]("hola") == "aloh"
    assert NATIVAS["al_reves"]([1, 2, 3]) == [3, 2, 1]


def test_contar_palabras():
    assert NATIVAS["contar_palabras"]("hola cómo estás") == 3


def test_indice_texto():
    assert NATIVAS["indice_texto"]("hola mundo", "mundo") == 5


# ---------- NÚMEROS ----------

def test_absoluto():
    assert NATIVAS["absoluto"](-5) == 5


def test_signo():
    assert NATIVAS["signo"](-5) == -1
    assert NATIVAS["signo"](0) == 0
    assert NATIVAS["signo"](5) == 1


def test_redondear():
    assert NATIVAS["redondear"](3.7) == 4
    assert NATIVAS["redondear"](3.14159, 2) == 3.14


def test_techo():
    assert NATIVAS["techo"](3.2) == 4


def test_piso():
    assert NATIVAS["piso"](3.8) == 3


def test_raiz():
    assert NATIVAS["raiz"](25) == 5


def test_potencia():
    assert NATIVAS["potencia"](2, 10) == 1024


def test_maximo():
    assert NATIVAS["maximo"](3, 7, 2, 9) == 9
    assert NATIVAS["maximo"]([3, 7, 2, 9]) == 9


def test_minimo():
    assert NATIVAS["minimo"](3, 7, 2, 9) == 2


def test_suma():
    assert NATIVAS["suma"]([1, 2, 3, 4]) == 10


def test_promedio():
    assert NATIVAS["promedio"]([2, 4, 6]) == 4


def test_aleatorio():
    assert NATIVAS["aleatorio"](1, 1) == 1


def test_entre():
    assert NATIVAS["entre"](5, 1, 10) is True
    assert NATIVAS["entre"](15, 1, 10) is False


def test_es_primo():
    assert NATIVAS["es_primo"](17) is True
    assert NATIVAS["es_primo"](18) is False


def test_factorial():
    assert NATIVAS["factorial"](5) == 120
    assert NATIVAS["factorial"](0) == 1


def test_fibonacci():
    assert NATIVAS["fibonacci"](10) == 55


# ---------- LISTAS ----------

def test_ordenar():
    assert NATIVAS["ordenar"]([3, 1, 2]) == [1, 2, 3]


def test_invertir_lista():
    assert NATIVAS["invertir"]([1, 2, 3]) == [3, 2, 1]


def test_repetir():
    assert NATIVAS["repetir"]([1, 2], 3) == [1, 2, 1, 2, 1, 2]


def test_rango():
    assert NATIVAS["rango"](5) == [0, 1, 2, 3, 4]
    assert NATIVAS["rango"](1, 5) == [1, 2, 3, 4]
    assert NATIVAS["rango"](0, 10, 2) == [0, 2, 4, 6, 8]


def test_buscar():
    assert NATIVAS["buscar"]([1, 2, 3], 2) == 1
    assert NATIVAS["buscar"]([1, 2, 3], 99) == -1


def test_contar():
    assert NATIVAS["contar"]([1, 1, 2, 3, 1], 1) == 3


def test_indice():
    assert NATIVAS["indice"]([10, 20, 30], 1) == 20


def test_primeros():
    assert NATIVAS["primeros"]([1, 2, 3, 4, 5], 3) == [1, 2, 3]


def test_ultimos():
    assert NATIVAS["ultimos"]([1, 2, 3, 4, 5], 2) == [4, 5]


def test_unicos():
    assert NATIVAS["unicos"]([1, 1, 2, 3, 3, 4]) == [1, 2, 3, 4]


def test_vacio():
    assert NATIVAS["vacio"]([]) is True
    assert NATIVAS["vacio"]([1]) is False


def test_lleno():
    assert NATIVAS["lleno"]([1, 2]) is True
    assert NATIVAS["lleno"]([]) is False


def test_concatenar():
    assert NATIVAS["concatenar"]([1, 2], [3, 4]) == [1, 2, 3, 4]
    assert NATIVAS["concatenar"]("hola ", "mundo") == "hola mundo"


# ---------- CONVERSIÓN ----------

def test_a_texto():
    assert NATIVAS["a_texto"](5) == "5"
    assert NATIVAS["a_texto"](True) == "verdadero"
    assert NATIVAS["a_texto"](None) == "nulo"


def test_a_numero():
    assert NATIVAS["a_numero"]("42") == 42
    assert NATIVAS["a_numero"]("3.14") == 3.14


def test_a_logico():
    assert NATIVAS["a_logico"]("verdadero") is True
    assert NATIVAS["a_logico"]("no") is False
    assert NATIVAS["a_logico"](0) is False
    assert NATIVAS["a_logico"](1) is True


# ---------- SISTEMA ----------

def test_tipo():
    assert NATIVAS["tipo"](5) == "numero"
    assert NATIVAS["tipo"]("hola") == "texto"
    assert NATIVAS["tipo"](True) == "logico"
    assert NATIVAS["tipo"]([1]) == "lista"
    assert NATIVAS["tipo"](None) == "nulo"


def test_copiar():
    original = [1, 2, 3]
    copia = NATIVAS["copiar"](original)
    copia.append(4)
    assert original == [1, 2, 3]


def test_claves():
    assert NATIVAS["claves"]({"a": 1, "b": 2}) == ["a", "b"]


def test_valores():
    assert NATIVAS["valores"]({"a": 1, "b": 2}) == [1, 2]


# ---------- ERRORES ----------

def test_raiz_negativa():
    with pytest.raises(ErrorValor):
        NATIVAS["raiz"](-1)


def test_mayus_numero():
    with pytest.raises(ErrorTipo):
        NATIVAS["mayus"](5)


# ---------- CSV ----------

def test_separar_csv():
    texto = "a,b,c\n1,2,3"
    assert NATIVAS["separar_csv"](texto) == [["a", "b", "c"], [1, 2, 3]]


def test_unir_csv():
    filas = [["a", "b"], [1, 2]]
    assert NATIVAS["unir_csv"](filas) == "a,b\n1,2"