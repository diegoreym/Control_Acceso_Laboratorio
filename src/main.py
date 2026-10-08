from sistema_acceso import SistemaAcceso
from datos_demo import cargar_datos_demo
from ui_laboratorios import UILaboratorios
from ui_personas import UIPersonas
from ui_autorizaciones import UIAutorizaciones


def main() -> None:
    # Una sola instancia 
    sistema = SistemaAcceso()
    cargar_datos_demo(sistema)

    ui_lab = UILaboratorios(sistema)
    ui_per = UIPersonas(sistema)
    ui_aut = UIAutorizaciones(sistema)

    while True:
        print("\n" + "=" * 45)
        print("   CONTROL DE ACCESO A LABORATORIOS")
        print("=" * 45)
        print("1. Laboratorios")
        print("2. Personas")
        print("3. Autorizaciones")
        print("0. Salir")
        print("=" * 45)

        try:
            opcion = input("Seleccione una opción: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSaliendo del sistema...")
            return

        if opcion == "1":
            ui_lab.ejecutar()
        elif opcion == "2":
            ui_per.ejecutar()
        elif opcion == "3":
            ui_aut.ejecutar()
        elif opcion == "0":
            print("Saliendo del sistema...")
            return
        else:
            print("Opción inválida. Ingrese un número del 0 al 3.")


if __name__ == "__main__":
    main()

