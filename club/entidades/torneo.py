"""
Entidad Torneo - Representa torneos organizados por actividades
"""

from typing import List
from datetime import datetime

# Se eliminan dependencias y se usa type hinting
# from club.entidades.actividad import Actividad
# from club.entidades.socio import Socio

class Torneo:
    """Representa un torneo deportivo. Contiene solo datos y estado."""
    
    def __init__(self, nombre: str, actividad: 'Actividad', fecha: str, costo_inscripcion: float = 0):
        self._nombre = nombre
        self._actividad = actividad
        self._fecha = fecha
        self._costo_inscripcion = costo_inscripcion
        self._participantes: List['Socio'] = []
        self._fecha_creacion = datetime.now()
    
    @property
    def nombre(self) -> str:
        return self._nombre
    
    @property
    def actividad(self) -> 'Actividad':
        return self._actividad
    
    @property
    def fecha(self) -> str:
        return self._fecha
    
    @property
    def costo_inscripcion(self) -> float:
        return self._costo_inscripcion
    
    @property
    def participantes(self) -> List['Socio']:
        return self._participantes.copy()
    
    def inscribir_participante(self, socio: 'Socio'):
        """Agrega un socio a la lista de participantes del torneo."""
        if socio not in self._participantes:
            self._participantes.append(socio)
    
    def __str__(self) -> str:
        return (f"Torneo: {self._nombre}\n"
                f"Actividad: {self._actividad.nombre}\n"
                f"Fecha: {self._fecha}\n"
                f"Costo inscripción: ${self._costo_inscripcion}\n"
                f"Participantes: {len(self._participantes)}")
    
    def __repr__(self) -> str:
        return f"Torneo(nombre='{self._nombre}', fecha='{self._fecha}')"