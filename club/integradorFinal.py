"""
INTEGRADOR FINAL - CONSOLIDACION COMPLETA DEL PROYECTO
============================================================================
Directorio raiz: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club
Fecha de generacion: 2025-11-04 17:46:03
Total de archivos integrados: 29
Total de directorios procesados: 10
============================================================================
"""

# ==============================================================================
# TABLA DE CONTENIDOS
# ==============================================================================

# DIRECTORIO: ..
#   1. main.py
#
# DIRECTORIO: .
#   2. __init__.py
#   3. excepciones.py
#
# DIRECTORIO: entidades
#   4. __init__.py
#   5. actividad.py
#   6. pago.py
#   7. profesor.py
#   8. socio.py
#   9. torneo.py
#
# DIRECTORIO: patrones
#   10. __init__.py
#
# DIRECTORIO: patrones/factory
#   11. __init__.py
#   12. actividad_factory.py
#   13. socio_factory.py
#
# DIRECTORIO: patrones/observer
#   14. __init__.py
#   15. notificador_pago.py
#   16. notificador_torneo.py
#   17. observer.py
#
# DIRECTORIO: patrones/registry
#   18. __init__.py
#   19. club_service_registry.py
#
# DIRECTORIO: patrones/singleton
#   20. __init__.py
#   21. club_registry.py
#
# DIRECTORIO: patrones/strategy
#   22. __init__.py
#   23. cuota_strategy.py
#
# DIRECTORIO: servicios
#   24. __init__.py
#   25. actividad_service.py
#   26. pago_service.py
#   27. persistencia_service.py
#   28. profesor_service.py
#   29. socio_service.py
#



################################################################################
# DIRECTORIO: ..
################################################################################

# ==============================================================================
# ARCHIVO 1/29: main.py
# Directorio: ..
# Ruta completa: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/main.py
# ==============================================================================

"""
Sistema de Gestión de Club Deportivo - DEMO AUTOMÁTICA CON PERSISTENCIA

Este script demuestra las funcionalidades y la persistencia de datos.
Al ejecutarlo por primera vez, creará y guardará los datos.
En ejecuciones posteriores, cargará los datos guardados.
"""

from club.servicios.socio_service import SocioService
from club.servicios.actividad_service import ActividadService
from club.servicios.profesor_service import ProfesorService
from club.servicios.pago_service import PagoService
from club.servicios.persistencia_service import PersistenciaService
from club.patrones.registry.club_service_registry import ClubServiceRegistry
from club.patrones.singleton.club_registry import ClubRegistry

def imprimir_titulo(titulo: str):
    """Imprime un título formateado"""
    print("\n" + "="*70)
    print(f"  {titulo}")
    print("="*70 + "\n")

def setup_services():
    """Inicializa y registra todos los servicios del sistema."""
    service_registry = ClubServiceRegistry.get_instance()
    
    if not service_registry.existe_servicio("socio"):
        service_registry.registrar_servicio("socio", SocioService())
        service_registry.registrar_servicio("actividad", ActividadService())
        service_registry.registrar_servicio("profesor", ProfesorService())
        service_registry.registrar_servicio("pago", PagoService())
        service_registry.registrar_servicio("persistencia", PersistenciaService())
        
    return service_registry

def demostracion_y_creacion_de_datos():
    """Ejecuta una demostración completa y crea los datos iniciales."""
    
    service_registry = ClubServiceRegistry.get_instance()
    socio_service = service_registry.obtener_servicio("socio")
    actividad_service = service_registry.obtener_servicio("actividad")
    profesor_service = service_registry.obtener_servicio("profesor")
    pago_service = service_registry.obtener_servicio("pago")

    imprimir_titulo("2. CREACIÓN DE ENTIDADES (USANDO FACTORY PATTERN)")
    
    print("--- Creando Socios ---")
    s1 = socio_service.crear_socio("regular", "Ana López", 40123456)
    s2 = socio_service.crear_socio("premium", "Carlos Gómez", 35789012)
    s3 = socio_service.crear_socio("infantil", "María Pérez", 50456789, edad=12)
    
    print("\n--- Creando Actividades ---")
    tenis = actividad_service.crear_actividad("Tenis", costo=25000, capacidad=10)
    natacion = actividad_service.crear_actividad("Natacion", costo=20000, capacidad=15)
    
    print("\n--- Creando Profesores ---")
    p1 = profesor_service.crear_profesor("Juan Martínez", 25123456, 150000)
    p2 = profesor_service.crear_profesor("Laura Sánchez", 28456789, 180000)

    imprimir_titulo("3. ESTABLECIENDO RELACIONES")

    print("--- Asignando profesores a actividades ---")
    actividad_service.asignar_profesor(tenis, p1)
    actividad_service.asignar_profesor(natacion, p2)

    print("\n--- Inscribiendo socios a actividades ---")
    actividad_service.inscribir_socio(tenis, s1)
    actividad_service.inscribir_socio(natacion, s1)
    actividad_service.inscribir_socio(tenis, s2)
    actividad_service.inscribir_socio(natacion, s3)

    imprimir_titulo("4. DEMO DE STRATEGY PATTERN (CÁLCULO DE CUOTAS)")

    for socio in socio_service.listar_socios():
        print(f"--- Calculando cuota para {socio.nombre} ({socio.get_tipo()}) ---")
        print(socio_service.obtener_descripcion_cuota(socio))

    imprimir_titulo("5. DEMO DE OBSERVER PATTERN (PAGOS Y TORNEOS)")

    print("--- Registrando un pago ---")
    cuota_ana = socio_service.calcular_cuota(s1)
    pago_service.registrar_pago(s1, cuota_ana, "Tarjeta de Crédito")

    print("\n--- Creando un nuevo torneo de Tenis ---")
    torneo_tenis = actividad_service.crear_torneo(tenis, "Torneo de Otoño", costo_inscripcion=5000)

    print("\n--- Inscribiendo un socio al torneo ---")
    actividad_service.inscribir_socio_torneo(torneo_tenis, s1)

    imprimir_titulo("DEMO FINALIZADA - DATOS CREADOS")
    print(ClubRegistry.get_instance())

