"""
Singleton Registry para la gestión centralizada de datos en memoria
"""

import threading
from typing import List, Dict, Optional

from club.entidades.socio import Socio
from club.entidades.actividad import Actividad
from club.entidades.profesor import Profesor
from club.entidades.pago import Pago


class ClubRegistry:
    """
    Singleton que actúa como una base de datos en memoria para el club
    Mantiene listas de todas las entidades principales
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
        
        self._socios: Dict[int, Socio] = {}
        self._actividades: Dict[str, Actividad] = {}
        self._profesores: Dict[int, Profesor] = {}
        self._pagos: List[Pago] = []
        self._initialized = True
        print("[INFO] ClubRegistry inicializado")
    
    @classmethod
    def get_instance(cls) -> 'ClubRegistry':
        """Obtiene la instancia única del Registry"""
        if cls._instance is None:
            cls._instance = ClubRegistry()
        return cls._instance
    
    # --- Métodos de Socios ---
    
    def registrar_socio(self, socio: Socio):
        if socio.dni in self._socios:
            raise ValueError(f"Socio con DNI {socio.dni} ya existe")
        self._socios[socio.dni] = socio
    
    def obtener_socio(self, dni: int) -> Optional[Socio]:
        return self._socios.get(dni)
    
    def listar_socios(self) -> List[Socio]:
        return list(self._socios.values())
    
    def eliminar_socio(self, dni: int) -> bool:
        if dni in self._socios:
            del self._socios[dni]
            return True
        return False
    
    # --- Métodos de Actividades ---
    
    def registrar_actividad(self, actividad: Actividad):
        if actividad.nombre.lower() in self._actividades:
            raise ValueError(f"Actividad '{actividad.nombre}' ya existe")
        self._actividades[actividad.nombre.lower()] = actividad
    
    def obtener_actividad(self, nombre: str) -> Optional[Actividad]:
        return self._actividades.get(nombre.lower())
    
    def listar_actividades(self) -> List[Actividad]:
        return list(self._actividades.values())
    
    def eliminar_actividad(self, nombre: str) -> bool:
        if nombre.lower() in self._actividades:
            del self._actividades[nombre.lower()]
            return True
        return False
    
    # --- Métodos de Profesores ---
    
    def registrar_profesor(self, profesor: Profesor):
        if profesor.dni in self._profesores:
            raise ValueError(f"Profesor con DNI {profesor.dni} ya existe")
        self._profesores[profesor.dni] = profesor
    
    def obtener_profesor(self, dni: int) -> Optional[Profesor]:
        return self._profesores.get(dni)
    
    def listar_profesores(self) -> List[Profesor]:
        return list(self._profesores.values())
    
    def eliminar_profesor(self, dni: int) -> bool:
        if dni in self._profesores:
            del self._profesores[dni]
            return True
        return False
    
    # --- Métodos de Pagos ---
    
    def registrar_pago(self, pago: Pago):
        self._pagos.append(pago)
    
    def listar_pagos(self) -> List[Pago]:
        return self._pagos
    
    def obtener_pagos_socio(self, dni: int) -> List[Pago]:
        return [p for p in self._pagos if p.socio.dni == dni]
    
    # --- Gestión de Estado ---
    
    def reset(self):
        """Limpia todos los datos (útil para testing)"""
        self._socios.clear()
        self._actividades.clear()
        self._profesores.clear()
        self._pagos.clear()
        print("[INFO] ClubRegistry reiniciado")
    
    def __str__(self) -> str:
        return ("ClubRegistry - Estado actual:\n"
                "  - Socios: {}\n"
                "  - Actividades: {}\n"
                "  - Profesores: {}\n"
                "  - Pagos: {}").format(len(self._socios), len(self._actividades), len(self._profesores), len(self._pagos))
