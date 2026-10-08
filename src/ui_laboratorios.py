from laboratorio import Laboratorio
from sistema_acceso import SistemaAcceso

def leer_entero(mensaje: str) -> int:
    try:
        return int(input(mensaje).strip())
    except ValueError:
        raise ValueError("Ingrese un numero entero") from None

def leer_cadena(mensaje: str) -> str:
    cadena = input(mensaje).strip()
    if cadena == "":
        raise ValueError("El dato no puede estar vacio")
    return cadena

class UILaboratorios:
    def __init__(self, sistema: SistemaAcceso) -> None:
        self.sistema = sistema

    def ejecutar(self) -> None:
        while True:
            try:
                print("=" * 10 + " SUBMENU - LABORATORIOS " + "=" * 10)
                print("1. Registrar laboratorio")
                print("2. Buscar laboratorio")
                print("3. Comprobar si existe")
                print("4. Modificar laboratorio")
                print("5. Eliminar laboratorio")
                print("6. Listar laboratorios")
                print("7. Demostrar conteo de frecuencias")
                print("0. Volver al menu principal")
                opcion = leer_entero("Ingrese una opcion: ")

                match opcion:
                    case 1:
                        codigo = leer_cadena("Codigo: ")
                        nombre = leer_cadena("Nombre: ")
                        capacidad = leer_entero("Capacidad: ")
                        pabellon = leer_cadena("Pabellon: ")
                        laboratorio = Laboratorio(codigo, nombre, capacidad, pabellon)
                        self.sistema.registrar_laboratorio(laboratorio)
                        print("Laboratorio registrado")
                    case 2:
                        codigo = leer_cadena("Codigo a buscar: ")
                        laboratorio = self.sistema.buscar_laboratorio(codigo)
                        if laboratorio is None:
                            print("Laboratorio inexistente")
                        else:
                            print(laboratorio)
                    case 3:
                        codigo = leer_cadena("Codigo a comprobar: ")
                        if self.sistema.existe_laboratorio(codigo):
                            print("El laboratorio existe")
                        else:
                            print("El laboratorio no existe")
                    case 4:
                        codigo = leer_cadena("Codigo a modificar: ")
                        nombre = leer_cadena("Nuevo nombre: ")
                        capacidad = leer_entero("Nueva capacidad: ")
                        pabellon = leer_cadena("Nuevo pabellon: ")
                        self.sistema.modificar_laboratorio(codigo, nombre, capacidad, pabellon)
                        print("Laboratorio modificado")
                    case 5:
                        codigo = leer_cadena("Codigo a eliminar: ")
                        self.sistema.eliminar_laboratorio(codigo)
                        print("Laboratorio eliminado")
                    case 6:
                        self.sistema.listar_laboratorios()
                    case 7:
                        datos: list[str] = []
                        while True:
                            codigo = input("Codigo (Enter para terminar): ").strip()
                            if codigo == "":
                                break
                            datos.append(codigo)
                        frecuencias = self.sistema.contar_frecuencias(datos)
                        print(frecuencias)
                    case 0:
                        return
                    case _:
                        print("Opcion fuera de rango")
            except (ValueError, KeyError) as error:
                print(f"Error ({type(error).__name__}): {error}")

if __name__ == "__main__":
    from datos_demo import cargar_datos_demo
    sistema = SistemaAcceso()
    cargar_datos_demo(sistema)
    UILaboratorios(sistema).ejecutar()
