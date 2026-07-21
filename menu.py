#!/usr/bin/env python3
import os
import sys
import subprocess
import glob

# Daftar folder yang akan discan
TOOL_FOLDERS = [
    "tools/recon",
    "tools/exploit",
    "tools/post-exploit"
]

def scan_tools():
    """Cari semua file .py di folder tools"""
    tools = []
    for folder in TOOL_FOLDERS:
        if os.path.exists(folder):
            for pyfile in glob.glob(f"{folder}/*.py"):
                tools.append(pyfile)
    return sorted(tools)

def get_tool_description(pyfile):
    """Ambil deskripsi dari komentar baris pertama (optional)"""
    try:
        with open(pyfile, "r") as f:
            first_line = f.readline().strip()
            if first_line.startswith("#"):
                return first_line[1:].strip()
    except:
        pass
    return os.path.basename(pyfile)

def main():
    tools = scan_tools()
    if not tools:
        print("[-] Tidak ada tool ditemukan. Pastikan folder tools sudah ada.")
        sys.exit(1)

    print("\n" + "="*50)
    print("  🔥 BlackOpz Toolkit v2.0 - Interactive Menu")
    print("="*50)
    print("\nPilih tool yang ingin dijalankan:\n")

    for i, tool in enumerate(tools, 1):
        desc = get_tool_description(tool)
        print(f"  {i:2d}. {desc}")

    print("\n  0. Keluar")
    print("="*50)

    try:
        choice = input("\n➜ Pilih nomor: ").strip()
    except KeyboardInterrupt:
        print("\n[!] Keluar.")
        sys.exit(0)

    if choice == "0" or choice == "":
        print("[!] Keluar.")
        sys.exit(0)

    try:
        idx = int(choice) - 1
        if idx < 0 or idx >= len(tools):
            print("[-] Nomor tidak valid.")
            sys.exit(1)
        selected = tools[idx]
    except ValueError:
        print("[-] Input harus angka.")
        sys.exit(1)

    print(f"\n[+] Menjalankan: {selected}")
    print("[+] Masukkan argumen jika diperlukan (spasi untuk pisah).")
    args = input("➜ Argumen: ").strip().split()

    cmd = ["python3", selected] + args
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n[!] Tool dihentikan.")
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    main()
