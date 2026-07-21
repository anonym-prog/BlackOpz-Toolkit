#!/usr/bin/env python3
import requests
import sys

def print_banner():
    print("\n[+] Social OSINT v1.0 - Username presence check\n")

def check_username(username):
    sites = {
        "Instagram": f"https://instagram.com/{username}",
        "Twitter/X": f"https://twitter.com/{username}",
        "Facebook": f"https://facebook.com/{username}",
        "GitHub": f"https://github.com/{username}",
        "Reddit": f"https://reddit.com/user/{username}",
        "YouTube": f"https://youtube.com/@{username}",
        "TikTok": f"https://tiktok.com/@{username}",
        "Pinterest": f"https://pinterest.com/{username}",
        "Twitch": f"https://twitch.tv/{username}",
        "Telegram": f"https://t.me/{username}"
    }
    
    results = []
    for name, url in sites.items():
        try:
            r = requests.get(url, timeout=5)
            if r.status_code < 400:
                results.append(f"[+] {name}: {url}")
        except:
            pass
    return results

def main():
    print_banner()

    if len(sys.argv) < 2:
        print("Usage: python3 social_osint.py <username>")
        sys.exit(1)

    username = sys.argv[1]
    print(f"[*] Checking username: {username}\n")

    results = check_username(username)
    if results:
        for res in results:
            print(res)
    else:
        print("[-] Username not found on major platforms.")

if __name__ == "__main__":
    main()
