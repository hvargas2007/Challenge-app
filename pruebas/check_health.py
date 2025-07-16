#!/usr/bin/env python3

import requests
import json
import time
import sys

# Colors
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'

url = "http://3.238.65.62/health"
wait = 2

print(f"{BLUE}Checking {url} every {wait} seconds...{RESET}")
print("Press Ctrl+C to stop\n")

while True:
    try:
        r = requests.get(url)
        data = r.json()
        
        print(f"{YELLOW}[{time.strftime('%H:%M:%S')}]{RESET}")
        
        # Color the JSON output
        output = json.dumps(data, indent=2)
        # Keys
        output = output.replace('"status":', f'"{GREEN}status{RESET}":')
        output = output.replace('"version":', f'"{RED}version{RESET}":')
        output = output.replace('"server_id":', f'"{BLUE}server_id{RESET}":')
        output = output.replace('"client_ip":', f'"{YELLOW}client_ip{RESET}":')
        output = output.replace('"requested_host":', f'"{YELLOW}requested_host{RESET}":')
        # Values
        output = output.replace('"healthy"', f'"{GREEN}healthy{RESET}"')
        output = output.replace('"docker"', f'"{RED}docker{RESET}"')
        # Server IDs in blue
        for line in output.split('\n'):
            if 'server_id' in line and '"' in line:
                parts = line.split('"')
                if len(parts) >= 4:
                    server_value = parts[3]
                    output = output.replace(f'"{server_value}"', f'"{BLUE}{server_value}{RESET}"')
        print(output)
        
        print("-" * 40)
        
        time.sleep(wait)
        
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Stopped{RESET}")
        break
    except Exception as e:
        print(f"{RED}Error: {e}{RESET}")
        time.sleep(wait)