def main():
    """Función principal del sistema con persistencia."""
    imprimir_titulo("SISTEMA DE GESTIÓN DE CLUB DEPORTIVO")
    
    # 1. Inicializar servicios
    service_registry = setup_services()
    persistencia_service = service_registry.obtener_servicio("persistencia")
    
    # 2. Intentar cargar datos
    print("Intentando cargar datos guardados...")
    datos_cargados = persistencia_service.cargar_datos()
    
    # 3. Decidir el flujo
    if datos_cargados:
        imprimir_titulo("DATOS CARGADOS EXITOSAMENTE")
        print("El sistema ha sido restaurado desde la carpeta /data.")
        print("Estado actual del club:")
        print(ClubRegistry.get_instance())
    else:
        imprimir_titulo("EJECUTANDO DEMO POR PRIMERA VEZ")
        print("No se encontraron datos, se creará un nuevo conjunto de datos de ejemplo.")
        demostracion_y_creacion_de_datos()
        
        # 4. Guardar los datos nuevos al final de la demo
        print("\nGuardando datos para la próxima ejecución...")
        persistencia_service.guardar_datos()

if __name__ == "__main__":
    main()




################################################################################
# DIRECTORIO: .
################################################################################

# ==============================================================================
# ARCHIVO 2/29: __init__.py
# Directorio: .
# Ruta completa: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 3/29: excepciones.py
# Directorio: .
# Ruta completa: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/excepciones.py
# ==============================================================================

"""
Excepciones personalizadas para el sistema del Club Deportivo.
"""

class ClubException(Exception):
    """Clase base para todas las excepciones personalizadas del club."""
    pass

class EntidadNoEncontradaError(ClubException):
    """Se lanza cuando una entidad (socio, actividad, etc.) no se encuentra."""
    pass

class SocioNoEncontradoError(EntidadNoEncontradaError):
    """Se lanza cuando un socio específico no se encuentra."""
    pass

class ActividadNoEncontradaError(EntidadNoEncontradaError):
    """Se lanza cuando una actividad específica no se encuentra."""
    pass

class ProfesorNoEncontradoError(EntidadNoEncontradaError):
    """Se lanza cuando un profesor específico no se encuentra."""
    pass

class EntidadYaExisteError(ClubException):
    """Se lanza cuando se intenta crear una entidad que ya existe."""
    pass

class SocioYaExisteError(EntidadYaExisteError):
    """Se lanza cuando se intenta registrar un socio con un DNI ya existente."""
    pass

class ActividadYaExisteError(EntidadYaExisteError):
    """Se lanza cuando se intenta registrar una actividad con un nombre ya existente."""
    pass

class ProfesorYaExisteError(EntidadYaExisteError):
    """Se lanza cuando se intenta registrar un profesor con un DNI ya existente."""
    pass

class CapacidadAlcanzadaError(ClubException):
    """Se lanza cuando se intenta inscribir un socio a una actividad llena."""
    pass

class InscripcionError(ClubException):
    """Se lanza por errores relacionados con la lógica de inscripción."""
    pass



################################################################################
# DIRECTORIO: entidades
################################################################################

# ==============================================================================
# ARCHIVO 4/29: __init__.py
# Directorio: entidades
# Ruta completa: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/entidades/__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 5/29: actividad.py
# Directorio: entidades
# Ruta completa: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/entidades/actividad.py
# ==============================================================================

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

# ==============================================================================
# ARCHIVO 6/29: pago.py
# Directorio: entidades
# Ruta completa: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/entidades/pago.py
# ==============================================================================

"""
Entidad Pago - Representa el registro de pagos de cuotas.
"""

# Standard library imports
from datetime import datetime

# Local application imports
# Se evita la importación directa para prevenir dependencias circulares
# from club.entidades.socio import Socio


class Pago:
    """Representa un pago de cuota realizado por un socio."""
    
    def __init__(self, socio: 'Socio', monto: float, metodo: str):
        """Inicializa un objeto Pago.

        Args:
            socio: La instancia del socio que realiza el pago.
            monto: El monto del pago.
            metodo: El método de pago (ej. 'Efectivo', 'Tarjeta').
        """
        self._socio = socio
        self._monto = monto
        self._metodo = metodo
        self._fecha = datetime.now()
        self._comprobante = self._generar_comprobante()
    
    @property
    def socio(self) -> 'Socio':
        return self._socio
    
    @property
    def monto(self) -> float:
        return self._monto
    
    @property
    def metodo(self) -> str:
        return self._metodo
    
    @property
    def fecha(self) -> datetime:
        return self._fecha
    
    @property
    def comprobante(self) -> str:
        return self._comprobante
    
    def _generar_comprobante(self) -> str:
        """Genera un número de comprobante único basado en el DNI y el timestamp."""
        timestamp = int(self._fecha.timestamp())
        return f"PAGO-{self._socio.dni}-{timestamp}"
    
    def __str__(self) -> str:
        return (f"Comprobante: {self._comprobante}\n"
                f"Socio: {self._socio.nombre}\n"
                f"Monto: ${self._monto}\n"
                f"Método: {self._metodo}\n"
                f"Fecha: {self._fecha.strftime('%Y-%m-%d %H:%M:%S')}")
    
    def __repr__(self) -> str:
        return f"Pago(socio='{self._socio.nombre}', monto={self._monto})"

# ==============================================================================
# ARCHIVO 7/29: profesor.py
# Directorio: entidades
# Ruta completa: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/entidades/profesor.py
# ==============================================================================

"""
Entidad Profesor - Representa a los instructores de actividades.
"""

# Standard library imports
from typing import List

# Local application imports
# Se evita la importación directa para prevenir dependencias circulares
# from club.entidades.actividad import Actividad


class Profesor:
    """Representa un profesor/instructor del club. Contiene solo datos y estado."""
    
    def __init__(self, nombre: str, dni: int, sueldo: float):
        """Inicializa un objeto Profesor.

        Args:
            nombre: El nombre completo del profesor.
            dni: El Documento Nacional de Identidad del profesor.
            sueldo: El sueldo mensual del profesor.
        """
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

# ==============================================================================
# ARCHIVO 8/29: socio.py
# Directorio: entidades
# Ruta completa: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/entidades/socio.py
# ==============================================================================

