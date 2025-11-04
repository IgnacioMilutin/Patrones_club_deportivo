"""
Archivo integrador generado automaticamente
Directorio: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/servicios
Fecha: 2025-11-04 17:46:03
Total de archivos integrados: 6
"""

# ================================================================================
# ARCHIVO 1/6: __init__.py
# Ruta: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/servicios/__init__.py
# ================================================================================

from .socio_service import SocioService
from .actividad_service import ActividadService
from .profesor_service import ProfesorService
from .pago_service import PagoService

__all__ = ['SocioService', 'ActividadService', 'ProfesorService', 'PagoService']

# ================================================================================
# ARCHIVO 2/6: actividad_service.py
# Ruta: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/servicios/actividad_service.py
# ================================================================================

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

# ================================================================================
# ARCHIVO 3/6: pago_service.py
# Ruta: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/servicios/pago_service.py
# ================================================================================

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

# ================================================================================
# ARCHIVO 4/6: persistencia_service.py
# Ruta: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/servicios/persistencia_service.py
# ================================================================================

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


# ================================================================================
# ARCHIVO 5/6: profesor_service.py
# Ruta: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/servicios/profesor_service.py
# ================================================================================

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


# ================================================================================
# ARCHIVO 6/6: socio_service.py
# Ruta: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/servicios/socio_service.py
# ================================================================================

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

