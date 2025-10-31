# bankole.org Jekyll Site

Personal blog built with Jekyll and hosted on GitHub Pages at [bankole.org](https://bankole.org).

## About

This is a minimalist personal blog focusing heavily on performance optimization. The site uses the [`riggraz/no-style-please`](https://github.com/riggraz/no-style-please) theme and is built with Jekyll, hosted on GitHub Pages.

## Tech Stack

- **Static Site Generator**: Jekyll 3.9.5
- **Theme**: `riggraz/no-style-please` (remote theme)
- **Hosting**: GitHub Pages
- **Markdown**: Kramdown
- **Key Plugins**:
  - jekyll-feed
  - jekyll-paginate
  - jekyll-seo-tag
  - jemoji
  - jekyll-remote-theme

## Project Structure

```
.
├── _config.yml           # Jekyll configuration
├── _includes/            # Reusable HTML components
│   ├── talkyard-comments.html  # Lazy-loaded comments
│   ├── lazy-image.html        # Lazy image loading component
│   ├── custom-head.html       # Performance monitoring
│   ├── analytics.html         # Google Analytics
│   └── buttondown.html        # Newsletter integration
├── _layouts/             # Page templates
│   └── post.html         # Blog post layout
├── _pages/               # Static pages (About, Archive, etc.)
├── _posts/               # Blog posts in markdown (YYYY-MM-DD-title.md)
├── assets/
│   ├── images/posts/     # Optimized post images
│   └── js/               # JavaScript files
├── tests/                # Test suites
│   ├── performance-tests.js
│   └── validate-assets.sh
└── redirects.json        # URL redirects configuration
```

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

### Initial Setup
```bash
# Install dependencies
bundle install

# Build the site
bundle exec jekyll build

# Serve locally with auto-reload
bundle exec jekyll serve --watch
```

Then open `http://localhost:4000` in your browser. Performance metrics will be logged to the console.

### Common Commands
```bash
# Build site
bundle exec jekyll build

# Serve with live reload
bundle exec jekyll serve --watch

# Run performance tests
node tests/performance-tests.js

# Validate assets
bash tests/validate-assets.sh
```

## GitHub Pages Compatibility

All optimizations are fully compatible with GitHub Pages:
- No custom plugins requiring Gemfile modifications
- Uses remote theme: `riggraz/no-style-please`
- All performance enhancements use vanilla JavaScript
- No server-side processing required

## Content Management

### Adding New Blog Posts
1. Create file in `_posts/` with format: `YYYY-MM-DD-title.md`
2. Add front matter:
   ```yaml
   ---
   layout: post
   author:
     - Bankole
   title: "Your Post Title"
   discussion_id: unique-discussion-id
   comments: true
   ---
   ```
3. Write content in Kramdown markdown
4. Optimize and add images to `/assets/images/posts/`
5. Test locally before committing

### Adding New Images
1. **Optimize images before committing** (this is critical!)
   ```bash
   sips -Z 1920 -s format jpeg -s formatOptions 90 input.jpg --out output.jpg
   ```
2. Place optimized images in `/assets/images/posts/`
3. Reference in posts with relative URLs: `/assets/images/posts/image-name.jpg`
4. **Never** commit large unoptimized images

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

## External Services

- **Comments**: [Talkyard](https://comments-for-makanju-org.talkyard.net)
- **Analytics**: Google Analytics (UA-160597721-1)
- **Newsletter**: Buttondown integration

## Repository Maintenance

### Recent Cleanup (October 2024)
The repository was cleaned up to remove migration artifacts and improve organization:
- Removed 57MB WordPress backup and migration scripts
- Consolidated favicon files (6 → 1)
- Migrated all images to `/assets/images/posts/` for consistency
- Updated `.gitignore` to prevent future clutter
- Total cleanup: ~68MB removed from repository, ~370MB freed locally

### Best Practices
1. **Always optimize images** before committing
2. **Use `/assets/images/posts/`** for all blog post images
3. **Test locally** before pushing to master
4. **Run test suites** before major changes
5. **Keep the repository clean** - no temporary files, backups, or large binaries

### GitHub Pages Constraints
- **No custom plugins** requiring build steps
- **Remote theme only** (not local theme modifications)
- **Vanilla JavaScript** (no build tools like webpack)
- All changes must work with GitHub's Jekyll environment

## Future Optimizations

Potential areas for further improvement:
- [ ] Implement service worker for offline support
- [ ] Add WebP image format with fallbacks
- [ ] Implement critical CSS inlining
- [ ] Add resource bundling for multiple CSS/JS files
- [ ] Implement prefetching for likely next navigation

## Contributing

This is a personal blog, but if you notice any issues or have suggestions for performance improvements, feel free to open an issue.

## License

Content is © Bankole. Theme is MIT licensed.