"""
Entidad Socio - Representa a los miembros del club deportivo.
Implementa jerarquía de herencia para diferentes tipos de socios.
"""

# Standard library imports
from abc import ABC, abstractmethod
from typing import List
from datetime import datetime

# Local application imports
# Se evita la importación directa para prevenir dependencias circulares
# from club.entidades.actividad import Actividad


class Socio(ABC):
    """Clase base abstracta para todos los tipos de socios. Contiene solo datos y estado."""
    
    def __init__(self, nombre: str, dni: int):
        """Inicializa un objeto Socio.

        Args:
            nombre: El nombre completo del socio.
            dni: El Documento Nacional de Identidad del socio.
        """
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
        """Retorna el tipo de socio como un string."""
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
    """Socio que paga según las actividades en las que participa."""
    
    def get_tipo(self) -> str:
        return "Regular"


class SocioPremium(Socio):
    """Socio que paga una cuota fija y accede a todas las actividades."""
    
    CUOTA_FIJA = 30000
    
    def get_tipo(self) -> str:
        return "Premium"


class SocioInfantil(Socio):
    """Socio menor de edad con cuota reducida y acceso limitado."""
    
    CUOTA_FIJA = 15000
    
    def __init__(self, nombre: str, dni: int, edad: int):
        """Inicializa un Socio Infantil.

        Args:
            nombre: El nombre completo del socio.
            dni: El DNI del socio.
            edad: La edad del socio infantil.
        """
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

# ==============================================================================
# ARCHIVO 9/29: torneo.py
# Directorio: entidades
# Ruta completa: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/entidades/torneo.py
# ==============================================================================

"""
Entidad Torneo - Representa torneos organizados por actividades.
"""

# Standard library imports
from typing import List
from datetime import datetime

# Local application imports
# Se evita la importación directa para prevenir dependencias circulares
# from club.entidades.actividad import Actividad
# from club.entidades.socio import Socio


class Torneo:
    """Representa un torneo deportivo. Contiene solo datos y estado."""
    
    def __init__(self, nombre: str, actividad: 'Actividad', fecha: str, costo_inscripcion: float = 0):
        """Inicializa un objeto Torneo.

        Args:
            nombre: El nombre del torneo.
            actividad: La actividad a la que pertenece el torneo.
            fecha: La fecha en formato string del torneo.
            costo_inscripcion: El costo de inscripción al torneo (por defecto 0).
        """
        self._nombre = nombre
        self._actividad = actividad
        self._fecha = fecha
        self._costo_inscripcion = costo_inscripcion
        self._participantes: List['Socio'] = []
        self._fecha_creacion = datetime.now()
    
    @property
    def nombre(self) -> str:
        return self._nombre
    
    @property
    def actividad(self) -> 'Actividad':
        return self._actividad
    
    @property
    def fecha(self) -> str:
        return self._fecha
    
    @property
    def costo_inscripcion(self) -> float:
        return self._costo_inscripcion
    
    @property
    def participantes(self) -> List['Socio']:
        return self._participantes.copy()
    
    def inscribir_participante(self, socio: 'Socio'):
        """Agrega un socio a la lista de participantes del torneo."""
        if socio not in self._participantes:
            self._participantes.append(socio)
    
    def __str__(self) -> str:
        return (f"Torneo: {self._nombre}\n"
                f"Actividad: {self._actividad.nombre}\n"
                f"Fecha: {self._fecha}\n"
                f"Costo inscripción: ${self._costo_inscripcion}\n"
                f"Participantes: {len(self._participantes)}")
    
    def __repr__(self) -> str:
        return f"Torneo(nombre='{self._nombre}', fecha='{self._fecha}')"


################################################################################
# DIRECTORIO: patrones
################################################################################

# ==============================================================================
# ARCHIVO 10/29: __init__.py
# Directorio: patrones
# Ruta completa: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/patrones/__init__.py
# ==============================================================================

__all__ = []


################################################################################
# DIRECTORIO: patrones/factory
################################################################################

# ==============================================================================
# ARCHIVO 11/29: __init__.py
# Directorio: patrones/factory
# Ruta completa: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/patrones/factory/__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 12/29: actividad_factory.py
# Directorio: patrones/factory
# Ruta completa: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/patrones/factory/actividad_factory.py
# ==============================================================================

"""
Factory Method para creación de Actividades.
Permite crear actividades predefinidas con configuraciones específicas.
"""

# Standard library imports
from typing import Optional

# Local application imports
from club.entidades.actividad import Actividad


class ActividadFactory:
    """
    Factory para crear instancias de actividades deportivas.
    Incluye configuraciones predefinidas para actividades comunes.
    """
    
    # Configuraciones predefinidas de actividades
    ACTIVIDADES_PREDEFINIDAS = {
        "tenis": {"costo": 20000, "capacidad": 10},
        "natacion": {"costo": 18000, "capacidad": 15},
        "padel": {"costo": 22000, "capacidad": 8},
        "gimnasia": {"costo": 15000, "capacidad": 20},
        "yoga": {"costo": 12000, "capacidad": 15},
        "futbol": {"costo": 25000, "capacidad": 22},
        "basketball": {"costo": 20000, "capacidad": 12},
        "voley": {"costo": 18000, "capacidad": 12},
        "pilates": {"costo": 16000, "capacidad": 10},
        "boxeo": {"costo": 24000, "capacidad": 8}
    }
    
    @staticmethod
    def crear_actividad(nombre: str, costo: Optional[float] = None, 
                       capacidad: Optional[int] = None) -> Actividad:
        """Crea una actividad deportiva.
        
        Args:
            nombre: Nombre de la actividad.
            costo: Costo mensual (si es None, usa valor predefinido).
            capacidad: Capacidad máxima (si es None, usa valor predefinido).
        
        Returns:
            Instancia de Actividad.
        """
        nombre_lower = nombre.lower().strip()
        
        if nombre_lower in ActividadFactory.ACTIVIDADES_PREDEFINIDAS:
            config = ActividadFactory.ACTIVIDADES_PREDEFINIDAS[nombre_lower]
            costo_final = costo if costo is not None else config["costo"]
            capacidad_final = capacidad if capacidad is not None else config["capacidad"]
        else:
            costo_final = costo if costo is not None else 15000
            capacidad_final = capacidad if capacidad is not None else 20
        
        nombre_formato = nombre.capitalize()
        
        return Actividad(nombre_formato, costo_final, capacidad_final)
    
    @staticmethod
    def actividades_disponibles() -> list:
        """Retorna la lista de actividades predefinidas."""
        return list(ActividadFactory.ACTIVIDADES_PREDEFINIDAS.keys())
    
    @staticmethod
    def obtener_info_actividad(nombre: str) -> dict:
        """Obtiene información de una actividad predefinida.

        Args:
            nombre: El nombre de la actividad.

        Returns:
            Un diccionario con la información de la actividad o None si no existe.
        """
        nombre_lower = nombre.lower().strip()
        if nombre_lower in ActividadFactory.ACTIVIDADES_PREDEFINIDAS:
            return ActividadFactory.ACTIVIDADES_PREDEFINIDAS[nombre_lower].copy()
        return None

