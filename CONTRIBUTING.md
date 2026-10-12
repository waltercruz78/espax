# Cómo contribuir a Espa+

¡Gracias por querer ayudar! Aquí te explico cómo.

---

## Formas de contribuir

| Tipo | Qué implica |
|---|---|
| **Reportar bugs** | Abrir un issue describiendo el problema |
| **Sugerir funciones** | Abrir un issue con la idea y por qué es útil |
| **Escribir código** | Pull request con mejoras al motor o la biblioteca |
| **Documentación** | Corregir el manual, añadir ejemplos |
| **Traducir** | Llevar Espa+ a otros idiomas |
| **Difundir** | Hablar de Espa+ en redes, foros, escuelas |

---

## Antes de escribir código

1. **Abre un issue** describiendo qué quieres hacer y por qué.
2. Espera respuesta. Así evitamos trabajo duplicado.
3. Si te dicen que sí, haz el cambio en una rama aparte.
4. Envía un pull request.

---

## Estilo del código

- **Nombres en español** para todo lo que el usuario ve.
- **Nombres en inglés** para variables internas (Python).
- **Comentarios en español**.
- **2 espacios** de indentación en archivos `.wal`.
- **4 espacios** en código Python.

---

## Estructura del proyecto

    espax/
    ├── corre                      # comando global
    ├── espa/                      # motor en Python
    │   ├── tokens.py
    │   ├── errores.py
    │   ├── lexer.py
    │   ├── ast.py
    │   ├── parser.py
    │   ├── entorno.py
    │   ├── nativas.py
    │   ├── interprete.py
    │   └── cli.py
    ├── ejemplos/                  # programas .wal
    ├── pruebas/                   # pruebas manuales
    ├── tests/                     # pruebas automáticas
    ├── docs/                      # documentación
    ├── pyproject.toml
    ├── README.md
    ├── CHANGELOG.md
    ├── CONTRIBUTING.md
    └── LICENSE

---

## Cómo probar tus cambios

**Instalar en modo desarrollo:**

```bash
pip install -e .
```

**Ejecutar las pruebas automáticas:**

```bash
python -m pytest tests/ -v
```

**Probar un archivo:**

```bash
corre ejemplos/hola.wal
```

**Abrir el REPL:**

```bash
corre
```

---

## Añadir una función nativa

1. Abre `espa/nativas.py`.
2. Escribe la función con validación de tipos:

```python
def n_mi_funcion(x):
    if not _num(x):
        raise ErrorTipo(f"mi_funcion espera un número, pero recibí {_tipo(x)}.")
    return x * 2
```

3. Añádela al diccionario `NATIVAS`:

```python
NATIVAS = {
    ...
    "mi_funcion": n_mi_funcion,
}
```

4. Añade una prueba en `tests/test_nativas.py`.
5. Documenta en `docs/manual.md`.

---

## Añadir una palabra clave

Es más trabajo. Toca 5 archivos:

1. `espa/lexer.py` — añadir la palabra a `PALABRAS`.
2. `espa/ast.py` — definir el nodo si es nuevo.
3. `espa/parser.py` — enseñarle a parsearlo.
4. `espa/interprete.py` — enseñarle a ejecutarlo.
5. `docs/manual.md` — documentarlo.

Abre un issue antes para discutir el diseño.

---

## Reglas de oro

1. **Todo en español** para lo que el usuario ve.
2. **Errores que enseñan** — cada mensaje explica qué pasó y cómo arreglarlo.
3. **Sin conflictos** — una palabra clave = un concepto.
4. **Sin huecos** — cada cambio incluye pruebas.
5. **Documentar** — si añades algo, documéntalo.

---

## Licencia

Al contribuir, aceptas que tu aporte se publique bajo la licencia MIT
del proyecto.