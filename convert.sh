#!/bin/bash

# Usage: ./make_icns.sh path/to/image.png

set -e

if [ $# -ne 1 ]; then
    echo "Usage: $0 path/to/image.png"
    exit 1
fi

INPUT_PNG="$1"
BASENAME=$(basename "$INPUT_PNG" .png)
ICONSET_DIR="${BASENAME}.iconset"
ICNS_FILE="${BASENAME}.icns"

echo "Creating iconset directory: $ICONSET_DIR"
mkdir -p "$ICONSET_DIR"

echo "Generating icons at various sizes..."
sips -z 16 16     "$INPUT_PNG" --out "$ICONSET_DIR/icon_16x16.png"
sips -z 32 32     "$INPUT_PNG" --out "$ICONSET_DIR/icon_16x16@2x.png"
sips -z 32 32     "$INPUT_PNG" --out "$ICONSET_DIR/icon_32x32.png"
sips -z 64 64     "$INPUT_PNG" --out "$ICONSET_DIR/icon_32x32@2x.png"
sips -z 128 128   "$INPUT_PNG" --out "$ICONSET_DIR/icon_128x128.png"
sips -z 256 256   "$INPUT_PNG" --out "$ICONSET_DIR/icon_128x128@2x.png"
sips -z 256 256   "$INPUT_PNG" --out "$ICONSET_DIR/icon_256x256.png"
sips -z 512 512   "$INPUT_PNG" --out "$ICONSET_DIR/icon_256x256@2x.png"
sips -z 512 512   "$INPUT_PNG" --out "$ICONSET_DIR/icon_512x512.png"
cp "$INPUT_PNG"           "$ICONSET_DIR/icon_512x512@2x.png"

echo "Converting to .icns format..."
iconutil -c icns "$ICONSET_DIR" -o "$ICNS_FILE"

echo "Cleaning up..."
rm -r "$ICONSET_DIR"

echo "✅ Done! Created: $ICNS_FILE"
