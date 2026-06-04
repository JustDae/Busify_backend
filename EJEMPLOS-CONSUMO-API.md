# EJEMPLOS DE CONSUMO DE LA API - BUSIFY

Ejemplos ficticios y reales para consumir todos los endpoints de la API Busify con tokens JWT.

## URLs Base

**Desarrollo (Local):** `http://127.0.0.1:8000/api`

**Producción:** `https://busify.daelabs.tech/api`

---

## Tabla de Contenidos

* [1. Autenticación](#1-autenticación)
* [2. Usuarios](#2-usuarios)
* [3. Cooperativas](#3-cooperativas)
* [4. Buses](#4-buses)
* [5. Choferes](#5-choferes)
* [6. Rutas](#6-rutas)
* [7. Paradas](#7-paradas)
* [8. Viajes](#8-viajes)
* [9. Flujo Completo](#9-flujo-completo)
* [10. Ejemplos Reales en Producción](#10-ejemplos-reales-en-producción)

---

## 1. AUTENTICACIÓN

### 1.1 Registro de Usuario

```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "juan_perez",
    "email": "juan.perez@example.com",
    "password": "SecurePass123!",
    "password2": "SecurePass123!"
  }'
```

**Respuesta exitosa (201):**
```json
{
  "id": 5,
  "username": "juan_perez",
  "email": "juan.perez@example.com",
  "is_staff": false,
  "message": "Usuario registrado exitosamente"
}
```

---

### 1.2 Login (Obtener Tokens)

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "juan_perez",
    "password": "SecurePass123!"
  }'
```

**Respuesta exitosa (200):**
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc4MDU4Mzc3NCwiaWF0IjoxNzgwNDk3Mzc0LCJqdGkiOiJkZjc3YjUxZjA3NmM0NzNiODBhMDFkOTE0YWIxOGY1NCIsInVzZXJfaWQiOiI1In0.XXX",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzgwNTAxMzc0LCJpYXQiOjE3ODA0OTczNzQsImp0aSI6IjM4NjhjZDg1YjI1OTRjYTA5ZTUwZTc1ZThhN2U5NTQ2IiwidXNlcl9pZCI6IjUifQ.XXX"
}
```

**Guardar los tokens:**
```bash
export ACCESS_TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzgwNTAxMzc0LCJpYXQiOjE3ODA0OTczNzQsImp0aSI6IjM4NjhjZDg1YjI1OTRjYTA5ZTUwZTc1ZThhN2U5NTQ2IiwidXNlcl9pZCI6IjUifQ.XXX"
export REFRESH_TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc4MDU4Mzc3NCwiaWF0IjoxNzgwNDk3Mzc0LCJqdGkiOiJkZjc3YjUxZjA3NmM0NzNiODBhMDFkOTE0YWIxOGY1NCIsInVzZXJfaWQiOiI1In0.XXX"
```

---

### 1.3 Refrescar Token

El access token expira en 1 hora. Para obtener uno nuevo:

```bash
curl -X POST http://127.0.0.1:8000/api/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d "{
    \"refresh\": \"$REFRESH_TOKEN\"
  }"
```

**Respuesta exitosa (200):**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzgwNTAxMzc0LCJpYXQiOjE3ODA0OTczNzQsImp0aSI6IjM4NjhjZDg1YjI1OTRjYTA5ZTUwZTc1ZThhN2U5NTQ2IiwidXNlcl9pZCI6IjUifQ.XXX"
}
```

---

### 1.4 Logout

```bash
curl -X POST http://127.0.0.1:8000/api/auth/logout/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d "{
    \"refresh\": \"$REFRESH_TOKEN\"
  }"
```

**Respuesta exitosa (200):**
```json
{
  "message": "Logout exitoso"
}
```

---

## 2. USUARIOS

### 2.1 Obtener Perfil (Token Requerido)

```bash
curl -X GET http://127.0.0.1:8000/api/users/profile/ \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

**Respuesta exitosa (200):**
```json
{
  "id": 5,
  "username": "juan_perez",
  "email": "juan.perez@example.com",
  "first_name": "",
  "last_name": "",
  "is_active": true,
  "is_staff": false,
  "date_joined": "2026-06-03T10:30:00Z"
}
```

---

### 2.2 Cambiar Contraseña

```bash
curl -X POST http://127.0.0.1:8000/api/users/change-password/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{
    "current_password": "SecurePass123!",
    "new_password": "NewSecurePass456!",
    "new_password2": "NewSecurePass456!"
  }'
```

**Respuesta exitosa (200):**
```json
{
  "message": "Contraseña cambiada exitosamente"
}
```

---

## 3. COOPERATIVAS

### 3.1 Listar Cooperativas

```bash
curl -X GET http://127.0.0.1:8000/api/cooperativas/ \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

**Respuesta exitosa (200):**
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Cooperativa Transportes Universal",
      "is_active": true,
      "created_at": "2026-06-01T08:00:00Z",
      "updated_at": "2026-06-01T08:00:00Z"
    },
    {
      "id": 2,
      "name": "Transportes Quito Express",
      "is_active": true,
      "created_at": "2026-06-02T10:30:00Z",
      "updated_at": "2026-06-02T10:30:00Z"
    }
  ]
}
```

---

### 3.2 Crear Cooperativa

```bash
curl -X POST http://127.0.0.1:8000/api/cooperativas/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{
    "name": "Cooperativa Sur Express",
    "is_active": true
  }'
```

**Respuesta exitosa (201):**
```json
{
  "id": 3,
  "name": "Cooperativa Sur Express",
  "is_active": true,
  "created_at": "2026-06-03T11:00:00Z",
  "updated_at": "2026-06-03T11:00:00Z"
}
```

---

### 3.3 Actualizar Cooperativa

```bash
curl -X PATCH http://127.0.0.1:8000/api/cooperativas/3/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{
    "name": "Cooperativa Sur Express Actualizada",
    "is_active": true
  }'
```

**Respuesta exitosa (200):**
```json
{
  "id": 3,
  "name": "Cooperativa Sur Express Actualizada",
  "is_active": true,
  "created_at": "2026-06-03T11:00:00Z",
  "updated_at": "2026-06-03T11:15:00Z"
}
```

---

### 3.4 Eliminar Cooperativa

```bash
curl -X DELETE http://127.0.0.1:8000/api/cooperativas/3/ \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

**Respuesta exitosa (204):** Sin contenido

---

## 4. BUSES

### 4.1 Listar Buses

```bash
curl -X GET http://127.0.0.1:8000/api/buses/ \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

**Respuesta exitosa (200):**
```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "unit_number": "C-045",
      "plate": "PCQ-7894",
      "model": "Mercedes-Benz Marcopolo",
      "capacity": 45,
      "status": "active",
      "created_at": "2026-06-01T08:00:00Z",
      "updated_at": "2026-06-01T08:00:00Z"
    },
    {
      "id": 2,
      "unit_number": "C-046",
      "plate": "PEQ-1234",
      "model": "Volvo B420",
      "capacity": 50,
      "status": "active",
      "created_at": "2026-06-01T09:00:00Z",
      "updated_at": "2026-06-01T09:00:00Z"
    }
  ]
}
```

---

### 4.2 Crear Bus

```bash
curl -X POST http://127.0.0.1:8000/api/buses/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{
    "unit_number": "C-047",
    "plate": "PFQ-5678",
    "model": "Mercedes-Benz Sprinter",
    "capacity": 40,
    "status": "active"
  }'
```

**Respuesta exitosa (201):**
```json
{
  "id": 3,
  "unit_number": "C-047",
  "plate": "PFQ-5678",
  "model": "Mercedes-Benz Sprinter",
  "capacity": 40,
  "status": "active",
  "created_at": "2026-06-03T11:20:00Z",
  "updated_at": "2026-06-03T11:20:00Z"
}
```

---

### 4.3 Filtrar Buses por Placa

```bash
curl -X GET "http://127.0.0.1:8000/api/buses/?plate=PCQ-7894" \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

---

### 4.4 Filtrar Buses por Estado

```bash
curl -X GET "http://127.0.0.1:8000/api/buses/?status=active" \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

---

## 5. CHOFERES

### 5.1 Listar Choferes

```bash
curl -X GET http://127.0.0.1:8000/api/choferes/ \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

**Respuesta exitosa (200):**
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "first_name": "Carlos",
      "last_name": "Andrade",
      "license_number": "1725896341",
      "daily_rate": "45.00",
      "trips_completed": 12,
      "is_active": true,
      "created_at": "2026-06-01T08:00:00Z",
      "updated_at": "2026-06-01T08:00:00Z"
    },
    {
      "id": 2,
      "first_name": "Juan",
      "last_name": "Fernández",
      "license_number": "1756234892",
      "daily_rate": "50.00",
      "trips_completed": 25,
      "is_active": true,
      "created_at": "2026-06-01T09:00:00Z",
      "updated_at": "2026-06-01T09:00:00Z"
    }
  ]
}
```

---

### 5.2 Crear Chofer

```bash
curl -X POST http://127.0.0.1:8000/api/choferes/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{
    "first_name": "Miguel",
    "last_name": "Gutierrez",
    "license_number": "1728543921",
    "daily_rate": "48.00",
    "trips_completed": 0,
    "is_active": true
  }'
```

**Respuesta exitosa (201):**
```json
{
  "id": 3,
  "first_name": "Miguel",
  "last_name": "Gutierrez",
  "license_number": "1728543921",
  "daily_rate": "48.00",
  "trips_completed": 0,
  "is_active": true,
  "created_at": "2026-06-03T11:30:00Z",
  "updated_at": "2026-06-03T11:30:00Z"
}
```

---

## 6. RUTAS

### 6.1 Listar Rutas

```bash
curl -X GET http://127.0.0.1:8000/api/rutas/ \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

**Respuesta exitosa (200):**
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Troncal Central Sur",
      "description": "Ruta principal desde El Recreo hasta La Marín",
      "origin": "Terminal Sur El Recreo",
      "destination": "Estación Marín Central",
      "base_fare": "0.35",
      "is_active": true,
      "created_at": "2026-06-01T08:00:00Z",
      "updated_at": "2026-06-01T08:00:00Z"
    }
  ]
}
```

---

### 6.2 Crear Ruta

```bash
curl -X POST http://127.0.0.1:8000/api/rutas/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{
    "name": "Línea Norte Express",
    "description": "Ruta rápida hacia el norte de la ciudad",
    "origin": "Terminal Central",
    "destination": "Terminal Norte",
    "base_fare": "0.40",
    "is_active": true
  }'
```

**Respuesta exitosa (201):**
```json
{
  "id": 2,
  "name": "Línea Norte Express",
  "description": "Ruta rápida hacia el norte de la ciudad",
  "origin": "Terminal Central",
  "destination": "Terminal Norte",
  "base_fare": "0.40",
  "is_active": true,
  "created_at": "2026-06-03T11:40:00Z",
  "updated_at": "2026-06-03T11:40:00Z"
}
```

---

### 6.3 Obtener Estadísticas de Rutas

```bash
curl -X GET http://127.0.0.1:8000/api/rutas/stats/ \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

**Respuesta exitosa (200):**
```json
{
  "total_routes": 2,
  "active_routes": 2,
  "inactive_routes": 0,
  "total_stops": 8,
  "average_stops_per_route": 4.0,
  "total_fare_collected": "125.50",
  "routes": [
    {
      "id": 1,
      "name": "Troncal Central Sur",
      "stops_count": 5,
      "trips_count": 12,
      "total_fare": "75.50"
    },
    {
      "id": 2,
      "name": "Línea Norte Express",
      "stops_count": 3,
      "trips_count": 8,
      "total_fare": "50.00"
    }
  ]
}
```

---

## 7. PARADAS

### 7.1 Listar Paradas

```bash
curl -X GET http://127.0.0.1:8000/api/paradas/ \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

**Respuesta exitosa (200):**
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Parada Villa Flora",
      "description": "Frente al centro comercial",
      "distance": "2.40",
      "sequence": 1,
      "is_active": true,
      "ruta_id": 1,
      "created_at": "2026-06-01T08:00:00Z",
      "updated_at": "2026-06-01T08:00:00Z"
    },
    {
      "id": 2,
      "name": "Parada La Gasca",
      "description": "Entrada a La Gasca",
      "distance": "5.20",
      "sequence": 2,
      "is_active": true,
      "ruta_id": 1,
      "created_at": "2026-06-01T08:30:00Z",
      "updated_at": "2026-06-01T08:30:00Z"
    }
  ]
}
```

---

### 7.2 Crear Parada

```bash
curl -X POST http://127.0.0.1:8000/api/paradas/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{
    "name": "Parada Carcelen",
    "description": "Centro comercial Carcelén",
    "distance": 8.5,
    "sequence": 3,
    "is_active": true,
    "ruta_id": 1
  }'
```

**Respuesta exitosa (201):**
```json
{
  "id": 6,
  "name": "Parada Carcelen",
  "description": "Centro comercial Carcelén",
  "distance": "8.50",
  "sequence": 3,
  "is_active": true,
  "ruta_id": 1,
  "created_at": "2026-06-03T11:50:00Z",
  "updated_at": "2026-06-03T11:50:00Z"
}
```

---

### 7.3 Actualizar Secuencia de Parada

```bash
curl -X POST http://127.0.0.1:8000/api/paradas/6/update-sequence/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{
    "sequence": 5
  }'
```

**Respuesta exitosa (200):**
```json
{
  "id": 6,
  "name": "Parada Carcelen",
  "description": "Centro comercial Carcelén",
  "distance": "8.50",
  "sequence": 5,
  "is_active": true,
  "ruta_id": 1,
  "created_at": "2026-06-03T11:50:00Z",
  "updated_at": "2026-06-03T12:00:00Z"
}
```

---

### 7.4 Obtener Paradas de una Ruta

```bash
curl -X GET http://127.0.0.1:8000/api/rutas/1/paradas/ \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

**Respuesta exitosa (200):**
```json
{
  "ruta_id": 1,
  "ruta_name": "Troncal Central Sur",
  "total_stops": 5,
  "paradas": [
    {
      "id": 1,
      "name": "Parada Villa Flora",
      "description": "Frente al centro comercial",
      "distance": "2.40",
      "sequence": 1
    },
    {
      "id": 2,
      "name": "Parada La Gasca",
      "description": "Entrada a La Gasca",
      "distance": "5.20",
      "sequence": 2
    }
  ]
}
```

---

### 7.5 Obtener Estadísticas de Paradas

```bash
curl -X GET http://127.0.0.1:8000/api/paradas/stats/ \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

**Respuesta exitosa (200):**
```json
{
  "total_stops": 6,
  "active_stops": 6,
  "inactive_stops": 0,
  "routes_with_stops": 2,
  "average_stops_per_route": 3.0,
  "longest_distance": "12.50",
  "shortest_distance": "2.40",
  "total_distance_covered": "42.80"
}
```

---

## 8. VIAJES

### 8.1 Listar Viajes

```bash
curl -X GET http://127.0.0.1:8000/api/viajes/ \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

**Respuesta exitosa (200):**
```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "ruta": 1,
      "ruta_name": "Troncal Central Sur",
      "bus": 1,
      "bus_unit": "C-045",
      "chofer": 1,
      "chofer_name": "Carlos Andrade",
      "status": "completed",
      "departure_time": "2026-06-01T08:00:00Z",
      "estimated_arrival": "2026-06-01T09:30:00Z",
      "actual_arrival": "2026-06-01T09:28:00Z",
      "passenger_count": 42,
      "created_at": "2026-06-01T07:50:00Z",
      "updated_at": "2026-06-01T09:30:00Z"
    }
  ]
}
```

---

### 8.2 Crear Viaje

```bash
curl -X POST http://127.0.0.1:8000/api/viajes/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{
    "ruta": 1,
    "bus": 1,
    "chofer": 1,
    "status": "scheduled",
    "departure_time": "2026-06-03T14:00:00Z",
    "estimated_arrival": "2026-06-03T15:30:00Z",
    "passenger_count": 0
  }'
```

**Respuesta exitosa (201):**
```json
{
  "id": 4,
  "ruta": 1,
  "ruta_name": "Troncal Central Sur",
  "bus": 1,
  "bus_unit": "C-045",
  "chofer": 1,
  "chofer_name": "Carlos Andrade",
  "status": "scheduled",
  "departure_time": "2026-06-03T14:00:00Z",
  "estimated_arrival": "2026-06-03T15:30:00Z",
  "actual_arrival": null,
  "passenger_count": 0,
  "created_at": "2026-06-03T12:10:00Z",
  "updated_at": "2026-06-03T12:10:00Z"
}
```

---

### 8.3 Agregar Pasajeros a un Viaje

```bash
curl -X POST http://127.0.0.1:8000/api/viajes/4/add-passenger/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{
    "quantity": 5
  }'
```

**Respuesta exitosa (200):**
```json
{
  "id": 4,
  "ruta": 1,
  "ruta_name": "Troncal Central Sur",
  "bus": 1,
  "bus_unit": "C-045",
  "bus_capacity": 45,
  "chofer": 1,
  "chofer_name": "Carlos Andrade",
  "status": "scheduled",
  "departure_time": "2026-06-03T14:00:00Z",
  "estimated_arrival": "2026-06-03T15:30:00Z",
  "passenger_count": 5,
  "message": "Se agregaron 5 pasajeros. Total actual: 5/45"
}
```

---

### 8.4 Iniciar Ruta

```bash
curl -X POST http://127.0.0.1:8000/api/viajes/4/start-route/ \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

**Respuesta exitosa (200):**
```json
{
  "id": 4,
  "status": "en_route",
  "message": "Viaje iniciado correctamente",
  "started_at": "2026-06-03T14:00:00Z"
}
```

---

### 8.5 Actualizar Estado de Viaje

```bash
curl -X PATCH http://127.0.0.1:8000/api/viajes/4/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{
    "status": "completed",
    "actual_arrival": "2026-06-03T15:28:00Z"
  }'
```

**Estados válidos:** `scheduled`, `en_route`, `completed`, `delayed`, `cancelled`

**Respuesta exitosa (200):**
```json
{
  "id": 4,
  "ruta": 1,
  "bus": 1,
  "chofer": 1,
  "status": "completed",
  "departure_time": "2026-06-03T14:00:00Z",
  "estimated_arrival": "2026-06-03T15:30:00Z",
  "actual_arrival": "2026-06-03T15:28:00Z",
  "passenger_count": 5,
  "updated_at": "2026-06-03T15:28:00Z"
}
```

---

### 8.6 Obtener Estadísticas de Viajes

```bash
curl -X GET http://127.0.0.1:8000/api/viajes/stats/ \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

**Respuesta exitosa (200):**
```json
{
  "total_trips": 4,
  "completed_trips": 1,
  "scheduled_trips": 2,
  "en_route_trips": 1,
  "delayed_trips": 0,
  "cancelled_trips": 0,
  "total_passengers": 47,
  "average_passengers_per_trip": 11.75,
  "statistics_by_status": {
    "completed": {
      "count": 1,
      "total_passengers": 42
    },
    "scheduled": {
      "count": 2,
      "total_passengers": 5
    },
    "en_route": {
      "count": 1,
      "total_passengers": 0
    }
  }
}
```

---

## 9. FLUJO COMPLETO

Ejemplo de un flujo típico desde registro hasta completar un viaje:

### Paso 1: Registrar Usuario

```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin_busify",
    "email": "admin@busify.com",
    "password": "Admin123!@#",
    "password2": "Admin123!@#"
  }'
```

### Paso 2: Hacer Login

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin_busify",
    "password": "Admin123!@#"
  }'
