"""
Servicio de Gestión de Profesores
Encapsula la lógica de negocio relacionada con profesores
"""

from typing import List, Optional
from club.entidades.profesor import Profesor
from club.patrones.singleton.club_registry import ClubRegistry


class ProfesorService:
    """
    Servicio para operaciones CRUD y lógica de negocio de profesores
    """
    
    def __init__(self):
        self._registry = ClubRegistry.get_instance()
    
    def crear_profesor(self, nombre: str, dni: int, sueldo: float) -> Optional[Profesor]:
        """
        Crea y registra un nuevo profesor
        
        Args:
            nombre: Nombre del profesor
            dni: DNI del profesor
            sueldo: Sueldo mensual
        
        Returns:
            Instancia del profesor creado o None si falla
        """
        try:
            profesor = Profesor(nombre, dni, sueldo)
            self.registrar_profesor(profesor)
            return profesor
        except ValueError as e:
            print(f"[ERROR] No se pudo crear el profesor: {e}")
            return None
    
    def registrar_profesor(self, profesor: Profesor):
        """
        Registra un profesor en el sistema
        
        Args:
            profesor: Instancia del profesor a registrar
        """
        try:
            self._registry.registrar_profesor(profesor)
            print(f"[INFO] Profesor {profesor.nombre} registrado exitosamente (DNI: {profesor.dni})")
        except ValueError as e:
            print(f"[ERROR] {e}")
    
    def obtener_profesor(self, dni: int) -> Optional[Profesor]:
        """
        Obtiene un profesor por su DNI
        
        Args:
            dni: DNI del profesor
        
        Returns:
            Instancia del profesor o None si no existe
        """
        profesor = self._registry.obtener_profesor(dni)
        if profesor is None:
            print(f"[ERROR] No se encontró profesor con DNI {dni}")
        return profesor
    
    def listar_profesores(self) -> List[Profesor]:
        """Retorna la lista de todos los profesores registrados"""
        return self._registry.listar_profesores()
    
    def eliminar_profesor(self, dni: int) -> bool:
        """
        Elimina un profesor del sistema
        
        Args:
            dni: DNI del profesor a eliminar
        
        Returns:
            True si se eliminó, False si no existía
        """
        profesor = self.obtener_profesor(dni)
        if profesor:
            # Desasignar de todas las actividades
            for actividad in profesor.actividades:
                actividad.eliminar_profesor(profesor)
            
            if self._registry.eliminar_profesor(dni):
                print(f"[INFO] Profesor {profesor.nombre} eliminado del sistema")
                return True
        
        return False
    
    def modificar_sueldo(self, dni: int, nuevo_sueldo: float) -> bool:
        """
        Modifica el sueldo de un profesor
        
        Args:
            dni: DNI del profesor
            nuevo_sueldo: Nuevo sueldo mensual
        
        Returns:
            True si se modificó, False si el profesor no existe
        """
        profesor = self.obtener_profesor(dni)
        if profesor:
            try:
                sueldo_anterior = profesor.sueldo
                profesor.sueldo = nuevo_sueldo
                print(f"[INFO] Sueldo de {profesor.nombre} actualizado: ${sueldo_anterior} -> ${nuevo_sueldo}")
                return True
            except ValueError as e:
                print(f"[ERROR] {e}")
                return False
        return False
    
    def mostrar_info_profesor(self, dni: int):
        """
        Muestra información completa de un profesor
        
        Args:
            dni: DNI del profesor
        """
        profesor = self.obtener_profesor(dni)
        if profesor:
            print("\n" + "="*60)
            print(str(profesor))
            print("="*60 + "\n")
    
    def calcular_nomina_total(self) -> float:
        """
        Calcula el total de la nómina de todos los profesores
        
        Returns:
            Suma de todos los sueldos
        """
        profesores = self.listar_profesores()
        total = sum(p.sueldo for p in profesores)
        print(f"[INFO] Nómina total de profesores: ${total}")
        return total
    
    def listar_profesores_por_actividad(self, nombre_actividad: str) -> List[Profesor]:
        """
        Lista los profesores que dictan una actividad específica
        
        Args:
            nombre_actividad: Nombre de la actividad
        
        Returns:
            Lista de profesores de esa actividad
        """
        todos = self.listar_profesores()
        return [p for p in todos 
                if any(a.nombre == nombre_actividad for a in p.actividades)]