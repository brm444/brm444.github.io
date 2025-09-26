#!/bin/bash

# Asset validation script for Jekyll site performance optimization
# Run with: bash tests/validate-assets.sh

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
TOTAL_TESTS=0
PASSED_TESTS=0

# Project root directory
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo -e "\n${YELLOW}=== Running Asset Validation Tests ===${NC}\n"

# Function to run a test
run_test() {
    local test_name="$1"
    local test_command="$2"
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    if eval "$test_command"; then
        echo -e "${GREEN}✓${NC} $test_name: Passed"
        PASSED_TESTS=$((PASSED_TESTS + 1))
        return 0
    else
        echo -e "${RED}✗${NC} $test_name: Failed"
        return 1
    fi
}

# Test 1: Check if assets/images/posts directory exists
test_images_directory() {
    [ -d "$PROJECT_ROOT/assets/images/posts" ]
}
run_test "Images directory structure" test_images_directory

# Test 2: Check if optimized images exist
test_optimized_images() {
    [ -f "$PROJECT_ROOT/assets/images/posts/manila-night.jpeg" ] && \
    [ -f "$PROJECT_ROOT/assets/images/posts/boracay-beach.jpeg" ]
}
run_test "Optimized Manila post images" test_optimized_images

# Test 3: Check image sizes (should be under 500KB for optimized web images)
test_image_sizes() {
    local large_images=0
    
    if [ -d "$PROJECT_ROOT/assets/images/posts" ]; then
        while IFS= read -r -d '' file; do
            size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null)
            size_kb=$((size / 1024))
            
            if [ "$size_kb" -gt 500 ]; then
                echo -e "  ${YELLOW}Warning: $(basename "$file") is ${size_kb}KB (recommended < 500KB)${NC}"
                large_images=$((large_images + 1))
            fi
        done < <(find "$PROJECT_ROOT/assets/images/posts" -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" \) -print0)
    fi
    
    # Allow up to 2 large images for hero/featured images
    [ "$large_images" -le 2 ]
}
run_test "Image size optimization" test_image_sizes

# Test 4: Check for broken image references in posts
test_broken_images() {
    local broken_refs=0
    
    if [ -d "$PROJECT_ROOT/_posts" ]; then
        # Extract all image references from markdown files
        while IFS= read -r img_path; do
            # Remove leading slash if present
            img_path="${img_path#/}"
            
            # Check if the referenced image exists
            if [ ! -f "$PROJECT_ROOT/$img_path" ]; then
                echo -e "  ${YELLOW}Missing image: $img_path${NC}"
                broken_refs=$((broken_refs + 1))
            fi
        done < <(grep -h -o '!\[.*\]([^)]*\(jpg\|jpeg\|png\)[^)]*)' "$PROJECT_ROOT"/_posts/*.md 2>/dev/null | \
                 sed -E 's/!\[.*\]\(([^)]*)\)/\1/' | \
                 grep -v '^http' | \
                 sort -u)
    fi
    
    [ "$broken_refs" -eq 0 ]
}
run_test "No broken image links" test_broken_images

# Test 5: Check if uploads directory has been cleaned of unused large images
test_uploads_cleanup() {
    local uploads_dir="$PROJECT_ROOT/uploads/2016/01"
    
    if [ -d "$uploads_dir" ]; then
        # Check if the original large images still exist (they can, but warn if they're very large)
        local large_count=0
        for img in "$uploads_dir"/*.jpg "$uploads_dir"/*.jpeg "$uploads_dir"/*.png; do
            [ -f "$img" ] || continue
            size=$(stat -f%z "$img" 2>/dev/null || stat -c%s "$img" 2>/dev/null)
            size_mb=$((size / 1024 / 1024))
            
            if [ "$size_mb" -gt 1 ]; then
                echo -e "  ${YELLOW}Info: Original large image still in uploads: $(basename "$img") (${size_mb}MB)${NC}"
                large_count=$((large_count + 1))
            fi
        done
        
        # This is informational, not a failure
        return 0
    fi
    
    return 0
}
run_test "Uploads directory check" test_uploads_cleanup

# Test 6: Verify lazy loading component exists
test_lazy_loading_component() {
    [ -f "$PROJECT_ROOT/_includes/lazy-image.html" ]
}
run_test "Lazy loading component exists" test_lazy_loading_component

# Test 7: Check for hardcoded external image URLs
test_no_external_images() {
    local external_count=0
    
    if [ -d "$PROJECT_ROOT/_posts" ]; then
        external_count=$(grep -h 'https://miro.medium.com\|https://cdn-images.*medium.com' "$PROJECT_ROOT"/_posts/*.md 2>/dev/null | wc -l)
    fi
    
    [ "$external_count" -eq 0 ]
}
run_test "No external Medium images" test_no_external_images

# Test 8: Verify performance monitoring in place
test_performance_monitoring() {
    [ -f "$PROJECT_ROOT/_includes/custom-head.html" ] && \
    grep -q "performance.mark" "$PROJECT_ROOT/_includes/custom-head.html"
}
run_test "Performance monitoring configured" test_performance_monitoring

# Test 9: Check Talkyard lazy loading
test_talkyard_lazy() {
    [ -f "$PROJECT_ROOT/_includes/talkyard-comments.html" ] && \
    grep -q "IntersectionObserver" "$PROJECT_ROOT/_includes/talkyard-comments.html"
}
run_test "Talkyard lazy loading" test_talkyard_lazy

# Test 10: Verify tests directory structure
test_tests_directory() {
    [ -f "$PROJECT_ROOT/tests/performance-tests.js" ] && \
    [ -f "$PROJECT_ROOT/tests/validate-assets.sh" ]
}
run_test "Test files present" test_tests_directory

# Summary
echo -e "\n${YELLOW}=== Test Summary ===${NC}"
echo -e "Total: $TOTAL_TESTS | Passed: ${GREEN}$PASSED_TESTS${NC} | Failed: ${RED}$((TOTAL_TESTS - PASSED_TESTS))${NC}\n"

# Exit with appropriate code
if [ "$PASSED_TESTS" -eq "$TOTAL_TESTS" ]; then
    echo -e "${GREEN}All tests passed!${NC}\n"
    exit 0
else
    echo -e "${RED}Some tests failed. Please review the output above.${NC}\n"
    exit 1
fi