```

Guardar `access_token` en variable de entorno:
```bash
export TOKEN="<access_token_aqui>"
```

### Paso 3: Crear Cooperativa

```bash
curl -X POST http://127.0.0.1:8000/api/cooperativas/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "Cooperativa El Dorado",
    "is_active": true
  }'
```

### Paso 4: Crear Bus

```bash
curl -X POST http://127.0.0.1:8000/api/buses/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "unit_number": "C-100",
    "plate": "PZZ-9999",
    "model": "Hino 500",
    "capacity": 50,
    "status": "active"
  }'
```

### Paso 5: Crear Chofer

```bash
curl -X POST http://127.0.0.1:8000/api/choferes/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "first_name": "Roberto",
    "last_name": "López",
    "license_number": "1798765432",
    "daily_rate": "55.00",
    "trips_completed": 0,
    "is_active": true
  }'
```

### Paso 6: Crear Ruta

```bash
curl -X POST http://127.0.0.1:8000/api/rutas/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "Ruta El Dorado",
    "description": "Ruta comercial principal",
    "origin": "Centro Comercial El Dorado",
    "destination": "Estación Terminal",
    "base_fare": "0.35",
    "is_active": true
  }'
```

### Paso 7: Crear Parada

```bash
curl -X POST http://127.0.0.1:8000/api/paradas/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "Parada Inicio",
    "description": "Punto de salida",
    "distance": 0.0,
    "sequence": 1,
    "is_active": true,
    "ruta_id": 3
  }'
