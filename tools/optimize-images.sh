#!/bin/bash
set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

MAX_WIDTH=1920
JPEG_QUALITY=90
WEBP_QUALITY=85
RESPONSIVE_SIZES=(1920 1280 640)

optimize_image() {
    local input_file="$1"
    local filename=$(basename "$input_file")
    local dirname=$(dirname "$input_file")
    local extension="${filename##*.}"
    local basename="${filename%.*}"

    echo -e "${BLUE}Processing: ${filename}${NC}"

    local dims=($(sips -g pixelWidth -g pixelHeight "$input_file" | grep -E "pixelWidth|pixelHeight" | awk '{print $2}'))
    local original_width=${dims[0]}

    # Generate responsive sizes
    for size in "${RESPONSIVE_SIZES[@]}"; do
        if [ "$original_width" -ge "$size" ]; then
            echo "  Creating ${size}w version..."
            sips -Z "$size" -s format jpeg -s formatOptions "$JPEG_QUALITY" "$input_file" --out "${dirname}/${basename}-${size}w.jpg" > /dev/null 2>&1
            cwebp -q "$WEBP_QUALITY" "${dirname}/${basename}-${size}w.jpg" -o "${dirname}/${basename}-${size}w.webp" > /dev/null 2>&1
        fi
    done

    # Optimize original if needed
    local file_size=$(stat -f%z "$input_file" 2>/dev/null || echo 0)
    if [ "$original_width" -gt "$MAX_WIDTH" ] || [ "$file_size" -gt 524288 ]; then
        echo "  Optimizing original..."
        local temp_file="${dirname}/.${basename}_temp.jpg"
        
        if [ "$original_width" -gt "$MAX_WIDTH" ]; then
            sips -Z "$MAX_WIDTH" -s format jpeg -s formatOptions "$JPEG_QUALITY" "$input_file" --out "$temp_file" > /dev/null 2>&1
        else
            sips -s format jpeg -s formatOptions "$JPEG_QUALITY" "$input_file" --out "$temp_file" > /dev/null 2>&1
        fi
        
        mv "$temp_file" "${dirname}/${basename}.jpg"
        
        if [ "$extension" != "jpg" ] && [ "$extension" != "jpeg" ]; then
            rm -f "$input_file"
        fi
    fi

    # Create WebP version
    local source="${dirname}/${basename}.jpg"
    [ ! -f "$source" ] && source="$input_file"
    cwebp -q "$WEBP_QUALITY" "$source" -o "${dirname}/${basename}.webp" > /dev/null 2>&1
    
    echo -e "  ${GREEN}✓ Done${NC}"
}

if [ -d "$1" ]; then
    for img in "$1"/*.{jpg,jpeg,png}; do
        [ -e "$img" ] || continue
        [[ "$(basename "$img")" =~ -[0-9]+w\. ]] && continue
        [[ "$(basename "$img")" == *.webp ]] && continue
        optimize_image "$img"
    done
elif [ -f "$1" ]; then
    optimize_image "$1"
fi

echo -e "${GREEN}=== Optimization Complete ===${NC}"
