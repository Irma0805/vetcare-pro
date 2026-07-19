import re

TABLA_LETRAS_MODULO_23 = "TRWAGMYFPDXBNJZSQVHLCKE"

PATRON_DNI = re.compile(r"^(\d{8})([A-Z])$")
PATRON_NIE = re.compile(r"^([XYZ])(\d{7})([A-Z])$")

VALORES_LETRA_INICIAL_NIE = {"X": "0", "Y": "1", "Z": "2"}


def validate_document(valor: str) -> str:
    """
    Valida y normaliza un documento de identidad (CU-15/FUS-14): DNI,
    NIE, o texto libre (pasaporte u otro).

    Validación condicional según Criterios de Aceptación de CU-15:
    - Si el formato coincide con DNI (8 dígitos + letra) o NIE
      (X/Y/Z + 7 dígitos + letra), se calcula la letra de control
      esperada mediante el algoritmo módulo 23 (verificado contra
      documentación de referencia del Ministerio del Interior/Agencia
      Tributaria) y se rechaza si no coincide con la letra introducida.
    - Si no coincide con ninguno de esos dos formatos, se acepta como
      texto libre sin validar (cubre pasaportes u otros documentos).

    En todos los casos, el valor se normaliza a mayúsculas y se le
    eliminan espacios y guiones antes de procesar o guardar.

    Lanza ValueError si el formato es DNI/NIE pero la letra de control
    no coincide con la calculada. Devuelve el valor normalizado en
    cualquier otro caso (DNI/NIE válido, o texto libre aceptado).
    """
    valor_normalizado = re.sub(r"[\s-]", "", valor).upper()

    coincidencia_dni = PATRON_DNI.match(valor_normalizado)
    if coincidencia_dni:
        digitos, letra_introducida = coincidencia_dni.groups()
        letra_esperada = TABLA_LETRAS_MODULO_23[int(digitos) % 23]
        if letra_introducida != letra_esperada:
            raise ValueError(
                f"La letra de control del DNI no es válida. Se esperaba '{letra_esperada}'."
            )
        return valor_normalizado

    coincidencia_nie = PATRON_NIE.match(valor_normalizado)
    if coincidencia_nie:
        letra_inicial, digitos, letra_introducida = coincidencia_nie.groups()
        digitos_completos = VALORES_LETRA_INICIAL_NIE[letra_inicial] + digitos
        letra_esperada = TABLA_LETRAS_MODULO_23[int(digitos_completos) % 23]
        if letra_introducida != letra_esperada:
            raise ValueError(
                f"La letra de control del NIE no es válida. Se esperaba '{letra_esperada}'."
            )
        return valor_normalizado

    # No coincide con DNI ni NIE: se acepta como texto libre (pasaporte)
    return valor_normalizado