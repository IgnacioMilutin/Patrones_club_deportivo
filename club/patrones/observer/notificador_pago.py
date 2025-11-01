"""
Observador concreto para notificaciones de pagos
"""

from .observer import Observer


class NotificadorPago(Observer):
    """
    Observador que maneja notificaciones de pagos de cuotas
    """
    
    def __init__(self, nombre: str = "Sistema de Pagos"):
        self._nombre = nombre
    
    def actualizar(self, evento: str, datos: dict):
        """
        Procesa eventos relacionados con pagos
        """
        if evento == "pago_registrado":
            self._notificar_pago_exitoso(datos)
        elif evento == "pago_vencido":
            self._notificar_pago_vencido(datos)
        elif evento == "recordatorio_pago":
            self._notificar_recordatorio(datos)
    
    def _notificar_pago_exitoso(self, datos: dict):
        """Notifica sobre un pago exitoso"""
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
        """Notifica sobre un pago vencido"""
        socio_nombre = datos.get('socio', 'Socio')
        monto = datos.get('monto', 0)
        
        print("\n" + "="*60)
        print(f"[AVISO DE PAGO VENCIDO] - {socio_nombre}")
        print("="*60)
        print(f"Monto adeudado: ${monto}")
        print("Por favor, regularice su situación a la brevedad.")
        print("="*60 + "\n")

    def _notificar_recordatorio(self, datos: dict):
        """Notifica un recordatorio de pago"""
        socio_nombre = datos.get('socio', 'Socio')
        monto = datos.get('monto', 0)
        vencimiento = datos.get('vencimiento', 'Próximamente')
        
        print("\n" + "="*60)
        print(f"[RECORDATORIO DE PAGO] - {socio_nombre}")
        print("="*60)
        print(f"Monto a pagar: ${monto}")
        print(f"Fecha de vencimiento: {vencimiento}")
        print("="*60 + "\n")