#!/bin/bash

# Image Optimization Test Suite
# Validates that images meet performance requirements

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Test configuration
MAX_IMAGE_SIZE=524288  # 500KB in bytes
IMAGES_DIR="assets/images/posts"

# Test counters
tests_run=0
tests_passed=0
tests_failed=0

# Helper functions
print_header() {
    echo -e "${BLUE}=== $1 ===${NC}"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
    ((tests_passed++))
    ((tests_run++))
}

print_failure() {
    echo -e "${RED}✗${NC} $1"
    ((tests_failed++))
    ((tests_run++))
}

# Test 1: Check that WebP versions exist
test_webp_existence() {
    print_header "Test 1: WebP Versions Exist"
    
    local passed=0
    local failed=0
    
    for img in ${IMAGES_DIR}/*.{jpg,jpeg,png}; do
        [ -e "$img" ] || continue
        
        local basename="${img%.*}"
        local filename=$(basename "$img")
        
        # Skip responsive versions
        if [[ "$filename" =~ -[0-9]+w\. ]]; then
            continue
        fi
        
        local webp_file="${basename}.webp"
        
        if [ -f "$webp_file" ]; then
            print_success "WebP exists for $(basename "$img")"
            ((passed++))
        else
            print_failure "Missing WebP for $(basename "$img")"
            ((failed++))
        fi
    done
    
    echo "  Summary: $passed passed, $failed failed"
}

# Test 2: Check image sizes
test_image_sizes() {
    print_header "Test 2: Main Images Under 500KB"
    
    local passed=0
    local failed=0
    
    for img in ${IMAGES_DIR}/*.{jpg,jpeg}; do
        [ -e "$img" ] || continue
        
        local filename=$(basename "$img")
        
        # Skip responsive versions
        if [[ "$filename" =~ -[0-9]+w\. ]]; then
            continue
        fi
        
        local size=$(stat -f%z "$img" 2>/dev/null || echo 0)
        local size_kb=$((size / 1024))
        
        if [ "$size" -le "$MAX_IMAGE_SIZE" ]; then
            print_success "$(basename "$img") is ${size_kb}KB"
            ((passed++))
        else
            print_failure "$(basename "$img") is ${size_kb}KB (over 500KB)"
            ((failed++))
        fi
    done
    
    echo "  Summary: $passed passed, $failed failed"
}

# Test 3: Check lazy-image component
test_lazy_image_component() {
    print_header "Test 3: Lazy Image Component"
    
    local component="_includes/lazy-image.html"
    
    if [ ! -f "$component" ]; then
        print_failure "lazy-image.html not found"
        return
    fi
    
    grep -q "image/webp" "$component" && print_success "Has WebP support" || print_failure "Missing WebP support"
    grep -q "srcset" "$component" && print_success "Has srcset" || print_failure "Missing srcset"
    grep -q 'loading="lazy"' "$component" && print_success "Has lazy loading" || print_failure "Missing lazy loading"
    grep -q "width=" "$component" && print_success "Has width attribute" || print_failure "Missing width attribute"
    grep -q "<picture>" "$component" && print_success "Uses picture element" || print_failure "Missing picture element"
}

# Test 4: Check optimization script
test_optimization_script() {
    print_header "Test 4: Optimization Script"
    
    local script="tools/optimize-images.sh"
    
    [ -f "$script" ] && print_success "Script exists" || print_failure "Script not found"
    [ -x "$script" ] && print_success "Script is executable" || print_failure "Script not executable"
    grep -q "cwebp" "$script" && print_success "Has WebP conversion" || print_failure "Missing WebP conversion"
    grep -q "RESPONSIVE_SIZES" "$script" && print_success "Has responsive sizes" || print_failure "Missing responsive sizes"
}

# Run all tests
print_header "Image Optimization Test Suite"
echo ""

test_webp_existence
echo ""

test_image_sizes
echo ""

test_lazy_image_component
echo ""

test_optimization_script
echo ""

# Summary
print_header "Summary"
echo "Total tests run: $tests_run"
echo -e "Passed: ${GREEN}$tests_passed${NC}"
echo -e "Failed: ${RED}$tests_failed${NC}"

if [ $tests_failed -eq 0 ]; then
    echo -e "\n${GREEN}All tests passed!${NC}"
    exit 0
else
    echo -e "\n${RED}Some tests failed${NC}"
    exit 1
fi
