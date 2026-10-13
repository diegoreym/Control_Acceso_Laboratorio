# Aporte de Diego al Map de personas

La implementación registra personas mediante asociaciones `CódigoPersona -> Persona` y permite buscar, verificar existencia, modificar, eliminar y listar. La modificación conserva la identidad del objeto, su código y sus autorizaciones. Las pruebas usan `unittest`, como las pruebas de autorizaciones existentes.

## Archivos y responsabilidad

- [operaciones_personas.py](../src/operaciones_personas.py): seis operaciones y validación de entradas.
- [ui_personas.py](../src/ui_personas.py): clase `UIPersonas`, con el sistema recibido en `self.sistema` y submenú mediante `ejecutar() -> None`.
- [test_personas.py](../src/tests/test_personas.py): 20 pruebas sencillas de operaciones del Map y conservación de datos y autorizaciones, con `unittest.TestCase` y objetos `Persona` reales.
- [evidencias_diego.txt](evidencias_diego.txt): salida real de la demostración con estados anteriores y posteriores e identificadores PER.

Se utiliza el modelo `Persona` disponible. Los archivos de modelos, laboratorios, autorizaciones e integración corresponden a los demás integrantes.

## Contrato para integrar con SistemaAcceso

Todas las funciones reciben como primer argumento el mismo `personas: dict[str, Persona]` mantenido por el sistema. Las firmas y el orden de parámetros son:

```python
registrar_persona(personas: dict[str, Persona], codigo: str,
                  apellidos: str, nombres: str) -> None
buscar_persona(personas: dict[str, Persona], codigo: str) -> Persona
existe_persona(personas: dict[str, Persona], codigo: str) -> bool
modificar_persona(personas: dict[str, Persona], codigo: str,
                  apellidos: str, nombres: str) -> None
eliminar_persona(personas: dict[str, Persona], codigo: str) -> None
listar_personas(personas: dict[str, Persona]) -> list[Persona]
```

Los métodos públicos de `SistemaAcceso` deben recibir esos parámetros sin el diccionario y delegar en estas funciones pasando `self._personas`. Por ejemplo, `sistema.modificar_persona("P001", "Rojas", "Luis")` debe delegar en `operaciones_personas.modificar_persona(self._personas, "P001", "Rojas", "Luis")`.

El registro agrega una asociación al diccionario recibido; no crea otro registro independiente. La búsqueda devuelve el objeto almacenado. El listado devuelve una lista nueva con esos mismos objetos, por lo que vaciar la lista no elimina asociaciones. No se exige un orden conceptual para el Map.

Los códigos se limpian de espacios exteriores y se convierten a mayúsculas. Se aceptan letras y números mediante `str.isalnum()`, sin imponer el prefijo P ni una longitud fija. Los códigos vacíos, con espacios internos, signos o tipos distintos de `str` producen `ValueError`. Un código repetido también produce `ValueError`; buscar, modificar o eliminar un código válido no registrado produce `KeyError`. La consulta de existencia devuelve `False` para un código válido no registrado.

Apellidos y nombres deben ser textos no vacíos y se limpian de espacios exteriores. Se validan ambos campos antes de asignarlos a la persona. Así, intentar cambiar los apellidos mientras se suministra un nombre inválido conserva todos los datos previos. No se admite cambiar el código ni se reemplaza la persona por otra con permisos vacíos.

## Submenú y ejecución

Las opciones son registrar, buscar, verificar existencia, modificar apellidos y nombres, eliminar, listar y volver mediante la opción `0`. La UI recoge datos y llama exclusivamente a los seis métodos públicos del sistema. Captura `ValueError` y `KeyError`, muestra sus mensajes y permite continuar. `0` termina con `return`; el fin de entrada o una interrupción también devuelven el control.

Desde `Control_Acceso_Laboratorio/src`:

```powershell
# Solo las pruebas de Diego
python -m unittest discover -s tests -p test_personas.py -v

# Todas las pruebas existentes
python -m unittest discover -s tests -v

# Submenú independiente, cuando estén disponibles los módulos de integración
python ui_personas.py
```

