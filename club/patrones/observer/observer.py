"""
Interfaces base del patrón Observer.
Define el contrato para observadores y sujetos observables.
"""

# Standard library imports
from abc import ABC, abstractmethod
from typing import List


class Observer(ABC):
    """
    Interfaz para los observadores que reciben notificaciones.
    """
    
    @abstractmethod
    def actualizar(self, evento: str, datos: dict):
        """Método llamado cuando ocurre un evento observable.
        
        Args:
            evento: Tipo de evento que ocurrió.
            datos: Información adicional sobre el evento.
        """
        pass


class Observable(ABC):
    """
    Clase base para sujetos observables que notifican a los observadores.
    """
    
    def __init__(self):
        """Inicializa un objeto Observable."""
        self._observadores: List[Observer] = []
    
    def agregar_observador(self, observador: Observer):
        """Registra un nuevo observador.

        Args:
            observador: La instancia del observador a registrar.
        """
        if observador not in self._observadores:
            self._observadores.append(observador)
    
    def eliminar_observador(self, observador: Observer):
        """Elimina un observador registrado.

        Args:
            observador: La instancia del observador a eliminar.
        """
        if observador in self._observadores:
            self._observadores.remove(observador)
    
    def notificar_observadores(self, evento: str, datos: dict):
        """Notifica a todos los observadores sobre un evento.

        Args:
            evento: Tipo de evento que ocurrió.
            datos: Información adicional sobre el evento.
        """
        for observador in self._observadores:
            observador.actualizar(evento, datos)