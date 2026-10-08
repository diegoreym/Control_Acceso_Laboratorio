class Laboratorio:

    def __init__(
        self,
        codigo: str,
        nombre: str,
        capacidad: int,
        pabellon: str
    ) -> None:
        # Validar código
        if not isinstance(codigo, str) or not codigo.strip():
            raise ValueError("El codigo debe ser un texto no vacio")

        self.__codigo: str = codigo.strip().upper()

        # Los setters realizan las validaciones correspondientes
        self.nombre = nombre
        self.capacidad = capacidad
        self.pabellon = pabellon

    @property
    def codigo(self) -> str:
        """Retorna el codigo del laboratorio."""
        return self.__codigo

    @property
    def nombre(self) -> str:
        """Retorna el nombre del laboratorio."""
        return self.__nombre

    @nombre.setter
    def nombre(self, nombre: str) -> None:
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre debe ser un texto no vacio")

        self.__nombre: str = nombre.strip()

    @property
    def capacidad(self) -> int:
        """Retorna la capacidad maxima del laboratorio."""
        return self.__capacidad

    @capacidad.setter
    def capacidad(self, capacidad: int) -> None:
        if not isinstance(capacidad, int) or isinstance(capacidad, bool):
            raise ValueError("La capacidad debe ser un numero entero")

        if capacidad <= 0:
            raise ValueError("La capacidad debe ser mayor que cero")

        self.__capacidad: int = capacidad

    @property
    def pabellon(self) -> str:
        """Retorna el pabellon donde se encuentra el laboratorio."""
        return self.__pabellon

    @pabellon.setter
    def pabellon(self, pabellon: str) -> None:
        if not isinstance(pabellon, str) or not pabellon.strip():
            raise ValueError("El pabellon debe ser un texto no vacio")

        self.__pabellon: str = pabellon.strip()

    def __str__(self) -> str:
        return (
            f"Codigo: {self.codigo} | "
            f"Nombre: {self.nombre} | "
            f"Capacidad: {self.capacidad} | "
            f"Pabellon: {self.pabellon}"
        )