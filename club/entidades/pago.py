"""
Entidad Pago - Representa el registro de pagos de cuotas
"""

from datetime import datetime

# Se elimina la dependencia y se usa type hinting
# from club.entidades.socio import Socio

class Pago:
    """Representa un pago de cuota realizado por un socio"""
    
    def __init__(self, socio: 'Socio', monto: float, metodo: str):
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
        """Genera un número de comprobante único"""
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