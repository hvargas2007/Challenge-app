# JSON Storage API

API REST para almacenamiento de documentos JSON con autenticación y balanceo de carga.

## 🚀 Características

- **API REST completa**: Operaciones CRUD para documentos JSON
- **Autenticación**: Token Bearer para endpoints protegidos
- **Alta disponibilidad**: Diseñada para funcionar con múltiples instancias
- **Almacenamiento compartido**: Compatible con EFS/NFS
- **Health checks**: Para monitoreo y balanceo de carga
- **Identificación de servidor**: Para verificar distribución de carga

## 📁 Estructura del proyecto

```
json-storage-api/
├── docker/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── main.py
│   ├── requirements.txt
│   └── README.md
├── pruebas/
│   ├── test_balanceo.py
│   ├── test_api.py
│   └── README.md
└── README.md
```

## 🛠️ Instalación rápida

### Prerrequisitos
- Docker y Docker Compose
- Python 3.8+ (para scripts de prueba)
- Acceso a almacenamiento compartido (EFS/NFS)

### Ejecutar con Docker Compose

```bash
cd docker
docker-compose up -d
```

### Ejecutar con Docker

```bash
cd docker
docker build -t json-api .
docker run -d -p 80:80 -e API_TOKEN=mi-token-secreto json-api
```

## 🔧 Configuración

### Variables de entorno

| Variable | Descripción | Por defecto |
|----------|-------------|-------------|
| `API_TOKEN` | Token de autenticación | `sk-proj-x7B9mN3pQ5vL2kR8fT6yH4jW1sZ0aE` |
| `SERVER_ID` | ID del servidor | Auto-generado |
| `STORAGE_PATH` | Ruta de almacenamiento | `/mnt/efs/json-storage` |

## 📡 API Endpoints

### Endpoints públicos

```bash
# Health check
curl http://localhost/health

# Leer JSON
curl http://localhost/json/mi-id
```

### Endpoints protegidos

```bash
# Crear JSON
curl -X POST http://localhost/json \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"id": "test", "data": {"key": "value"}}'

# Actualizar JSON
curl -X PUT http://localhost/json/test \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"key": "new value"}'

# Eliminar JSON
curl -X DELETE http://localhost/json/test \
  -H "Authorization: Bearer ${API_TOKEN}"
```

## 🧪 Pruebas

### Instalar dependencias

```bash
pip install requests
```

### Probar balanceo de carga

```bash
cd pruebas
python3 test_balanceo.py
```

### Probar operaciones CRUD

```bash
cd pruebas
# Editar test_api.py para configurar URL y token
python3 test_api.py
```

## 🏗️ Arquitectura

La aplicación está diseñada para:

1. **Múltiples instancias**: Cada servidor tiene un ID único
2. **Almacenamiento compartido**: Los JSONs se guardan en EFS/NFS
3. **Concurrencia**: File locking previene conflictos
4. **Stateless**: No hay sesiones, solo tokens

## 📝 Ejemplo de uso completo

```python
import requests

# Configuración
base_url = "http://mi-load-balancer.com"
token = "mi-token-secreto"
headers = {"Authorization": f"Bearer {token}"}

# Crear
data = {"id": "usuario123", "data": {"nombre": "Juan", "edad": 30}}
r = requests.post(f"{base_url}/json", json=data, headers=headers)

# Leer
r = requests.get(f"{base_url}/json/usuario123")
print(r.json())

# Actualizar
new_data = {"nombre": "Juan", "edad": 31, "ciudad": "Madrid"}
r = requests.put(f"{base_url}/json/usuario123", json=new_data, headers=headers)

# Eliminar
r = requests.delete(f"{base_url}/json/usuario123", headers=headers)
```

## 🔒 Seguridad

- **Cambiar el token por defecto** antes de usar en producción
- Usar **HTTPS** en producción
- Implementar **rate limiting** si es necesario
- Considerar **CORS** según tus necesidades

## 🤝 Contribuir

1. Fork el proyecto
2. Crea tu rama (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es parte de una prueba técnica.