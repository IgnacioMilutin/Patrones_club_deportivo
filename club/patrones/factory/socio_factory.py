"""
Factory Method para creación de Socios
Permite crear diferentes tipos de socios sin conocer las clases concretas
"""

from typing import Optional
from club.entidades.socio import Socio, SocioRegular, SocioPremium, SocioInfantil


class SocioFactory:
    """
    Factory para crear instancias de diferentes tipos de socios
    """
    
    @staticmethod
    def crear_socio(tipo: str, nombre: str, dni: int, edad: Optional[int] = None) -> Socio:
        """
        Crea un socio según el tipo especificado
        
        Args:
            tipo: Tipo de socio ('regular', 'premium', 'infantil')
            nombre: Nombre del socio
            dni: DNI del socio
            edad: Edad (requerida solo para socio infantil)
        
        Returns:
            Instancia de Socio correspondiente
        
        Raises:
            ValueError: Si el tipo de socio no es válido
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
        """Retorna la lista de tipos de socios disponibles"""
        return ["regular", "premium", "infantil"]