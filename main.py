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
