#!/usr/bin/env python3
import sys
import dns.resolver
from dns.exception import DNSException

# ---------------- KONFIGURASI ----------------
RECORD_TYPES = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME', 'SOA']
# ---------------------------------------------

def print_banner():
    banner = """
    ██████  ███    ██ ███████ ███████ ███    ██ ██    ██ ███    ██ 
    ██   ██ ████   ██ ██      ██      ████   ██ ██    ██ ████   ██ 
    ██   ██ ██ ██  ██ █████   █████   ██ ██  ██ ██    ██ ██ ██  ██ 
    ██   ██ ██  ██ ██ ██      ██      ██  ██ ██ ██    ██ ██  ██ ██ 
    ██████  ██   ████ ███████ ███████ ██   ████  ██████  ██   ████ 
    """
    print(f"\033[92m{banner}\033[0m")
    print("[+] DNS Enumeration Tool v1.0 - Full Record Fetch\n")

def resolve_record(domain, record_type):
    """Meresolve satu tipe record dan return list hasil."""
    try:
        answers = dns.resolver.resolve(domain, record_type)
        return [str(rdata) for rdata in answers]
    except dns.resolver.NXDOMAIN:
        return None  # Domain tidak ada
    except dns.resolver.NoAnswer:
        return []    # Tipe record ini tidak ada
    except DNSException as e:
        return None  # Error lain

def main():
    print_banner()

    if len(sys.argv) < 2:
        print("Usage: python3 dns_enum.py <domain>")
        print("Contoh: python3 dns_enum.py example.com")
        sys.exit(1)

    domain = sys.argv[1]
    print(f"[*] Target Domain: {domain}\n")

    found_any = False

    for rec in RECORD_TYPES:
        print(f"[*] Checking {rec} records...")
        results = resolve_record(domain, rec)

        if results is None:
            print(f"[-] Domain {domain} tidak valid atau tidak ditemukan.")
            break

        if len(results) == 0:
            print(f"[-] Tidak ada {rec} record.")
        else:
            print(f"[+] Found {len(results)} {rec} record(s):")
            for i, val in enumerate(results, 1):
                print(f"    {i}. {val}")
        print("")  # Baris kosong antar tipe record

        found_any = True

    if not found_any:
        print("[-] Tidak ada record yang ditemukan. Cek nama domain.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Scanning dihentikan.")
        sys.exit(0)
