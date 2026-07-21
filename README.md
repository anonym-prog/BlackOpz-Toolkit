<p align="center">
  <img src="https://img.shields.io/badge/Version-2.0.1-00ffff?style=for-the-badge&logo=github&logoColor=white" />
  <img src="https://img.shields.io/badge/Status-Active-ff00ff?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Platform-Termux_|_Linux-00ff00?style=for-the-badge" />
  <img src="https://img.shields.io/badge/License-UNLICENSED-ffffff?style=for-the-badge" />
</p>

<pre style="background: #0d1117; color: #00ff00; padding: 20px; border: 1px solid #00ffff; border-radius: 8px; text-align: left; font-family: monospace; white-space: pre-wrap;">

  ██████  ██████  ██████  ██████  ██    ██ ██████  ██████  ███████ ███████ ██████  ██    ██
  ██   ██ ██   ██ ██    ██ ██   ██ ██    ██ ██   ██ ██   ██ ██      ██      ██   ██  ██  ██
  ██████  ██████  ██    ██ ██   ██ ██    ██ ██████  ██████  ███████ ███████ ██████    ████
  ██   ██ ██   ██ ██    ██ ██   ██ ██    ██ ██   ██ ██   ██      ██      ██ ██   ██   ██
  ██████  ██   ██  ██████  ██████   ██████  ██   ██ ██   ██ ███████ ███████ ██   ██   ██

═══════════════════════════════════════════════════════════════════════════════
  BLACKOPZ TOOLKIT v2.0.1
  > 30 Custom Offensive Scripts
  > System: Terminal Ready
  > Mode: God Mode
═══════════════════════════════════════════════════════════════════════════════

$ whoami
blackopz

$ cat disclaimer.txt
[!] For educational and testing purposes only.
[!] Do NOT use on systems without permission.

$ _
</pre>

---

## 🧩 Tools Catalog

<details>
<summary>🟦  RECONNAISSANCE (10 Tools)</summary>

- `port_scanner.py` - Fast TCP port scanner
- `subdomain_finder.py` - Enumerate subdomains
- `mass_subdomain_scanner.py` - Multithreaded brute-forcer
- `whois_lookup.py` - WHOIS domain info
- `dns_enum.py` - DNS record enumeration
- `tech_fingerprinter.py` - Detect CMS/framework/version
- `dir_buster.py` - Directory & file brute-forcer
- `email_harvester.py` - Scrape emails from pages
- `ip_geolocator.py` - IP location & ISP details
- `social_osint.py` - Username search across platforms
</details>

<details>
<summary>🟥  EXPLOITATION (10 Tools)</summary>

- `php_backdoor.py` - Obfuscated PHP backdoor
- `aspx_web_shell.py` - ASPX shell for IIS servers
- `sql_injector_auto.py` - Automated SQLi scanner/dumper
- `xss_payload_gen.py` - XSS payload with encoding
- `wordpress_rce.py` - Exploit vulnerable WP plugins
- `command_injector.py` - OS command injection payloads
- `file_upload_bug.py` - Bypass upload filters
- `ssrf_scanner.py` - Server-Side Request Forgery
- `local_file_include.py` - LFI to RCE via log poisoning
- `reverse_shell_gen.py` - Multi-platform reverse shell
</details>

<details>
<summary>🟩  POST-EXPLOITATION (10 Tools)</summary>

- `credential_dumper_ultimate.py` - Multi-source credential dump
- `screenshot_capture_ultimate.py` - Periodic stealth screenshot
- `keylogger_advanced.py` - Silent keylogger + clipboard
- `persistence_win_advanced.py` - 6-layer Windows persistence
- `persistence_linux_advanced.py` - 5-layer Linux persistence
- `exfil_http_advanced.py` - HTTP exfil with XOR/chunking
- `exfil_dns_advanced.py` - DNS tunneling exfiltration
- `priv_esc_win_advanced.py` - Windows privilege scanner
- `priv_esc_linux_advanced.py` - Linux privilege scanner
- `cleanup_advanced.py` - Total trace wiping & memory flush
</details>

---

## ⚡ Quick Start

```bash
# Clone & install
git clone https://github.com/anonym-prog/BlackOpz-Toolkit.git
cd BlackOpz-Toolkit
chmod +x install.sh && ./install.sh

# Launch interactive menu
python3 menu.py
