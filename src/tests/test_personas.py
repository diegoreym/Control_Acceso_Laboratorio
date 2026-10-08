import sys
import unittest
from pathlib import Path

# Permite importar los módulos de la carpeta src.
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


class TestPersonas(unittest.TestCase):
    def setUp(self) -> None:
        # Cada prueba comienza con un diccionario nuevo y vacío.
        self.personas: dict[str, Persona] = {}

    def test_PER_01_map_vacio(self) -> None:
        self.assertEqual(listar_personas(self.personas), [])
        self.assertFalse(existe_persona(self.personas, "P001"))
        with self.assertRaises(KeyError):
            buscar_persona(self.personas, "P001")
        with self.assertRaises(KeyError):
            eliminar_persona(self.personas, "P001")
        self.assertEqual(self.personas, {})

    def test_PER_02_registrar_una_persona(self) -> None:
        registrar_persona(self.personas, "P001", "Pérez", "Juan")
        persona = self.personas["P001"]

        self.assertIsInstance(persona, Persona)
        self.assertEqual(persona.codigo, "P001")
        self.assertEqual(persona.apellidos, "Pérez")
        self.assertEqual(persona.nombres, "Juan")
        self.assertEqual(persona.laboratorios_autorizados, set())
        self.assertEqual(listar_personas(self.personas), [persona])

    def test_PER_03_varias_personas_con_datos_repetidos(self) -> None:
        for codigo in ("P001", "P002", "P003"):
            registrar_persona(self.personas, codigo, "Pérez", "Juan")

        self.assertEqual(len(self.personas), 3)
        self.assertEqual(set(self.personas), {"P001", "P002", "P003"})
        self.assertIsNot(self.personas["P001"], self.personas["P002"])
        # assertCountEqual comprueba los elementos sin exigir un orden.
        self.assertCountEqual(listar_personas(self.personas), self.personas.values())

    def test_PER_04_normalizar_codigos_y_textos(self) -> None:
        registrar_persona(self.personas, " p001 ", " Pérez ", " Juan ")
        persona = buscar_persona(self.personas, " p001 ")

        self.assertEqual(persona.codigo, "P001")
        self.assertEqual(persona.apellidos, "Pérez")
        self.assertEqual(persona.nombres, "Juan")
        self.assertTrue(existe_persona(self.personas, " p001 "))

        modificar_persona(self.personas, " p001 ", " Rojas ", " Luis ")
        self.assertEqual(persona.apellidos, "Rojas")
        self.assertEqual(persona.nombres, "Luis")
        eliminar_persona(self.personas, " p001 ")
        self.assertEqual(self.personas, {})

    def test_PER_05_duplicado_no_sobrescribe(self) -> None:
        registrar_persona(self.personas, "P001", "Pérez", "Juan")
        persona = self.personas["P001"]
        persona.agregar_laboratorio("LAB01")

        for codigo in ("P001", " p001 "):
            with self.subTest(codigo=codigo):
                with self.assertRaisesRegex(ValueError, "ya está registrada"):
                    registrar_persona(self.personas, codigo, "Otro", "Nombre")
                self.assertEqual(self.personas, {"P001": persona})
                self.assertEqual(persona.apellidos, "Pérez")
                self.assertEqual(persona.nombres, "Juan")
                self.assertEqual(persona.laboratorios_autorizados, {"LAB01"})

    def test_PER_06_codigos_invalidos_no_alteran_registros(self) -> None:
        registrar_persona(self.personas, "P001", "Pérez", "Juan")
        persona = self.personas["P001"]
        persona.agregar_laboratorio("LAB01")

        for codigo in ("", "   ", "P 001", "P-001", "P_001", "P001!", None, 123, True):
            with self.subTest(codigo=codigo):
                with self.assertRaises(ValueError):
                    registrar_persona(self.personas, codigo, "Rojas", "Luis")
                with self.assertRaises(ValueError):
                    buscar_persona(self.personas, codigo)
                with self.assertRaises(ValueError):
                    existe_persona(self.personas, codigo)
                with self.assertRaises(ValueError):
                    modificar_persona(self.personas, codigo, "Rojas", "Luis")
                with self.assertRaises(ValueError):
                    eliminar_persona(self.personas, codigo)
                self.assertEqual(self.personas, {"P001": persona})
                self.assertEqual(persona.codigo, "P001")
                self.assertEqual(persona.apellidos, "Pérez")
                self.assertEqual(persona.nombres, "Juan")
                self.assertEqual(persona.laboratorios_autorizados, {"LAB01"})

    def test_PER_07_registro_con_datos_invalidos(self) -> None:
        registrar_persona(self.personas, "P001", "Pérez", "Juan")
        persona = self.personas["P001"]
        persona.agregar_laboratorio("LAB01")

        for dato in ("", "   ", None, 123):
            with self.subTest(dato=dato):
                with self.assertRaises(ValueError):
                    registrar_persona(self.personas, "P003", dato, "Luis")
                with self.assertRaises(ValueError):
                    registrar_persona(self.personas, "P003", "Rojas", dato)
                self.assertEqual(self.personas, {"P001": persona})
                self.assertEqual(persona.apellidos, "Pérez")
                self.assertEqual(persona.nombres, "Juan")
                self.assertEqual(persona.laboratorios_autorizados, {"LAB01"})

    def test_PER_08_buscar_devuelve_el_objeto_original(self) -> None:
        registrar_persona(self.personas, "P001", "Pérez", "Juan")
        persona = buscar_persona(self.personas, "P001")
        self.assertIs(persona, self.personas["P001"])

    def test_PER_09_buscar_inexistente(self) -> None:
        registrar_persona(self.personas, "P001", "Pérez", "Juan")
        persona = self.personas["P001"]
        with self.assertRaisesRegex(KeyError, "P999"):
            buscar_persona(self.personas, "P999")
        self.assertEqual(self.personas, {"P001": persona})
        self.assertEqual(persona.apellidos, "Pérez")
        self.assertEqual(persona.nombres, "Juan")

    def test_PER_10_existe_persona(self) -> None:
        registrar_persona(self.personas, "P001", "Pérez", "Juan")
        self.assertIs(existe_persona(self.personas, "P001"), True)
        self.assertIs(existe_persona(self.personas, "P999"), False)

    def test_PER_11_modificar_conserva_objeto_codigo_y_permisos(self) -> None:
        registrar_persona(self.personas, "P001", "Pérez", "Juan")
        registrar_persona(self.personas, "P002", "Gómez", "Ana")
        persona = self.personas["P001"]
        otra_persona = self.personas["P002"]
        persona.agregar_laboratorio("LAB01")
        persona.agregar_laboratorio("LAB03")
        otra_persona.agregar_laboratorio("LAB02")

        modificar_persona(self.personas, "P001", "Rojas", "Luis")

        self.assertIs(self.personas["P001"], persona)
        self.assertEqual(persona.codigo, "P001")
        self.assertEqual(persona.apellidos, "Rojas")
        self.assertEqual(persona.nombres, "Luis")
        self.assertEqual(persona.laboratorios_autorizados, {"LAB01", "LAB03"})
        self.assertIs(self.personas["P002"], otra_persona)
        self.assertEqual(otra_persona.apellidos, "Gómez")
        self.assertEqual(otra_persona.nombres, "Ana")
        self.assertEqual(otra_persona.laboratorios_autorizados, {"LAB02"})

    def test_PER_12_modificacion_invalida_no_cambia_datos(self) -> None:
        registrar_persona(self.personas, "P001", "Pérez", "Juan")
        persona = self.personas["P001"]
        persona.agregar_laboratorio("LAB01")

        for dato in ("", "   ", None, 123):
            with self.subTest(dato=dato):
                with self.assertRaises(ValueError):
                    modificar_persona(self.personas, "P001", dato, "Luis")
                with self.assertRaises(ValueError):
                    modificar_persona(self.personas, "P001", "Rojas", dato)
                self.assertEqual(self.personas, {"P001": persona})
                self.assertEqual(persona.codigo, "P001")
                self.assertEqual(persona.apellidos, "Pérez")
                self.assertEqual(persona.nombres, "Juan")
                self.assertEqual(persona.laboratorios_autorizados, {"LAB01"})

    def test_PER_13_modificar_inexistente(self) -> None:
        registrar_persona(self.personas, "P001", "Pérez", "Juan")
        persona = self.personas["P001"]
        with self.assertRaises(KeyError):
            modificar_persona(self.personas, "P999", "Rojas", "Luis")
        self.assertEqual(self.personas, {"P001": persona})
        self.assertEqual(persona.apellidos, "Pérez")
        self.assertEqual(persona.nombres, "Juan")

    def test_PER_14_registrar_y_eliminar_P003_sin_afectar_otras(self) -> None:
        registrar_persona(self.personas, "P001", "Pérez", "Juan")
        registrar_persona(self.personas, "P002", "Gómez", "Ana")
        primera = self.personas["P001"]
        segunda = self.personas["P002"]
        primera.agregar_laboratorio("LAB01")
        segunda.agregar_laboratorio("LAB02")

        registrar_persona(self.personas, "P003", "Torres", "Diego")
        self.assertEqual(len(self.personas), 3)
        self.assertEqual(self.personas["P003"].laboratorios_autorizados, set())
        eliminar_persona(self.personas, "P003")

        self.assertEqual(self.personas, {"P001": primera, "P002": segunda})
        self.assertEqual(primera.apellidos, "Pérez")
        self.assertEqual(primera.nombres, "Juan")
        self.assertEqual(primera.laboratorios_autorizados, {"LAB01"})
        self.assertEqual(segunda.apellidos, "Gómez")
        self.assertEqual(segunda.nombres, "Ana")
        self.assertEqual(segunda.laboratorios_autorizados, {"LAB02"})

    def test_PER_15_eliminar_unica_persona(self) -> None:
        registrar_persona(self.personas, "P001", "Pérez", "Juan")
        eliminar_persona(self.personas, "P001")
        self.assertEqual(listar_personas(self.personas), [])
        self.assertFalse(existe_persona(self.personas, "P001"))

    def test_PER_16_eliminar_inexistente(self) -> None:
        registrar_persona(self.personas, "P001", "Pérez", "Juan")
        persona = self.personas["P001"]
        persona.agregar_laboratorio("LAB01")
        with self.assertRaisesRegex(KeyError, "P999"):
            eliminar_persona(self.personas, "P999")
        self.assertEqual(self.personas, {"P001": persona})
        self.assertEqual(persona.apellidos, "Pérez")
        self.assertEqual(persona.nombres, "Juan")
        self.assertEqual(persona.laboratorios_autorizados, {"LAB01"})

    def test_PER_17_listar_no_cambia_el_diccionario(self) -> None:
        registrar_persona(self.personas, "P001", "Pérez", "Juan")
        registrar_persona(self.personas, "P002", "Gómez", "Ana")
        primera = self.personas["P001"]
        segunda = self.personas["P002"]

        listado = listar_personas(self.personas)
        self.assertCountEqual(listado, [primera, segunda])
        listado.clear()
        self.assertEqual(self.personas, {"P001": primera, "P002": segunda})

    def test_PER_18_P001_y_P002_tienen_sets_independientes(self) -> None:
        registrar_persona(self.personas, "P001", "Pérez", "Juan")
        registrar_persona(self.personas, "P002", "Gómez", "Ana")
        primera = self.personas["P001"]
        segunda = self.personas["P002"]
        self.assertIsNot(primera, segunda)

        primera.agregar_laboratorio("LAB01")
        primera.agregar_laboratorio("LAB03")
        segunda.agregar_laboratorio("LAB02")
        primera.retirar_laboratorio("LAB01")

        self.assertEqual(primera.laboratorios_autorizados, {"LAB03"})
        self.assertEqual(segunda.laboratorios_autorizados, {"LAB02"})

    def test_PER_19_consulta_de_permisos_devuelve_copia(self) -> None:
        registrar_persona(self.personas, "P001", "Pérez", "Juan")
        persona = self.personas["P001"]
        persona.agregar_laboratorio("LAB01")

        permisos = persona.laboratorios_autorizados
        permisos.clear()
        permisos.add("LAB99")
        self.assertEqual(persona.laboratorios_autorizados, {"LAB01"})

    def test_PER_20_codigo_de_solo_lectura_y_representacion(self) -> None:
        registrar_persona(self.personas, "P001", "Pérez", "Juan")
        persona = self.personas["P001"]
        with self.assertRaises(AttributeError):
            persona.codigo = "P003"
        self.assertEqual(persona.codigo, "P001")
        self.assertIn("P001", str(persona))
        self.assertIn("Pérez", str(persona))
        self.assertIn("Juan", str(persona))


if __name__ == "__main__":
    unittest.main(verbosity=2)
