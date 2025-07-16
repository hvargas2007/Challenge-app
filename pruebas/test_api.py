import requests
import time

# Colores
VERDE = '\033[92m'
ROJO = '\033[91m'
AZUL = '\033[94m'
AMARILLO = '\033[93m'
RESET = '\033[0m'

url_base = "http://98.84.55.132"
token = "sk-proj-x7B9mN3pQ5vL2kR8fT6yH4jW1sZ0aE"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

print("\nProbando API JSON Storage...\n")

# Test 1: Crear
print(f"{AZUL}1. CREAR - POST /json{RESET}")
try:
    r = requests.post(f"{url_base}/json", 
                     headers=headers,
                     json={"id": "prueba123", "data": {"nombre": "Test", "valor": 42}})
    print(f"{VERDE if r.status_code == 200 else ROJO}   Status: {r.status_code} - {r.json()}{RESET}")
except Exception as e:
    print(f"{ROJO}   Error: {e}{RESET}")

time.sleep(1)

# Test 2: Leer
print(f"\n{AZUL}2. LEER - GET /json/prueba123{RESET}")
try:
    r = requests.get(f"{url_base}/json/prueba123")
    print(f"{VERDE if r.status_code == 200 else ROJO}   Status: {r.status_code}{RESET}")
    if r.status_code == 200:
        print(f"   Data: {r.json()}")
except Exception as e:
    print(f"{ROJO}   Error: {e}{RESET}")

time.sleep(1)

# Test 3: Modificar
print(f"\n{AZUL}3. MODIFICAR - PUT /json/prueba123{RESET}")
try:
    r = requests.put(f"{url_base}/json/prueba123", 
                    headers=headers,
                    json={"nombre": "Test Actualizado", "valor": 100, "nuevo": True})
    print(f"{VERDE if r.status_code == 200 else ROJO}   Status: {r.status_code} - {r.json()}{RESET}")
except Exception as e:
    print(f"{ROJO}   Error: {e}{RESET}")

time.sleep(1)

# Test 4: Eliminar
print(f"\n{AZUL}4. ELIMINAR - DELETE /json/prueba123{RESET}")
try:
    r = requests.delete(f"{url_base}/json/prueba123", headers=headers)
    print(f"{VERDE if r.status_code == 200 else ROJO}   Status: {r.status_code} - {r.json()}{RESET}")
except Exception as e:
    print(f"{ROJO}   Error: {e}{RESET}")

print("\n✅ Pruebas completadas\n")