#!/usr/bin/env python3
import requests
import sys
import json

def print_banner():
    print("\n[+] IP Geolocator v1.0 - Track IP Location\n")

def geolocate(ip):
    url = f"http://ip-api.com/json/{ip}"
    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        if data['status'] == 'success':
            return data
        else:
            return None
    except:
        return None

def main():
    print_banner()

    if len(sys.argv) < 2:
        print("Usage: python3 ip_geolocator.py <ip_address>")
        sys.exit(1)

    ip = sys.argv[1]
    print(f"[*] Looking up: {ip}\n")

    data = geolocate(ip)
    if data:
        print(f"IP: {data['query']}")
        print(f"Country: {data['country']} ({data['countryCode']})")
        print(f"Region: {data['regionName']}")
        print(f"City: {data['city']}")
        print(f"ISP: {data['isp']}")
        print(f"Coordinates: {data['lat']}, {data['lon']}")
        print(f"Timezone: {data['timezone']}")
    else:
        print("[-] Failed to get geolocation data.")

if __name__ == "__main__":
    main()
