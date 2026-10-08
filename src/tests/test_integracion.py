
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from datos_demo import cargar_datos_demo
from laboratorio import Laboratorio
from sistema_acceso import SistemaAcceso


class TestSistemaAcceso(unittest.TestCase):
    def setUp(self) -> None:
        """Sistema nuevo con tres laboratorios y dos personas, sin permisos."""
        self.sistema = SistemaAcceso()
        self.sistema.registrar_laboratorio(Laboratorio("LAB01", "Programación", 30, "A"))
        self.sistema.registrar_laboratorio(Laboratorio("LAB02", "Redes", 25, "B"))
        self.sistema.registrar_laboratorio(Laboratorio("LAB03", "IA", 20, "C"))
        self.sistema.registrar_persona("P001", "Pérez", "Juan")
        self.sistema.registrar_persona("P002", "Gómez", "Ana")

    def test_INT_01_recorrido_completo(self) -> None:
        # registrar
        self.sistema.registrar_laboratorio(Laboratorio("LAB06", "Robótica", 12, "F"))
        self.sistema.registrar_persona("P003", "Torres", "Diego")
        self.assertTrue(self.sistema.existe_laboratorio("LAB06"))
        self.assertTrue(self.sistema.existe_persona("P003"))
        # autorizar y consultar
        self.sistema.autorizar_laboratorio("P003", "LAB06")
        self.assertTrue(self.sistema.puede_acceder("P003", "LAB06"))
        self.assertFalse(self.sistema.puede_acceder("P003", "LAB01"))
        # revocar
        self.sistema.revocar_autorizacion("P003", "LAB06")
        self.assertFalse(self.sistema.puede_acceder("P003", "LAB06"))
        # eliminar
        self.sistema.eliminar_laboratorio("LAB06")
        self.sistema.eliminar_persona("P003")
        self.assertFalse(self.sistema.existe_laboratorio("LAB06"))
        self.assertFalse(self.sistema.existe_persona("P003"))
        self.assertEqual(len(self.sistema.listar_personas()), 2)

    def test_INT_02_codigos_inexistentes(self) -> None:
        with self.assertRaises(KeyError):
            self.sistema.autorizar_laboratorio("P999", "LAB01")
        with self.assertRaises(KeyError):
            self.sistema.autorizar_laboratorio("P001", "LAB99")
        with self.assertRaises(KeyError):
            self.sistema.revocar_autorizacion("P999", "LAB01")
        with self.assertRaises(KeyError):
            self.sistema.puede_acceder("P001", "LAB99")
        with self.assertRaises(KeyError):
            self.sistema.comparar_autorizaciones("P001", "P999")
        with self.assertRaises(KeyError):
            self.sistema.buscar_persona("P999")
        with self.assertRaises(KeyError):
            self.sistema.eliminar_persona("P999")
        # Los módulos de laboratorios (Harold) devuelven None / ValueError.
        self.assertIsNone(self.sistema.buscar_laboratorio("LAB99"))
        with self.assertRaises(ValueError):
            self.sistema.eliminar_laboratorio("LAB99")
        # Nada cambió.
        self.assertEqual(len(self.sistema.listar_personas()), 2)
        self.assertTrue(self.sistema.existe_laboratorio("LAB01"))

    def test_INT_03_eliminar_laboratorio_limpia_permisos(self) -> None:
        self.sistema.autorizar_laboratorio("P001", "LAB01")
        self.sistema.autorizar_laboratorio("P001", "LAB02")
        self.sistema.autorizar_laboratorio("P002", "LAB01")

        self.sistema.eliminar_laboratorio("LAB01")

        p1 = self.sistema.buscar_persona("P001")
        p2 = self.sistema.buscar_persona("P002")
        self.assertEqual(p1.laboratorios_autorizados, {"LAB02"})
        self.assertEqual(p2.laboratorios_autorizados, set())

    def test_INT_04_conteo_integrado(self) -> None:
        datos = ["LAB01", "LAB02", "LAB01", "LAB03", "LAB01", "LAB02", "LAB05"]
        copia = list(datos)
        self.assertEqual(
            self.sistema.contar_frecuencias(datos),
            {"LAB01": 3, "LAB02": 2, "LAB03": 1, "LAB05": 1},
        )
        self.assertEqual(datos, copia)  # no modifica la entrada
        self.assertEqual(self.sistema.contar_frecuencias([]), {})
        self.assertEqual(self.sistema.contar_frecuencias(["LAB01"]), {"LAB01": 1})

    def test_INT_05_normalizacion_de_codigos(self) -> None:
        self.sistema.autorizar_laboratorio(" p001 ", " lab01 ")
        self.assertTrue(self.sistema.puede_acceder("P001", "LAB01"))
        self.assertTrue(self.sistema.puede_acceder(" p001 ", "lab01"))
        self.assertTrue(self.sistema.existe_laboratorio(" lab01 "))
        self.sistema.revocar_autorizacion("p001", "lab01")
        self.assertFalse(self.sistema.puede_acceder("P001", "LAB01"))

    def test_INT_06_comparar_via_sistema_sin_efectos(self) -> None:
        for lab in ("LAB01", "LAB02", "LAB03"):
            self.sistema.autorizar_laboratorio("P001", lab)
        self.sistema.registrar_laboratorio(Laboratorio("LAB05", "Bases de Datos", 40, "D"))
        for lab in ("LAB02", "LAB03", "LAB05"):
            self.sistema.autorizar_laboratorio("P002", lab)

        r = self.sistema.comparar_autorizaciones("P001", "P002")

        self.assertEqual(r["union"], {"LAB01", "LAB02", "LAB03", "LAB05"})
        self.assertEqual(r["interseccion"], {"LAB02", "LAB03"})
        self.assertEqual(r["diferencia_a_b"], {"LAB01"})
        self.assertEqual(r["diferencia_b_a"], {"LAB05"})
        self.assertEqual(self.sistema.buscar_persona("P001").laboratorios_autorizados,
                         {"LAB01", "LAB02", "LAB03"})
        self.assertEqual(self.sistema.buscar_persona("P002").laboratorios_autorizados,
                         {"LAB02", "LAB03", "LAB05"})

    def test_INT_07_un_error_no_altera_el_estado(self) -> None:
        self.sistema.autorizar_laboratorio("P001", "LAB01")
        with self.assertRaises(ValueError):
            self.sistema.autorizar_laboratorio("P001", "LAB01")  # duplicado
        with self.assertRaises(ValueError):
            self.sistema.registrar_persona("P001", "Otro", "Nombre")  # clave repetida
        with self.assertRaises(ValueError):
            self.sistema.registrar_laboratorio(Laboratorio("LAB01", "Otro", 5, "Z"))
        persona = self.sistema.buscar_persona("P001")
        self.assertEqual(persona.apellidos, "Pérez")
        self.assertEqual(persona.laboratorios_autorizados, {"LAB01"})
        self.assertEqual(self.sistema.buscar_laboratorio("LAB01").nombre, "Programación")

    def test_INT_08_datos_demo_y_sistemas_independientes(self) -> None:
        demo = SistemaAcceso()
        cargar_datos_demo(demo)
        for codigo in ("LAB01", "LAB02", "LAB03", "LAB04", "LAB05"):
            self.assertTrue(demo.existe_laboratorio(codigo))
        self.assertTrue(demo.existe_persona("P001"))
        self.assertTrue(demo.existe_persona("P002"))
        # Otro sistema nuevo no comparte datos con el demo.
        vacio = SistemaAcceso()
        self.assertFalse(vacio.existe_laboratorio("LAB01"))
        self.assertEqual(vacio.listar_personas(), [])

    def test_INT_09_modificar_via_sistema_conserva_permisos(self) -> None:
        self.sistema.autorizar_laboratorio("P001", "LAB01")
        self.sistema.modificar_persona("P001", "Rojas", "Luis")
        self.sistema.modificar_laboratorio("LAB01", "Programación Avanzada", 35, "B")
        persona = self.sistema.buscar_persona("P001")
        self.assertEqual(persona.apellidos, "Rojas")
        self.assertEqual(persona.laboratorios_autorizados, {"LAB01"})
        lab = self.sistema.buscar_laboratorio("LAB01")
        self.assertEqual((lab.nombre, lab.capacidad, lab.pabellon), ("Programación Avanzada", 35, "B"))
        self.assertEqual(lab.codigo, "LAB01")


if __name__ == "__main__":
    unittest.main(verbosity=2)