# Scripts de Prueba - API JSON Storage

Esta carpeta contiene scripts de prueba para verificar el funcionamiento de la API JSON Storage y el balanceo de carga.

## Scripts disponibles

### 1. test_balanceo.py
Verifica que el load balancer esté distribuyendo las peticiones entre los servidores.

**Uso:**
```bash
python3 test_balanceo.py
```

**Salida esperada:**
```
Probando balanceo de carga...

Request 1: servidor 699b871d - status: healthy
Request 2: servidor acaac95b - status: healthy
Request 3: servidor 699b871d - status: healthy
...

Servidores encontrados: 2
- 699b871d: 5 requests
- acaac95b: 5 requests
```

### 2. test_api.py
Prueba todas las operaciones CRUD de la API.

**Configuración antes de usar:**
1. Abre el archivo `test_api.py`
2. Modifica estas líneas según tu configuración:
```python
url_base = "http://98.84.55.132"  # Cambia por tu IP o dominio
token = "sk-proj-x7B9mN3pQ5vL2kR8fT6yH4jW1sZ0aE"  # Cambia por tu token
```

**Uso:**
```bash
python3 test_api.py
```

## Ejemplos con CURL

### Endpoints públicos (sin autenticación)

**Health Check:**
```bash
curl http://98.84.55.132/health
```

**Leer un JSON:**
```bash
curl http://98.84.55.132/json/test123
```

### Endpoints protegidos (requieren token)

**Crear un JSON:**
```bash
curl -X POST http://98.84.55.132/json \
  -H "Authorization: Bearer sk-proj-x7B9mN3pQ5vL2kR8fT6yH4jW1sZ0aE" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "test123",
    "data": {
      "nombre": "Mi JSON",
      "valor": 42
    }
  }'
```

**Actualizar un JSON:**
```bash
curl -X PUT http://98.84.55.132/json/test123 \
  -H "Authorization: Bearer sk-proj-x7B9mN3pQ5vL2kR8fT6yH4jW1sZ0aE" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "JSON Actualizado",
    "valor": 100,
    "nuevo_campo": true
  }'
```

**Eliminar un JSON:**
```bash
curl -X DELETE http://98.84.55.132/json/test123 \
  -H "Authorization: Bearer sk-proj-x7B9mN3pQ5vL2kR8fT6yH4jW1sZ0aE"
```

## Requisitos

```bash
pip install requests
```

## Notas

- Los IDs de los JSON son estáticos, debes definirlos al crear
- El token de autenticación se puede cambiar con la variable de entorno `API_TOKEN`
- Los archivos JSON se guardan en el EFS compartido entre servidores