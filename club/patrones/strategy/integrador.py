"""
Archivo integrador generado automaticamente
Directorio: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/patrones/strategy
Fecha: 2025-11-04 17:46:03
Total de archivos integrados: 2
"""

# ================================================================================
# ARCHIVO 1/2: __init__.py
# Ruta: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/patrones/strategy/__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/2: cuota_strategy.py
# Ruta: /home/ignaciomilutin/Documentos/UM/DisenoDeSistemas2025/TRABAJO_CLUB/Club_Deportivo/club/patrones/strategy/cuota_strategy.py
# ================================================================================

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


