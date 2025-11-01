"""
Sistema de Gestión de Club Deportivo - DEMO AUTOMÁTICA

Este script demuestra todas las funcionalidades clave y los patrones de diseño implementados.
"""

from club.servicios.socio_service import SocioService
from club.servicios.actividad_service import ActividadService
from club.servicios.profesor_service import ProfesorService
from club.servicios.pago_service import PagoService
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
        
    return service_registry

def demostracion_completa():
    """Ejecuta una demostración completa de las funcionalidades del sistema."""
    
    # --- 1. CONFIGURACIÓN INICIAL ---
    imprimir_titulo("1. CONFIGURACIÓN INICIAL")
    service_registry = setup_services()
    
    # Limpiar datos de ejecuciones anteriores
    ClubRegistry.get_instance().reset()

    socio_service = service_registry.obtener_servicio("socio")
    actividad_service = service_registry.obtener_servicio("actividad")
    profesor_service = service_registry.obtener_servicio("profesor")
    pago_service = service_registry.obtener_servicio("pago")

    print("Servicios inicializados y registrados en ClubServiceRegistry.")
    print(ClubRegistry.get_instance())

    # --- 2. CREACIÓN DE ENTIDADES ---
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

    # --- 3. ESTABLECIENDO RELACIONES ---
    imprimir_titulo("3. ESTABLECIENDO RELACIONES")

    print("--- Asignando profesores a actividades ---")
    actividad_service.asignar_profesor(tenis, p1)
    actividad_service.asignar_profesor(natacion, p2)

    print("\n--- Inscribiendo socios a actividades ---")
    actividad_service.inscribir_socio(tenis, s1) # Ana a Tenis
    actividad_service.inscribir_socio(natacion, s1) # Ana a Natación
    actividad_service.inscribir_socio(tenis, s2) # Carlos a Tenis (siendo Premium)
    actividad_service.inscribir_socio(natacion, s3) # María a Natación

    # --- 4. DEMOSTRACIÓN DE STRATEGY PATTERN (CÁLCULO DE CUOTAS) ---
    imprimir_titulo("4. DEMO DE STRATEGY PATTERN (CÁLCULO DE CUOTAS)")

    for socio in socio_service.listar_socios():
        print(f"--- Calculando cuota para {socio.nombre} ({socio.get_tipo()}) ---")
        descripcion = socio_service.obtener_descripcion_cuota(socio)
        print(descripcion)

    # --- 5. DEMOSTRACIÓN DE OBSERVER PATTERN (PAGOS) ---
    imprimir_titulo("5. DEMO DE OBSERVER PATTERN (PAGOS)")

    print("--- Enviando recordatorios de pago ---")
    for socio in socio_service.listar_socios():
        cuota = socio_service.calcular_cuota(socio)
        pago_service.notificar_recordatorio_pago(socio, cuota, "2025-11-10")

    print("\n--- Registrando un pago ---")
    cuota_ana = socio_service.calcular_cuota(s1)
    pago_service.registrar_pago(s1, cuota_ana, "Tarjeta de Crédito")
    print(f"Estado de pago de {s1.nombre}: {s1.estado_pago}")

    # --- 6. DEMOSTRACIÓN DE OBSERVER PATTERN (TORNEOS) ---
    imprimir_titulo("6. DEMO DE OBSERVER PATTERN (TORNEOS)")

    print("--- Creando un nuevo torneo de Tenis ---")
    print("El sistema notificará automáticamente a los socios inscritos en Tenis (Ana y Carlos).")
    torneo_tenis = actividad_service.crear_torneo(tenis, "Torneo de Otoño", costo_inscripcion=5000)

    print("\n--- Inscribiendo un socio al torneo ---")
    actividad_service.inscribir_socio_torneo(torneo_tenis, s1)
    actividad_service.inscribir_socio_torneo(torneo_tenis, s3) # Intento fallido, no está en la actividad

    # --- 7. DEMOSTRACIÓN DE SINGLETON Y REGISTRY ---
    imprimir_titulo("7. DEMO DE SINGLETON Y REGISTRY")

    print("--- Singleton: ClubRegistry ---")
    r1 = ClubRegistry.get_instance()
    r2 = ClubRegistry.get_instance()
    print(f"Instancia 1 ID: {id(r1)}")
    print(f"Instancia 2 ID: {id(r2)}")
    print(f"¿Son la misma instancia? {r1 is r2}")
    print(r1)

    print("\n--- Registry: ClubServiceRegistry ---")
    sr1 = ClubServiceRegistry.get_instance()
    print(f"Servicios registrados: {sr1.listar_servicios()}")
    print("El patrón Registry nos permite acceder a los servicios de forma centralizada.")

    imprimir_titulo("DEMO FINALIZADA")

if __name__ == "__main__":
    demostracion_completa()
