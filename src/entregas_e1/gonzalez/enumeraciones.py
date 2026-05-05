from enum import Enum

class UbicacionEstacion(Enum):
    """
    Enumeración que representa las posibles ubicaciones de una estación espacial en 
    la empresa Imperio Galactico.
    """
    ENDOR = "Endor"
    CUMULO_RAIMOS = "Cúmulo Raimos"
    NEBULOSA_KALIIDA = "Nebulosa Kaliida"

class ClaseNaveEstelar(Enum):
    """
    Enumeración que representa las posibles clases de naves estelares en la empresa 
    Imperio Galactico.
    """
    EJECUTOR = "Ejecutor"
    ECLIPSE = "Eclipse"
    SOBERANO = "Soberano"