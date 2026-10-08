
"""Pruebas de Diego: Map de personas y contrato del submenú."""

import io
import runpy
import sys
import types
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from operaciones_personas import (
    buscar_persona,
    eliminar_persona,
    existe_persona,
    listar_personas,
    modificar_persona,
    registrar_persona,
)
from persona import Persona
from ui_personas import UIPersonas


class TestPersonas(unittest.TestCase):
    def setUp(self) -> None:
        self.personas: dict[str, Persona] = {}

    def preparar_personas(self) -> tuple[Persona, Persona]:
        registrar_persona(self.personas, "P001", "Pérez", "Juan")
        registrar_persona(self.personas, "P002", "Gómez", "Ana")
        primera = self.personas["P001"]
        segunda = self.personas["P002"]
        primera.agregar_laboratorio("LAB01")
        segunda.agregar_laboratorio("LAB02")
        return primera, segunda

    def estado(self) -> dict[str, tuple[Persona, str, str, str, set[str]]]:
        """Incluye identidad, datos y permisos para detectar efectos secundarios."""
        return {codigo: (persona,persona.codigo,persona.apellidos,persona.nombres,persona.laboratorios_autorizados,)
            for codigo, persona in self.personas.items()
        }

    def test_PER_01_map_vacio(self) -> None:
        self.assertEqual(listar_personas(self.personas), [])
        self.assertIs(existe_persona(self.personas, "P001"), False)
        with self.assertRaises(KeyError):
            buscar_persona(self.personas, "P001")
        with self.assertRaises(KeyError):
            eliminar_persona(self.personas, "P001")
        self.assertEqual(self.personas, {})

    def test_PER_02_registrar_una_persona(self) -> None:
        self.assertIsNone(registrar_persona(self.personas, "P001", "Pérez", "Juan"))
        persona = self.personas["P001"]
        self.assertIsInstance(persona, Persona)
        self.assertEqual((persona.codigo, persona.apellidos, persona.nombres),
                         ("P001", "Pérez", "Juan"))
        self.assertEqual(persona.laboratorios_autorizados, set())
        self.assertEqual(listar_personas(self.personas), [persona])

    def test_PER_03_varias_personas_con_datos_repetidos(self) -> None:
        for codigo in ("P001", "P002", "P003"):
            registrar_persona(self.personas, codigo, "Pérez", "Juan")
        self.assertEqual(set(self.personas), {"P001", "P002", "P003"})
        self.assertEqual({p.codigo for p in listar_personas(self.personas)},
                         {"P001", "P002", "P003"})
        self.assertIsNot(self.personas["P001"], self.personas["P002"])

    def test_PER_04_normalizar_codigos_y_textos(self) -> None:
        registrar_persona(self.personas, " p001 ", " Pérez ", " Juan ")
        persona = buscar_persona(self.personas, " p001 ")
        self.assertEqual(set(self.personas), {"P001"})
        self.assertEqual((persona.apellidos, persona.nombres), ("Pérez", "Juan"))
        self.assertIs(existe_persona(self.personas, " p001 "), True)
        modificar_persona(self.personas, " p001 ", " Rojas ", " Luis ")
        self.assertEqual((persona.apellidos, persona.nombres), ("Rojas", "Luis"))
        eliminar_persona(self.personas, " p001 ")
        self.assertEqual(self.personas, {})

    def test_PER_05_duplicado_no_sobrescribe(self) -> None:
        self.preparar_personas()
        anterior = self.estado()
        for codigo in ("P001", " p001 "):
            with self.subTest(codigo=codigo):
                with self.assertRaisesRegex(ValueError, "ya está registrada"):
                    registrar_persona(self.personas, codigo, "Otro", "Nombre")
                self.assertEqual(self.estado(), anterior)

    def test_PER_06_codigos_invalidos_no_alteran_registros(self) -> None:
        self.preparar_personas()
        anterior = self.estado()
        operaciones = (
            lambda codigo: registrar_persona(self.personas, codigo, "Rojas", "Luis"),
            lambda codigo: buscar_persona(self.personas, codigo),
            lambda codigo: existe_persona(self.personas, codigo),
            lambda codigo: modificar_persona(self.personas, codigo, "Rojas", "Luis"),
            lambda codigo: eliminar_persona(self.personas, codigo),
        )
        for codigo in ("", "   ", "P 001", "P-001", "P_001", "P001!", None, 123, True):
            for indice, operacion in enumerate(operaciones):
                with self.subTest(codigo=codigo, operacion=indice):
                    with self.assertRaises(ValueError):
                        operacion(codigo)
                    self.assertEqual(self.estado(), anterior)

    def test_PER_07_registro_con_datos_invalidos_es_atomico(self) -> None:
        self.preparar_personas()
        anterior = self.estado()
        for dato in ("", "  ", None, 123):
            for apellidos, nombres in ((dato, "Luis"), ("Rojas", dato)):
                with self.subTest(apellidos=apellidos, nombres=nombres):
                    with self.assertRaises(ValueError):
                        registrar_persona(self.personas, "P003", apellidos, nombres)
                    self.assertEqual(self.estado(), anterior)

    def test_PER_08_buscar_devuelve_el_objeto_original(self) -> None:
        primera, _ = self.preparar_personas()
        self.assertIs(buscar_persona(self.personas, "P001"), primera)

    def test_PER_09_buscar_inexistente_conserva_estado(self) -> None:
        self.preparar_personas()
        anterior = self.estado()
        with self.assertRaisesRegex(KeyError, "P999.*no está registrada"):
            buscar_persona(self.personas, "P999")
        self.assertEqual(self.estado(), anterior)

    def test_PER_10_existe_devuelve_bool(self) -> None:
        self.preparar_personas()
        self.assertIs(existe_persona(self.personas, "P001"), True)
        self.assertIs(existe_persona(self.personas, "P999"), False)

    def test_PER_11_modificar_conserva_objeto_codigo_y_permisos(self) -> None:
        primera, segunda = self.preparar_personas()
        primera.agregar_laboratorio("LAB03")
        anterior_segunda = self.estado()["P002"]
        self.assertIsNone(modificar_persona(self.personas, "P001", "Rojas", "Luis"))
        self.assertIs(self.personas["P001"], primera)
        self.assertEqual((primera.codigo, primera.apellidos, primera.nombres),
                         ("P001", "Rojas", "Luis"))
        self.assertEqual(primera.laboratorios_autorizados, {"LAB01", "LAB03"})
        self.assertIs(self.personas["P002"], segunda)
        self.assertEqual(self.estado()["P002"], anterior_segunda)

    def test_PER_12_modificacion_invalida_no_actualiza_parcialmente(self) -> None:
        self.preparar_personas()
        anterior = self.estado()
        for dato in ("", "  ", None, 123):
            for apellidos, nombres in ((dato, "Luis"), ("Rojas", dato)):
                with self.subTest(apellidos=apellidos, nombres=nombres):
                    with self.assertRaises(ValueError):
                        modificar_persona(self.personas, "P001", apellidos, nombres)
                    self.assertEqual(self.estado(), anterior)

    def test_PER_13_modificar_inexistente_conserva_estado(self) -> None:
        self.preparar_personas()
        anterior = self.estado()
        with self.assertRaises(KeyError):
            modificar_persona(self.personas, "P999", "Rojas", "Luis")
        self.assertEqual(self.estado(), anterior)

    def test_PER_14_registrar_y_eliminar_P003_sin_afectar_otras(self) -> None:
        self.preparar_personas()
        anterior = self.estado()
        registrar_persona(self.personas, "P003", "Torres", "Diego")
        self.assertEqual(set(self.personas), {"P001", "P002", "P003"})
        self.assertIsNone(eliminar_persona(self.personas, "P003"))
        self.assertEqual(self.estado(), anterior)

    def test_PER_15_eliminar_unica_persona_deja_map_vacio(self) -> None:
        registrar_persona(self.personas, "P001", "Pérez", "Juan")
        eliminar_persona(self.personas, "P001")
        self.assertEqual(listar_personas(self.personas), [])
        self.assertIs(existe_persona(self.personas, "P001"), False)

    def test_PER_16_eliminar_inexistente_conserva_estado(self) -> None:
        self.preparar_personas()
        anterior = self.estado()
        with self.assertRaisesRegex(KeyError, "P999.*no está registrada"):
            eliminar_persona(self.personas, "P999")
        self.assertEqual(self.estado(), anterior)

    def test_PER_17_listar_no_expone_el_contenedor(self) -> None:
        self.preparar_personas()
        anterior = self.estado()
        listado = listar_personas(self.personas)
        self.assertEqual({p.codigo for p in listado}, {"P001", "P002"})
        for persona in listado:
            self.assertIs(persona, self.personas[persona.codigo])
        listado.clear()
        self.assertEqual(self.estado(), anterior)

    def test_PER_18_P001_y_P002_tienen_sets_independientes(self) -> None:
        primera, segunda = self.preparar_personas()
        self.assertIsNot(primera, segunda)
        primera.agregar_laboratorio("LAB03")
        primera.retirar_laboratorio("LAB01")
        self.assertEqual(primera.laboratorios_autorizados, {"LAB03"})
        self.assertEqual(segunda.laboratorios_autorizados, {"LAB02"})

    def test_PER_19_consulta_de_permisos_devuelve_copia(self) -> None:
        primera, _ = self.preparar_personas()
        permisos = primera.laboratorios_autorizados
        permisos.clear()
        permisos.add("LAB99")
        self.assertEqual(primera.laboratorios_autorizados, {"LAB01"})

    def test_PER_20_codigo_de_solo_lectura_y_representacion(self) -> None:
        primera, _ = self.preparar_personas()
        with self.assertRaises(AttributeError):
            primera.codigo = "P003"
        self.assertEqual(primera.codigo, "P001")
        for texto in ("P001", "Pérez", "Juan"):
            self.assertIn(texto, str(primera))