```

### Paso 8: Crear Viaje

```bash
curl -X POST http://127.0.0.1:8000/api/viajes/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "ruta": 3,
    "bus": 3,
    "chofer": 3,
    "status": "scheduled",
    "departure_time": "2026-06-04T08:00:00Z",
    "estimated_arrival": "2026-06-04T09:00:00Z",
    "passenger_count": 0
  }'
```

### Paso 9: Agregar Pasajeros

```bash
curl -X POST http://127.0.0.1:8000/api/viajes/5/add-passenger/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "quantity": 35
  }'
```

### Paso 10: Iniciar Ruta

```bash
curl -X POST http://127.0.0.1:8000/api/viajes/5/start-route/ \
  -H "Authorization: Bearer $TOKEN"
```

### Paso 11: Completar Viaje

```bash
curl -X PATCH http://127.0.0.1:8000/api/viajes/5/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "status": "completed",
    "actual_arrival": "2026-06-04T08:58:00Z"
  }'
```

### Paso 12: Obtener Estadísticas Finales

```bash
curl -X GET http://127.0.0.1:8000/api/viajes/stats/ \
  -H "Authorization: Bearer $TOKEN"
```

---

## NOTAS IMPORTANTES

### Manejo de Errores

**Error 401 - No Autorizado:**
```json
{
  "detail": "Token inválido o expirado"
}
```

**Error 403 - Permiso Denegado:**
```json
{
  "detail": "No tienes permiso para realizar esta acción"
}
```

**Error 404 - No Encontrado:**
```json
{
  "detail": "No encontrado"
}
```

**Error 400 - Solicitud Incorrecta:**
```json
{
  "field_name": [
    "Este campo es obligatorio."
  ]
}
```

### Paginación

Para endpoints que devuelven listas, puedes usar paginación:

```bash
curl -X GET "http://127.0.0.1:8000/api/viajes/?page=2&page_size=10" \
  -H "Authorization: Bearer $TOKEN"
