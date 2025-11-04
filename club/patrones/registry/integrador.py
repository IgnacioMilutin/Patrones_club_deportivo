"""
Archivo integrador generado automaticamente
Directorio: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/patrones/registry
Fecha: 2025-11-04 17:46:03
Total de archivos integrados: 2
"""

# ================================================================================
# ARCHIVO 1/2: __init__.py
# Ruta: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/patrones/registry/__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/2: club_service_registry.py
# Ruta: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/patrones/registry/club_service_registry.py
# ================================================================================

"""
Patrón Registry para gestión centralizada de servicios.
Evita el uso de condicionales if/isinstance para despachar métodos.
"""

# Standard library imports
import threading
from typing import Dict, Optional, Any


class ClubServiceRegistry:
    """
    Registry que centraliza el acceso a todos los servicios del club.
    Implementa Singleton para garantizar una única instancia.
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._servicios: Dict[str, Any] = {}
        self._initialized = True
    
    @classmethod
    def get_instance(cls) -> 'ClubServiceRegistry':
        """Obtiene la instancia única del Registry."""
        if cls._instance is None:
            cls._instance = ClubServiceRegistry()
        return cls._instance
    
    def registrar_servicio(self, nombre: str, servicio: Any):
        """Registra un servicio en el registry.

        Args:
            nombre: Identificador único del servicio.
            servicio: Instancia del servicio a registrar.
        """
        if nombre in self._servicios:
            print(f"[WARNING] Servicio '{nombre}' ya existe. Se sobrescribirá.")
        
        self._servicios[nombre] = servicio
        print(f"[INFO] Servicio '{nombre}' registrado exitosamente")
    
    def obtener_servicio(self, nombre: str) -> Optional[Any]:
        """Obtiene un servicio registrado.

        Args:
            nombre: Identificador del servicio.

        Returns:
            La instancia del servicio o None si no existe.
        """
        servicio = self._servicios.get(nombre)
        if servicio is None:
            print(f"[ERROR] Servicio '{nombre}' no encontrado")
        return servicio
    
    def eliminar_servicio(self, nombre: str) -> bool:
        """Elimina un servicio del registry.

        Args:
            nombre: Identificador del servicio.

        Returns:
            True si se eliminó, False si no existía.
        """
        if nombre in self._servicios:
            del self._servicios[nombre]
            print(f"[INFO] Servicio '{nombre}' eliminado")
            return True
        print(f"[WARNING] Servicio '{nombre}' no existe")
        return False
    
    def listar_servicios(self) -> list:
        """Retorna la lista de nombres de servicios registrados."""
        return list(self._servicios.keys())
    
    def existe_servicio(self, nombre: str) -> bool:
        """Verifica si un servicio está registrado."""
        return nombre in self._servicios
    
    def reset(self):
        """Limpia todos los servicios registrados (útil para testing)."""
        self._servicios.clear()
        print("[INFO] Registry reiniciado")
    
    def __str__(self) -> str:
        servicios_str = ", ".join(self._servicios.keys()) if self._servicios else "Ninguno"
        return f"ClubServiceRegistry - Servicios registrados: {servicios_str}"

