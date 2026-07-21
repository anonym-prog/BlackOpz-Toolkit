#!/usr/bin/env python3
import requests
import re
import sys
import json
import time
from urllib.parse import urlparse

# Matikan warning SSL
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ---------------- KONFIGURASI FINGERPRINT ----------------
# Pola deteksi untuk berbagai CMS / Framework / Server
SIGNATURES = {
    "WordPress": {
        "markers": [
            r'(?i)<meta name="generator" content="WordPress',
            r'(?i)wp-content',
            r'(?i)wp-includes',
            r'(?i)wp-json',
            r'(?i)/wp-login.php',
            r'(?i)wordpress'
        ],
        "version_pattern": r'(?i)<meta name="generator" content="WordPress\s*([0-9\.]+)'
    },
    "Joomla": {
        "markers": [
            r'(?i)<meta name="generator" content="Joomla',
            r'(?i)joomla',
            r'(?i)/templates/',
            r'(?i)/administrator/'
        ],
        "version_pattern": r'(?i)<meta name="generator" content="Joomla\s*([0-9\.]+)'
    },
    "Drupal": {
        "markers": [
            r'(?i)<meta name="generator" content="Drupal',
            r'(?i)drupal',
            r'(?i)/sites/default/',
            r'(?i)libraries/drupal'
        ],
        "version_pattern": r'(?i)<meta name="generator" content="Drupal\s*([0-9\.]+)'
    },
    "Laravel": {
        "markers": [
            r'(?i)laravel',
            r'(?i)csrf-token',
            r'(?i)XSRF-TOKEN',
            r'(?i)laravel_session',
            r'(?i)Illuminate'
        ],
        "version_pattern": r'(?i)Laravel\s*v([0-9\.]+)'
    },
    "CodeIgniter": {
        "markers": [
            r'(?i)codeigniter',
            r'(?i)ci_session',
            r'(?i)ci_csrf_token'
        ],
        "version_pattern": r'(?i)CodeIgniter\s*([0-9\.]+)'
    },
    "Apache": {
        "markers": [
            r'(?i)apache',
            r'(?i)Apache/'
        ],
        "version_pattern": r'(?i)Apache/([0-9\.]+)'
    },
    "Nginx": {
        "markers": [
            r'(?i)nginx',
            r'(?i)nginx/'
        ],
        "version_pattern": r'(?i)nginx/([0-9\.]+)'
    },
    "IIS": {
        "markers": [
            r'(?i)microsoft-iis',
            r'(?i)asp.net',
            r'(?i)iis/'
        ],
        "version_pattern": r'(?i)IIS/([0-9\.]+)'
    },
    "PHP": {
        "markers": [
            r'(?i)php',
            r'(?i)x-powered-by',
            r'(?i)PHPSESSID'
        ],
        "version_pattern": r'(?i)PHP/([0-9\.]+)'
    },
    "Node.js": {
        "markers": [
            r'(?i)node',
            r'(?i)express',
            r'(?i)connect',
            r'(?i)socket.io'
        ],
        "version_pattern": r'(?i)Node\.js\s*([0-9\.]+)'
    },
    "React": {
        "markers": [
            r'(?i)react',
            r'(?i)react-dom',
            r'(?i)__REACT_DEVTOOLS_GLOBAL_HOOK__',
            r'(?i)_reactRoot'
        ],
        "version_pattern": r'(?i)react\s*([0-9\.]+)'
    },
    "Vue.js": {
        "markers": [
            r'(?i)vue',
            r'(?i)Vue\.js',
            r'(?i)_vue_'
        ],
        "version_pattern": r'(?i)Vue\.js\s*([0-9\.]+)'
    },
    "jQuery": {
        "markers": [
            r'(?i)jquery',
            r'(?i)jQuery'
        ],
        "version_pattern": r'(?i)jQuery\s*([0-9\.]+)'
    },
    "Bootstrap": {
        "markers": [
            r'(?i)bootstrap',
            r'(?i)Bootstrap'
        ],
        "version_pattern": r'(?i)Bootstrap\s*([0-9\.]+)'
    }
}

# ---------------- FUNGSI UTIL ----------------
def print_banner():
    banner = """
    ████████ ███████ ██████   ██████ ██   ██ ██   ██ ██ ██████  ██████  ██████  ██ ███    ██ ████████ ███████ ██████  
       ██    ██      ██   ██ ██      ██   ██ ██   ██ ██ ██   ██ ██   ██ ██   ██ ██ ████   ██    ██    ██      ██   ██ 
       ██    █████   ██████  ██      ███████ ███████ ██ ██████  ██████  ██████  ██ ██ ██  ██    ██    █████   ██████  
       ██    ██      ██   ██ ██      ██   ██ ██   ██ ██ ██   ██ ██   ██ ██   ██ ██ ██  ██ ██    ██    ██      ██   ██ 
       ██    ███████ ██   ██  ██████ ██   ██ ██   ██ ██ ██   ██ ██████  ██████  ██ ██   ████    ██    ███████ ██   ██ 
    """
    print(f"\033[92m{banner}\033[0m")
    print("[+] Technology Fingerprinter v1.0 - CMS, Server, Framework Detection\n")

def get_headers_and_content(url):
    """Mengambil header dan konten dari URL target."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        return response.headers, response.text
    except Exception as e:
        print(f"[-] Error fetching URL: {e}")
        return {}, ""

def detect_technologies(url, headers, content):
    """Mendeteksi teknologi berdasarkan signature."""
    results = {}
    combined = str(headers) + " " + content

    for tech, sig in SIGNATURES.items():
        # Cek marker
        matched = False
        for marker in sig["markers"]:
            if re.search(marker, combined):
                matched = True
                break
        
        if matched:
            version = "Unknown"
            if "version_pattern" in sig:
                match = re.search(sig["version_pattern"], combined)
                if match:
                    version = match.group(1)
            results[tech] = version
    
    return results

def print_results(url, results):
    """Menampilkan hasil fingerprinting dengan rapi."""
    print(f"\n[+] Target: {url}")
    print("[+] Detected Technologies:\n")
    if not results:
        print("    No specific technologies detected.\n")
        return
    
    # Tampilkan dalam format tabel sederhana
    print(f"{'Technology':<20} {'Version':<15}")
    print("-" * 40)
    for tech, version in results.items():
        print(f"{tech:<20} {version:<15}")
    print("\n[*] Use this information to search for known exploits.")
    print("[*] For example: searchsploit <tech_name> <version>\n")

def save_results_to_file(url, results, output_file):
    """Menyimpan hasil ke file."""
    with open(output_file, "w") as f:
        f.write(f"Target: {url}\n")
        f.write("Technologies Detected:\n")
        for tech, version in results.items():
            f.write(f"{tech}: {version}\n")
    print(f"[+] Results saved to: {output_file}")

# ---------------- MAIN ----------------
def main():
    print_banner()

    if len(sys.argv) < 2:
        print("Usage: python3 tech_fingerprinter.py <url> [output_file]")
        print("Contoh: python3 tech_fingerprinter.py https://example.com output.json")
        sys.exit(1)

    url = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "fingerprint_results.txt"

    # Pastikan URL punya skema
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    print(f"[*] Scanning: {url}")
    headers, content = get_headers_and_content(url)
    
    if not headers and not content:
        print("[-] Failed to get response from target.")
        sys.exit(1)

    results = detect_technologies(url, headers, content)
    print_results(url, results)
    save_results_to_file(url, results, output_file)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Scanning interrupted by user.")
        sys.exit(0)
