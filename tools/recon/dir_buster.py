#!/usr/bin/env python3
import requests
import sys
import threading
import queue
from urllib.parse import urljoin

# Matikan warning SSL
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ---------------- KONFIGURASI ----------------
DEFAULT_WORDLIST = [
    "admin", "backup", "config", "login", "uploads", "css", "js", "images", "api", "v1",
    ".env", ".git", ".gitignore", ".htaccess", ".htpasswd", "wp-admin", "wp-content",
    "wp-includes", "wp-config.php", "phpinfo.php", "info.php", "test.php", "shell.php",
    "database", "db", "sql", "dump", "export", "backup.zip", "backup.tar.gz", "robots.txt",
    "sitemap.xml", "crossdomain.xml", "clientaccesspolicy.xml", "README.md", "LICENSE"
]

# ---------------- FUNGSI UTIL ----------------
def print_banner():
    banner = """
    ██████  ██ ██████   ██████  ██    ██ ██ ███████ ████████ ███████ ██████  
    ██   ██ ██ ██   ██ ██    ██ ██    ██ ██ ██         ██    ██      ██   ██ 
    ██████  ██ ██████  ██    ██ ██    ██ ██ ███████    ██    █████   ██████  
    ██   ██ ██ ██   ██ ██    ██ ██    ██ ██      ██    ██    ██      ██   ██ 
    ██   ██ ██ ██████   ██████   ██████  ██ ███████    ██    ███████ ██   ██ 
    """
    print(f"\033[92m{banner}\033[0m")
    print("[+] Directory Buster v1.0 - Multithreaded\n")

def worker(base_url, q, results, lock, found_files):
    while True:
        try:
            path = q.get(timeout=1)
        except queue.Empty:
            break
        
        url = urljoin(base_url, path)
        try:
            r = requests.get(url, timeout=3, verify=False)
            if r.status_code < 400:
                with lock:
                    results.append(f"[{r.status_code}] {url}")
                    found_files.append(url)
                    print(f"[{r.status_code}] {url}")
        except:
            pass
        q.task_done()

# ---------------- MAIN ----------------
def main():
    print_banner()

    if len(sys.argv) < 2:
        print("Usage: python3 dir_buster.py <base_url> [wordlist_file]")
        print("Contoh: python3 dir_buster.py https://example.com common.txt")
        sys.exit(1)

    base_url = sys.argv[1]
    if not base_url.endswith('/'):
        base_url += '/'

    # Ambil wordlist
    wordlist = DEFAULT_WORDLIST
    if len(sys.argv) == 3:
        try:
            with open(sys.argv[2], "r") as f:
                wordlist = [line.strip() for line in f if line.strip()]
            print(f"[*] Loaded {len(wordlist)} paths from {sys.argv[2]}")
        except FileNotFoundError:
            print(f"[-] Wordlist {sys.argv[2]} tidak ditemukan. Pakai default.")
    else:
        print(f"[*] Menggunakan wordlist default ({len(wordlist)} path).")

    # Konfigurasi threading
    threads = 30
    q = queue.Queue()
    results = []
    found_files = []
    lock = threading.Lock()

    print(f"[*] Target: {base_url}")
    print(f"[*] Threads: {threads}\n")
    print("[*] Memulai scanning... (tekan Ctrl+C untuk berhenti)\n")

    # Masukkan semua path ke queue
    for path in wordlist:
        q.put(path)

    # Jalankan threads
    thread_list = []
    for _ in range(threads):
        t = threading.Thread(target=worker, args=(base_url, q, results, lock, found_files))
        t.daemon = True
        t.start()
        thread_list.append(t)

    # Tunggu selesai
    q.join()

    print(f"\n[+] Scan selesai. Total ditemukan: {len(results)}")
    if found_files:
        print("[+] File/directory yang ditemukan:")
        for f in found_files:
            print(f"    {f}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Scanning dihentikan.")
        sys.exit(0)
