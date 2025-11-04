"""
Archivo integrador generado automaticamente
Directorio: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/entidades
Fecha: 2025-11-04 17:46:03
Total de archivos integrados: 6
"""

# ================================================================================
# ARCHIVO 1/6: __init__.py
# Ruta: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/entidades/__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/6: actividad.py
# Ruta: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/entidades/actividad.py
# ================================================================================

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

# ================================================================================
# ARCHIVO 3/6: pago.py
# Ruta: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/entidades/pago.py
# ================================================================================

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

# ================================================================================
# ARCHIVO 4/6: profesor.py
# Ruta: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/entidades/profesor.py
# ================================================================================

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

# ================================================================================
# ARCHIVO 5/6: socio.py
# Ruta: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/entidades/socio.py
# ================================================================================

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

# ================================================================================
# ARCHIVO 6/6: torneo.py
# Ruta: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/entidades/torneo.py
# ================================================================================

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

