class Laboratorio:
    
    def __init__(self, codigo: str, nombre: str, capacidad: int, pabellon: str) -> None:
        if codigo.strip() == "":
            raise ValueError("El codigo no puede estar vacio")
        self.__codigo: str = codigo.strip()
        self.nombre = nombre
        self.capacidad = capacidad
        self.pabellon = pabellon

    @property
    def codigo(self) -> str:
        return self.__codigo

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, nombre: str) -> None:
        if nombre.strip() == "":
            raise ValueError("El nombre no puede estar vacio")
        self.__nombre: str = nombre.strip()

    @property
    def capacidad(self) -> int:
        return self.__capacidad

    @capacidad.setter
    def capacidad(self, capacidad: int) -> None:
        if type(capacidad) is not int or capacidad <= 0:
            raise ValueError("La capacidad debe ser un entero positivo")
        self.__capacidad: int = capacidad

    @property
    def pabellon(self) -> str:
        return self.__pabellon

    @pabellon.setter
    def pabellon(self, pabellon: str) -> None:
        if pabellon.strip() == "":
            raise ValueError("El pabellon no puede estar vacio")
        self.__pabellon: str = pabellon.strip()

    def __str__(self) -> str:
        return (
            f"Codigo: {self.codigo} | Nombre: {self.nombre} | "
            f"Capacidad: {self.capacidad} | Pabellon: {self.pabellon}"
        )
