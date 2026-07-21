#!/usr/bin/env python3
import sys
import os
import socket
import threading
import queue
import time
import requests
import urllib3

# Matikan warning SSL biar layar nggak penuh
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ---------------- KONFIGURASI ----------------
DEFAULT_WORDLIST = [
    "www", "mail", "ftp", "admin", "api", "dev", "staging", "test", "vpn", "portal",
    "blog", "shop", "support", "help", "cdn", "static", "assets", "files", "uploads",
    "backup", "config", "login", "auth", "dashboard", "panel", "cp", "webmail",
    "ns1", "ns2", "mx", "remote", "ssh", "smtp", "pop3", "imap", "calendar", "docs",
    "wiki", "forum", "community", "m", "mobile", "app", "apps", "api-1", "v1", "v2"
]

# ---------------- FUNGSI UTIL ----------------
def print_banner():
    banner = """
    ███████  ██   ██ ██    ██ ██████  ██████   ██████  ███    ███  █████  ██ ███    ██ 
    ██      ██   ██ ██    ██ ██   ██ ██   ██ ██    ██ ████  ████ ██   ██ ██ ████   ██ 
    ███████ ███████ ██    ██ ██████  ██   ██ ██    ██ ██ ████ ██ ███████ ██ ██ ██  ██ 
         ██ ██   ██ ██    ██ ██   ██ ██   ██ ██    ██ ██  ██  ██ ██   ██ ██ ██  ██ ██ 
    ███████ ██   ██  ██████  ██   ██ ██████   ██████  ██      ██ ██   ██ ██ ██   ████ 
    """
    print(f"\033[92m{banner}\033[0m")
    print("[+] Mass Subdomain Scanner v2.0 - Multithreaded\n")

def resolve_domain(domain):
    """Meresolve domain ke IP. Jika gagal, return None."""
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None

def check_port(ip, port):
    """Cek apakah port terbuka di IP target."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.5)
        result = s.connect_ex((ip, port))
        s.close()
        return result == 0
    except:
        return False

# ---------------- WORKER THREAD ----------------
def worker(q, base_domain, results, lock, output_file):
    while True:
        try:
            sub = q.get(timeout=1)
        except queue.Empty:
            break

        full_domain = f"{sub}.{base_domain}"
        ip = resolve_domain(full_domain)

        if ip:
            # Jika domain hidup, cek port 80 dan 443
            port80 = check_port(ip, 80)
            port443 = check_port(ip, 443)

            log_line = f"[+] {full_domain} -> {ip} (80: {port80}, 443: {port443})"
            
            with lock:
                results.append(log_line)
                print(log_line)
                # Tulis ke file log real-time
                with open(output_file, "a") as f:
                    f.write(log_line + "\n")
        
        q.task_done()

# ---------------- MAIN ----------------
def main():
    print_banner()

    if len(sys.argv) < 2:
        print("Usage: python3 mass_subdomain_scanner.py <domain> [wordlist_file]")
        print("Contoh: python3 mass_subdomain_scanner.py google.com subdomains.txt")
        sys.exit(1)

    base_domain = sys.argv[1]
    output_file = f"{base_domain}_subdomains.txt"
    
    # Hapus file log lama kalau ada
    if os.path.exists(output_file):
        os.remove(output_file)

    # Ambil wordlist (dari file atau default)
    wordlist = DEFAULT_WORDLIST
    if len(sys.argv) == 3:
        try:
            with open(sys.argv[2], "r") as f:
                wordlist = [line.strip() for line in f if line.strip()]
            print(f"[*] Loaded {len(wordlist)} subdomains from {sys.argv[2]}")
        except FileNotFoundError:
            print(f"[-] Wordlist {sys.argv[2]} tidak ditemukan. Pakai default.")
    else:
        print(f"[*] Menggunakan wordlist default ({len(wordlist)} subdomain).")

    # Konfigurasi threading
    num_threads = min(50, os.cpu_count() * 5)  # Maks 50 thread agar HP ga panas
    q = queue.Queue()
    results = []
    lock = threading.Lock()

    print(f"[*] Target: {base_domain}")
    print(f"[*] Threads: {num_threads}")
    print(f"[*] Output log: {output_file}\n")
    print("[*] Memulai scanning... (tekan Ctrl+C untuk berhenti)\n")

    # Masukkan semua subdomain ke queue
    for sub in wordlist:
        q.put(sub)

    # Jalankan threads
    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=worker, args=(q, base_domain, results, lock, output_file))
        t.daemon = True
        t.start()
        threads.append(t)

    # Tunggu semua selesai
    q.join()

    # Tampilkan summary
    total_found = len(results)
    print(f"\n[+] Scan selesai. Total subdomain ditemukan: {total_found}")
    print(f"[+] Hasil disimpan di: {output_file}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Scanning dihentikan paksa oleh user.")
        sys.exit(0)
