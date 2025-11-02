# Image Optimization Tools

## Overview

This directory contains tools for optimizing images on bankole.org with a focus on performance and GitHub Pages compatibility.

## optimize-images.sh

Automated image optimization script that generates WebP versions and responsive image sizes.

### Features

- **WebP Conversion**: Creates WebP versions with JPEG fallbacks
- **Responsive Images**: Generates 640w, 1280w, and 1920w sizes
- **JPEG Optimization**: Reduces file sizes while maintaining quality
- **Batch Processing**: Can process individual files or entire directories

### Usage

```bash
# Optimize a single image
bash tools/optimize-images.sh path/to/image.jpg

# Optimize all images in a directory
bash tools/optimize-images.sh assets/images/posts/

# Preview what would be optimized (dry run)
bash tools/optimize-images.sh --dry-run image.jpg

# Custom quality settings
bash tools/optimize-images.sh --quality 85 --webp-quality 80 image.jpg
```

### Configuration

Default settings in the script:
- **Max Width**: 1920px
- **JPEG Quality**: 90%
- **WebP Quality**: 85%
- **Responsive Sizes**: 1920w, 1280w, 640w

### Output

For each input image, the script generates:

1. **Original optimized JPEG** (if over 500KB or wider than 1920px)
   - Example: `image.jpg`

2. **WebP version**
   - Example: `image.webp`

3. **Responsive JPEG versions**
   - Example: `image-640w.jpg`, `image-1280w.jpg`, `image-1920w.jpg`

4. **Responsive WebP versions**
   - Example: `image-640w.webp`, `image-1280w.webp`, `image-1920w.webp`

### Requirements

- **sips**: Built into macOS
- **cwebp**: Install with `brew install webp`

### Example

```bash
# Before
boracay-beach.jpeg: 1.5MB (4032x3024)

# After running optimization
boracay-beach.jpg: 933KB (1920x1440)
boracay-beach.webp: 397KB
boracay-beach-1920w.jpg: 933KB
boracay-beach-1920w.webp: 397KB
boracay-beach-1280w.jpg: 431KB
boracay-beach-1280w.webp: 184KB
boracay-beach-640w.jpg: 108KB
boracay-beach-640w.webp: 47KB
```

### Performance Impact

- **JPEG Optimization**: 38-70% file size reduction
- **WebP Format**: Additional 50-60% reduction vs optimized JPEG
- **Responsive Images**: Serve appropriate size based on viewport
- **Total Page Weight Savings**: Up to 4.2MB per page with images

## Integration with Jekyll

The optimized images work with the enhanced `_includes/lazy-image.html` component:

```liquid
{% include lazy-image.html
   src="/assets/images/posts/photo.jpg"
   alt="Description"
   width="1920"
   height="1440"
%}
```

The component automatically:
1. Serves WebP to supporting browsers
2. Uses responsive srcset for different viewport sizes
3. Lazy-loads images as users scroll
4. Prevents layout shift with width/height attributes

## Testing

Run the image optimization test suite:

```bash
bash tests/image-optimization-tests.sh
```

Tests verify:
- WebP versions exist for all images
- Image file sizes are optimized
- Responsive versions are generated
- Lazy-image component has required features
- Optimization script is properly configured

## Best Practices

1. **Always optimize before committing**
   ```bash
   bash tools/optimize-images.sh assets/images/posts/new-image.jpg
   git add assets/images/posts/
   ```

2. **Use descriptive alt text** in the lazy-image component

3. **Specify width and height** to prevent layout shift

4. **Test on multiple devices** to verify responsive images load correctly

5. **Check file sizes** after optimization:
   ```bash
   ls -lh assets/images/posts/ | grep "new-image"
   ```

## Troubleshooting

### WebP files not generated
- Ensure cwebp is installed: `brew install webp`
- Check file permissions in the output directory

### Images too large
- Adjust JPEG quality: `--quality 85`
- Verify source image dimensions
- Consider manual editing for specific images

### Responsive versions missing
- Image must be at least 640px wide
- Check script output for errors
- Verify sips command is available

## Performance Metrics

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Largest image | 1.7MB | 424KB (WebP) | 75% smaller |
| Average image size | 1.6MB | 436KB | 73% smaller |
| Total payload (3 images) | 4.8MB | 1.3MB | 73% reduction |
| Mobile viewport (640w) | 4.8MB | 156KB | 97% reduction |

## Future Enhancements

- [ ] AVIF format support
- [ ] Automatic image dimension detection for lazy-image includes
- [ ] Pre-commit hook for automatic optimization
- [ ] CI/CD integration for pull requests
- [ ] Blur-up placeholder generation
