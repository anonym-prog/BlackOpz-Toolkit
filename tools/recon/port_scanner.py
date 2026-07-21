#!/usr/bin/env python3
import socket
import sys

def scan_port(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    try:
        s.connect((ip, port))
        return True
    except:
        return False
    finally:
        s.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 port_scanner.py <target_ip>")
        sys.exit(1)
    
    target = sys.argv[1]
    print(f"[*] Scanning target: {target}")
    
    for port in range(1, 1024):
        if scan_port(target, port):
            print(f"[+] Port {port} is OPEN")