Al realizar esta entrega, `sistema_acceso.py` y `datos_demo.py` están vacíos en `src/tests/`; aún no existe su implementación importable desde `src`. La UI usa una importación normal de `SistemaAcceso`, por lo que su ejecución depende de que Garrido entregue esa clase con el contrato indicado. La carga de demostración es opcional: si `datos_demo` o `cargar_datos_demo` no se pueden importar, captura `ImportError`, muestra un aviso e inicia con el sistema vacío; si están disponibles, carga los datos antes de ejecutar la UI.

Las pruebas actuales importan únicamente las operaciones de personas y el modelo `Persona`; no necesitan iniciar el menú ni disponer de `SistemaAcceso`. La verificación del submenú queda separada de estas pruebas de operaciones y podrá realizarse cuando esté disponible la integración.

## Pruebas ejecutadas

Se ejecutó `python -B -m unittest discover -s tests -v` desde `src`, con Python 3 el 7 de octubre de 2026. Resultado: **24 pruebas ejecutadas, todas aprobadas**: 20 de Diego y 4 de autorizaciones que ya existían.

Preparación común: `setUp()` crea un diccionario vacío antes de cada prueba. Cada método registra las personas que necesita, llama directamente a la operación y comprueba el resultado con métodos de `unittest`, como `assertEqual`, `assertIs` y `assertRaises`. Los casos con varias entradas inválidas usan un bucle sencillo y `subTest` para identificar el dato que falló. Las pruebas no usan objetos simulados, entradas automáticas, captura de pantalla ni ejecución de otros módulos.

| ID | Preparación | Estado anterior | Operación | Resultado esperado | Resultado obtenido | Aprobación |
| --- | --- | --- | --- | --- | --- | --- |
| PER-01 | Map nuevo | Vacío | Listar, verificar, buscar y eliminar P001 | Lista vacía, False y KeyError; Map intacto | Resultados esperados y Map vacío | Aprobada |
| PER-02 | Map nuevo | Vacío | Registrar P001 y listar | Persona con código, nombres y Set vacío | P001/Pérez/Juan; un objeto y Set vacío | Aprobada |
| PER-03 | Map nuevo | Vacío | Registrar P001, P002 y P003 con datos personales iguales | Tres asociaciones; permitir datos repetidos | Tres registros y listado correcto sin exigir orden | Aprobada |
| PER-04 | Textos con espacios y minúsculas | Vacío | Registrar, buscar, verificar, modificar y eliminar | Código P001 y textos limpios | Normalización correcta; Map vacío al terminar | Aprobada |
| PER-05 | Registrar P001 y agregar LAB01 | P001/Pérez/Juan con permiso | Registrar P001 y « p001 » otra vez | ValueError; conservar datos y permiso | Duplicados rechazados; registro intacto | Aprobada |
| PER-06 | Registrar P001 y agregar LAB01 | Un registro válido | Usar nueve códigos inválidos en las cinco operaciones con código | ValueError en cada caso; sin cambios | Todos los subcasos rechazados; datos y permiso conservados | Aprobada |
| PER-07 | Registrar P001 y agregar LAB01 | Un registro válido | Registrar P003 con apellidos o nombres inválidos | ValueError; no agregar P003 ni alterar P001 | Entradas rechazadas y P001 intacta | Aprobada |
| PER-08 | Registrar P001 | Una asociación | Buscar P001 | Retornar el objeto almacenado | Misma identidad | Aprobada |
| PER-09 | Registrar P001 | P999 ausente | Buscar P999 | KeyError con el código; Map intacto | Error esperado y conservación de P001 | Aprobada |
| PER-10 | Registrar P001 | P001 presente y P999 ausente | Verificar ambas claves | bool True y False | True y False | Aprobada |
| PER-11 | Registrar P001 y P002 con permisos | P001/Pérez/Juan con LAB01 y LAB03; P002/Gómez/Ana con LAB02 | Modificar P001 a Rojas/Luis | Mismo objeto, código y permisos; P002 intacta | Modificación correcta y conservación de ambas personas | Aprobada |
| PER-12 | Registrar P001 y agregar LAB01 | Datos válidos y permiso existente | Modificar con un campo válido y el otro inválido | ValueError; ninguna actualización parcial | Identidad, código, nombres y permiso conservados | Aprobada |
| PER-13 | Registrar P001 | P999 ausente | Modificar P999 | KeyError; P001 intacta | Error esperado; datos anteriores conservados | Aprobada |
| PER-14 | Registrar P001 y P002 con LAB01 y LAB02 | Dos asociaciones con permisos independientes | Registrar y eliminar P003 | Agregar y quitar solo P003 | P003 comienza sin permisos; P001 y P002 conservan datos y permisos | Aprobada |
| PER-15 | Registrar solo P001 | Una asociación | Eliminar P001 | Lista vacía y existencia False | Map vacío y False | Aprobada |
| PER-16 | Registrar P001 y agregar LAB01 | P999 ausente | Eliminar P999 | KeyError; conservar el registro válido | Error esperado; datos y permiso intactos | Aprobada |
| PER-17 | Registrar P001 y P002 | Dos asociaciones | Listar y vaciar la lista resultante | Listado correcto; Map conserva sus asociaciones | Dos objetos en el listado; Map intacto al vaciarlo | Aprobada |
| PER-18 | Registrar P001 y P002 | Dos objetos con Sets vacíos | Agregar permisos a ambos y retirar LAB01 de P001 | Sets independientes | P001 queda con LAB03 y P002 conserva LAB02 | Aprobada |
| PER-19 | Registrar P001 y agregar LAB01 | Un permiso | Vaciar la copia pública y agregar LAB99 a ella | Permisos internos intactos | P001 conserva solo LAB01 | Aprobada |
| PER-20 | Registrar P001 | Código fijo | Reasignar código y consultar str | AttributeError; representación con datos | Código conservado; P001, Pérez y Juan visibles | Aprobada |

