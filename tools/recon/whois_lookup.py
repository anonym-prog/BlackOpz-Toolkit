#!/usr/bin/env python3
import whois
import sys

if len(sys.argv) < 2:
    print("Usage: python3 whois_lookup.py <domain>")
    sys.exit(1)

domain = sys.argv[1]
try:
    info = whois.whois(domain)
    print(f"Domain: {info.domain_name}")
    print(f"Registrar: {info.registrar}")
    print(f"Creation Date: {info.creation_date}")
    print(f"Expiration Date: {info.expiration_date}")
    print(f"Name Servers: {info.name_servers}")
except Exception as e:
    print(f"Error: {e}")
