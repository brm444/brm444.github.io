# Using the Enhanced Lazy Image Component

## Overview

The enhanced `lazy-image.html` component now supports WebP format with responsive images, providing optimal performance across all devices and browsers.

## Basic Usage

In your blog posts or pages, include images like this:

```liquid
{% include lazy-image.html
   src="/assets/images/posts/boracay-beach"
   alt="White sand beach in Boracay with crystal clear turquoise water"
   width="1920"
   height="1440"
%}
```

**Important Notes:**
- `src` should NOT include the file extension (.jpg)
- `alt` text is REQUIRED for accessibility
- `width` and `height` should match the original image dimensions
- These prevent layout shift (CLS) and improve Core Web Vitals

## How It Works

The component automatically generates this HTML:

```html
<picture>
  <!-- WebP sources for modern browsers -->
  <source type="image/webp"
          srcset="/assets/images/posts/boracay-beach-640w.webp 640w,
                  /assets/images/posts/boracay-beach-1280w.webp 1280w,
                  /assets/images/posts/boracay-beach-1920w.webp 1920w"
          sizes="(max-width: 640px) 640px, (max-width: 1280px) 1280px, 1920px" />

  <!-- JPEG fallback for older browsers -->
  <source type="image/jpeg"
          srcset="/assets/images/posts/boracay-beach-640w.jpg 640w,
                  /assets/images/posts/boracay-beach-1280w.jpg 1280w,
                  /assets/images/posts/boracay-beach-1920w.jpg 1920w"
          sizes="(max-width: 640px) 640px, (max-width: 1280px) 1280px, 1920px" />

  <!-- Main image tag -->
  <img src="/assets/images/posts/boracay-beach.jpg"
       alt="White sand beach in Boracay with crystal clear turquoise water"
       loading="lazy"
       width="1920"
       height="1440" />
</picture>
```

## What Gets Loaded

### On a Modern Desktop (Chrome, Firefox, Edge, Safari)
- **Viewport > 1280px**: `boracay-beach-1920w.webp` (397KB)
- **Viewport 640-1280px**: `boracay-beach-1280w.webp` (184KB)
- **Total savings vs original**: 75% smaller

### On Mobile (iPhone, Android)
- **Viewport < 640px**: `boracay-beach-640w.webp` (47KB)
- **Total savings vs original**: 97% smaller!

### On Older Browsers (IE11, older Safari)
- Falls back to JPEG versions
- Still gets responsive sizing benefits
- Loads `boracay-beach-640w.jpg` (108KB) on mobile

## Custom Sizes

You can override the default sizes attribute:

```liquid
{% include lazy-image.html
   src="/assets/images/posts/photo"
   alt="Description"
   width="1920"
   height="1080"
   sizes="(max-width: 768px) 100vw, 50vw"
%}
```

This tells the browser:
- On mobile: use full viewport width
- On desktop: use 50% of viewport width

## Additional CSS Classes

Add custom classes for styling:

```liquid
{% include lazy-image.html
   src="/assets/images/posts/photo"
   alt="Description"
   width="1920"
   height="1080"
   class="rounded shadow-lg"
%}
```

## Finding Image Dimensions

If you don't know the width and height of your image:

```bash
# On macOS
sips -g pixelWidth -g pixelHeight assets/images/posts/photo.jpg

# Or use ImageMagick
identify -format "%wx%h" assets/images/posts/photo.jpg
```

## Optimization Workflow

1. **Add new image to repository**
   ```bash
   cp ~/Downloads/new-photo.jpg assets/images/posts/
   ```

2. **Optimize the image**
   ```bash
   bash tools/optimize-images.sh assets/images/posts/new-photo.jpg
   ```

3. **Check what was generated**
   ```bash
   ls -lh assets/images/posts/new-photo*
   ```

4. **Get dimensions**
   ```bash
   sips -g pixelWidth -g pixelHeight assets/images/posts/new-photo.jpg
   ```

5. **Use in your post**
   ```liquid
   {% include lazy-image.html
      src="/assets/images/posts/new-photo"
      alt="Descriptive text about the image"
      width="1920"
      height="1440"
   %}
   ```

## Accessibility Best Practices

### Good Alt Text Examples

✅ **Good**: "Aerial view of Manhattan skyline at dusk with illuminated buildings"
✅ **Good**: "Developer typing code on laptop with multiple monitors"
✅ **Good**: "Graph showing 40% increase in website performance"

### Bad Alt Text Examples

❌ **Bad**: "Image of city"
❌ **Bad**: "Picture of someone coding"
❌ **Bad**: "DSC_1234.jpg"
❌ **Bad**: "" (empty - should only be used for purely decorative images)

### Complex Images

For charts, diagrams, or complex images, provide context in surrounding text:

```markdown
The chart below shows the dramatic improvement in page load times after
implementing image optimization...

{% include lazy-image.html
   src="/assets/images/posts/performance-chart"
   alt="Bar chart comparing page load times before and after optimization"
   width="1920"
   height="1080"
%}

As shown, the optimized pages load 73% faster on average.
```

## Verifying It Works

After adding images to your site:

1. **Build locally**
   ```bash
   bundle exec jekyll serve
   ```

2. **Open DevTools (Network tab)**
   - On desktop: Look for `.webp` files being loaded
   - On mobile: Check that smaller sizes are loaded

3. **Test responsive behavior**
   - Resize browser window
   - Check which image sizes are loaded at different breakpoints

4. **Validate Core Web Vitals**
   - Use Lighthouse in Chrome DevTools
   - Check for CLS (Cumulative Layout Shift) - should be < 0.1
   - Check for LCP (Largest Contentful Paint) - should be < 2.5s

## Performance Impact

### Before Optimization
- Desktop loads 1.5MB JPEG
- Mobile loads same 1.5MB JPEG
- Total page weight: ~3MB with 2 images

### After Optimization
- Desktop loads 397KB WebP
- Mobile loads 47KB WebP
- Total page weight: ~500KB with 2 images
- **83% reduction in page weight**

## Troubleshooting

### Images not lazy-loading
- Check browser console for JavaScript errors
- Verify `loading="lazy"` attribute is present in rendered HTML
- Some browsers require polyfill for older versions

### WebP not loading
- Check file actually exists: `ls assets/images/posts/*.webp`
- Verify browser supports WebP (all modern browsers do)
- Check DevTools Network tab to see what's actually loading

### Wrong image size loading
- Inspect rendered HTML and check `srcset` attribute
- Use DevTools responsive mode to test different viewport sizes
- Verify `sizes` attribute matches your layout

### Layout shift occurring
- Ensure `width` and `height` attributes are set
- Check CSS isn't overriding aspect ratio
- Verify dimensions match actual image dimensions

## Examples from Real Posts

```liquid
<!-- Hero image at top of post -->
{% include lazy-image.html
   src="/assets/images/posts/manila-night"
   alt="Manila skyline at night with illuminated skyscrapers reflected in water"
   width="1920"
   height="1436"
%}

<!-- Smaller inline image -->
{% include lazy-image.html
   src="/assets/images/posts/school-songs"
   alt="Sheet music showing traditional school songs"
   width="1500"
   height="1000"
   class="border"
%}
```

## Further Reading

- [MDN: Responsive Images](https://developer.mozilla.org/en-US/docs/Learn/HTML/Multimedia_and_embedding/Responsive_images)
- [web.dev: Serve images in modern formats](https://web.dev/uses-webp-images/)
- [web.dev: Lazy loading images](https://web.dev/lazy-loading-images/)
- [web.dev: Optimize Cumulative Layout Shift](https://web.dev/optimize-cls/)
