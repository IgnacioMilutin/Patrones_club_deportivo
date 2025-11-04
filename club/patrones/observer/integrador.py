"""
Archivo integrador generado automaticamente
Directorio: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/patrones/observer
Fecha: 2025-11-04 17:46:03
Total de archivos integrados: 4
"""

# ================================================================================
# ARCHIVO 1/4: __init__.py
# Ruta: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/patrones/observer/__init__.py
# ================================================================================

from .observer import Observer, Observable
from .notificador_torneo import NotificadorTorneo
from .notificador_pago import NotificadorPago

__all__ = ['Observer', 'Observable', 'NotificadorTorneo', 'NotificadorPago']

# ================================================================================
# ARCHIVO 2/4: notificador_pago.py
# Ruta: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/patrones/observer/notificador_pago.py
# ================================================================================

"""
Observador concreto para notificaciones de pagos.
"""

# Local application imports
from .observer import Observer


class NotificadorPago(Observer):
    """
    Observador que maneja notificaciones de pagos de cuotas.
    """
    
    def __init__(self, nombre: str = "Sistema de Pagos"):
        """Inicializa el notificador.

        Args:
            nombre: El nombre del notificador.
        """
        self._nombre = nombre
    
    def actualizar(self, evento: str, datos: dict):
        """Procesa eventos relacionados con pagos.

        Args:
            evento: El tipo de evento a procesar.
            datos: Un diccionario con los datos del evento.
        """
        if evento == "pago_registrado":
            self._notificar_pago_exitoso(datos)
        elif evento == "pago_vencido":
            self._notificar_pago_vencido(datos)
        elif evento == "recordatorio_pago":
            self._notificar_recordatorio(datos)
    
    def _notificar_pago_exitoso(self, datos: dict):
        """Notifica sobre un pago exitoso."""
        socio_nombre = datos.get('socio', 'Socio')
        monto = datos.get('monto', 0)
        comprobante = datos.get('comprobante', 'N/A')
        metodo = datos.get('metodo', 'Efectivo')
        
        print("\n" + "="*60)
        print(f"[PAGO REGISTRADO] ✓ - {socio_nombre}")
        print("="*60)
        print(f"Monto: ${monto} | Método: {metodo}")
        print(f"Comprobante: {comprobante}")
        print("¡Muchas gracias! Su pago ha sido procesado exitosamente.")
        print("="*60 + "\n")

    def _notificar_pago_vencido(self, datos: dict):
        """Notifica sobre un pago vencido."""
        socio_nombre = datos.get('socio', 'Socio')
        monto = datos.get('monto', 0)
        
        print("\n" + "="*60)
        print(f"[AVISO DE PAGO VENCIDO] - {socio_nombre}")
        print("="*60)
        print(f"Monto adeudado: ${monto}")
        print("Por favor, regularice su situación a la brevedad.")
        print("="*60 + "\n")

    def _notificar_recordatorio(self, datos: dict):
        """Notifica un recordatorio de pago."""
        socio_nombre = datos.get('socio', 'Socio')
        monto = datos.get('monto', 0)
        vencimiento = datos.get('vencimiento', 'Próximamente')
        
        print("\n" + "="*60)
        print(f"[RECORDATORIO DE PAGO] - {socio_nombre}")
        print("="*60)
        print(f"Monto a pagar: ${monto}")
        print(f"Fecha de vencimiento: {vencimiento}")
        print("="*60 + "\n")

# ================================================================================
# ARCHIVO 3/4: notificador_torneo.py
# Ruta: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/patrones/observer/notificador_torneo.py
# ================================================================================

"""
Observador concreto para notificaciones de torneos.
"""

# Local application imports
from .observer import Observer


class NotificadorTorneo(Observer):
    """
    Observador que maneja notificaciones de nuevos torneos.
    """
    
    def __init__(self, nombre: str = "Sistema de Torneos"):
        """Inicializa el notificador.

        Args:
            nombre: El nombre del notificador.
        """
        self._nombre = nombre
    
    def actualizar(self, evento: str, datos: dict):
        """Procesa eventos relacionados con torneos.

        Args:
            evento: El tipo de evento a procesar.
            datos: Un diccionario con los datos del evento.
        """
        if evento == "nuevo_torneo":
            self._notificar_nuevo_torneo(datos)
        elif evento == "torneo_cancelado":
            self._notificar_cancelacion(datos)
        elif evento == "inscripcion_torneo":
            self._notificar_inscripcion(datos)
    
    def _notificar_nuevo_torneo(self, datos: dict):
        """Notifica sobre un nuevo torneo a los socios inscritos en la actividad."""
        torneo = datos.get('torneo', 'Torneo')
        actividad = datos.get('actividad', 'Actividad')
        fecha = datos.get('fecha', 'Sin fecha')
        costo = datos.get('costo', 0)
        socios_a_notificar = datos.get('socios', [])

        print("\n" + "="*60)
        print(f"[NUEVO TORNEO] ¡{torneo} de {actividad}!")
        print("="*60)
        print(f"Fecha: {fecha} | Costo de inscripción: ${costo}")
        print("\nNotificando a los siguientes socios:")
        if socios_a_notificar:
            for socio in socios_a_notificar:
                print(f"  - {socio.nombre}")
        else:
            print("  (No hay socios inscritos en esta actividad para notificar)")
        print("="*60 + "\n")

    def _notificar_cancelacion(self, datos: dict):
        """Notifica sobre cancelación de torneo."""
        torneo = datos.get('torneo', 'Torneo')
        print(f"\n[AVISO] El torneo '{torneo}' ha sido cancelado.")
    
    def _notificar_inscripcion(self, datos: dict):
        """Notifica sobre inscripción exitosa a un torneo."""
        socio = datos.get('socio')
        torneo = datos.get('torneo')
        if socio and torneo:
            print(f"\n[INSCRIPCIÓN A TORNEO] {socio.nombre} se ha inscrito exitosamente en '{torneo.nombre}'.")

# ================================================================================
# ARCHIVO 4/4: observer.py
# Ruta: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/patrones/observer/observer.py
# ================================================================================

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