```

### Filtrado y Búsqueda

Algunos endpoints soportan filtrado:

```bash
# Filtrar buses por estado
curl -X GET "http://127.0.0.1:8000/api/buses/?status=active" \
  -H "Authorization: Bearer $TOKEN"

# Buscar por texto
curl -X GET "http://127.0.0.1:8000/api/buses/?search=Mercedes" \
  -H "Authorization: Bearer $TOKEN"
```

---

**Última actualización:** 3 de junio de 2026

---

## 10. EJEMPLOS REALES EN PRODUCCIÓN

Esta sección contiene ejemplos reales usando el backend en producción.

### URL Base Producción

```
https://busify.daelabs.tech/api
```

---

### 10.1 Registro de Usuario (Producción)

```bash
curl -X POST https://busify.daelabs.tech/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "usuario_produccion",
    "email": "usuario@empresa.com",
    "password": "SecurePass123!",
    "password2": "SecurePass123!"
  }'
```

---

### 10.2 Login en Producción

```bash
curl -X POST https://busify.daelabs.tech/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "usuario_produccion",
    "password": "SecurePass123!"
  }'
```

Guardar tokens para uso posterior:
```bash
export PROD_TOKEN="<access_token_aqui>"
export PROD_REFRESH="<refresh_token_aqui>"
```

---

### 10.3 Obtener Perfil (Producción)

```bash
curl -X GET https://busify.daelabs.tech/api/users/profile/ \
  -H "Authorization: Bearer $PROD_TOKEN"