## Evidencias de personas

[evidencias_diego.txt](evidencias_diego.txt) conserva la salida de una ejecución real adicional con estos permisos de demostración:

| Clave | Valor inicial | Autorizaciones |
| --- | --- | --- |
| P001 | Persona(P001, Pérez, Juan) | LAB01, LAB02, LAB03 |
| P002 | Persona(P002, Gómez, Ana) | LAB02, LAB03, LAB05 |

P001 y P002 son objetos distintos. Agregar temporalmente LAB04 a P001 deja los permisos de P002 intactos. Los permisos de esta evidencia se preparan mediante los métodos de `Persona`, por lo que la evidencia demuestra independencia de Sets; la validación del catálogo pertenece a autorizaciones.

En PER-14 se registra P003/Torres/Diego con un Set vacío. Tras eliminar P003, los datos y permisos de P001 y P002 coinciden con los iniciales. En PER-11, P001 cambia a Rojas/Luis conservando su referencia y los tres permisos. En PER-05, PER-12 y PER-16 se registran respectivamente los errores de duplicado, nombres vacíos y eliminación inexistente; en cada caso, el estado anterior es igual al posterior.

## Relación entre Map, objetos y modificación segura

El código identifica la asociación; el objeto `Persona` contiene los apellidos, nombres y el Set de códigos de laboratorios autorizados. Guardar un objeto como valor permite modificar sus datos sin cambiar la clave. La búsqueda devuelve ese mismo objeto, y la modificación utiliza sus propiedades públicas después de validar ambos textos. Se conserva así el vínculo que pueda mantener otro módulo con la persona y sus autorizaciones.

El Set pertenece a cada instancia. El constructor disponible crea un conjunto nuevo por persona y la propiedad pública devuelve una copia. Las pruebas PER-18 y PER-19 comprueban independencia y protección del estado sin acceder a atributos privados.

## Complejidad

Para `n` personas, considerando longitudes de textos acotadas:

