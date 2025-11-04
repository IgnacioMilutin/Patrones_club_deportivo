"""
Servicio de Gestión de Profesores
Encapsula la lógica de negocio relacionada con profesores.
"""

# Standard library imports
from typing import List, Optional

# Local application imports
from club.entidades.profesor import Profesor
from club.excepciones import ProfesorNoEncontradoError, ProfesorYaExisteError
from club.patrones.singleton.club_registry import ClubRegistry


class ProfesorService:
    """
    Servicio para operaciones CRUD y lógica de negocio de profesores.
    """
    
    def __init__(self):
        """Inicializa el servicio obteniendo la instancia del registry."""
        self._registry = ClubRegistry.get_instance()
    
    def crear_profesor(self, nombre: str, dni: int, sueldo: float) -> Optional[Profesor]:
        """Crea y registra un nuevo profesor."""
        try:
            profesor = Profesor(nombre, dni, sueldo)
            self.registrar_profesor(profesor)
            print(f"[INFO] Profesor {profesor.nombre} registrado exitosamente (DNI: {profesor.dni})")
            return profesor
        except (ValueError, ProfesorYaExisteError) as e:
            print(f"[ERROR] No se pudo crear el profesor: {e}")
            return None
    
    def registrar_profesor(self, profesor: Profesor):
        """Registra un profesor en el sistema."""
        try:
            self._registry.registrar_profesor(profesor)
        except ValueError as e:
            raise ProfesorYaExisteError(e)
    
    def obtener_profesor(self, dni: int) -> Profesor:
        """Obtiene un profesor por su DNI."""
        profesor = self._registry.obtener_profesor(dni)
        if profesor is None:
            raise ProfesorNoEncontradoError(f"No se encontró profesor con DNI {dni}")
        return profesor
    
    def listar_profesores(self) -> List[Profesor]:
        """Retorna la lista de todos los profesores registrados."""
        return self._registry.listar_profesores()
    
    def eliminar_profesor(self, dni: int) -> bool:
        """Elimina un profesor del sistema."""
        try:
            profesor = self.obtener_profesor(dni)
            # Desasignar de todas las actividades
            for actividad in list(profesor.actividades):
                actividad.eliminar_profesor(profesor)
            
            if self._registry.eliminar_profesor(dni):
                print(f"[INFO] Profesor {profesor.nombre} eliminado del sistema")
                return True
            return False
        except ProfesorNoEncontradoError as e:
            print(f"[ERROR] {e}")
            return False

    def modificar_sueldo(self, dni: int, nuevo_sueldo: float) -> bool:
        """Modifica el sueldo de un profesor."""
        try:
            profesor = self.obtener_profesor(dni)
            sueldo_anterior = profesor.sueldo
            profesor.sueldo = nuevo_sueldo
            print(f"[INFO] Sueldo de {profesor.nombre} actualizado: ${sueldo_anterior} -> ${nuevo_sueldo}")
            return True
        except (ProfesorNoEncontradoError, ValueError) as e:
            print(f"[ERROR] {e}")
            return False

    def mostrar_info_profesor(self, dni: int):
        """Muestra información completa de un profesor."""
        try:
            profesor = self.obtener_profesor(dni)
            print("\n" + "="*60)
            print(str(profesor))
            print("="*60 + "\n")
        except ProfesorNoEncontradoError as e:
            print(f"[ERROR] {e}")
    
    def calcular_nomina_total(self) -> float:
        """Calcula el total de la nómina de todos los profesores."""
        profesores = self.listar_profesores()
        total = sum(p.sueldo for p in profesores)
        print(f"[INFO] Nómina total de profesores: ${total}")
        return total
    
    def listar_profesores_por_actividad(self, nombre_actividad: str) -> List[Profesor]:
        """Lista los profesores que dictan una actividad específica."""
        todos = self.listar_profesores()
        return [p for p in todos if any(a.nombre == nombre_actividad for a in p.actividades)]
