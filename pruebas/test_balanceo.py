import requests
import time

# Colores ANSI
AZUL = '\033[94m'
VERDE = '\033[92m'
RESET = '\033[0m'

url = "http://98.84.55.132/health"

print("\nProbando balanceo de carga...\n")

servidores = {}

for i in range(10):
    try:
        r = requests.get(url)
        data = r.json()
        server_id = data['server_id']
        status = data['status']
        
        if server_id not in servidores:
            servidores[server_id] = 0
        servidores[server_id] += 1
        
        print(f"Request {i+1}: servidor {AZUL}{server_id}{RESET} - status: {VERDE}{status}{RESET}")
        time.sleep(0.5)
        
    except Exception as e:
        print(f"Error: {e}")

print(f"\nServidores encontrados: {len(servidores)}")
for server, count in servidores.items():
    print(f"- {AZUL}{server}{RESET}: {count} requests")