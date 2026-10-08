
def contar_frecuencias(self, datos: list[str]) -> dict[str, int]:
    frecuencias: dict[str, int] = {}
    for codigo in datos:
        if codigo in frecuencias:
            cantidad = frecuencias[codigo]
            frecuencias[codigo] = cantidad + 1
        else:
            frecuencias[codigo] = 1
    return frecuencias
