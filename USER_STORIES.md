# Historias de Usuario - Sistema de Gestion de Club Deportivo

**Proyecto**: ClubDeportivoPy
**Version**: 1.0.0
**Fecha**: Octubre 2025
**Metodologia**: User Story Mapping

---

## Indice

1. [Epic 1: Gestion de Socios](#epic-1-gestion-de-socios)
2. [Epic 2: Gestion de Actividades y Profesores](#epic-2-gestion-de-actividades-y-profesores)
3. [Epic 3: Sistema de Pagos y Cuotas](#epic-3-sistema-de-pagos-y-cuotas)
4. [Epic 4: Notificaciones y Torneos](#epic-4-notificaciones-y-torneos)
5. [Epic 5: Persistencia y Servicios Centrales](#epic-5-persistencia-y-servicios-centrales)
6. [Historias Tecnicas (Patrones de Diseno)](#historias-tecnicas-patrones-de-diseno)

---

## Epic 1: Gestion de Socios

### US-001: Registrar Socio

**Como** administrador del club
**Quiero** registrar nuevos socios en el sistema
**Para** gestionar su participacion en actividades y pagos

#### Criterios de Aceptacion

* [x] Permitir alta de socio con nombre, tipo (regular, premium, infantil) y DNI unico.
* [x] Tipo de socio se crea via Factory Method.
* [x] No se permite duplicar DNI.
* [x] Mostrar mensaje de confirmacion al registrar.

#### Ejemplo de codigo

```python
socio = SocioFactory.crear_socio("regular", nombre="Ana Perez", dni=40123456)
```

---

### US-002: Ver Datos de Socio

**Como** administrador o socio
**Quiero** consultar mis datos personales y actividades
**Para** saber en que deportes estoy inscripto

#### Criterios de Aceptacion

* [x] Debe mostrar nombre, tipo, actividades y estado de pagos.
* [x] Si el socio no tiene actividades, mostrar mensaje informativo.

#### Ejemplo de salida

```
Socio: Ana Perez
Tipo: Regular
Actividades: Tenis, Natacion
Estado de pagos: Al dia
```

---

### US-003: Modificar o Eliminar Socio

**Como** administrador
**Quiero** modificar o eliminar socios registrados
**Para** mantener la base de datos actualizada

#### Criterios de Aceptacion

* [x] Permitir editar tipo o actividades.
* [x] Si se elimina un socio, se eliminan sus inscripciones.

---

## Epic 2: Gestion de Actividades y Profesores

### US-004: Crear Actividad Deportiva

**Como** administrador
**Quiero** crear nuevas actividades deportivas
**Para** ampliar la oferta del club

#### Criterios de Aceptacion

* [x] Cada actividad tiene nombre, costo base y capacidad maxima.
* [x] Creacion via Factory Method.
* [x] Si ya existe una actividad con ese nombre, mostrar error.

#### Ejemplo de codigo

```python
actividad = ActividadFactory.crear_actividad("tenis", costo=20000, capacidad=10)
```

---

### US-005: Asignar Profesores a Actividad

**Como** administrador
**Quiero** asignar uno o mas profesores a una actividad
**Para** garantizar la disponibilidad de instructores

#### Criterios de Aceptacion

* [x] Una actividad puede tener multiples profesores.
* [x] Un profesor puede estar en varias actividades.
* [x] El profesor tiene nombre, DNI y sueldo.

#### Ejemplo de codigo

```python
profesor = Profesor(nombre="Carlos Diaz", dni=30000111, sueldo=150000)
actividad.agregar_profesor(profesor)
```

---

### US-006: Inscribir Socio en Actividad

**Como** socio del club
**Quiero** inscribirme en una actividad deportiva
**Para** participar en torneos y entrenamientos

#### Criterios de Aceptacion

* [x] Solo socios activos pueden inscribirse.
* [x] Verificar capacidad maxima.
* [x] Registrar inscripcion en lista de socios de la actividad.

#### Ejemplo de codigo

```python
actividad_service.inscribir_socio(actividad, socio)
```

---

## Epic 3: Sistema de Pagos y Cuotas

### US-007: Calcular Cuota Mensual

**Como** sistema del club
**Quiero** calcular la cuota mensual de cada socio
**Para** emitir los pagos correspondientes

#### Criterios de Aceptacion

* [x] Usar Strategy Pattern para calcular el monto.
* [x] Regular: suma de costos de actividades inscritas.
* [x] Premium: monto fijo de 30000.
* [x] Infantil: monto fijo reducido de 15000.

#### Ejemplo de codigo

```python
cuota = socio_service.calcular_cuota(socio)
```

---

### US-008: Registrar Pago de Cuota

**Como** socio del club
**Quiero** registrar el pago de mi cuota
**Para** mantenerme al dia

#### Criterios de Aceptacion

* [x] Registrar fecha, monto y metodo de pago.
* [x] Al pagar, se notifica al socio (Observer Pattern).
* [x] Actualizar estado a “Pagado”.

#### Ejemplo de codigo

```python
pago_service.registrar_pago(socio, monto=25000)
```

---

## Epic 4: Notificaciones y Torneos

### US-009: Crear Torneo para una Actividad

**Como** profesor o administrador
**Quiero** crear un torneo asociado a una actividad
**Para** incentivar la participacion de los socios

#### Criterios de Aceptacion

* [x] Registrar nombre, fecha y costo de inscripcion.
* [x] Notificar automaticamente a socios inscriptos (Observer Pattern).

#### Ejemplo de codigo

```python
actividad.crear_torneo("Torneo Primavera", fecha="2025-11-10")
```

---

### US-010: Notificar Pago de Cuota

**Como** sistema del club
**Quiero** enviar notificaciones a los socios al registrar el pago de su cuota
**Para** confirmar la transaccion y mantener transparencia

#### Criterios de Aceptacion

* [x] Al recibir evento de pago, se notifica al socio.
* [x] Usar Observer Pattern para la comunicacion.

#### Ejemplo de salida

```
[NOTIFICACION] Se registro su pago por $25000. Muchas gracias.
```

---

## Epic 5: Persistencia y Servicios Centrales

### US-011: Guardar Datos del Sistema

**Como** administrador
**Quiero** guardar la informacion de socios, actividades y pagos
**Para** no perder los datos al cerrar el programa

#### Criterios de Aceptacion

* [x] Guardar objetos serializados con Pickle.
* [x] Directorio: `data/`.
* [x] Archivos por entidad (socios, actividades, pagos).

---

### US-012: Registry Central de Servicios

**Como** desarrollador del sistema
**Quiero** disponer de un registro central de servicios
**Para** despachar metodos sin usar condicionales `if`

#### Criterios de Aceptacion

* [x] Usar Registry Pattern.
* [x] Unico acceso via Singleton.
* [x] Soportar registro dinamico de servicios.

#### Ejemplo de codigo

```python
registry = ClubServiceRegistry.get_instance()
registry.registrar_servicio("pago", PagoService())
```

---

## Historias Tecnicas (Patrones de Diseno)

### US-TECH-001: Implementar Singleton

**Como** arquitecto de software
**Quiero** garantizar una unica instancia del registro del club
**Para** mantener consistencia en los servicios

---

### US-TECH-002: Implementar Factory Method

**Como** desarrollador
**Quiero** crear socios y actividades sin conocer clases concretas
**Para** simplificar la logica de instanciacion

---

### US-TECH-003: Implementar Observer

**Como** arquitecto del sistema
**Quiero** implementar observadores de notificaciones y pagos
**Para** desacoplar eventos del sistema

---

### US-TECH-004: Implementar Strategy

**Como** desarrollador
**Quiero** calcular cuotas con diferentes estrategias
**Para** mantener flexible la logica de pagos

---

### US-TECH-005: Implementar Registry Pattern

**Como** desarrollador
**Quiero** centralizar los servicios del club
**Para** mejorar la extensibilidad del sistema