```

---

### 10.4 Listar Cooperativas (Producción)

```bash
curl -X GET https://busify.daelabs.tech/api/cooperativas/ \
  -H "Authorization: Bearer $PROD_TOKEN"
```

---

### 10.5 Listar Buses (Producción)

```bash
curl -X GET https://busify.daelabs.tech/api/buses/ \
  -H "Authorization: Bearer $PROD_TOKEN"
```

---

### 10.6 Listar Choferes (Producción)

```bash
curl -X GET https://busify.daelabs.tech/api/choferes/ \
  -H "Authorization: Bearer $PROD_TOKEN"
```

---

### 10.7 Listar Rutas (Producción)

```bash
curl -X GET https://busify.daelabs.tech/api/rutas/ \
  -H "Authorization: Bearer $PROD_TOKEN"
```

---

### 10.8 Listar Paradas (Producción)

```bash
curl -X GET https://busify.daelabs.tech/api/paradas/ \
  -H "Authorization: Bearer $PROD_TOKEN"
```

---

### 10.9 Listar Viajes (Producción)

```bash
curl -X GET https://busify.daelabs.tech/api/viajes/ \
  -H "Authorization: Bearer $PROD_TOKEN"
```

---

### 10.10 Crear Cooperativa (Producción)

```bash
curl -X POST https://busify.daelabs.tech/api/cooperativas/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $PROD_TOKEN" \
  -d '{
    "name": "Cooperativa Producción",
    "is_active": true
  }'
