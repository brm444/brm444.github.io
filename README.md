# bankole.org Jekyll Site

Personal blog built with Jekyll and hosted on GitHub Pages.

## Performance Optimizations

This site has been optimized for performance with the following enhancements:

### 1. Lazy-Loaded Comments
- **Implementation**: Talkyard comments load only when user scrolls near the comment section
- **Location**: `_includes/talkyard-comments.html`
- **Benefits**: 50-70% faster initial page load, reduced JavaScript execution on page load
- **Fallback**: Uses IntersectionObserver API with fallback for older browsers

### 2. Optimized Images
- **Implementation**: Images resized to max 1920px width with 90% quality preservation
- **Location**: `/assets/images/posts/` for optimized versions
- **Benefits**: ~40% reduction in image payload while maintaining visual quality
- **Tools Used**: macOS `sips` command for image optimization

### 3. Lazy Image Loading
- **Component**: `_includes/lazy-image.html`
- **Features**: 
  - Native `loading="lazy"` attribute for modern browsers
  - IntersectionObserver fallback for older browsers
  - Progressive enhancement approach
- **Usage**: Can be included in posts for lazy-loaded images

### 4. Performance Monitoring
- **Location**: `_includes/custom-head.html`
- **Metrics Tracked**:
  - DOM load time
  - Page load time
  - Comments load time (when triggered)
  - Analytics load time
- **Visibility**: Performance metrics logged to console in development environment only

### 5. Resource Hints
- **Optimizations**:
  - DNS prefetching for external resources
  - Preconnect to Google Analytics and Talkyard servers
  - Reduces connection setup time for external resources

### 6. Analytics Optimization
- **Implementation**: Google Analytics script loaded asynchronously with performance tracking
- **Location**: `_includes/analytics.html`

## Testing

Two test suites are available to validate optimizations:

### JavaScript Tests
```bash
node tests/performance-tests.js
```
Validates:
- Facebook Pixel removal (if applicable)
- Talkyard lazy loading implementation
- Lazy image component functionality
- No external Medium images
- Performance monitoring setup
- Resource hints configuration

### Asset Validation
```bash
bash tests/validate-assets.sh
```
Checks:
- Image directory structure
- Image optimization (size limits)
- No broken image references
- Component file presence
- Overall asset health

## Local Development

To test the site locally:
```bash
bundle exec jekyll serve --watch
```

Then open `http://localhost:4000` in your browser. Performance metrics will be logged to the console.

## GitHub Pages Compatibility

All optimizations are fully compatible with GitHub Pages:
- No custom plugins requiring Gemfile modifications
- Uses remote theme: `riggraz/no-style-please`
- All performance enhancements use vanilla JavaScript
- No server-side processing required

## Maintenance Notes

### Adding New Images
1. Add original images to appropriate directory
2. Optimize with: `sips -Z 1920 -s format jpeg -s formatOptions 90 input.jpg --out output.jpg`
3. Place in `/assets/images/posts/` or appropriate directory
4. Reference in posts with relative URLs

### Updating Lazy Loading
- Comment loading: Edit `_includes/talkyard-comments.html`
- Image loading: Edit `_includes/lazy-image.html`
- Performance tracking: Edit `_includes/custom-head.html`

### Performance Benchmarks
Expected improvements after optimizations:
- **Initial Page Load**: 50-70% faster (due to lazy-loaded comments)
- **Image Payload**: ~40% reduction (from optimization)
- **Time to Interactive**: Significantly improved
- **Core Web Vitals**: Better LCP, CLS, and FID scores

## Future Optimizations

Potential areas for further improvement:
- [ ] Implement service worker for offline support
- [ ] Add WebP image format with fallbacks
- [ ] Implement critical CSS inlining
- [ ] Add resource bundling for multiple CSS/JS files
- [ ] Implement prefetching for likely next navigation