"""
Archivo integrador generado automaticamente
Directorio: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/patrones/factory
Fecha: 2025-11-04 17:46:03
Total de archivos integrados: 3
"""

# ================================================================================
# ARCHIVO 1/3: __init__.py
# Ruta: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/patrones/factory/__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/3: actividad_factory.py
# Ruta: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/patrones/factory/actividad_factory.py
# ================================================================================

"""
Factory Method para creación de Actividades.
Permite crear actividades predefinidas con configuraciones específicas.
"""

# Standard library imports
from typing import Optional

# Local application imports
from club.entidades.actividad import Actividad


class ActividadFactory:
    """
    Factory para crear instancias de actividades deportivas.
    Incluye configuraciones predefinidas para actividades comunes.
    """
    
    # Configuraciones predefinidas de actividades
    ACTIVIDADES_PREDEFINIDAS = {
        "tenis": {"costo": 20000, "capacidad": 10},
        "natacion": {"costo": 18000, "capacidad": 15},
        "padel": {"costo": 22000, "capacidad": 8},
        "gimnasia": {"costo": 15000, "capacidad": 20},
        "yoga": {"costo": 12000, "capacidad": 15},
        "futbol": {"costo": 25000, "capacidad": 22},
        "basketball": {"costo": 20000, "capacidad": 12},
        "voley": {"costo": 18000, "capacidad": 12},
        "pilates": {"costo": 16000, "capacidad": 10},
        "boxeo": {"costo": 24000, "capacidad": 8}
    }
    
    @staticmethod
    def crear_actividad(nombre: str, costo: Optional[float] = None, 
                       capacidad: Optional[int] = None) -> Actividad:
        """Crea una actividad deportiva.
        
        Args:
            nombre: Nombre de la actividad.
            costo: Costo mensual (si es None, usa valor predefinido).
            capacidad: Capacidad máxima (si es None, usa valor predefinido).
        
        Returns:
            Instancia de Actividad.
        """
        nombre_lower = nombre.lower().strip()
        
        if nombre_lower in ActividadFactory.ACTIVIDADES_PREDEFINIDAS:
            config = ActividadFactory.ACTIVIDADES_PREDEFINIDAS[nombre_lower]
            costo_final = costo if costo is not None else config["costo"]
            capacidad_final = capacidad if capacidad is not None else config["capacidad"]
        else:
            costo_final = costo if costo is not None else 15000
            capacidad_final = capacidad if capacidad is not None else 20
        
        nombre_formato = nombre.capitalize()
        
        return Actividad(nombre_formato, costo_final, capacidad_final)
    
    @staticmethod
    def actividades_disponibles() -> list:
        """Retorna la lista de actividades predefinidas."""
        return list(ActividadFactory.ACTIVIDADES_PREDEFINIDAS.keys())
    
    @staticmethod
    def obtener_info_actividad(nombre: str) -> dict:
        """Obtiene información de una actividad predefinida.

        Args:
            nombre: El nombre de la actividad.

        Returns:
            Un diccionario con la información de la actividad o None si no existe.
        """
        nombre_lower = nombre.lower().strip()
        if nombre_lower in ActividadFactory.ACTIVIDADES_PREDEFINIDAS:
            return ActividadFactory.ACTIVIDADES_PREDEFINIDAS[nombre_lower].copy()
        return None

# ================================================================================
# ARCHIVO 3/3: socio_factory.py
# Ruta: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/patrones/factory/socio_factory.py
# ================================================================================

"""
Factory Method para creación de Socios.
Permite crear diferentes tipos de socios sin conocer las clases concretas.
"""

# Standard library imports
from typing import Optional

# Local application imports
from club.entidades.socio import Socio, SocioRegular, SocioPremium, SocioInfantil


class SocioFactory:
    """
    Factory para crear instancias de diferentes tipos de socios.
    """
    
    @staticmethod
    def crear_socio(tipo: str, nombre: str, dni: int, edad: Optional[int] = None) -> Socio:
        """Crea un socio según el tipo especificado.
        
        Args:
            tipo: Tipo de socio ('regular', 'premium', 'infantil').
            nombre: Nombre del socio.
            dni: DNI del socio.
            edad: Edad (requerida solo para socio infantil).
        
        Returns:
            Una instancia de Socio correspondiente al tipo.
        
        Raises:
            ValueError: Si el tipo de socio no es válido o falta la edad.
        """
        tipo = tipo.lower().strip()
        
        if tipo == "regular":
            return SocioRegular(nombre, dni)
        
        elif tipo == "premium":
            return SocioPremium(nombre, dni)
        
        elif tipo == "infantil":
            if edad is None:
                raise ValueError("Se requiere especificar la edad para un socio infantil")
            if edad >= 18:
                raise ValueError("Un socio infantil debe ser menor de 18 años")
            return SocioInfantil(nombre, dni, edad)
        
        else:
            tipos_validos = ["regular", "premium", "infantil"]
            raise ValueError(f"Tipo de socio inválido: '{tipo}'. Tipos válidos: {tipos_validos}")
    
    @staticmethod
    def tipos_disponibles() -> list:
        """Retorna la lista de tipos de socios disponibles."""
        return ["regular", "premium", "infantil"]

