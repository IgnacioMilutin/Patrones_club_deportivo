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