# ==============================================================================
# ARCHIVO 13/29: socio_factory.py
# Directorio: patrones/factory
# Ruta completa: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/patrones/factory/socio_factory.py
# ==============================================================================

"""
Factory Method para creación de Socios.
Permite crear diferentes tipos de socios sin conocer las clases concretas.
"""

# Standard library imports
from typing import Optional

# Local application imports
from club.entidades.socio import Socio, SocioRegular, SocioPremium, SocioInfantil


class SocioFactory:
    """
    Factory para crear instancias de diferentes tipos de socios.
    """
    
    @staticmethod
    def crear_socio(tipo: str, nombre: str, dni: int, edad: Optional[int] = None) -> Socio:
        """Crea un socio según el tipo especificado.
        
        Args:
            tipo: Tipo de socio ('regular', 'premium', 'infantil').
            nombre: Nombre del socio.
            dni: DNI del socio.
            edad: Edad (requerida solo para socio infantil).
        
        Returns:
            Una instancia de Socio correspondiente al tipo.
        
        Raises:
            ValueError: Si el tipo de socio no es válido o falta la edad.
        """
        tipo = tipo.lower().strip()
        
        if tipo == "regular":
            return SocioRegular(nombre, dni)
        
        elif tipo == "premium":
            return SocioPremium(nombre, dni)
        
        elif tipo == "infantil":
            if edad is None:
                raise ValueError("Se requiere especificar la edad para un socio infantil")
            if edad >= 18:
                raise ValueError("Un socio infantil debe ser menor de 18 años")
            return SocioInfantil(nombre, dni, edad)
        
        else:
            tipos_validos = ["regular", "premium", "infantil"]
            raise ValueError(f"Tipo de socio inválido: '{tipo}'. Tipos válidos: {tipos_validos}")
    
    @staticmethod
    def tipos_disponibles() -> list:
        """Retorna la lista de tipos de socios disponibles."""
        return ["regular", "premium", "infantil"]


################################################################################
# DIRECTORIO: patrones/observer
################################################################################

# ==============================================================================
# ARCHIVO 14/29: __init__.py
# Directorio: patrones/observer
# Ruta completa: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/patrones/observer/__init__.py
# ==============================================================================

from .observer import Observer, Observable
from .notificador_torneo import NotificadorTorneo
from .notificador_pago import NotificadorPago

__all__ = ['Observer', 'Observable', 'NotificadorTorneo', 'NotificadorPago']

# ==============================================================================
# ARCHIVO 15/29: notificador_pago.py
# Directorio: patrones/observer
# Ruta completa: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/patrones/observer/notificador_pago.py
# ==============================================================================

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

# ==============================================================================
# ARCHIVO 16/29: notificador_torneo.py
# Directorio: patrones/observer
# Ruta completa: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/patrones/observer/notificador_torneo.py
# ==============================================================================

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

# ==============================================================================
# ARCHIVO 17/29: observer.py
# Directorio: patrones/observer
# Ruta completa: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/patrones/observer/observer.py
# ==============================================================================

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


################################################################################
# DIRECTORIO: patrones/registry
################################################################################

# ==============================================================================
# ARCHIVO 18/29: __init__.py
# Directorio: patrones/registry
# Ruta completa: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/patrones/registry/__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 19/29: club_service_registry.py
# Directorio: patrones/registry
# Ruta completa: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/patrones/registry/club_service_registry.py
# ==============================================================================

"""
Patrón Registry para gestión centralizada de servicios.
Evita el uso de condicionales if/isinstance para despachar métodos.
"""

# Standard library imports
import threading
from typing import Dict, Optional, Any


