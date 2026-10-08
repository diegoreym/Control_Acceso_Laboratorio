import sys
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from laboratorio import Laboratorio
import operaciones_laboratorios as operaciones

class TestOperacionesLaboratorios(unittest.TestCase):
    def setUp(self) -> None:
        self.laboratorios: dict[str, Laboratorio] = {}
        self.laboratorio = Laboratorio("LAB01", "Programacion", 30, "A")
        operaciones.registrar_laboratorio(self.laboratorios, self.laboratorio)

    def test_registrar(self) -> None:
        self.assertEqual(len(self.laboratorios), 1)
        self.assertIs(self.laboratorios["LAB01"], self.laboratorio)

    def test_map_vacio(self) -> None:
        laboratorios: dict[str, Laboratorio] = {}
        self.assertEqual(len(laboratorios), 0)
        self.assertIsNone(operaciones.buscar_laboratorio(laboratorios, "LAB01"))
        with self.assertRaises(ValueError):
            operaciones.eliminar_laboratorio(laboratorios, "LAB01")
        with self.assertRaises(ValueError):
            operaciones.modificar_laboratorio(laboratorios, "LAB01", "Redes", 20, "B")
        with self.assertRaises(ValueError):
            operaciones.listar_laboratorios(laboratorios)

    def test_varias_entradas(self) -> None:
        otro = Laboratorio("LAB02", "Redes", 20, "B")
        operaciones.registrar_laboratorio(self.laboratorios, otro)
        self.assertEqual(len(self.laboratorios), 2)
        self.assertIs(operaciones.buscar_laboratorio(self.laboratorios, "LAB02"), otro)
        operaciones.eliminar_laboratorio(self.laboratorios, "LAB01")
        self.assertIs(self.laboratorios["LAB02"], otro)

    def test_rechazar_duplicado(self) -> None:
        with self.assertRaises(ValueError):
            operaciones.registrar_laboratorio(self.laboratorios, self.laboratorio)

    def test_buscar(self) -> None:
        self.assertIs(
            operaciones.buscar_laboratorio(self.laboratorios, "LAB01"),self.laboratorio)
        self.assertIsNone(operaciones.buscar_laboratorio(self.laboratorios, "LAB99"))

    def test_modificar(self) -> None:
        operaciones.modificar_laboratorio(self.laboratorios, "LAB01", "Redes", 20, "B")
        self.assertEqual(self.laboratorio.nombre, "Redes")
        self.assertEqual(self.laboratorio.capacidad, 20)
        self.assertEqual(self.laboratorio.pabellon, "B")
        self.assertEqual(self.laboratorio.codigo, "LAB01")
        self.assertIs(self.laboratorios["LAB01"], self.laboratorio)

    def test_capacidad_invalida(self) -> None:
        for capacidad in (0, -1):
            with self.subTest(capacidad=capacidad):
                with self.assertRaises(ValueError):
                    Laboratorio("LAB02", "Redes", capacidad, "B")
                with self.assertRaises(ValueError):
                    operaciones.modificar_laboratorio(self.laboratorios, "LAB01", "Redes", capacidad, "B")

    def test_eliminar(self) -> None:
        with self.assertRaises(ValueError):
            operaciones.eliminar_laboratorio(self.laboratorios, "LAB99")
        operaciones.eliminar_laboratorio(self.laboratorios, "LAB01")
        self.assertNotIn("LAB01", self.laboratorios)

    def test_listar(self) -> None:
        salida = StringIO()
        with redirect_stdout(salida):
            operaciones.listar_laboratorios(self.laboratorios)
        self.assertIn(f"{'LAB01':<12} | Programacion | 30 | A", salida.getvalue())

if __name__ == "__main__":
    unittest.main(verbosity=2)

