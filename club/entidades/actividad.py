"""
Entidad Actividad - Representa las actividades deportivas del club.
"""

# Standard library imports
from typing import List

# Local application imports
from club.patrones.observer.observer import Observer


class Actividad:
    """Representa una actividad deportiva del club. Contiene solo datos y estado."""
    
    def __init__(self, nombre: str, costo: float, capacidad: int):
        """Inicializa una Actividad.

        Args:
            nombre: El nombre de la actividad.
            costo: El costo mensual de la actividad.
            capacidad: El número máximo de socios que pueden inscribirse.
        """
        self._nombre = nombre
        self._costo = costo
        self._capacidad = capacidad
        self._profesores: List['Profesor'] = []
        self._socios: List['Socio'] = []
        self._torneos: List['Torneo'] = []
        self._observadores: List['Observer'] = []
        
    @property
    def nombre(self) -> str:
        return self._nombre
    
    @property
    def costo(self) -> float:
        return self._costo
    
    @costo.setter
    def costo(self, valor: float):
        if valor < 0:
            raise ValueError("El costo no puede ser negativo")
        self._costo = valor
    
    @property
    def capacidad(self) -> int:
        return self._capacidad

    @property
    def profesores(self) -> List['Profesor']:
        return self._profesores.copy()
    
    @property
    def socios(self) -> List['Socio']:
        return self._socios.copy()
    
    @property
    def torneos(self) -> List['Torneo']:
        return self._torneos.copy()
    
    def agregar_profesor(self, profesor: 'Profesor'):
        """Agrega un profesor a la lista interna de la actividad."""
        if profesor not in self._profesores:
            self._profesores.append(profesor)
    
    def eliminar_profesor(self, profesor: 'Profesor'):
        """Elimina un profesor de la lista interna."""
        if profesor in self._profesores:
            self._profesores.remove(profesor)
    
    def inscribir_socio(self, socio: 'Socio'):
        """Agrega un socio a la lista interna de la actividad."""
        if socio not in self._socios:
            self._socios.append(socio)
    
    def desinscribir_socio(self, socio: 'Socio'):
        """Elimina un socio de la lista interna."""
        if socio in self._socios:
            self._socios.remove(socio)

    def agregar_torneo(self, torneo: 'Torneo'):
        """Agrega un torneo a la lista de torneos de la actividad."""
        if torneo not in self._torneos:
            self._torneos.append(torneo)
    
    def agregar_observador(self, observador: 'Observer'):
        """Agrega un observador para notificaciones (Observer Pattern)."""
        if observador not in self._observadores:
            self._observadores.append(observador)
    
    def eliminar_observador(self, observador: 'Observer'):
        """Elimina un observador."""
        if observador in self._observadores:
            self._observadores.remove(observador)
    
    def notificar_observadores(self, evento: str, datos: dict):
        """Notifica a todos los observadores sobre un evento."""
        for observador in self._observadores:
            observador.actualizar(evento, datos)
    
    def __str__(self) -> str:
        profesores_str = ", ".join([p.nombre for p in self._profesores]) if self._profesores else "Sin asignar"
        return (f"Actividad: {self._nombre}\n"
                f"Costo: ${self._costo}\n"
                f"Capacidad: {len(self._socios)}/{self._capacidad}\n"
                f"Profesores: {profesores_str}")
    
    def __repr__(self) -> str:
        return f"Actividad(nombre='{self._nombre}', costo={self._costo})"