class ClubServiceRegistry:
    """
    Registry que centraliza el acceso a todos los servicios del club.
    Implementa Singleton para garantizar una única instancia.
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._servicios: Dict[str, Any] = {}
        self._initialized = True
    
    @classmethod
    def get_instance(cls) -> 'ClubServiceRegistry':
        """Obtiene la instancia única del Registry."""
        if cls._instance is None:
            cls._instance = ClubServiceRegistry()
        return cls._instance
    
    def registrar_servicio(self, nombre: str, servicio: Any):
        """Registra un servicio en el registry.

        Args:
            nombre: Identificador único del servicio.
            servicio: Instancia del servicio a registrar.
        """
        if nombre in self._servicios:
            print(f"[WARNING] Servicio '{nombre}' ya existe. Se sobrescribirá.")
        
        self._servicios[nombre] = servicio
        print(f"[INFO] Servicio '{nombre}' registrado exitosamente")
    
    def obtener_servicio(self, nombre: str) -> Optional[Any]:
        """Obtiene un servicio registrado.

        Args:
            nombre: Identificador del servicio.

        Returns:
            La instancia del servicio o None si no existe.
        """
        servicio = self._servicios.get(nombre)
        if servicio is None:
            print(f"[ERROR] Servicio '{nombre}' no encontrado")
        return servicio
    
    def eliminar_servicio(self, nombre: str) -> bool:
        """Elimina un servicio del registry.

        Args:
            nombre: Identificador del servicio.

        Returns:
            True si se eliminó, False si no existía.
        """
        if nombre in self._servicios:
            del self._servicios[nombre]
            print(f"[INFO] Servicio '{nombre}' eliminado")
            return True
        print(f"[WARNING] Servicio '{nombre}' no existe")
        return False
    
    def listar_servicios(self) -> list:
        """Retorna la lista de nombres de servicios registrados."""
        return list(self._servicios.keys())
    
    def existe_servicio(self, nombre: str) -> bool:
        """Verifica si un servicio está registrado."""
        return nombre in self._servicios
    
    def reset(self):
        """Limpia todos los servicios registrados (útil para testing)."""
        self._servicios.clear()
        print("[INFO] Registry reiniciado")
    
    def __str__(self) -> str:
        servicios_str = ", ".join(self._servicios.keys()) if self._servicios else "Ninguno"
        return f"ClubServiceRegistry - Servicios registrados: {servicios_str}"


################################################################################
# DIRECTORIO: patrones/singleton
################################################################################

# ==============================================================================
# ARCHIVO 20/29: __init__.py
# Directorio: patrones/singleton
# Ruta completa: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/patrones/singleton/__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 21/29: club_registry.py
# Directorio: patrones/singleton
# Ruta completa: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/patrones/singleton/club_registry.py
# ==============================================================================

"""
Singleton Registry para la gestión centralizada de datos en memoria.
"""

# Standard library imports
import threading
from typing import List, Dict, Optional

# Local application imports
from club.entidades.socio import Socio
from club.entidades.actividad import Actividad
from club.entidades.profesor import Profesor
from club.entidades.pago import Pago


class ClubRegistry:
    """
    Singleton que actúa como una base de datos en memoria para el club.
    Mantiene listas de todas las entidades principales.
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._socios: Dict[int, Socio] = {}
        self._actividades: Dict[str, Actividad] = {}
        self._profesores: Dict[int, Profesor] = {}
        self._pagos: List[Pago] = []
        self._initialized = True
        print("[INFO] ClubRegistry inicializado")
    
    @classmethod
    def get_instance(cls) -> 'ClubRegistry':
        """Obtiene la instancia única del Registry."""
        if cls._instance is None:
            cls._instance = ClubRegistry()
        return cls._instance
    
    # --- Métodos de Socios ---
    
    def registrar_socio(self, socio: Socio):
        """Registra un nuevo socio en el diccionario de socios."""
        if socio.dni in self._socios:
            raise ValueError(f"Socio con DNI {socio.dni} ya existe")
        self._socios[socio.dni] = socio
    
    def obtener_socio(self, dni: int) -> Optional[Socio]:
        """Obtiene un socio por su DNI."""
        return self._socios.get(dni)
    
    def listar_socios(self) -> List[Socio]:
        """Retorna una lista con todos los socios."""
        return list(self._socios.values())
    
    def eliminar_socio(self, dni: int) -> bool:
        """Elimina un socio del registro."""
        if dni in self._socios:
            del self._socios[dni]
            return True
        return False
    
    # --- Métodos de Actividades ---
    
    def registrar_actividad(self, actividad: Actividad):
        """Registra una nueva actividad."""
        if actividad.nombre.lower() in self._actividades:
            raise ValueError(f"Actividad '{actividad.nombre}' ya existe")
        self._actividades[actividad.nombre.lower()] = actividad
    
    def obtener_actividad(self, nombre: str) -> Optional[Actividad]:
        """Obtiene una actividad por su nombre."""
        return self._actividades.get(nombre.lower())
    
    def listar_actividades(self) -> List[Actividad]:
        """Retorna una lista con todas las actividades."""
        return list(self._actividades.values())
    
    def eliminar_actividad(self, nombre: str) -> bool:
        """Elimina una actividad del registro."""
        if nombre.lower() in self._actividades:
            del self._actividades[nombre.lower()]
            return True
        return False
    
    # --- Métodos de Profesores ---
    
    def registrar_profesor(self, profesor: Profesor):
        """Registra un nuevo profesor."""
        if profesor.dni in self._profesores:
            raise ValueError(f"Profesor con DNI {profesor.dni} ya existe")
        self._profesores[profesor.dni] = profesor
    
    def obtener_profesor(self, dni: int) -> Optional[Profesor]:
        """Obtiene un profesor por su DNI."""
        return self._profesores.get(dni)
    
    def listar_profesores(self) -> List[Profesor]:
        """Retorna una lista con todos los profesores."""
        return list(self._profesores.values())
    
    def eliminar_profesor(self, dni: int) -> bool:
        """Elimina un profesor del registro."""
        if dni in self._profesores:
            del self._profesores[dni]
            return True
        return False
    
    # --- Métodos de Pagos ---
    
    def registrar_pago(self, pago: Pago):
        """Registra un nuevo pago."""
        self._pagos.append(pago)
    
    def listar_pagos(self) -> List[Pago]:
        """Retorna la lista de todos los pagos."""
        return self._pagos
    
    def obtener_pagos_socio(self, dni: int) -> List[Pago]:
        """Obtiene todos los pagos de un socio específico."""
        return [p for p in self._pagos if p.socio.dni == dni]
    
    # --- Gestión de Estado ---
    
    def reset(self):
        """Limpia todos los datos del registro (útil para testing)."""
        self._socios.clear()
        self._actividades.clear()
        self._profesores.clear()
        self._pagos.clear()
        print("[INFO] ClubRegistry reiniciado")
    
    def __str__(self) -> str:
        return ("ClubRegistry - Estado actual:\n"
                "  - Socios: {}\n"
                "  - Actividades: {}\n"
                "  - Profesores: {}\n"
                "  - Pagos: {}").format(len(self._socios), len(self._actividades), len(self._profesores), len(self._pagos))



################################################################################
# DIRECTORIO: patrones/strategy
################################################################################

# ==============================================================================
# ARCHIVO 22/29: __init__.py
# Directorio: patrones/strategy
# Ruta completa: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/patrones/strategy/__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 23/29: cuota_strategy.py
# Directorio: patrones/strategy
# Ruta completa: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/patrones/strategy/cuota_strategy.py
# ==============================================================================

"""
Strategy Pattern para el cálculo de cuotas de socios.
Permite definir diferentes algoritmos de cálculo según el tipo de socio.
"""

# Standard library imports
from abc import ABC, abstractmethod

# Local application imports
from club.entidades.socio import Socio, SocioRegular, SocioPremium, SocioInfantil


