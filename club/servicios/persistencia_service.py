"""
Servicio de Persistencia de Datos
Encapsula la lógica para guardar y cargar el estado del sistema usando Pickle
"""

import pickle
import os
from club.patrones.singleton.club_registry import ClubRegistry

class PersistenciaService:
    """
    Servicio para guardar y cargar datos del ClubRegistry en archivos .dat separados.
    """
    
    def __init__(self, directorio: str = "data"):
        self._directorio = directorio
        self._registry = ClubRegistry.get_instance()
        self._filenames = {
            "socios": "socios.dat",
            "actividades": "actividades.dat",
            "profesores": "profesores.dat",
            "pagos": "pagos.dat"
        }

    def _get_path(self, filename: str) -> str:
        return os.path.join(self._directorio, filename)

    def guardar_datos(self):
        """
        Guarda cada diccionario/lista de entidades del ClubRegistry en un archivo .dat separado.
        """
        try:
            if not os.path.exists(self._directorio):
                os.makedirs(self._directorio)
            
            data_to_save = {
                "socios": self._registry._socios,
                "actividades": self._registry._actividades,
                "profesores": self._registry._profesores,
                "pagos": self._registry._pagos
            }

            for key, data in data_to_save.items():
                filepath = self._get_path(self._filenames[key])
                with open(filepath, "wb") as f:
                    pickle.dump(data, f)
            
            print(f"[INFO] Datos guardados exitosamente en el directorio '{self._directorio}'")
            
        except Exception as e:
            print(f"[ERROR] No se pudieron guardar los datos: {e}")

    def cargar_datos(self) -> bool:
        """
        Carga el estado del ClubRegistry desde archivos .dat separados.
        
        Returns:
            True si al menos un archivo de datos se cargó, False en caso contrario.
        """
        cargado = False
        for key, filename in self._filenames.items():
            filepath = self._get_path(filename)
            if os.path.exists(filepath):
                try:
                    with open(filepath, "rb") as f:
                        data = pickle.load(f)
                        setattr(self._registry, f"_{key}", data)
                    print(f"[INFO] Datos de '{key}' cargados desde {filepath}")
                    cargado = True
                except Exception as e:
                    print(f"[ERROR] No se pudo cargar el archivo {filepath}: {e}")
        
        if not cargado:
            print("[INFO] No se encontraron archivos de datos existentes.")

        return cargado
