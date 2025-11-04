"""
Archivo integrador generado automaticamente
Directorio: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club
Fecha: 2025-11-04 17:46:03
Total de archivos integrados: 2
"""

# ================================================================================
# ARCHIVO 1/2: __init__.py
# Ruta: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/2: excepciones.py
# Ruta: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/excepciones.py
# ================================================================================

"""
Excepciones personalizadas para el sistema del Club Deportivo.
"""

class ClubException(Exception):
    """Clase base para todas las excepciones personalizadas del club."""
    pass

class EntidadNoEncontradaError(ClubException):
    """Se lanza cuando una entidad (socio, actividad, etc.) no se encuentra."""
    pass

class SocioNoEncontradoError(EntidadNoEncontradaError):
    """Se lanza cuando un socio específico no se encuentra."""
    pass

class ActividadNoEncontradaError(EntidadNoEncontradaError):
    """Se lanza cuando una actividad específica no se encuentra."""
    pass

class ProfesorNoEncontradoError(EntidadNoEncontradaError):
    """Se lanza cuando un profesor específico no se encuentra."""
    pass

class EntidadYaExisteError(ClubException):
    """Se lanza cuando se intenta crear una entidad que ya existe."""
    pass

class SocioYaExisteError(EntidadYaExisteError):
    """Se lanza cuando se intenta registrar un socio con un DNI ya existente."""
    pass

class ActividadYaExisteError(EntidadYaExisteError):
    """Se lanza cuando se intenta registrar una actividad con un nombre ya existente."""
    pass

class ProfesorYaExisteError(EntidadYaExisteError):
    """Se lanza cuando se intenta registrar un profesor con un DNI ya existente."""
    pass

class CapacidadAlcanzadaError(ClubException):
    """Se lanza cuando se intenta inscribir un socio a una actividad llena."""
    pass

class InscripcionError(ClubException):
    """Se lanza por errores relacionados con la lógica de inscripción."""
    pass


