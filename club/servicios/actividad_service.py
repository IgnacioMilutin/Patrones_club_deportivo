"""
Servicio de Gestión de Actividades
Encapsula la lógica de negocio relacionada con actividades deportivas
"""

from typing import List, Optional
from datetime import datetime

from club.entidades.actividad import Actividad
from club.entidades.socio import Socio
from club.entidades.profesor import Profesor
from club.entidades.torneo import Torneo
from club.patrones.factory.actividad_factory import ActividadFactory
from club.patrones.singleton.club_registry import ClubRegistry
from club.patrones.observer.notificador_torneo import NotificadorTorneo


class ActividadService:
    """
    Servicio para operaciones CRUD y lógica de negocio de actividades
    """
    
    def __init__(self):
        self._registry = ClubRegistry.get_instance()
        self._notificador_torneo = NotificadorTorneo()
    
    def crear_actividad(self, nombre: str, costo: Optional[float] = None, 
                       capacidad: Optional[int] = None) -> Optional[Actividad]:
        """
        Crea una nueva actividad usando Factory Method
        """
        try:
            # La factory ya no necesita sueldoProfesor
            actividad = ActividadFactory.crear_actividad(nombre, costo, capacidad)
            self.registrar_actividad(actividad)
            
            # Agregar observador de torneos
            actividad.agregar_observador(self._notificador_torneo)
            
            return actividad
        except Exception as e:
            print(f"No se pudo crear la actividad: {e}")
            return None
    
    def registrar_actividad(self, actividad: Actividad):
        """
        Registra una actividad en el sistema
        """
        try:
            self._registry.registrar_actividad(actividad)
            print(f"Actividad '{actividad.nombre}' registrada exitosamente")
        except ValueError as e:
            print(f"{e}")
    
    def obtener_actividad(self, nombre: str) -> Optional[Actividad]:
        """
        Obtiene una actividad por su nombre
        """
        actividad = self._registry.obtener_actividad(nombre)
        if actividad is None:
            print(f"[ERROR] No se encontró la actividad '{nombre}'")
        return actividad
    
    def listar_actividades(self) -> List[Actividad]:
        """Retorna la lista de todas las actividades registradas"""
        return self._registry.listar_actividades()
    
    def eliminar_actividad(self, nombre: str) -> bool:
        """
        Elimina una actividad del sistema
        """
        actividad = self.obtener_actividad(nombre)
        if actividad:
            for socio in actividad.socios:
                socio.eliminar_actividad(actividad)
            
            for profesor in actividad.profesores:
                profesor.desasignar_actividad(actividad)
            
            if self._registry.eliminar_actividad(nombre):
                print(f"[INFO] Actividad '{nombre}' eliminada del sistema")
                return True
        
        return False
    
    def inscribir_socio(self, actividad: Actividad, socio: Socio) -> bool:
        """
        Inscribe un socio en una actividad, manejando la lógica de negocio.
        """
        if len(actividad.socios) >= actividad.capacidad:
            print(f"Actividad {actividad.nombre} ha alcanzado su capacidad máxima")
            return False
        
        if socio in actividad.socios:
            print(f"Socio {socio.nombre} ya está inscrito en {actividad.nombre}")
            return False

        actividad.inscribir_socio(socio)
        socio.agregar_actividad(actividad)
        print(f"Socio {socio.nombre} inscrito en {actividad.nombre}")
        return True
    
    def desinscribir_socio(self, actividad: Actividad, socio: Socio):
        """
        Desinscribe un socio de una actividad.
        """
        if socio not in actividad.socios:
            print(f"Socio {socio.nombre} no está inscrito en {actividad.nombre}")
            return

        actividad.desinscribir_socio(socio)
        socio.eliminar_actividad(actividad)
        print(f"[INFO] Socio {socio.nombre} desinscrito de {actividad.nombre}")
    
    def asignar_profesor(self, actividad: Actividad, profesor: Profesor):
        """
        Asigna un profesor a una actividad.
        """
        if profesor in actividad.profesores:
            print(f"Profesor {profesor.nombre} ya esta asignado a la actividad {actividad.nombre}")
            return

        actividad.agregar_profesor(profesor)
        profesor.asignar_actividad(actividad)
        print(f"Profesor {profesor.nombre} asignado a {actividad.nombre}")

    def desasignar_profesor(self, actividad: Actividad, profesor: Profesor):
        """
        Desasigna un profesor de una actividad.
        """
        if profesor not in actividad.profesores:
            print(f"Profesor {profesor.nombre} no se encuentra asignado a la actividad {actividad.nombre}")
            return

        actividad.eliminar_profesor(profesor)
        profesor.desasignar_actividad(actividad)
        print(f"[INFO] Profesor {profesor.nombre} desasignado de {actividad.nombre}")
    
    def crear_torneo(self, actividad: Actividad, nombre_torneo: str, 
                    fecha: str = None, costo_inscripcion: float = 0) -> Optional[Torneo]:
        """
        Crea un torneo, lo asocia a una actividad y notifica a los observadores.
        """
        if fecha is None:
            fecha = datetime.now().strftime("%Y-%m-%d")
        
        torneo = Torneo(nombre_torneo, actividad, fecha, costo_inscripcion)
        actividad.agregar_torneo(torneo)
        
        datos_evento = {
            'torneo': nombre_torneo,
            'actividad': actividad.nombre,
            'fecha': fecha,
            'costo': costo_inscripcion,
            'socios': actividad.socios  # <-- BUG FIX: Añadir socios al evento
        }
        
        # El observer se encarga de la notificación
        actividad.notificar_observadores('nuevo_torneo', datos_evento)
        
        print(f"[INFO] Torneo '{nombre_torneo}' creado para {actividad.nombre}")
        return torneo

    def inscribir_socio_torneo(self, torneo: Torneo, socio: Socio) -> bool:
        """Inscribe un socio en un torneo con validaciones."""
        if socio not in torneo.actividad.socios:
            print(f"{socio.nombre} no está inscrito en la actividad {torneo.actividad.nombre} del torneo.")
            return False
        
        if socio in torneo.participantes:
            print(f"{socio.nombre} ya está inscrito en el torneo '{torneo.nombre}'")
            return False

        torneo.inscribir_participante(socio)
        print(f"{socio.nombre} inscrito en torneo '{torneo.nombre}'")
        return True

    def mostrar_info_actividad(self, nombre: str):
        """
        Muestra información completa de una actividad
        """
        actividad = self.obtener_actividad(nombre)
        if actividad:
            print("\n" + "="*60)
            # El método __str__ ahora retorna el string formateado
            print(str(actividad))
            print(f"\nSocios inscritos ({len(actividad.socios)}):")
            if not actividad.socios:
                print("  No hay socios inscritos.")
            else:
                for socio in actividad.socios:
                    print(f"  • {socio.nombre} ({socio.get_tipo()})")
            
            print(f"\nTorneos organizados ({len(actividad.torneos)}):")
            if not actividad.torneos:
                print("  No hay torneos organizados.")
            else:
                for torneo in actividad.torneos:
                    print(f"  • {torneo.nombre} - {torneo.fecha}")
            print("="*60 + "\n")
    
    def listar_actividades_disponibles(self) -> List[str]:
        """
        Lista las actividades predefinidas disponibles para crear
        """
        return ActividadFactory.actividades_disponibles()