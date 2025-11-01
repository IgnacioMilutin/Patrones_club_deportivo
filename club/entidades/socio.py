"""
Entidad Socio - Representa a los miembros del club deportivo
Implementa jerarquía de herencia para diferentes tipos de socios
"""

from abc import ABC, abstractmethod
from typing import List
from datetime import datetime

# Se elimina la dependencia circular y se usa type hinting
# from club.entidades.actividad import Actividad

class Socio(ABC):
    """Clase base abstracta para todos los tipos de socios. Contiene solo datos y estado."""
    
    def __init__(self, nombre: str, dni: int):
        self._nombre = nombre
        self._dni = dni
        self._actividades: List['Actividad'] = []
        self._fecha_registro = datetime.now()
        self._estado_pago = "Pendiente"
        
    @property
    def nombre(self) -> str:
        return self._nombre
    
    @property
    def dni(self) -> int:
        return self._dni
    
    @property
    def actividades(self) -> List['Actividad']:
        return self._actividades.copy()
    
    @property
    def fecha_registro(self) -> datetime:
        return self._fecha_registro
    
    @property
    def estado_pago(self) -> str:
        return self._estado_pago
    
    @estado_pago.setter
    def estado_pago(self, valor: str):
        self._estado_pago = valor
    
    def agregar_actividad(self, actividad: 'Actividad'):
        """Agrega una actividad a la lista interna del socio."""
        if actividad not in self._actividades:
            self._actividades.append(actividad)
    
    def eliminar_actividad(self, actividad: 'Actividad'):
        """Elimina una actividad de la lista interna del socio."""
        if actividad in self._actividades:
            self._actividades.remove(actividad)
    
    @abstractmethod
    def get_tipo(self) -> str:
        """Retorna el tipo de socio"""
        pass
    
    def __str__(self) -> str:
        actividades_str = ", ".join([a.nombre for a in self._actividades]) if self._actividades else "Ninguna"
        return (f"Socio: {self._nombre}\n"
                f"DNI: {self._dni}\n"
                f"Tipo: {self.get_tipo()}\n"
                f"Actividades: {actividades_str}\n"
                f"Estado de pagos: {self._estado_pago}")
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(nombre='{self._nombre}', dni={self._dni})"


class SocioRegular(Socio):
    """Socio que paga según las actividades en las que participa"""
    
    def get_tipo(self) -> str:
        return "Regular"


class SocioPremium(Socio):
    """Socio que paga una cuota fija y accede a todas las actividades"""
    
    CUOTA_FIJA = 30000
    
    def get_tipo(self) -> str:
        return "Premium"


class SocioInfantil(Socio):
    """Socio menor de edad con cuota reducida y acceso limitado"""
    
    CUOTA_FIJA = 15000
    
    def __init__(self, nombre: str, dni: int, edad: int):
        super().__init__(nombre, dni)
        self._edad = edad
    
    @property
    def edad(self) -> int:
        return self._edad
    
    def get_tipo(self) -> str:
        return "Infantil"
    
    def __str__(self) -> str:
        base_str = super().__str__()
        return f"{base_str}\nEdad: {self._edad}"