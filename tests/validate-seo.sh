#!/bin/bash
# Quick SEO validation test

echo "Testing SEO Enhancements..."
echo ""

# Check sitemap
if [ -f "_site/sitemap.xml" ]; then
    url_count=$(grep -c "<loc>" _site/sitemap.xml)
    echo "✓ Sitemap generated with $url_count URLs"
else
    echo "✗ Sitemap not found"
    exit 1
fi

# Check robots.txt
if [ -f "_site/robots.txt" ] && grep -q "sitemap.xml" "_site/robots.txt"; then
    echo "✓ Robots.txt configured correctly"
else
    echo "✗ Robots.txt issue"
    exit 1
fi

# Check structured data in a post
sample_post=$(find _site -name "*.html" -path "*2020*" | head -1)
if grep -q "schema.org/Article" "$sample_post" && \
   grep -q "itemprop=\"wordCount\"" "$sample_post" && \
   grep -q "min read" "$sample_post"; then
    echo "✓ Structured data and reading time present"
else
    echo "✗ Structured data incomplete"
    exit 1
fi

# Check Open Graph tags
if grep -q "og:title" "$sample_post" && \
   grep -q "og:description" "$sample_post"; then
    echo "✓ Open Graph meta tags present"
else
    echo "✗ Open Graph tags missing"
    exit 1
fi

# Check Twitter Card tags
if grep -q "twitter:card" "$sample_post"; then
    echo "✓ Twitter Card meta tags present"
else
    echo "✗ Twitter Card tags missing"
    exit 1
fi

echo ""
echo "All SEO enhancements validated successfully!"
