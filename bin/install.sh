#!/bin/bash
#
# Install clad to ~/.local/bin
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE="$SCRIPT_DIR/clad"
DEST="$HOME/.local/bin/clad"

if [ ! -f "$SOURCE" ]; then
    echo "Error: clad not found at $SOURCE"
    exit 1
fi

mkdir -p "$HOME/.local/bin"
cp "$SOURCE" "$DEST"
chmod +x "$DEST"

echo "Installed clad → $DEST"
