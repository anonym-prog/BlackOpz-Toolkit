#!/bin/bash
echo "[+] Installing dependencies..."
pip3 install -r requirements.txt
chmod +x tools/recon/*.py
chmod +x tools/exploit/*.py
chmod +x tools/post-exploit/*.py
echo "[+] Done."