class CuotaStrategy(ABC):
    """Interfaz abstracta para las estrategias de cálculo de cuota."""
    
    @abstractmethod
    def calcular_cuota(self, socio: Socio) -> float:
        """Calcula la cuota para un socio dado.

        Args:
            socio: La instancia del socio.

        Returns:
            El monto de la cuota.
        """
        pass
    
    @abstractmethod
    def obtener_descripcion(self, socio: Socio) -> str:
        """Obtiene una descripción del cálculo de la cuota.

        Args:
            socio: La instancia del socio.

        Returns:
            Una cadena de texto que describe cómo se calculó la cuota.
        """
        pass


class CuotaRegularStrategy(CuotaStrategy):
    """Estrategia para socios regulares: suma el costo de sus actividades."""
    
    def calcular_cuota(self, socio: SocioRegular) -> float:
        return sum(actividad.costo for actividad in socio.actividades)
    
    def obtener_descripcion(self, socio: SocioRegular) -> str:
        if not socio.actividades:
            return "Cuota Regular: $0 (sin actividades inscritas)"
        
        calculo_str = " + ".join([f"${a.costo}" for a in socio.actividades])
        total = self.calcular_cuota(socio)
        return f"Cuota Regular: {calculo_str} = ${total}"


class CuotaPremiumStrategy(CuotaStrategy):
    """Estrategia para socios premium: cuota fija."""
    
    def calcular_cuota(self, socio: SocioPremium) -> float:
        return SocioPremium.CUOTA_FIJA
    
    def obtener_descripcion(self, socio: SocioPremium) -> str:
        return f"Cuota Premium: ${SocioPremium.CUOTA_FIJA} (acceso a todas las actividades)"


class CuotaInfantilStrategy(CuotaStrategy):
    """Estrategia para socios infantiles: cuota fija reducida."""
    
    def calcular_cuota(self, socio: SocioInfantil) -> float:
        return SocioInfantil.CUOTA_FIJA
    
    def obtener_descripcion(self, socio: SocioInfantil) -> str:
        return f"Cuota Infantil: ${SocioInfantil.CUOTA_FIJA} (cuota reducida)"


class ContextoCuota:
    """Contexto que utiliza una estrategia para calcular la cuota."""
    
    def __init__(self, estrategia: CuotaStrategy):
        """Inicializa el contexto con una estrategia específica.

        Args:
            estrategia: La estrategia a utilizar para los cálculos.
        """
        self._estrategia = estrategia
    
    def calcular_cuota(self, socio: Socio) -> float:
        """Ejecuta el cálculo de la cuota usando la estrategia asignada."""
        return self._estrategia.calcular_cuota(socio)
    
    def obtener_descripcion(self, socio: Socio) -> str:
        """Obtiene la descripción del cálculo usando la estrategia asignada."""
        return self._estrategia.obtener_descripcion(socio)



################################################################################
# DIRECTORIO: servicios
################################################################################

# ==============================================================================
# ARCHIVO 24/29: __init__.py
# Directorio: servicios
# Ruta completa: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/servicios/__init__.py
# ==============================================================================

from .socio_service import SocioService
from .actividad_service import ActividadService
from .profesor_service import ProfesorService
from .pago_service import PagoService

__all__ = ['SocioService', 'ActividadService', 'ProfesorService', 'PagoService']

# ==============================================================================
# ARCHIVO 25/29: actividad_service.py
# Directorio: servicios
# Ruta completa: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/servicios/actividad_service.py
# ==============================================================================

"""
Servicio de Gestión de Actividades
Encapsula la lógica de negocio relacionada con actividades deportivas.
"""

# Standard library imports
from typing import List, Optional
from datetime import datetime

# Local application imports
from club.entidades.actividad import Actividad
from club.entidades.socio import Socio
from club.entidades.profesor import Profesor
from club.entidades.torneo import Torneo
from club.excepciones import (
    ActividadNoEncontradaError, ActividadYaExisteError, 
    CapacidadAlcanzadaError, InscripcionError
)
from club.patrones.factory.actividad_factory import ActividadFactory
from club.patrones.singleton.club_registry import ClubRegistry
from club.patrones.observer.notificador_torneo import NotificadorTorneo


