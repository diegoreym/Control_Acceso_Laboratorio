from persona import Persona
from laboratorio import Laboratorio

def autorizar_laboratorio(personas: dict[str, Persona], laboratorios: dict[str, Laboratorio], cod_persona: str, cod_lab: str) -> None:
    if cod_persona not in personas:
        raise KeyError(f"La persona con código {cod_persona} no está registrada.")
    if cod_lab not in laboratorios:
        raise KeyError(f"El laboratorio con código {cod_lab} no está registrado.")

    persona = personas[cod_persona]

    if persona.tiene_laboratorio(cod_lab):
        raise ValueError(f"La persona {cod_persona} ya cuenta con autorización para {cod_lab}.")

    persona.agregar_laboratorio(cod_lab)


def revocar_autorizacion(personas: dict[str, Persona], laboratorios: dict[str, Laboratorio], cod_persona: str, cod_lab: str) -> None:
    if cod_persona not in personas:
        raise KeyError(f"La persona con código {cod_persona} no está registrada.")
    if cod_lab not in laboratorios:
        raise KeyError(f"El laboratorio con código {cod_lab} no está registrado.")

    persona = personas[cod_persona]
    
    if not persona.tiene_laboratorio(cod_lab):
        raise ValueError(f"La persona {cod_persona} no tiene acceso a {cod_lab} para revocarlo.")

    persona.retirar_laboratorio(cod_lab)


def puede_acceder(personas: dict[str, Persona], laboratorios: dict[str, Laboratorio], cod_persona: str, cod_lab: str) -> bool:
    if cod_persona not in personas:
        raise KeyError(f"La persona con código {cod_persona} no está registrada.")
    if cod_lab not in laboratorios:
        raise KeyError(f"El laboratorio con código {cod_lab} no está registrado.")
    return personas[cod_persona].tiene_laboratorio(cod_lab)


def comparar_autorizaciones(personas: dict[str, Persona], cod_persona_a: str, cod_persona_b: str) -> dict:
    if cod_persona_a not in personas:
        raise KeyError(f"La persona {cod_persona_a} no está registrada.")
    if cod_persona_b not in personas:
        raise KeyError(f"La persona {cod_persona_b} no está registrada.")
    set_a = personas[cod_persona_a].laboratorios_autorizados
    set_b = personas[cod_persona_b].laboratorios_autorizados
    return {
        "union": set_a | set_b,
        "interseccion": set_a & set_b,
        "diferencia_a_b": set_a - set_b,
        "diferencia_b_a": set_b - set_a,
        "diferencia_simetrica": set_a ^ set_b
    }
