# API JSON Storage - Docker

API REST simple para almacenar y gestionar documentos JSON con autenticación por token.

## Características

- ✅ CRUD completo (Create, Read, Update, Delete)
- 🔐 Autenticación por token Bearer
- 📁 Almacenamiento en sistema de archivos (EFS compatible)
- 🔄 File locking para concurrencia
- 🏥 Health check endpoint
- 🆔 Identificación única de servidor

## Requisitos

- Python 3.11+
- Docker
- Docker Compose

## Instalación

### Con Docker Compose

```bash
docker-compose up -d
```

### Con Docker

```bash
# Construir imagen
docker build -t json-api .

# Ejecutar contenedor
docker run -d \
  -p 80:80 \
  -v /mnt/efs/json-storage:/mnt/efs/json-storage \
  -e API_TOKEN=tu-token-secreto \
  -e SERVER_ID=servidor1 \
  json-api
```

## Variables de entorno

| Variable | Descripción | Valor por defecto |
|----------|-------------|-------------------|
| `API_TOKEN` | Token de autenticación | `sk-proj-x7B9mN3pQ5vL2kR8fT6yH4jW1sZ0aE` |
| `SERVER_ID` | ID único del servidor | Primeros 8 caracteres del hostname |
| `STORAGE_PATH` | Ruta de almacenamiento | `/mnt/efs/json-storage` |

## Endpoints

### Públicos (sin autenticación)

- `GET /` - Información de la API
- `GET /health` - Estado del servidor
- `GET /json/{id}` - Leer un JSON

### Protegidos (requieren token)

- `POST /json` - Crear un nuevo JSON
- `PUT /json/{id}` - Actualizar un JSON existente
- `DELETE /json/{id}` - Eliminar un JSON

## Estructura del proyecto

```
docker/
├── Dockerfile          # Imagen Docker
├── docker-compose.yml  # Configuración Docker Compose
├── main.py            # Aplicación FastAPI
├── requirements.txt   # Dependencias Python
└── README.md         # Este archivo
```

## Desarrollo local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
uvicorn main:app --reload

# O con gunicorn (como en producción)
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:80
```

## Notas de seguridad

- Cambiar el token por defecto en producción
- Usar HTTPS en producción
- Considerar rate limiting para prevenir abuso