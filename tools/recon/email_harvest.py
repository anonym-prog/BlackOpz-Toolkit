#!/usr/bin/env python3
import requests
import re
import sys
from urllib.parse import urljoin

# Matikan warning SSL
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ---------------- KONFIGURASI ----------------
EMAIL_REGEX = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
# ---------------------------------------------

def print_banner():
    banner = """
    ███████ ███    ███  █████  ██ ██      ██       ██████  ██████   ██████  ███    ██ ████████ 
    ██      ████  ████ ██   ██ ██ ██      ██      ██    ██ ██   ██ ██    ██ ████   ██    ██    
    █████   ██ ████ ██ ███████ ██ ██      ██      ██    ██ ██████  ██    ██ ██ ██  ██    ██    
    ██      ██  ██  ██ ██   ██ ██ ██      ██      ██    ██ ██   ██ ██    ██ ██  ██ ██    ██    
    ███████ ██      ██ ██   ██ ██ ███████ ███████  ██████  ██   ██  ██████  ██   ████    ██    
    """
    print(f"\033[92m{banner}\033[0m")
    print("[+] Email Harvester v1.0 - Extract emails from target pages\n")

def extract_emails(text):
    """Ekstrak semua email dari teks menggunakan regex."""
    return re.findall(EMAIL_REGEX, text)

def get_page(url):
    """Ambil konten halaman."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers, timeout=10, verify=False)
        if r.status_code == 200:
            return r.text
        return None
    except:
        return None

def crawl_links(content, base_url):
    """Ambil semua link href dari halaman (untuk crawling lanjutan)."""
    links = re.findall(r'href=[\'"]?([^\'" >]+)', content)
    full_urls = []
    for link in links:
        if link.startswith('http'):
            full_urls.append(link)
        elif link.startswith('/'):
            full_urls.append(urljoin(base_url, link))
        elif link.startswith('mailto:'):
            continue  # skip email link
        else:
            full_urls.append(urljoin(base_url, link))
    return full_urls

# ---------------- MAIN ----------------
def main():
    print_banner()

    if len(sys.argv) < 2:
        print("Usage: python3 email_harvester.py <url>")
        sys.exit(1)

    start_url = sys.argv[1]
    print(f"[*] Target: {start_url}\n")

    # Antrean halaman untuk dikunjungi
    visited = set()
    to_visit = [start_url]
    emails = set()

    while to_visit:
        current = to_visit.pop(0)
        if current in visited:
            continue
        visited.add(current)

        print(f"[*] Crawling: {current}")
        content = get_page(current)
        if not content:
            continue

        # Ekstrak email dari halaman ini
        new_emails = extract_emails(content)
        for email in new_emails:
            if email not in emails:
                emails.add(email)
                print(f"[+] Found email: {email}")

        # Temukan link baru untuk di-crawl
        if len(visited) < 50:  # Batasi agar tidak terlalu dalam
            links = crawl_links(content, current)
            for link in links:
                if link not in visited and link not in to_visit:
                    if link.startswith('http'):
                        to_visit.append(link)

    print(f"\n[+] Selesai. Total email ditemukan: {len(emails)}")
    if emails:
        print("[+] Daftar email:")
        for email in sorted(emails):
            print(f"    {email}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Scanning dihentikan.")
        sys.exit(0)
