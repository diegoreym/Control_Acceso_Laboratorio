from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sistema_acceso import SistemaAcceso


class UIPersonas:
    def __init__(self, sistema: SistemaAcceso) -> None:
        self.sistema = sistema

    def leer_codigo(self, mensaje: str) -> str:
        return input(mensaje).strip().upper()

    def ejecutar(self) -> None:
        while True:
            try:
                print("\n" + "=" * 45)
                print("   SUBMENÚ - PERSONAS (MAP)")
                print("=" * 45)
                print("1. Registrar persona")
                print("2. Buscar persona")
                print("3. Verificar existencia de persona")
                print("4. Modificar apellidos y nombres")
                print("5. Eliminar persona")
                print("6. Listar personas")
                print("0. Volver al menú principal")

                opcion = input("Seleccione una opción: ").strip()

                if opcion == "1":
                    codigo = self.leer_codigo("Código de la persona: ")
                    apellidos = input("Apellidos: ")
                    nombres = input("Nombres: ")
                    self.sistema.registrar_persona(codigo, apellidos, nombres)
                    print(f"Persona {codigo} registrada correctamente.")

                elif opcion == "2":
                    codigo = self.leer_codigo("Código de la persona: ")
                    persona = self.sistema.buscar_persona(codigo)
                    print(persona)

                elif opcion == "3":
                    codigo = self.leer_codigo("Código de la persona: ")
                    if self.sistema.existe_persona(codigo):
                        print(f"La persona {codigo} está registrada.")
                    else:
                        print(f"La persona {codigo} no está registrada.")

                elif opcion == "4":
                    codigo = self.leer_codigo("Código de la persona: ")
                    apellidos = input("Nuevos apellidos: ")
                    nombres = input("Nuevos nombres: ")
                    self.sistema.modificar_persona(codigo, apellidos, nombres)
                    print(f"Persona {codigo} modificada correctamente.")

                elif opcion == "5":
                    codigo = self.leer_codigo("Código de la persona: ")
                    self.sistema.eliminar_persona(codigo)
                    print(f"Persona {codigo} eliminada correctamente.")

                elif opcion == "6":
                    personas = self.sistema.listar_personas()
                    if not personas:
                        print("No hay personas registradas.")
                    for persona in personas:
                        print(f"{persona.codigo} -> {persona}")

                elif opcion == "0":
                    print("Volviendo al menú principal...")
                    return

                else:
                    print("Opción inválida. Ingrese un número del 0 al 6.")

            except KeyError as error:
                print(f"Error de búsqueda: {error.args[0]}")
            except ValueError as error:
                print(f"Error de validación: {error}")
            except (EOFError, KeyboardInterrupt):
                print("\nCerrando submenú de personas...")
                return


if __name__ == "__main__":
    from sistema_acceso import SistemaAcceso
    from datos_demo import cargar_datos_demo

    sistema = SistemaAcceso()
    cargar_datos_demo(sistema)
    UIPersonas(sistema).ejecutar()
