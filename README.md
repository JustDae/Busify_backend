# BUSIFY - Sistema de Gestión de Transporte

**BUSIFY** es una plataforma backend para la gestión de transporte, desarrollada con Django REST Framework. Permite administrar cooperativas, choferes, buses, rutas, paradas y viajes con autenticación JWT y permisos granulares.

---

## Tabla de Contenidos

* [Características](#características)
* [Requisitos Previos](#requisitos-previos)
* [Instalación](#instalación)
* [Configuración](#configuración)
* [Ejecutar el Backend](#ejecutar-el-backend)
* [Documentación de Endpoints](#documentación-de-endpoints)
* [Ejemplos de Uso de la API](#ejemplos-de-uso-de-la-api)
* [Colección Postman](#colección-postman)
* [Estructura del Proyecto](#estructura-del-proyecto)
* [Notas de Seguridad](#notas-de-seguridad)

---

## Características

* **Autenticación JWT**: Registro y login con tokens JWT
* **Gestión de Usuarios**: Perfiles de usuario con roles (admin, usuario)
* **Gestión de Cooperativas**: Crear, actualizar y listar cooperativas
* **Gestión de Choferes**: Registro y control de choferes con licencia
* **Gestión de Buses**: Control de flota con capacidades
* **Gestión de Rutas**: Definición de rutas con paradas
* **Gestión de Paradas**: Creación de paradas en rutas
* **Gestión de Viajes**: Programación y control de viajes
* **Filtrado y Búsqueda**: Filtros avanzados y búsqueda por texto
* **Paginación**: Resultados paginados para mejor performance
* **CORS**: Habilitado para frontend en desarrollo
* **PostgreSQL**: Base de datos relacional robusta

---

## Requisitos Previos

* **Python 3.12+**
* **PostgreSQL 13+**
* **pip** (gestor de paquetes de Python)
* **Git** (para clonar el repositorio)
* **Postman o Thunder Client** (para probar la API)

Verifica tu versión de Python:

```bash
python --version
```

Debe ser `>= 3.12`.

---

## Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/JustDae/Busify_backend.git
cd busify
```

### 2. Crear un Entorno Virtual

```bash
# Windows
python -m venv .venv
.\.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

O si usa `pyproject.toml`:

```bash
pip install -e .
```

### 4. Configurar Variables de Entorno

Crear un archivo `.env` en la raíz del proyecto:

```env
SECRET_KEY=your-super-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_ENGINE=django.db.backends.postgresql
DB_NAME=busify_db
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=127.0.0.1
DB_PORT=5432

JWT_ALGORITHM=HS256
```

**Nota:** En producción no deben exponerse credenciales.

### 5. Crear Base de Datos PostgreSQL

```bash
psql -U postgres
```

```sql
CREATE DATABASE busify_db;
CREATE USER busify_user WITH PASSWORD 'your_postgres_password';

ALTER ROLE busify_user SET client_encoding TO 'utf8';
ALTER ROLE busify_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE busify_user SET default_transaction_deferrable TO on;
ALTER ROLE busify_user SET timezone TO 'America/Lima';

GRANT ALL PRIVILEGES ON DATABASE busify_db TO busify_user;
```

Salir:

```sql
\q
```

### 6. Ejecutar Migraciones

```bash
python manage.py migrate
```

### 7. Crear Superusuario

```bash
python manage.py createsuperuser
```

Ejemplo:

```txt
Username: admin
Email: admin@busify.com
Password: ********
```

---

## Configuración

### Configuración de CORS

En `config/settings.py`:

```python
CORS_ALLOWED_ORIGINS = [
    "https://tudominio.com",
    "https://www.tudominio.com",
]
```

### Configuración JWT

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}
```

---

## Ejecutar el Backend

### Desarrollo

```bash
python manage.py runserver
```

La API estará disponible en:

```txt
http://127.0.0.1:8000/
```

### Verificar Estado

```bash
curl http://127.0.0.1:8000/health/
```

Respuesta esperada:

```json
{
  "status": "ok",
  "message": "Backend is running successfully"
}
```

### Producción

```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

---

## Documentación de Endpoints

### Base URL

```txt
http://127.0.0.1:8000/api/
```

### Autenticación

Todos los endpoints, excepto registro y login, requieren JWT:

```txt
Authorization: Bearer <tu_token_de_acceso>
```

### Endpoints de Autenticación

#### Registro de Usuario

```http
POST /auth/register/
```

#### Login

```http
POST /auth/login/
```

#### Refrescar Token

```http
POST /auth/token/refresh/
```

#### Verificar Token

```http
POST /auth/token/verify/
```

#### Logout

```http
POST /auth/logout/
```

---

## Endpoints de Usuarios

* `GET /users/`
* `GET /users/{id}/`
* `PUT /users/{id}/`
* `PATCH /users/{id}/`
* `DELETE /users/{id}/`
* `GET /users/profile/me/`
* `POST /users/{id}/change-password/`

---

## Endpoints de Cooperativas

* `GET /cooperativas/`
* `POST /cooperativas/`
* `PATCH /cooperativas/{id}/`
* `DELETE /cooperativas/{id}/`

---

## Endpoints de Buses

* `GET /buses/`
* `POST /buses/`

Filtros disponibles:

* `plate`
* `status`
* `search`

---

## Endpoints de Choferes

* `GET /choferes/`
* `POST /choferes/`

---

## Endpoints de Rutas

* `GET /rutas/`
* `POST /rutas/`

---

## Endpoints de Paradas

* `GET /paradas/`
* `POST /paradas/`

---

## Endpoints de Viajes

* `GET /viajes/`
* `POST /viajes/`
* `GET /viajes/{id}/`
* `PATCH /viajes/{id}/`
* `POST /viajes/{id}/add-passenger/`
* `POST /viajes/{id}/start-route/`
* `POST /viajes/{id}/update-status/`
* `GET /viajes/stats/`

Estados válidos:

```txt
scheduled
en_route
completed
delayed
cancelled
```

---

## Ejemplos de Uso de la API

### Registro

```bash
curl -X POST http://127.0.0.1:8000/auth/register/ \
-H "Content-Type: application/json" \
-d '{
  "username": "juan_perez",
  "email": "juan@example.com",
  "password": "SecurePass123!",
  "password2": "SecurePass123!"
}'
```

### Obtener Perfil

```bash
curl -X GET http://127.0.0.1:8000/users/profile/me/ \
-H "Authorization: Bearer $ACCESS_TOKEN"
```

### Crear Cooperativa

```bash
curl -X POST http://127.0.0.1:8000/cooperativas/ \
-H "Content-Type: application/json" \
-H "Authorization: Bearer $ACCESS_TOKEN"
```

### Crear Bus

```bash
curl -X POST http://127.0.0.1:8000/buses/
```

### Crear Chofer

```bash
curl -X POST http://127.0.0.1:8000/choferes/
```

### Crear Ruta

```bash
curl -X POST http://127.0.0.1:8000/rutas/
```

### Crear Parada

```bash
curl -X POST http://127.0.0.1:8000/paradas/
```

### Crear Viaje

```bash
curl -X POST http://127.0.0.1:8000/viajes/
```

---

## Colección Postman

Archivo incluido:

```txt
Busify API.postman_collection.json
```

Carpetas incluidas:

### Authentication

* Register User
* Login User
* Refresh Token
* Verify Token
* Logout

### Users Management

* List Users
* Get User by ID
* Update User
* Delete User
* My Profile
* Change Password

### Company Data

* Cooperativas
* Buses
* Choferes

### Routes Management

* Rutas
* Paradas

### Trips Management

* Viajes
* Estadísticas
* Estado de Viajes
* Inicio de Ruta

Variables recomendadas:

```json
{
  "base_url": "http://127.0.0.1:8000",
  "access_token": "",
  "refresh_token": ""
}
```

---

## Estructura del Proyecto

```txt
busify/
├── config/
├── transit/
│   ├── models/
│   ├── serializers/
│   ├── views/
│   ├── migrations/
│   ├── tests/
│   ├── filters.py
│   ├── pagination.py
│   ├── permissions.py
│   └── urls.py
├── .env
├── .env.example
├── manage.py
├── pyproject.toml
├── requirements.txt
├── README.md
└── Busify API.postman_collection.json
```


### Configuración Recomendada para Producción

```python
DEBUG = False

ALLOWED_HOSTS = [
    'tudominio.com',
    'www.tudominio.com'
]

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

---

## Testing

Ejecutar todos los tests:

```bash
python manage.py test
```

Tests específicos:

```bash
python manage.py test transit.tests.test_auth
```



## Créditos

Desarrollado con:

* Django 6.0+
* Django REST Framework
* PostgreSQL
* JWT Authentication

### Recursos y Agradecimientos
* Basado en las guías y tutoriales de desarrollo de [Ing. Francisco Higuera](https://franciscohiguera.site/about).
---

**Última actualización:** Junio 2026
**Versión:** 1.0.0
