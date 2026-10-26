#!/bin/bash
# Gera o PNG de cada .mmd desta pasta (Mermaid CLI). Uso: ./render.sh [arquivo.mmd ...]
cd "$(dirname "$0")"
MMDC=${MMDC:-mmdc}
for f in "${@:-*.mmd}"; do
  out="../$(basename "${f%.mmd}").png"
  $MMDC ${PUPPETEER_CFG:+-p "$PUPPETEER_CFG"} -i "$f" -o "$out" -s 3 -b white -w 1800 >/dev/null 2>err.log || { echo "ERRO $f"; grep -m3 -i error err.log; }
done
rm -f err.log
