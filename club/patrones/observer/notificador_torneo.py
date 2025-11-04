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