| Operación sobre dict de Python | Tiempo promedio | Peor caso de acceso al dict | Espacio adicional |
| --- | --- | --- | --- |
| Registrar | O(1) amortizado | O(n) | O(1), más el objeto registrado |
| Buscar | O(1) | O(n) | O(1) |
| Verificar existencia | O(1) | O(n) | O(1) |
| Modificar | O(1) | O(n) | O(1), más los textos normalizados |
| Eliminar | O(1) | O(n) | O(1) |
| Listar | O(n) | O(n) | O(n) para la lista de referencias |

La normalización y validación recorren los textos; si sus longitudes varían, su coste se suma al de la operación sobre el diccionario. Las garantías anteriores corresponden a la implementación práctica con `dict`, no a cualquier implementación del TAD Map. El listado y las pruebas no dependen del orden conceptual de las asociaciones.

## Respuestas de análisis previo asignadas

**Pregunta 1. ¿Qué información debe representarse mediante CódigoPersona → Persona?**

Se representa el registro de personas que pueden solicitar acceso. Cada código apunta a una instancia con apellidos, nombres y sus autorizaciones. Por ejemplo, `personas["P001"]` contiene a Juan Pérez con su propio Set; no contiene únicamente un nombre ni una lista de laboratorios independiente de la persona.

**Pregunta 4. ¿Los valores de un Map tienen que ser únicos?**

No. La unicidad corresponde a las claves. Dos personas con códigos diferentes pueden tener los mismos nombres y apellidos sin impedir el registro. PER-03 registra P001, P002 y P003 con esos datos repetidos y verifica tres asociaciones. En esta implementación cada registro crea su propio objeto y Set; esa independencia es una decisión del dominio y no una regla general de unicidad de valores del TAD Map.

## Respuestas de sustentación asignadas

**Pregunta 2. ¿Qué objeto actúa como valor en cada Map?**

En el Map de personas el valor es un objeto `Persona`, como el creado por `registrar_persona` para P001. En el Map de laboratorios el valor corresponde a un objeto `Laboratorio`, que incluye código, nombre, capacidad y pabellón. Los códigos de autorizaciones se guardan como cadenas dentro del Set de la persona.

**Pregunta 4. ¿Qué diferencia existe entre clave y valor?**

La clave identifica una asociación para localizarla y debe ser única dentro del Map; aquí es una cadena como `"P001"`. El valor es la información asociada: el objeto `Persona`. Sus nombres y apellidos pueden cambiar mientras la clave permanece igual. PER-11 verifica que modificar esos datos conserva P001, el mismo objeto y sus permisos.

## Conclusión

Usar un Map de código a objeto permite localizar y administrar personas directamente, mientras cada Set conserva las autorizaciones de su instancia. Validar todos los datos antes de modificar y conservar el objeto original evita cambios parciales y pérdida de permisos. Los 20 casos de Diego ejecutados con `unittest` comprueban las operaciones del registro y sus casos límite mediante objetos reales y comprobaciones directas.

## Fuentes y revisión

- [Trabajo Aplicativo Caso 02](../../Trabajo_Aplicativo_Caso_2_Control_Acceso_Laboratorios_Map_Set.docx), apartados 3, 4, 5, 10, 11, 12 y 13: requisitos, restricciones, análisis y sustentación.
- [Reparto del proyecto](../../Reparto_Control_Acceso_Map_Set.pdf), páginas 2, 3, 5, 6 y 7: responsabilidad de Diego, modelos, contrato de UI, errores y aporte al informe.
- [Persona](../src/persona.py): constructor, propiedades y métodos usados sin modificar el modelo.
- [Pruebas existentes de autorizaciones](../src/tests/test_autorizaciones.py): referencia para organización y uso de `unittest`.

El reparto también asigna a Diego la revisión de Harold. Al momento de esta entrega, `operaciones_laboratorios.py`, `ui_laboratorios.py` y `tests/test_laboratorios.py` están vacíos, por lo que esa revisión queda pendiente de la entrega de Harold.
