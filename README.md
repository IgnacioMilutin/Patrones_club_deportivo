# Sistema de Gestion de Club Deportivo

[![Python Version](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-PEP%208-orange.svg)](https://www.python.org/dev/peps/pep-0008/)

Sistema de gestion integral de un **club deportivo**, desarrollado en Python, que demuestra la implementacion de multiples **patrones de diseno**: Singleton, Factory, Observer, Strategy y Registry. El sistema permite administrar socios, actividades deportivas, profesores, torneos y pagos de cuotas, integrando logica de negocio moderna y arquitectura escalable.

---

## Tabla de Contenidos

* [Contexto del Dominio](#contexto-del-dominio)
* [Caracteristicas Principales](#caracteristicas-principales)
* [Arquitectura del Sistema](#arquitectura-del-sistema)
* [Patrones de Diseno Implementados](#patrones-de-diseno-implementados)
* [Requisitos del Sistema](#requisitos-del-sistema)
* [Instalacion](#instalacion)
* [Uso del Sistema](#uso-del-sistema)
* [Estructura del Proyecto](#estructura-del-proyecto)
* [Contribucion](#contribucion)
* [Licencia](#licencia)

---

## Contexto del Dominio

### Problema que Resuelve

El sistema **ClubDeportivoPy** busca facilitar la gestion de socios, actividades deportivas, profesores, pagos y notificaciones dentro de un club. Permite automatizar procesos, reducir errores administrativos y ofrecer una experiencia moderna para los miembros.

### Actores del Sistema

* **Socio Regular**: Paga segun las actividades en las que participa.
* **Socio Premium**: Paga una cuota fija y accede a todas las actividades.
* **Socio Infantil**: Paga una cuota reducida y tiene acceso limitado a ciertas actividades.
* **Profesor**: Enseña una o mas actividades, recibe un sueldo mensual.
* **Administrador**: Gestiona socios, profesores, actividades y torneos.

### Flujo de Operaciones Tipico

```
1. REGISTRO DE SOCIO --> Se crea un nuevo socio (Regular, Premium o Infantil)
2. INSCRIPCION A ACTIVIDADES --> El socio se inscribe en una o mas actividades
3. ASIGNACION DE PROFESORES --> Cada actividad cuenta con uno o mas profesores
4. CALCULO DE CUOTA --> El sistema calcula la cuota segun el tipo de socio y las actividades
5. PAGO DE CUOTA --> Al pagar, se notifica al socio (Observer)
6. TORNEOS --> Las actividades pueden crear torneos, y los socios inscriptos son notificados automaticamente
7. PERSISTENCIA --> Toda la informacion se guarda para futuras consultas
```

---

## Caracteristicas Principales

### Funcionalidades del Sistema

#### 1. Gestion de Socios

* Alta, baja y modificacion de socios.
* Creacion dinamica via **Factory Method** segun tipo (Regular, Premium, Infantil).
* Calculo de cuotas mediante **Strategy Pattern**.
* Registro de actividades asociadas y notificaciones personalizadas.

#### 2. Gestion de Actividades

* Actividades individuales (Tenis, Natacion, Padel, Gimnasia, etc.).
* Cada actividad tiene:

  * Un costo base
  * Uno o mas profesores
  * Lista de socios inscriptos
  * Torneos asociados
* Creacion mediante **Factory Method**.

#### 3. Sistema de Profesores

* Registro de profesores con sueldo fijo.
* Asociacion de profesores a una o varias actividades.
* Control de multiples profesores por actividad.

#### 4. Pagos y Cuotas

* Calculo automatico de cuotas segun **Strategy Pattern**.
* Notificacion del pago via **Observer Pattern**.
* Registro de pagos en el sistema.

#### 5. Notificaciones y Torneos

* Sistema de eventos y notificaciones basado en **Observer Pattern**.
* Los socios reciben notificaciones sobre:

  * Nuevos torneos en actividades donde participan.
  * Confirmacion de pago de cuotas.

#### 6. Registry Centralizado

* Un **Registry Pattern** centraliza los servicios del sistema:

  * `SocioService`, `ActividadService`, `ProfesorService`, `PagoService`.
* Evita el uso de condicionales `if isinstance()` para despachar metodos.

#### 7. Persistencia

* Uso de **Pickle** para almacenamiento de datos (socios, actividades, torneos, profesores).
* Recuperacion de datos persistidos para consultas futuras.

---

## Arquitectura del Sistema

### Principios Arquitectonicos

El sistema aplica los principios **SOLID**, con una arquitectura por capas:

```
+-----------------------------------+
|   PRESENTACION (CLI o API)       |
+-----------------------------------+
|   SERVICIOS (Socios, Actividades) |
+-----------------------------------+
|   ENTIDADES (Datos de Dominio)    |
+-----------------------------------+
|   PATRONES (Singleton, Factory...) |
+-----------------------------------+
|   INFRAESTRUCTURA (Persistencia)  |
+-----------------------------------+
```

---

## Patrones de Diseno Implementados

### 1. Singleton

**Ubicacion**: `club/patrones/singleton/club_registry.py`

**Uso**: Gestiona una unica instancia del registro general de servicios (Socios, Actividades, Pagos).

**Beneficio**: Estado consistente y unico acceso global.

---

### 2. Factory Method

**Ubicacion**: `club/patrones/factory/socio_factory.py` y `club/patrones/factory/actividad_factory.py`

**Uso**: Creacion de socios y actividades sin depender de clases concretas.

**Ejemplo**:

```python
SocioFactory.crear_socio("premium", nombre="Juan Perez")
ActividadFactory.crear_actividad("tenis", costo=20000)
```

---

### 3. Observer

**Ubicacion**: `club/patrones/observer/`

**Uso**: Notificaciones de torneos y pagos.

**Ejemplo**:

* Cuando se crea un torneo, todos los socios inscriptos son notificados.
* Cuando un socio paga su cuota, se dispara un evento de confirmacion.

---

### 4. Strategy

**Ubicacion**: `club/patrones/strategy/cuota_strategy.py`

**Uso**: Calculo de cuotas segun tipo de socio.

**Ejemplo**:

* `CuotaRegularStrategy`: suma el costo de las actividades inscritas.
* `CuotaPremiumStrategy`: paga un monto fijo.
* `CuotaInfantilStrategy`: paga un monto fijo reducido.

---

### 5. Registry (Bonus)

**Ubicacion**: `club/patrones/registry/club_service_registry.py`

**Uso**: Despacho polimorfico de servicios.

**Ejemplo**:

```python
registry = ClubServiceRegistry.get_instance()
service = registry.obtener_servicio("socio")
service.registrar_nuevo_socio(socio)
```

---

## Requisitos del Sistema

* **Python 3.13+**
* Librerias estandar de Python (sin dependencias externas)
* RAM minima: 512MB
* Espacio libre en disco: 50MB

---

## Instalacion

```bash
git clone https://github.com/usuario/club-deportivo.git
cd club-deportivo
python main.py
```

---

## Uso del Sistema

Ejemplo rapido:

```python
from club.servicios.socio_service import SocioService
from club.servicios.actividad_service import ActividadService

socio_service = SocioService()
actividad_service = ActividadService()

socio = socio_service.crear_socio("regular", nombre="Ana Lopez")
actividad = actividad_service.crear_actividad("tenis", costo=20000)
actividad_service.inscribir_socio(actividad, socio)

# Calculo de cuota (Strategy)
print(socio_service.calcular_cuota(socio))

# Notificacion (Observer)
actividad.crear_torneo("Torneo de Primavera")
```

---

## Estructura del Proyecto

```
ClubDeportivo/
|
+-- main.py
+-- README.md
+-- USER_STORIES.md
|
+-- club/
    +-- entidades/
    |   +-- socio.py
    |   +-- actividad.py
    |   +-- profesor.py
    |   +-- torneo.py
    |   +-- pago.py
    |
    +-- servicios/
    |   +-- socio_service.py
    |   +-- actividad_service.py
    |   +-- profesor_service.py
    |   +-- pago_service.py
    |
    +-- patrones/
        +-- singleton/
        +-- factory/
        +-- observer/
        +-- strategy/
        +-- registry/
```

---

## Contribucion

1. Forkea el repositorio.
2. Crea una rama: `git checkout -b feature/nueva-funcion`.
3. Realiza tus cambios y haz commit.
4. Crea un Pull Request.

---

## Licencia

Proyecto distribuido bajo licencia **MIT**.
