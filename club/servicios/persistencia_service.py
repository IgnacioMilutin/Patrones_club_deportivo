"""
Servicio de Persistencia de Datos
Encapsula la lógica para guardar y cargar el estado del sistema usando Pickle
"""

import pickle
import os
from club.patrones.singleton.club_registry import ClubRegistry

class PersistenciaService:
    """
    Servicio para guardar y cargar datos del ClubRegistry
    """
    
    def __init__(self, directorio: str = "data"):
        self._directorio = directorio
        self._filepath = os.path.join(directorio, "club_data.pkl")
        self._registry = ClubRegistry.get_instance()
    
    def guardar_datos(self):
        """
        Guarda el estado completo del ClubRegistry en un archivo pickle
        """
        try:
            if not os.path.exists(self._directorio):
                os.makedirs(self._directorio)
            
            with open(self._filepath, "wb") as f:
                pickle.dump(self._registry, f)
            
            print(f"[INFO] Datos guardados exitosamente en {self._filepath}")
            
        except Exception as e:
            print(f"[ERROR] No se pudieron guardar los datos: {e}")

    def cargar_datos(self) -> bool:
        """
        Carga el estado del ClubRegistry desde un archivo pickle
        
        Returns:
            True si los datos se cargaron, False en caso contrario
        """
        if not os.path.exists(self._filepath):
            print("[INFO] No se encontró archivo de datos. Se iniciará con un registro vacío.")
            return False
        
        try:
            with open(self._filepath, "rb") as f:
                registry_cargado = pickle.load(f)
            
            # Transferir los datos al singleton existente
            self._registry._socios = registry_cargado._socios
            self._registry._actividades = registry_cargado._actividades
            self._registry._profesores = registry_cargado._profesores
            self._registry._pagos = registry_cargado._pagos
            
            print(f"[INFO] Datos cargados exitosamente desde {self._filepath}")
            return True
            
        except Exception as e:
            print(f"[ERROR] No se pudieron cargar los datos: {e}")
            return False
