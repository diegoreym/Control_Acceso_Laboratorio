from laboratorio import Laboratorio

def registrar_laboratorio(laboratorios:dict[str,Laboratorio],laboratorio:Laboratorio)->None:
    if laboratorio.codigo in laboratorios:
        raise ValueError("Existe un laboratorio con ese codigo")
    laboratorios[laboratorio.codigo]=laboratorio

def buscar_laboratorio(laboratorios:dict[str,Laboratorio],codigo:str)->Laboratorio|None:
    return laboratorios.get(codigo)

def existe_laboratorio(laboratorios:dict[str,Laboratorio],codigo:str)->bool:
    return codigo in laboratorios

def modificar_laboratorio(laboratorios:dict[str,Laboratorio],codigo:str,nombre:str,capacidad:int,pabellon:str)->None:
    if not laboratorios:
        raise ValueError("No hay laboratorios")
    laboratorio = buscar_laboratorio(laboratorios, codigo)
    if laboratorio is None:
        raise ValueError("Laboratorio inexistente")
    else:
        datos = Laboratorio(codigo, nombre, capacidad, pabellon)
        laboratorio.nombre = datos.nombre
        laboratorio.capacidad = datos.capacidad
        laboratorio.pabellon = datos.pabellon

def eliminar_laboratorio(laboratorios:dict[str,Laboratorio],codigo:str)->None:
    if not laboratorios:
        raise ValueError("No hay laboratorios")
    elif codigo not in laboratorios:
        raise ValueError("Laboratorio inexistente")
    else:
        del laboratorios[codigo]
    
def listar_laboratorios(laboratorios:dict[str,Laboratorio])->None:
    if not laboratorios:
        raise ValueError("No hay laboratorios")
    print(f"{'Clave':<12} | Valor")
    print("-" * 30)
    for codigo in laboratorios:
        print(
        f"{codigo:<12} | "
        f"{laboratorios[codigo].nombre} | "
        f"{laboratorios[codigo].capacidad} | "
        f"{laboratorios[codigo].pabellon}"
        )     
 