```

---

### 10.11 Crear Bus (Producción)

```bash
curl -X POST https://busify.daelabs.tech/api/buses/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $PROD_TOKEN" \
  -d '{
    "unit_number": "PROD-001",
    "plate": "ABC-1234",
    "model": "Mercedes-Benz Marcopolo",
    "capacity": 45,
    "status": "active"
  }'
```

---

### 10.12 Crear Chofer (Producción)

```bash
curl -X POST https://busify.daelabs.tech/api/choferes/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $PROD_TOKEN" \
  -d '{
    "first_name": "Juan",
    "last_name": "Pérez",
    "license_number": "1234567890",
    "daily_rate": "50.00",
    "trips_completed": 0,
    "is_active": true
  }'
```

---

### 10.13 Crear Ruta (Producción)

```bash
curl -X POST https://busify.daelabs.tech/api/rutas/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $PROD_TOKEN" \
  -d '{
    "name": "Ruta Principal Producción",
    "description": "Ruta operativa en producción",
    "origin": "Terminal Central",
    "destination": "Terminal Sur",
    "base_fare": "0.35",
    "is_active": true
  }'
```

---

### 10.14 Crear Parada (Producción)

```bash
curl -X POST https://busify.daelabs.tech/api/paradas/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $PROD_TOKEN" \
  -d '{
    "name": "Parada Principal",
    "description": "Primera parada de la ruta",
    "distance": 0.0,
    "sequence": 1,
    "is_active": true,
    "ruta_id": 1
  }'
