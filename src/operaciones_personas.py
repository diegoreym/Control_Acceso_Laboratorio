from persona import Persona

def _normalizar_codigo(codigo: str) -> str:
    """Acepta letras y números, sin espacios interiores ni signos."""
    if not isinstance(codigo, str):
        raise ValueError("El código de la persona debe ser un texto no vacío.")

    codigo = codigo.strip().upper()
    if not codigo or not codigo.isalnum():
        raise ValueError("El código de la persona debe contener solo letras y números sin espacios interiores.")
    return codigo

def _validar_texto(texto: str, campo: str) -> str:
    if not isinstance(texto, str) or not texto.strip():
        raise ValueError(f"{campo} deben ser un texto no vacío.")
    return texto.strip()


def registrar_persona(personas: dict[str, Persona], codigo: str, apellidos: str, nombres: str) -> None:
    """Registra una persona nueva sin sobrescribir claves existentes."""
    codigo = _normalizar_codigo(codigo)
    if codigo in personas:
        raise ValueError(f"La persona con código {codigo} ya está registrada.")

    apellidos = _validar_texto(apellidos, "Los apellidos")
    nombres = _validar_texto(nombres, "Los nombres")
    personas[codigo] = Persona(codigo, apellidos, nombres)


def buscar_persona(personas: dict[str, Persona], codigo: str) -> Persona:
    """Devuelve el objeto registrado o informa que la clave no existe."""
    codigo = _normalizar_codigo(codigo)
    if codigo not in personas:
        raise KeyError(f"La persona con código {codigo} no está registrada.")
    return personas[codigo]


def existe_persona(personas: dict[str, Persona], codigo: str) -> bool:
    """Consulta pertenencia; un código mal formado produce ValueError."""
    return _normalizar_codigo(codigo) in personas


def modificar_persona(personas: dict[str, Persona], codigo: str, apellidos: str, nombres: str) -> None:
    """Valida ambos datos antes de actualizar el mismo objeto y sus permisos."""
    persona = buscar_persona(personas, codigo)
    apellidos = _validar_texto(apellidos, "Los apellidos")
    nombres = _validar_texto(nombres, "Los nombres")

    persona.apellidos = apellidos
    persona.nombres = nombres


def eliminar_persona(personas: dict[str, Persona], codigo: str) -> None:
    """Elimina únicamente la asociación indicada; falla si no existe."""
    codigo = _normalizar_codigo(codigo)
    if codigo not in personas:
        raise KeyError(f"La persona con código {codigo} no está registrada.")
    del personas[codigo]


def listar_personas(personas: dict[str, Persona]) -> list[Persona]:
    """Retornar valores del diccionario personas"""
    return list(personas.values())
