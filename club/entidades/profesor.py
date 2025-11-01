"""
Entidad Profesor - Representa a los instructores de actividades
"""

from typing import List

# Se elimina la dependencia circular y se usa type hinting
# from club.entidades.actividad import Actividad

class Profesor:
    """Representa un profesor/instructor del club. Contiene solo datos y estado."""
    
    def __init__(self, nombre: str, dni: int, sueldo: float):
        self._nombre = nombre
        self._dni = dni
        self._sueldo = sueldo
        self._actividades: List['Actividad'] = []
    
    @property
    def nombre(self) -> str:
        return self._nombre
    
    @property
    def dni(self) -> int:
        return self._dni
    
    @property
    def sueldo(self) -> float:
        return self._sueldo
    
    @sueldo.setter
    def sueldo(self, valor: float):
        if valor < 0:
            raise ValueError("El sueldo no puede ser negativo")
        self._sueldo = valor
    
    @property
    def actividades(self) -> List['Actividad']:
        return self._actividades.copy()
    
    def asignar_actividad(self, actividad: 'Actividad'):
        """Asigna una actividad a la lista interna del profesor."""
        if actividad not in self._actividades:
            self._actividades.append(actividad)
    
    def desasignar_actividad(self, actividad: 'Actividad'):
        """Desasigna una actividad de la lista interna."""
        if actividad in self._actividades:
            self._actividades.remove(actividad)
    
    def __str__(self) -> str:
        actividades_str = ", ".join([a.nombre for a in self._actividades]) if self._actividades else "Ninguna"
        return (f"Profesor: {self._nombre}\n"
                f"DNI: {self._dni}\n"
                f"Sueldo: ${self._sueldo}\n"
                f"Actividades: {actividades_str}")
    
    def __repr__(self) -> str:
        return f"Profesor(nombre='{self._nombre}', dni={self._dni}, sueldo={self._sueldo})"