```

---

### 10.15 Crear Viaje (Producción)

```bash
curl -X POST https://busify.daelabs.tech/api/viajes/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $PROD_TOKEN" \
  -d '{
    "ruta": 1,
    "bus": 1,
    "chofer": 1,
    "status": "scheduled",
    "departure_time": "2026-06-03T08:00:00Z",
    "estimated_arrival": "2026-06-03T09:00:00Z",
    "passenger_count": 0
  }'
```

---

### 10.16 Agregar Pasajeros (Producción)

```bash
curl -X POST https://busify.daelabs.tech/api/viajes/1/add-passenger/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $PROD_TOKEN" \
  -d '{
    "quantity": 25
  }'
```

---

### 10.17 Iniciar Ruta (Producción)

```bash
curl -X POST https://busify.daelabs.tech/api/viajes/1/start-route/ \
  -H "Authorization: Bearer $PROD_TOKEN"
```

---

### 10.18 Obtener Estadísticas (Producción)

```bash
curl -X GET https://busify.daelabs.tech/api/viajes/stats/ \
  -H "Authorization: Bearer $PROD_TOKEN"
```

---

### 10.19 Refrescar Token en Producción

```bash
curl -X POST https://busify.daelabs.tech/api/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d "{
    \"refresh\": \"$PROD_REFRESH\"
  }"
```

---

### 10.20 Cambiar Contraseña (Producción)

```bash
curl -X POST https://busify.daelabs.tech/api/users/change-password/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $PROD_TOKEN" \
  -d '{
    "current_password": "SecurePass123!",
    "new_password": "NewSecurePass456!",
    "new_password2": "NewSecurePass456!"
  }'
```


---

## NOTAS DE SEGURIDAD PARA PRODUCCIÓN

1. **No compartas tokens**: Los tokens JWT son personales y confidenciales
2. **HTTPS obligatorio**: La URL de producción usa HTTPS para proteger datos
3. **Tiempo de expiración**: Los tokens expiran después de 1 hora
4. **Mantén refresh tokens seguros**: Úsalos para obtener nuevos access tokens
5. **Cierra sesión**: Usa logout para invalidar tokens cuando termines
6. **Credenciales seguras**: No guardes contraseñas en scripts o repositorios

---

**Última actualización:** 3 de junio de 2026
