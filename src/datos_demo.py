
from laboratorio import Laboratorio
from sistema_acceso import SistemaAcceso


def cargar_datos_demo(sistema: SistemaAcceso) -> None:
    #Carga LAB01-LAB05 y P001-P002 en un sistema nuevo (sin autorizaciones).
    laboratorios = [
        Laboratorio("LAB01", "Laboratorio de Programación", 30, "A"),
        Laboratorio("LAB02", "Laboratorio de Redes", 25, "B"),
        Laboratorio("LAB03", "Laboratorio de IA", 20, "C"),
        Laboratorio("LAB04", "Laboratorio de Hardware", 15, "D"),
        Laboratorio("LAB05", "Laboratorio de Bases de Datos", 40, "E"),
    ]
    for laboratorio in laboratorios:
        sistema.registrar_laboratorio(laboratorio)

    sistema.registrar_persona("P001", "Pérez", "Juan")
    sistema.registrar_persona("P002", "Gómez", "Ana")