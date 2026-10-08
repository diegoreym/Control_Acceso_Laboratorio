from sistema_acceso import SistemaAcceso

try:
    from datos_demo import cargar_datos_demo
except ImportError:
    cargar_datos_demo = None

class UIAutorizaciones:
    def __init__(self, sistema: SistemaAcceso) -> None:
     
        self.sistema = sistema

    def leer_codigo(self, mensaje: str) -> str:
        return input(mensaje).strip().upper()

    def ejecutar(self) -> None:
        while True:
            try:
                print("\n" + "=" * 45)
                print("   SUBMENÚ - AUTORIZACIONES (SET)")
                print("=" * 45)
                print("1. Autorizar acceso a laboratorio")
                print("2. Revocar autorización")
                print("3. Consultar acceso de una persona")
                print("4. Comparar autorizaciones (A y B)")
                print("0. Volver al menú principal")
                print("=" * 45)
                
                opcion = input("Seleccione una opción: ").strip()

                if opcion == "1":
                    cod_per = self.leer_codigo("Ingrese código de la persona: ")
                    cod_lab = self.leer_codigo("Ingrese código del laboratorio: ")
                    if cod_per and cod_lab:
                        self.sistema.autorizar_laboratorio(cod_per, cod_lab)
                        print(f" Éxito: {cod_per} autorizado para el laboratorio {cod_lab}.")

                elif opcion == "2":
                    cod_per = self.leer_codigo("Ingrese código de la persona: ")
                    cod_lab = self.leer_codigo("Ingrese código del laboratorio: ")
                    if cod_per and cod_lab:
                        self.sistema.revocar_autorizacion(cod_per, cod_lab)
                        print(f" Éxito: Autorización revocada a {cod_per} para {cod_lab}.")

                elif opcion == "3":
                    cod_per = self.leer_codigo("Ingrese código de la persona: ")
                    cod_lab = self.leer_codigo("Ingrese código del laboratorio: ")
                    if cod_per and cod_lab:
                        acceso = self.sistema.puede_acceder(cod_per, cod_lab)
                        if acceso:
                            print(f"RESULTADO: {cod_per} SÍ TIENE acceso a {cod_lab}.")
                        else:
                            print(f"RESULTADO: {cod_per} NO TIENE acceso a {cod_lab}.")

                elif opcion == "4":
                    cod_a = self.leer_codigo("Ingrese código de la Persona A: ")
                    cod_b = self.leer_codigo("Ingrese código de la Persona B: ")
                    if cod_a and cod_b:
                        resultados = self.sistema.comparar_autorizaciones(cod_a, cod_b)
                        print(f"\n--- COMPARACIÓN MATEMÁTICA DE SETS ---")
                        print(f"Comparando accesos: {cod_a} vs {cod_b}")
                        print(f"Unión (A | B)        : {resultados['union']}")
                        print(f"Intersección (A & B) : {resultados['interseccion']}")
                        print(f"Diferencia (A - B)   : {resultados['diferencia_a_b']}")
                        print(f"Diferencia (B - A)   : {resultados['diferencia_b_a']}")
                        print(f"Dif. Simétrica (A ^ B) : {resultados['diferencia_simetrica']}")
                elif opcion == "0":
                    print("Cerrando submenú de autorizaciones...")
                    return
                else:
                    print(" Opción inválida. Ingrese un número del 0 al 4.")

           
            except KeyError as error:
                print(f" Error de Búsqueda: {error}")
            except ValueError as error:
                print(f" Error de Validación: {error}")
            except Exception as error:
                print(f" Error inesperado: {error}")

if __name__ == "__main__":
    sistema_test = SistemaAcceso()
    if cargar_datos_demo:
        cargar_datos_demo(sistema_test)
    else:
        print(" Iniciando con sistema vacío (datos_demo.py no encontrado).")
    
    app = UIAutorizaciones(sistema_test)
    app.ejecutar()
