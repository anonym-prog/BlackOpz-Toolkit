#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import sys

# Matikan warning SSL
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def print_banner():
    print("\n[+] Web Crawler v1.0 - Discover hidden endpoints\n")

def get_links(url, base_domain):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers, timeout=10, verify=False)
        if r.status_code != 200:
            return []
        
        soup = BeautifulSoup(r.text, 'html.parser')
        links = []
        for tag in soup.find_all(['a', 'link', 'script', 'img', 'form']):
            attr = tag.get('href') or tag.get('src') or tag.get('action')
            if attr:
                full_url = urljoin(url, attr)
                # Hanya ambil link yang masih dalam domain yang sama
                if base_domain in full_url and full_url not in links:
                    links.append(full_url)
        return links
    except:
        return []

def main():
    print_banner()

    if len(sys.argv) < 2:
        print("Usage: python3 web_crawler.py <url>")
        sys.exit(1)

    start_url = sys.argv[1]
    if not start_url.startswith('http'):
        start_url = 'http://' + start_url

    parsed = urlparse(start_url)
    base_domain = parsed.netloc

    visited = set()
    to_visit = [start_url]
    all_links = set()

    print(f"[*] Target: {start_url}")
    print(f"[*] Crawling...\n")

    while to_visit:
        current = to_visit.pop(0)
        if current in visited:
            continue
        visited.add(current)
        
        print(f"[*] Crawling: {current}")
        new_links = get_links(current, base_domain)
        
        for link in new_links:
            if link not in all_links:
                all_links.add(link)
                if link not in visited and link not in to_visit:
                    to_visit.append(link)
        
        if len(visited) > 30:  # Batas kedalaman crawl
            break

    print(f"\n[+] Found {len(all_links)} unique internal links:")
    for link in sorted(all_links):
        print(f"    {link}")

if __name__ == "__main__":
    main()
