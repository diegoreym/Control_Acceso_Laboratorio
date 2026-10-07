import sys
import unittest
from pathlib import Path
# Permite importar los archivos desde la carpeta principal del proyecto
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from persona import Persona
from laboratorio import Laboratorio 
from operaciones_autorizaciones import (
    autorizar_laboratorio,
    revocar_autorizacion,
    puede_acceder,
    comparar_autorizaciones
)

class TestAutorizaciones(unittest.TestCase):
    def setUp(self) -> None:
        """Preparación del entorno de pruebas con objetos reales antes de cada test."""
        self.personas: dict[str, Persona] = {}
        self.laboratorios: dict[str, Laboratorio] = {} 

        self.laboratorios["LAB01"] = Laboratorio("LAB01", "Laboratorio de Programación", 30, "A")
        self.laboratorios["LAB02"] = Laboratorio("LAB02", "Laboratorio de Redes", 25, "B")
        self.laboratorios["LAB03"] = Laboratorio("LAB03", "Laboratorio de IA", 20, "C")
        self.laboratorios["LAB05"] = Laboratorio("LAB05", "Laboratorio de Bases de Datos", 40, "D")
        self.personas["P001"] = Persona("P001", "Pérez", "Juan")
        self.personas["P002"] = Persona("P002", "Gómez", "Ana")

    # =================================================================
    # AUT-01: Pruebas de Autorización y Duplicados
    # =================================================================
    def test_autorizar_valido_y_duplicado(self) -> None:
        autorizar_laboratorio(self.personas, self.laboratorios, "P001", "LAB01")
        self.assertTrue(puede_acceder(self.personas, self.laboratorios, "P001", "LAB01"))

        with self.assertRaises(ValueError):
            autorizar_laboratorio(self.personas, self.laboratorios, "P001", "LAB01")

    # =================================================================
    # AUT-02: Pruebas de Revocación
    # =================================================================
    def test_revocar_existente_e_inexistente(self) -> None:
        autorizar_laboratorio(self.personas, self.laboratorios, "P001", "LAB02")
        
        revocar_autorizacion(self.personas, self.laboratorios, "P001", "LAB02")
        self.assertFalse(puede_acceder(self.personas, self.laboratorios, "P001", "LAB02"))

        with self.assertRaises(ValueError):
            revocar_autorizacion(self.personas, self.laboratorios, "P001", "LAB02")

    # =================================================================
    # AUT-03: Pruebas de Registros Inexistentes (KeyError)
    # =================================================================
    def test_operar_con_registros_inexistentes(self) -> None:
        with self.assertRaises(KeyError):
            autorizar_laboratorio(self.personas, self.laboratorios, "P999", "LAB01")
        
        with self.assertRaises(KeyError):
            autorizar_laboratorio(self.personas, self.laboratorios, "P001", "LAB99")

    # =================================================================
    # AUT-04: Demostración PARTE B (Comparación de Sets)
    # =================================================================
    def test_comparacion_parte_b_y_ausencia_efectos(self) -> None:
        for lab in ["LAB01", "LAB02", "LAB03"]:
            autorizar_laboratorio(self.personas, self.laboratorios, "P001", lab)
            
        for lab in ["LAB02", "LAB03", "LAB05"]:
            autorizar_laboratorio(self.personas, self.laboratorios, "P002", lab)

        resultado = comparar_autorizaciones(self.personas, "P001", "P002")

        self.assertEqual(resultado["union"], {"LAB01", "LAB02", "LAB03", "LAB05"})
        self.assertEqual(resultado["interseccion"], {"LAB02", "LAB03"})
        self.assertEqual(resultado["diferencia_a_b"], {"LAB01"})
        self.assertEqual(resultado["diferencia_b_a"], {"LAB05"})

        self.assertEqual(self.personas["P001"].laboratorios_autorizados, {"LAB01", "LAB02", "LAB03"})
        self.assertEqual(self.personas["P002"].laboratorios_autorizados, {"LAB02", "LAB03", "LAB05"})

if __name__ == "__main__":
    unittest.main(verbosity=2)
