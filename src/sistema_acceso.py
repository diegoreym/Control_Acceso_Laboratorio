from laboratorio import Laboratorio
from persona import Persona
import operaciones_laboratorios as ops_lab
import operaciones_personas as ops_per
import operaciones_autorizaciones as ops_aut


class SistemaAcceso:
    def __init__(self) -> None:
        self._personas: dict[str, Persona] = {}
        self._laboratorios: dict[str, Laboratorio] = {}

    @staticmethod
    def _normalizar(codigo: str) -> str:
        """Quita espacios exteriores y convierte a mayúsculas"""
        if not isinstance(codigo, str):
            raise ValueError("El código debe ser un texto.")
        return codigo.strip().upper()

    # ------------------------------------------------------------------
    # Laboratorios (Map) 
    # ------------------------------------------------------------------
    def registrar_laboratorio(self, laboratorio: Laboratorio) -> None:
        ops_lab.registrar_laboratorio(self._laboratorios, laboratorio)

    def buscar_laboratorio(self, codigo: str) -> Laboratorio | None:
        return ops_lab.buscar_laboratorio(self._laboratorios, self._normalizar(codigo))

    def existe_laboratorio(self, codigo: str) -> bool:
        return ops_lab.existe_laboratorio(self._laboratorios, self._normalizar(codigo))

    def modificar_laboratorio(self, codigo: str, nombre: str, capacidad: int, pabellon: str) -> None:
        ops_lab.modificar_laboratorio(
            self._laboratorios, self._normalizar(codigo), nombre, capacidad, pabellon
        )

    def eliminar_laboratorio(self, codigo: str) -> None:
        """Elimina el laboratorio y retira su código de todas las personas."""
        codigo = self._normalizar(codigo)
        ops_lab.eliminar_laboratorio(self._laboratorios, codigo)  # falla si no existe
        for persona in self._personas.values():
            persona.retirar_laboratorio(codigo)  # discard: no falla si no lo tenía

    def listar_laboratorios(self) -> None:
        ops_lab.listar_laboratorios(self._laboratorios)

    # ------------------------------------------------------------------
    # Personas (Map) 
    # ------------------------------------------------------------------
    def registrar_persona(self, codigo: str, apellidos: str, nombres: str) -> None:
        ops_per.registrar_persona(self._personas, codigo, apellidos, nombres)

    def buscar_persona(self, codigo: str) -> Persona:
        return ops_per.buscar_persona(self._personas, codigo)

    def existe_persona(self, codigo: str) -> bool:
        return ops_per.existe_persona(self._personas, codigo)

    def modificar_persona(self, codigo: str, apellidos: str, nombres: str) -> None:
        ops_per.modificar_persona(self._personas, codigo, apellidos, nombres)

    def eliminar_persona(self, codigo: str) -> None:
        ops_per.eliminar_persona(self._personas, codigo)

    def listar_personas(self) -> list[Persona]:
        return ops_per.listar_personas(self._personas)

    # ------------------------------------------------------------------
    # Autorizaciones (Set)
    # ------------------------------------------------------------------
    def autorizar_laboratorio(self, cod_persona: str, cod_lab: str) -> None:
        ops_aut.autorizar_laboratorio(
            self._personas, self._laboratorios,
            self._normalizar(cod_persona), self._normalizar(cod_lab),
        )

    def revocar_autorizacion(self, cod_persona: str, cod_lab: str) -> None:
        ops_aut.revocar_autorizacion(
            self._personas, self._laboratorios,
            self._normalizar(cod_persona), self._normalizar(cod_lab),
        )

    def puede_acceder(self, cod_persona: str, cod_lab: str) -> bool:
        return ops_aut.puede_acceder(
            self._personas, self._laboratorios,
            self._normalizar(cod_persona), self._normalizar(cod_lab),
        )

    def comparar_autorizaciones(self, cod_persona_a: str, cod_persona_b: str) -> dict[str, set[str]]:
        return ops_aut.comparar_autorizaciones(
            self._personas,
            self._normalizar(cod_persona_a), self._normalizar(cod_persona_b),
        )

    # ------------------------------------------------------------------
    #  Conteo de frecuencias 
    # ------------------------------------------------------------------
    def contar_frecuencias(self, datos: list[str]) -> dict[str, int]:
        frecuencias: dict[str, int] = {}
        for codigo in datos:
            if codigo in frecuencias:
                cantidad = frecuencias[codigo]
                frecuencias[codigo] = cantidad + 1
            else:
                frecuencias[codigo] = 1
        return frecuencias