class ActividadService:
    """
    Servicio para operaciones CRUD y lógica de negocio de actividades.
    """
    
    def __init__(self):
        self._registry = ClubRegistry.get_instance()
        self._notificador_torneo = NotificadorTorneo()
    
    def crear_actividad(self, nombre: str, costo: Optional[float] = None, 
                       capacidad: Optional[int] = None) -> Optional[Actividad]:
        """Crea una nueva actividad usando Factory Method."""
        try:
            actividad = ActividadFactory.crear_actividad(nombre, costo, capacidad)
            self.registrar_actividad(actividad)
            actividad.agregar_observador(self._notificador_torneo)
            print(f"Actividad '{actividad.nombre}' registrada exitosamente")
            return actividad
        except (ValueError, ActividadYaExisteError) as e:
            print(f"[ERROR] No se pudo crear la actividad: {e}")
            return None
    
    def registrar_actividad(self, actividad: Actividad):
        """Registra una actividad en el sistema."""
        try:
            self._registry.registrar_actividad(actividad)
        except ValueError as e:
            raise ActividadYaExisteError(e)
    
    def obtener_actividad(self, nombre: str) -> Actividad:
        """Obtiene una actividad por su nombre."""
        actividad = self._registry.obtener_actividad(nombre)
        if actividad is None:
            raise ActividadNoEncontradaError(f"No se encontró la actividad '{nombre}'")
        return actividad

    def eliminar_actividad(self, nombre: str) -> bool:
        """Elimina una actividad del sistema."""
        try:
            actividad = self.obtener_actividad(nombre)
            for socio in actividad.socios:
                socio.eliminar_actividad(actividad)
            for profesor in actividad.profesores:
                profesor.desasignar_actividad(actividad)
            if self._registry.eliminar_actividad(nombre):
                print(f"[INFO] Actividad '{nombre}' eliminada del sistema")
                return True
            return False
        except ActividadNoEncontradaError as e:
            print(f"[ERROR] {e}")
            return False

    def inscribir_socio(self, actividad: Actividad, socio: Socio):
        """Inscribe un socio en una actividad."""
        if len(actividad.socios) >= actividad.capacidad:
            raise CapacidadAlcanzadaError(f"Actividad {actividad.nombre} ha alcanzado su capacidad máxima")
        if socio in actividad.socios:
            raise InscripcionError(f"Socio {socio.nombre} ya está inscrito en {actividad.nombre}")
        actividad.inscribir_socio(socio)
        socio.agregar_actividad(actividad)
        print(f"Socio {socio.nombre} inscrito en {actividad.nombre}")

    def desinscribir_socio(self, actividad: Actividad, socio: Socio):
        """Desinscribe un socio de una actividad."""
        if socio not in actividad.socios:
            raise InscripcionError(f"Socio {socio.nombre} no está inscrito en {actividad.nombre}")
        actividad.desinscribir_socio(socio)
        socio.eliminar_actividad(actividad)
        print(f"[INFO] Socio {socio.nombre} desinscrito de {actividad.nombre}")
    
    def asignar_profesor(self, actividad: Actividad, profesor: Profesor):
        """Asigna un profesor a una actividad."""
        if profesor in actividad.profesores:
            print(f"Profesor {profesor.nombre} ya esta asignado a la actividad {actividad.nombre}")
            return
        actividad.agregar_profesor(profesor)
        profesor.asignar_actividad(actividad)
        print(f"Profesor {profesor.nombre} asignado a {actividad.nombre}")

    def desasignar_profesor(self, actividad: Actividad, profesor: Profesor):
        """Desasigna un profesor de una actividad."""
        if profesor not in actividad.profesores:
            print(f"Profesor {profesor.nombre} no se encuentra asignado a la actividad {actividad.nombre}")
            return
        actividad.eliminar_profesor(profesor)
        profesor.desasignar_actividad(actividad)
        print(f"[INFO] Profesor {profesor.nombre} desasignado de {actividad.nombre}")
    
    def crear_torneo(self, actividad: Actividad, nombre_torneo: str, 
                    fecha: str = None, costo_inscripcion: float = 0) -> Optional[Torneo]:
        """Crea un torneo, lo asocia a una actividad y notifica a los observadores."""
        if fecha is None:
            fecha = datetime.now().strftime("%Y-%m-%d")
        torneo = Torneo(nombre_torneo, actividad, fecha, costo_inscripcion)
        actividad.agregar_torneo(torneo)
        datos_evento = {
            'torneo': nombre_torneo,
            'actividad': actividad.nombre,
            'fecha': fecha,
            'costo': costo_inscripcion,
            'socios': actividad.socios
        }
        actividad.notificar_observadores('nuevo_torneo', datos_evento)
        print(f"[INFO] Torneo '{nombre_torneo}' creado para {actividad.nombre}")
        return torneo

    def inscribir_socio_torneo(self, torneo: Torneo, socio: Socio):
        """Inscribe un socio en un torneo con validaciones."""
        if socio not in torneo.actividad.socios:
            raise InscripcionError(f"{socio.nombre} no está inscrito en la actividad {torneo.actividad.nombre} del torneo.")
        if socio in torneo.participantes:
            raise InscripcionError(f"{socio.nombre} ya está inscrito en el torneo '{torneo.nombre}'")
        torneo.inscribir_participante(socio)
        print(f"{socio.nombre} inscrito en torneo '{torneo.nombre}'")

    def mostrar_info_actividad(self, nombre: str):
        """Muestra información completa de una actividad."""
        try:
            actividad = self.obtener_actividad(nombre)
            print("\n" + "="*60)
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
        except ActividadNoEncontradaError as e:
            print(f"[ERROR] {e}")
    
    def listar_actividades_disponibles(self) -> List[str]:
        """Lista las actividades predefinidas disponibles para crear."""
        return ActividadFactory.actividades_disponibles()

# ==============================================================================
# ARCHIVO 26/29: pago_service.py
# Directorio: servicios
# Ruta completa: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/servicios/pago_service.py
# ==============================================================================

"""
Servicio de Gestión de Pagos
Encapsula la lógica de negocio relacionada con pagos de cuotas.
"""

# Standard library imports
from typing import List, Optional

# Local application imports
from club.entidades.pago import Pago
from club.entidades.socio import Socio
from club.patrones.singleton.club_registry import ClubRegistry
from club.patrones.observer.notificador_pago import NotificadorPago
from club.patrones.observer.observer import Observable


