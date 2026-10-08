class Persona:

    def __init__(self,codigo: str,apellidos: str,nombres: str) -> None:
        if not isinstance(codigo, str) or not codigo.strip():
            raise ValueError("El codigo debe ser un texto no vacio")

        self.__codigo: str = codigo.strip().upper()

        self.apellidos = apellidos
        self.nombres = nombres

        # Cada persona crea su propio conjunto de autorizaciones
        self.__laboratorios_autorizados: set[str] = set()

    @property
    def codigo(self) -> str:
        """Retorna el codigo de la persona."""
        return self.__codigo

    @property
    def apellidos(self) -> str:
        """Retorna los apellidos de la persona."""
        return self.__apellidos

    @apellidos.setter
    def apellidos(self, apellidos: str) -> None:
        if not isinstance(apellidos, str) or not apellidos.strip():
            raise ValueError("Los apellidos deben ser un texto no vacio")

        self.__apellidos: str = apellidos.strip()

    @property
    def nombres(self) -> str:
        """Retorna los nombres de la persona."""
        return self.__nombres

    @nombres.setter
    def nombres(self, nombres: str) -> None:
        if not isinstance(nombres, str) or not nombres.strip():
            raise ValueError("Los nombres deben ser un texto no vacio")

        self.__nombres: str = nombres.strip()

    @property
    def laboratorios_autorizados(self) -> set[str]:
        """Retorna una copia de los laboratorios autorizados."""
        return self.__laboratorios_autorizados.copy()

    def agregar_laboratorio(self, codigo_laboratorio: str) -> None:
        """Agrega un laboratorio al conjunto de autorizaciones."""
        self.__laboratorios_autorizados.add(codigo_laboratorio)

    def retirar_laboratorio(self, codigo_laboratorio: str) -> None:
        """Retira un laboratorio del conjunto de autorizaciones."""
        self.__laboratorios_autorizados.discard(codigo_laboratorio)

    def tiene_laboratorio(self, codigo_laboratorio: str) -> bool:
        """Indica si la persona tiene autorizado un laboratorio."""
        return codigo_laboratorio in self.__laboratorios_autorizados

    def __str__(self) -> str:
        return (
            f"Codigo: {self.codigo} | "
            f"Apellidos: {self.apellidos} | "
            f"Nombres: {self.nombres}"
        )
