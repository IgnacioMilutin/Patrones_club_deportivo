"""
Servicio de Gestión de Socios
Encapsula la lógica de negocio relacionada con socios.
"""

# Standard library imports
from typing import List, Optional

# Local application imports
from club.entidades.socio import Socio
from club.excepciones import SocioNoEncontradoError, SocioYaExisteError
from club.patrones.factory.socio_factory import SocioFactory
from club.patrones.singleton.club_registry import ClubRegistry
from club.patrones.strategy.cuota_strategy import (
    CuotaRegularStrategy,
    CuotaPremiumStrategy,
    CuotaInfantilStrategy,
    ContextoCuota
)
from club.patrones.registry.club_service_registry import ClubServiceRegistry


class SocioService:
    """
    Servicio para operaciones CRUD y lógica de negocio de socios.
    """
    
    def __init__(self):
        self._registry = ClubRegistry.get_instance()
    
    def crear_socio(self, tipo: str, nombre: str, dni: int, edad: Optional[int] = None) -> Optional[Socio]:
        """Crea un nuevo socio usando Factory Method."""
        try:
            socio = SocioFactory.crear_socio(tipo, nombre, dni, edad)
            self.registrar_socio(socio)
            print(f"[INFO] Socio {socio.nombre} registrado exitosamente (DNI: {socio.dni})")
            return socio
        except (ValueError, SocioYaExisteError) as e:
            print(f"[ERROR] No se pudo crear el socio: {e}")
            return None
    
    def registrar_socio(self, socio: Socio):
        """Registra un socio en el sistema."""
        try:
            self._registry.registrar_socio(socio)
        except ValueError as e:
            raise SocioYaExisteError(e)
    
    def obtener_socio(self, dni: int) -> Socio:
        """Obtiene un socio por su DNI."""
        socio = self._registry.obtener_socio(dni)
        if socio is None:
            raise SocioNoEncontradoError(f"No se encontró socio con DNI {dni}")
        return socio
    
    def listar_socios(self) -> List[Socio]:
        """Retorna la lista de todos los socios registrados."""
        return self._registry.listar_socios()

    def modificar_socio(self, dni: int, nuevo_tipo: str, nueva_edad: Optional[int] = None) -> Optional[Socio]:
        """Modifica el tipo de un socio existente."""
        try:
            socio_actual = self.obtener_socio(dni)
            nuevo_socio = SocioFactory.crear_socio(
                tipo=nuevo_tipo,
                nombre=socio_actual.nombre,
                dni=socio_actual.dni,
                edad=nueva_edad
            )
            for actividad in socio_actual.actividades:
                nuevo_socio.agregar_actividad(actividad)
            self._registry.eliminar_socio(dni)
            self._registry.registrar_socio(nuevo_socio)
            print(f"[INFO] Socio {socio_actual.nombre} modificado a tipo '{nuevo_tipo.capitalize()}'")
            return nuevo_socio
        except (SocioNoEncontradoError, ValueError) as e:
            print(f"[ERROR] No se pudo modificar el socio: {e}")
            return None

    def eliminar_socio(self, dni: int) -> bool:
        """Elimina un socio del sistema."""
        try:
            socio = self.obtener_socio(dni)
            service_registry = ClubServiceRegistry.get_instance()
            actividad_service = service_registry.obtener_servicio("actividad")
            if actividad_service:
                for actividad in list(socio.actividades):
                    actividad_service.desinscribir_socio(actividad, socio)
            if self._registry.eliminar_socio(dni):
                print(f"[INFO] Socio {socio.nombre} eliminado del sistema")
                return True
        except SocioNoEncontradoError as e:
            print(f"[ERROR] {e}")
            return False
        return False
    
    def _get_strategy_for_socio(self, socio: Socio):
        """Selecciona la estrategia de cuota apropiada para un socio."""
        tipo = socio.get_tipo().lower()
        if tipo == 'regular':
            return CuotaRegularStrategy()
        elif tipo == 'premium':
            return CuotaPremiumStrategy()
        elif tipo == 'infantil':
            return CuotaInfantilStrategy()
        return None

    def calcular_cuota(self, socio: Socio) -> float:
        """Calcula la cuota mensual del socio."""
        estrategia = self._get_strategy_for_socio(socio)
        if estrategia is None:
            print(f"[ERROR] No hay estrategia definida para tipo '{socio.get_tipo()}'")
            return 0.0
        contexto = ContextoCuota(estrategia)
        return contexto.calcular_cuota(socio)
    
    def obtener_descripcion_cuota(self, socio: Socio) -> str:
        """Obtiene la descripción detallada del cálculo de cuota."""
        estrategia = self._get_strategy_for_socio(socio)
        if estrategia is None:
            return f"No hay estrategia definida para tipo '{socio.get_tipo()}'"
        contexto = ContextoCuota(estrategia)
        return contexto.obtener_descripcion(socio)
    
    def mostrar_info_socio(self, dni: int):
        """Muestra información completa de un socio."""
        try:
            socio = self.obtener_socio(dni)
            print("\n" + "="*60)
            print(str(socio))
            print("\nDetalle de cuota:")
            print(self.obtener_descripcion_cuota(socio))
            print("="*60 + "\n")
        except SocioNoEncontradoError as e:
            print(f"[ERROR] {e}")
    
    def listar_socios_por_tipo(self, tipo: str) -> List[Socio]:
        """Lista socios filtrados por tipo."""
        tipo_lower = tipo.lower().strip()
        if tipo_lower not in ["regular", "premium", "infantil"]:
            print(f"[ERROR] Tipo de socio inválido: '{tipo}'")
            return []
        todos = self.listar_socios()
        return [s for s in todos if s.get_tipo().lower() == tipo_lower]