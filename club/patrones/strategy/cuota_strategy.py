"""
Strategy Pattern para el cálculo de cuotas de socios
Permite definir diferentes algoritmos de cálculo según el tipo de socio
"""

from abc import ABC, abstractmethod
from club.entidades.socio import Socio, SocioRegular, SocioPremium, SocioInfantil


class CuotaStrategy(ABC):
    """Interfaz para las estrategias de cálculo de cuota"""
    
    @abstractmethod
    def calcular_cuota(self, socio: Socio) -> float:
        pass
    
    @abstractmethod
    def obtener_descripcion(self, socio: Socio) -> str:
        pass


class CuotaRegularStrategy(CuotaStrategy):
    """Estrategia para socios regulares: suma el costo de sus actividades"""
    
    def calcular_cuota(self, socio: SocioRegular) -> float:
        return sum(actividad.costo for actividad in socio.actividades)
    
    def obtener_descripcion(self, socio: SocioRegular) -> str:
        if not socio.actividades:
            return "Cuota Regular: $0 (sin actividades inscritas)"
        
        calculo_str = " + ".join([f"${a.costo}" for a in socio.actividades])
        total = self.calcular_cuota(socio)
        return f"Cuota Regular: {calculo_str} = ${total}"


class CuotaPremiumStrategy(CuotaStrategy):
    """Estrategia para socios premium: cuota fija"""
    
    def calcular_cuota(self, socio: SocioPremium) -> float:
        return SocioPremium.CUOTA_FIJA
    
    def obtener_descripcion(self, socio: SocioPremium) -> str:
        return f"Cuota Premium: ${SocioPremium.CUOTA_FIJA} (acceso a todas las actividades)"


class CuotaInfantilStrategy(CuotaStrategy):
    """Estrategia para socios infantiles: cuota fija reducida"""
    
    def calcular_cuota(self, socio: SocioInfantil) -> float:
        return SocioInfantil.CUOTA_FIJA
    
    def obtener_descripcion(self, socio: SocioInfantil) -> str:
        return f"Cuota Infantil: ${SocioInfantil.CUOTA_FIJA} (cuota reducida)"


class ContextoCuota:
    """Contexto que utiliza una estrategia para calcular la cuota"""
    
    def __init__(self, estrategia: CuotaStrategy):
        self._estrategia = estrategia
    
    def calcular_cuota(self, socio: Socio) -> float:
        return self._estrategia.calcular_cuota(socio)
    
    def obtener_descripcion(self, socio: Socio) -> str:
        return self._estrategia.obtener_descripcion(socio)