class TestUIPersonas(unittest.TestCase):
    def setUp(self) -> None:
        # El integrador aún no está implementado. El doble ofrece solo la API pública.
        self.sistema = Mock(spec=[
            "registrar_persona", "buscar_persona", "existe_persona",
            "modificar_persona", "eliminar_persona", "listar_personas",
        ])
        self.ui = UIPersonas(self.sistema)

    def ejecutar_con_entradas(self, entradas: list[str]) -> str:
        salida = io.StringIO()
        with patch("builtins.input", side_effect=entradas), redirect_stdout(salida):
            self.assertIsNone(self.ui.ejecutar())
        return salida.getvalue()

    def test_PER_21_UI_compartir_sistema_y_volver(self) -> None:
        self.assertIs(self.ui.sistema, self.sistema)
        salida = self.ejecutar_con_entradas(["0"])
        self.assertIn("Volviendo al menú principal", salida)
        self.assertEqual(self.sistema.mock_calls, [])

    def test_PER_22_UI_registrar(self) -> None:
        self.ejecutar_con_entradas(["1", " p003 ", "Torres", "Diego", "0"])
        self.sistema.registrar_persona.assert_called_once_with("P003", "Torres", "Diego")

    def test_PER_23_UI_buscar(self) -> None:
        self.sistema.buscar_persona.return_value = Persona("P001", "Pérez", "Juan")
        salida = self.ejecutar_con_entradas(["2", "p001", "0"])
        self.sistema.buscar_persona.assert_called_once_with("P001")
        self.assertIn("Pérez", salida)
        self.assertIn("Juan", salida)

    def test_PER_24_UI_verificar_existencia(self) -> None:
        for existe in (True, False):
            with self.subTest(existe=existe):
                self.sistema.existe_persona.reset_mock()
                self.sistema.existe_persona.return_value = existe
                salida = self.ejecutar_con_entradas(["3", "P001", "0"])
                self.sistema.existe_persona.assert_called_once_with("P001")
                mensaje = "P001 está registrada" if existe else "P001 no está registrada"
                self.assertIn(mensaje, salida)

    def test_PER_25_UI_modificar(self) -> None:
        self.ejecutar_con_entradas(["4", "p001", "Rojas", "Luis", "0"])
        self.sistema.modificar_persona.assert_called_once_with("P001", "Rojas", "Luis")

    def test_PER_26_UI_eliminar(self) -> None:
        self.ejecutar_con_entradas(["5", "p003", "0"])
        self.sistema.eliminar_persona.assert_called_once_with("P003")

    def test_PER_27_UI_listar_vacio_y_varias_personas(self) -> None:
        for listado in ([], [Persona("P001", "Pérez", "Juan"),
                             Persona("P002", "Gómez", "Ana")]):
            with self.subTest(cantidad=len(listado)):
                self.sistema.listar_personas.reset_mock()
                self.sistema.listar_personas.return_value = listado
                salida = self.ejecutar_con_entradas(["6", "0"])
                self.sistema.listar_personas.assert_called_once_with()
                if listado:
                    for persona in listado:
                        self.assertIn(f"{persona.codigo} ->", salida)
                else:
                    self.assertIn("No hay personas registradas", salida)

    def test_PER_28_UI_opcion_invalida_permite_continuar(self) -> None:
        salida = self.ejecutar_con_entradas(["abc", "99", "0"])
        self.assertEqual(salida.count("Opción inválida"), 2)
        self.assertEqual(self.sistema.mock_calls, [])

    def test_PER_29_UI_errores_permiten_continuar(self) -> None:
        casos = (
            ("registrar_persona", ["1", "", "Pérez", "Juan", "0"], ValueError("Código inválido")),
            ("buscar_persona", ["2", "P999", "0"], KeyError("Persona inexistente")),
            ("existe_persona", ["3", "", "0"], ValueError("Código inválido")),
            ("modificar_persona", ["4", "P001", "", "Juan", "0"], ValueError("Apellidos inválidos")),
            ("eliminar_persona", ["5", "P999", "0"], KeyError("Persona inexistente")),
        )
        for metodo, entradas, error in casos:
            with self.subTest(metodo=metodo):
                llamada = getattr(self.sistema, metodo)
                llamada.side_effect = error
                salida = self.ejecutar_con_entradas(entradas)
                self.assertIn(str(error.args[0]), salida)
                self.assertIn("Volviendo al menú principal", salida)
                llamada.side_effect = None

    def test_PER_30_UI_fin_de_entrada_e_interrupcion(self) -> None:
        for error in (EOFError, KeyboardInterrupt):
            with self.subTest(error=error.__name__):
                salida = io.StringIO()
                with patch("builtins.input", side_effect=error), redirect_stdout(salida):
                    self.assertIsNone(self.ui.ejecutar())
                self.assertIn("Cerrando submenú", salida.getvalue())

    def test_PER_31_UI_recorrido_con_operaciones_reales(self) -> None:
        personas: dict[str, Persona] = {}
        self.sistema.registrar_persona.side_effect = (
            lambda codigo, apellidos, nombres:
            registrar_persona(personas, codigo, apellidos, nombres)
        )
        self.sistema.buscar_persona.side_effect = lambda codigo: buscar_persona(personas, codigo)
        self.sistema.existe_persona.side_effect = lambda codigo: existe_persona(personas, codigo)
        self.sistema.modificar_persona.side_effect = (
            lambda codigo, apellidos, nombres:
            modificar_persona(personas, codigo, apellidos, nombres)
        )
        self.sistema.eliminar_persona.side_effect = lambda codigo: eliminar_persona(personas, codigo)
        self.sistema.listar_personas.side_effect = lambda: listar_personas(personas)
        salida = self.ejecutar_con_entradas([
            "1", "p003", "Torres", "Diego",
            "1", "P003", "Otro", "Nombre",
            "4", "P003", "Rojas", "Luis",
            "2", "P003",
            "3", "P003",
            "6",
            "5", "P003",
            "3", "P003",
            "0",
        ])
        self.assertEqual(personas, {})
        self.assertIn("ya está registrada", salida)
        self.assertIn("Apellidos: Rojas | Nombres: Luis", salida)
        self.assertIn("P003 está registrada", salida)
        self.assertIn("P003 no está registrada", salida)

    def test_PER_32_UI_guarda_independiente_con_contrato_de_integracion(self) -> None:
        # Simula los módulos pendientes, sin crear una implementación de Garrido.
        modulo_sistema = types.ModuleType("sistema_acceso")
        modulo_demo = types.ModuleType("datos_demo")
        modulo_sistema.SistemaAcceso = Mock(return_value=self.sistema)
        modulo_demo.cargar_datos_demo = Mock()
        salida = io.StringIO()
        with patch.dict(sys.modules, {
            "sistema_acceso": modulo_sistema, "datos_demo": modulo_demo,
        }), patch("builtins.input", return_value="0"), redirect_stdout(salida):
            runpy.run_path(str(Path(__file__).resolve().parents[1] / "ui_personas.py"),
                           run_name="__main__")
        modulo_sistema.SistemaAcceso.assert_called_once_with()
        modulo_demo.cargar_datos_demo.assert_called_once_with(self.sistema)
        self.assertIn("Volviendo al menú principal", salida.getvalue())


if __name__ == "__main__":
    unittest.main(verbosity=2)