class PagoService(Observable):
    """
    Servicio para operaciones de pagos y notificaciones.
    Implementa Observable del patrón Observer.
    """
    
    def __init__(self):
        super().__init__()
        self._registry = ClubRegistry.get_instance()
        self._notificador_pago = NotificadorPago()
        self.agregar_observador(self._notificador_pago)
    
    def registrar_pago(self, socio: Socio, monto: float, metodo: str = "Efectivo") -> Optional[Pago]:
        """Registra un pago de cuota y notifica a los observadores.

        Args:
            socio: Socio que realiza el pago.
            monto: Monto pagado.
            metodo: Método de pago (Efectivo, Tarjeta, Transferencia).

        Returns:
            La instancia del pago registrado o None si falla.
        """
        try:
            pago = Pago(socio, monto, metodo)
            self._registry.registrar_pago(pago)
            socio.estado_pago = "Pagado"
            datos_evento = {
                'socio': socio.nombre,
                'monto': monto,
                'metodo': metodo,
                'comprobante': pago.comprobante
            }
            self.notificar_observadores('pago_registrado', datos_evento)
            print(f"[INFO] Pago registrado exitosamente - Comprobante: {pago.comprobante}")
            return pago
        except Exception as e:
            print(f"[ERROR] No se pudo registrar el pago: {e}")
            return None
    
    def listar_pagos(self) -> List[Pago]:
        """Retorna la lista de todos los pagos registrados."""
        return self._registry.listar_pagos()
    
    def obtener_pagos_socio(self, dni: int) -> List[Pago]:
        """Obtiene todos los pagos realizados por un socio.

        Args:
            dni: DNI del socio.

        Returns:
            Una lista de pagos del socio.
        """
        return self._registry.obtener_pagos_socio(dni)
    
    def calcular_total_recaudado(self) -> float:
        """Calcula el total recaudado en pagos.

        Returns:
            La suma de todos los montos pagados.
        """
        return sum(p.monto for p in self.listar_pagos())
    
    def calcular_total_recaudado_socio(self, dni: int) -> float:
        """Calcula el total pagado por un socio específico.

        Args:
            dni: DNI del socio.

        Returns:
            La suma de todos los pagos del socio.
        """
        return sum(p.monto for p in self.obtener_pagos_socio(dni))
    
    def mostrar_historial_pagos(self, dni: int):
        """Muestra el historial de pagos de un socio.

        Args:
            dni: DNI del socio.
        """
        from club.servicios.socio_service import SocioService
        socio = SocioService().obtener_socio(dni)
        if not socio:
            return
        pagos = self.obtener_pagos_socio(dni)
        print("\n" + "="*60)
        print(f"HISTORIAL DE PAGOS - {socio.nombre}")
        print("="*60)
        if not pagos:
            print("No hay pagos registrados para este socio")
        else:
            for i, pago in enumerate(pagos, 1):
                print(f"\nPago #{i}")
                print(f"Fecha: {pago.fecha.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"Monto: ${pago.monto}")
                print(f"Método: {pago.metodo}")
                print(f"Comprobante: {pago.comprobante}")
            total = sum(p.monto for p in pagos)
            print(f"\n{'='*60}")
            print(f"Total pagado: ${total}")
        print("="*60 + "\n")
    
    def notificar_recordatorio_pago(self, socio: Socio, monto: float, vencimiento: str):
        """Envía un recordatorio de pago a un socio.

        Args:
            socio: Socio al que recordar.
            monto: Monto a pagar.
            vencimiento: Fecha de vencimiento.
        """
        datos_evento = {
            'socio': socio.nombre,
            'monto': monto,
            'vencimiento': vencimiento
        }
        self.notificar_observadores('recordatorio_pago', datos_evento)
    
    def marcar_pago_vencido(self, socio: Socio, monto: float):
        """Notifica sobre un pago vencido.

        Args:
            socio: Socio con pago vencido.
            monto: Monto adeudado.
        """
        socio.estado_pago = "Vencido"
        datos_evento = {
            'socio': socio.nombre,
            'monto': monto
        }
        self.notificar_observadores('pago_vencido', datos_evento)
    
    def generar_reporte_recaudacion(self):
        """Genera un reporte de recaudación total."""
        pagos = self.listar_pagos()
        total = self.calcular_total_recaudado()
        print("\n" + "="*60)
        print("REPORTE DE RECAUDACIÓN")
        print("="*60)
        print(f"Total de pagos registrados: {len(pagos)}")
        print(f"Total recaudado: ${total}")
        if pagos:
            por_metodo = {}
            for pago in pagos:
                metodo = pago.metodo
                por_metodo[metodo] = por_metodo.get(metodo, 0) + pago.monto
            print("\nRecaudación por método de pago:")
            for metodo, monto in por_metodo.items():
                print(f"  • {metodo}: ${monto}")
        print("="*60 + "\n")

# ==============================================================================
# ARCHIVO 27/29: persistencia_service.py
# Directorio: servicios
# Ruta completa: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/servicios/persistencia_service.py
# ==============================================================================

"""
Servicio de Persistencia de Datos
Encapsula la lógica para guardar y cargar el estado del sistema usando Pickle.
"""

# Standard library imports
import pickle
import os

# Local application imports
from club.patrones.singleton.club_registry import ClubRegistry


class PersistenciaService:
    """
    Servicio para guardar y cargar datos del ClubRegistry en archivos .dat separados.
    """
    
    def __init__(self, directorio: str = "data"):
        """Inicializa el servicio de persistencia.

        Args:
            directorio: El nombre del directorio donde se guardarán los datos.
        """
        self._directorio = directorio
        self._registry = ClubRegistry.get_instance()
        self._filenames = {
            "socios": "socios.dat",
            "actividades": "actividades.dat",
            "profesores": "profesores.dat",
            "pagos": "pagos.dat"
        }

    def _get_path(self, filename: str) -> str:
        return os.path.join(self._directorio, filename)

    def guardar_datos(self):
        """Guarda cada diccionario/lista de entidades en un archivo .dat separado."""
        try:
            if not os.path.exists(self._directorio):
                os.makedirs(self._directorio)
            
            data_to_save = {
                "socios": self._registry._socios,
                "actividades": self._registry._actividades,
                "profesores": self._registry._profesores,
                "pagos": self._registry._pagos
            }

            for key, data in data_to_save.items():
                filepath = self._get_path(self._filenames[key])
                with open(filepath, "wb") as f:
                    pickle.dump(data, f)
            
            print(f"[INFO] Datos guardados exitosamente en el directorio '{self._directorio}'")
            
        except Exception as e:
            print(f"[ERROR] No se pudieron guardar los datos: {e}")

    def cargar_datos(self) -> bool:
        """Carga el estado del ClubRegistry desde archivos .dat separados.

        Returns:
            True si al menos un archivo de datos se cargó, False en caso contrario.
        """
        cargado = False
        for key, filename in self._filenames.items():
            filepath = self._get_path(filename)
            if os.path.exists(filepath):
                try:
                    with open(filepath, "rb") as f:
                        data = pickle.load(f)
                        setattr(self._registry, f"_{key}", data)
                    print(f"[INFO] Datos de '{key}' cargados desde {filepath}")
                    cargado = True
                except Exception as e:
                    print(f"[ERROR] No se pudo cargar el archivo {filepath}: {e}")
        
        if not cargado:
            print("[INFO] No se encontraron archivos de datos existentes.")

        return cargado


# ==============================================================================
# ARCHIVO 28/29: profesor_service.py
# Directorio: servicios
# Ruta completa: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/servicios/profesor_service.py
# ==============================================================================

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


# ==============================================================================
# ARCHIVO 29/29: socio_service.py
# Directorio: servicios
# Ruta completa: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/servicios/socio_service.py
# ==============================================================================

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


################################################################################
# FIN DEL INTEGRADOR FINAL
# Total de archivos: 29
# Generado: 2025-11-04 17:46:03
################################################################################
