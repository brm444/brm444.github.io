# bankole.org - Claude Context

## Project Overview

This is a personal blog built with Jekyll and hosted on GitHub Pages at [bankole.org](https://bankole.org). The site uses the minimalist `no-style-please` theme and focuses heavily on performance optimization.

## Tech Stack

- **Static Site Generator**: Jekyll
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
│   ├── buttondown.html        # Newsletter integration
│   └── youtube.html           # YouTube embeds
├── _layouts/             # Page templates
│   └── post.html         # Blog post layout
├── _pages/               # Static pages (About, Archive, etc.)
├── _posts/               # Blog posts in markdown
├── assets/
│   ├── images/posts/     # Optimized post images
│   └── js/               # JavaScript files
├── tests/                # Test suites
│   ├── performance-tests.js
│   └── validate-assets.sh
└── redirects.json        # URL redirects configuration
```

## Performance Philosophy

**Performance is a core feature of this site.** All optimizations must be compatible with GitHub Pages (no custom plugins requiring server-side processing).

### Current Optimizations

1. **Lazy-loaded Comments**: Talkyard comments load only when user scrolls near the comment section
   - 50-70% faster initial page load
   - Location: [_includes/talkyard-comments.html](_includes/talkyard-comments.html)

2. **Optimized Images**: Images resized to max 1920px with 90% quality
   - ~40% reduction in payload
   - Command: `sips -Z 1920 -s format jpeg -s formatOptions 90 input.jpg --out output.jpg`

3. **Lazy Image Loading**: Progressive enhancement approach
   - Component: [_includes/lazy-image.html](_includes/lazy-image.html)
   - Uses native `loading="lazy"` with IntersectionObserver fallback

4. **Performance Monitoring**: Console logging in development
   - Tracks DOM load, page load, comments load, analytics load
   - Location: [_includes/custom-head.html](_includes/custom-head.html)

5. **Resource Hints**: DNS prefetching and preconnect for external resources

6. **Async Analytics**: Google Analytics loaded asynchronously

## Coding Conventions

### HTML/Liquid Templates
- Use semantic HTML5 elements
- Keep includes focused and single-purpose
- Use Liquid includes for reusable components
- Maintain compatibility with GitHub Pages (no custom plugins)

### CSS
- Respect the minimalist theme aesthetic
- Use compressed SASS output (`style: compressed`)
- Avoid heavy CSS frameworks

### JavaScript
- Use vanilla JavaScript (no jQuery or large frameworks)
- Progressive enhancement approach
- IntersectionObserver for lazy loading with fallbacks
- Performance first: async/defer script loading

### Images
- **Always optimize** before committing
- Max width: 1920px
- Format: JPEG at 90% quality for photos
- Store in: `/assets/images/posts/`
- Use relative URLs in posts

### Posts
- Format: Markdown (Kramdown)
- Naming: `YYYY-MM-DD-title.md`
- Permalink structure: `/:year-:month-:day/:title`
- Front matter required:
  ```yaml
  ---
  layout: post
  title: "Post Title"
  date: YYYY-MM-DD
  ---
  ```

## Testing

Before deploying changes, run:

```bash
# JavaScript validation
node tests/performance-tests.js

# Asset validation
bash tests/validate-assets.sh

# Local preview
bundle exec jekyll serve --watch
```

## GitHub Pages Constraints

- **No custom plugins** that require Gemfile modifications beyond approved list
- **Remote theme only** (not local theme)
- **Vanilla JavaScript only** (no build step for JS)
- All changes must work with GitHub's Jekyll build environment

## External Services

- **Comments**: Talkyard (https://comments-for-makanju-org.talkyard.net)
- **Analytics**: Google Analytics (UA-160597721-1)
- **Newsletter**: Buttondown integration (check [_includes/buttondown.html](_includes/buttondown.html))

## Development Workflow

1. Create/edit content in `_posts/` or `_pages/`
2. Optimize any new images before adding
3. Test locally with `bundle exec jekyll serve`
4. Run test suites
5. Commit and push to `master` branch
6. GitHub Pages auto-deploys

## Common Tasks

### Adding a New Blog Post
1. Create file: `_posts/YYYY-MM-DD-title.md`
2. Add front matter (layout, title, date)
3. Write content in Kramdown markdown
4. Optimize and add any images to `/assets/images/posts/`
5. Test locally

### Optimizing Images
```bash
sips -Z 1920 -s format jpeg -s formatOptions 90 input.jpg --out output.jpg
```

### Adding Custom Includes
1. Create in `_includes/`
2. Keep focused on single purpose
3. Use vanilla JavaScript only
4. Follow progressive enhancement pattern

## Future Optimization Ideas

- Service worker for offline support
- WebP format with fallbacks
- Critical CSS inlining
- Resource bundling
- Prefetching for navigation

## Notes for AI Assistants

- **Always preserve performance optimizations** when making changes
- **Never remove lazy loading** without explicit instruction
- **Test compatibility** with GitHub Pages before suggesting changes
- **Optimize images** if adding new ones
- **Respect the minimalist aesthetic** of the no-style-please theme
- **Use vanilla JavaScript only** - no frameworks or build tools
- **Reference files using markdown links** for VSCode navigation: [filename.ext](path/to/filename.ext)
