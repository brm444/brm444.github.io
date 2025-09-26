#!/usr/bin/env node

/**
 * Performance optimization validation tests for Jekyll site
 * Run with: node tests/performance-tests.js
 */

const fs = require('fs');
const path = require('path');

const colors = {
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  reset: '\x1b[0m'
};

class PerformanceTests {
  constructor() {
    this.rootDir = path.join(__dirname, '..');
    this.testResults = [];
  }

  log(message, type = 'info') {
    const prefix = type === 'success' ? colors.green + '✓' : 
                   type === 'error' ? colors.red + '✗' : 
                   colors.yellow + '•';
    console.log(`${prefix} ${message}${colors.reset}`);
  }

  addResult(testName, passed, message) {
    this.testResults.push({ testName, passed, message });
    this.log(`${testName}: ${message}`, passed ? 'success' : 'error');
  }

  // Test 1: Check if Facebook Pixel code is removed
  testFacebookPixelRemoved() {
    const filesToCheck = [
      '_includes/custom-head.html',
      '_includes/analytics.html',
      '_layouts/post.html'
    ];

    let pixelFound = false;
    const pixelPatterns = [
      /facebook.*pixel/i,
      /fbq\(/,
      /!function\(f,b,e,v,n,t,s\)/
    ];

    filesToCheck.forEach(file => {
      const filePath = path.join(this.rootDir, file);
      if (fs.existsSync(filePath)) {
        const content = fs.readFileSync(filePath, 'utf8');
        pixelPatterns.forEach(pattern => {
          if (pattern.test(content)) {
            pixelFound = true;
          }
        });
      }
    });

    this.addResult(
      'Facebook Pixel Removed',
      !pixelFound,
      pixelFound ? 'Facebook Pixel code still present' : 'No Facebook Pixel code found'
    );
  }

  // Test 2: Check if Talkyard lazy loading is implemented
  testTalkyardLazyLoading() {
    const talkyardFile = path.join(this.rootDir, '_includes/talkyard-comments.html');
    
    if (!fs.existsSync(talkyardFile)) {
      this.addResult('Talkyard Lazy Loading', false, 'Talkyard comments file not found');
      return;
    }

    const content = fs.readFileSync(talkyardFile, 'utf8');
    const hasIntersectionObserver = content.includes('IntersectionObserver');
    const hasLazyLoadFunction = content.includes('loadComments');
    const hasPlaceholder = content.includes('Loading comments');
    
    const isImplemented = hasIntersectionObserver && hasLazyLoadFunction && hasPlaceholder;

    this.addResult(
      'Talkyard Lazy Loading',
      isImplemented,
      isImplemented ? 'Lazy loading properly implemented' : 'Lazy loading not fully implemented'
    );
  }

  // Test 3: Check if lazy image component exists
  testLazyImageComponent() {
    const lazyImageFile = path.join(this.rootDir, '_includes/lazy-image.html');
    
    if (!fs.existsSync(lazyImageFile)) {
      this.addResult('Lazy Image Component', false, 'Lazy image component not found');
      return;
    }

    const content = fs.readFileSync(lazyImageFile, 'utf8');
    const hasLoadingAttr = content.includes('loading="lazy"');
    const hasIntersectionObserver = content.includes('IntersectionObserver');
    const hasDataSrc = content.includes('data-src');
    
    const isImplemented = hasLoadingAttr && hasIntersectionObserver && hasDataSrc;

    this.addResult(
      'Lazy Image Component',
      isImplemented,
      isImplemented ? 'Component properly implemented with native and JS fallback' : 'Component missing required features'
    );
  }

  // Test 4: Check for external Medium image references
  testNoMediumImages() {
    const postsDir = path.join(this.rootDir, '_posts');
    let mediumImagesFound = false;
    const mediumPatterns = [
      /https:\/\/miro\.medium\.com/,
      /https:\/\/cdn-images.*\.medium\.com/
    ];

    if (fs.existsSync(postsDir)) {
      const posts = fs.readdirSync(postsDir);
      posts.forEach(post => {
        if (post.endsWith('.md') || post.endsWith('.markdown')) {
          const content = fs.readFileSync(path.join(postsDir, post), 'utf8');
          mediumPatterns.forEach(pattern => {
            if (pattern.test(content)) {
              mediumImagesFound = true;
            }
          });
        }
      });
    }

    this.addResult(
      'No External Medium Images',
      !mediumImagesFound,
      mediumImagesFound ? 'Medium-hosted images still found in posts' : 'All images are self-hosted'
    );
  }

  // Test 5: Check if performance monitoring is added
  testPerformanceMonitoring() {
    const customHeadFile = path.join(this.rootDir, '_includes/custom-head.html');
    
    if (!fs.existsSync(customHeadFile)) {
      this.addResult('Performance Monitoring', false, 'Custom head file not found');
      return;
    }

    const content = fs.readFileSync(customHeadFile, 'utf8');
    const hasPerformanceMark = content.includes('performance.mark');
    const hasDOMLoadedMark = content.includes('dom-loaded');
    const hasPageLoadedMark = content.includes('page-loaded');
    
    const isImplemented = hasPerformanceMark && hasDOMLoadedMark && hasPageLoadedMark;

    this.addResult(
      'Performance Monitoring',
      isImplemented,
      isImplemented ? 'Performance marks properly implemented' : 'Performance monitoring not fully implemented'
    );
  }

  // Test 6: Check if optimized images exist
  testOptimizedImages() {
    const optimizedImagesDir = path.join(this.rootDir, 'assets/images/posts');
    
    if (!fs.existsSync(optimizedImagesDir)) {
      this.addResult('Optimized Images Directory', false, 'Optimized images directory not found');
      return;
    }

    const images = fs.readdirSync(optimizedImagesDir);
    const hasImages = images.length > 0;
    
    if (hasImages) {
      // Check if Manila post images are present
      const hasManilaImages = images.includes('manila-night.jpeg') && images.includes('boracay-beach.jpeg');
      this.addResult(
        'Optimized Images',
        hasManilaImages,
        hasManilaImages ? 'Optimized images present in assets/images/posts' : 'Expected images not found'
      );
    } else {
      this.addResult('Optimized Images', false, 'No images found in optimization directory');
    }
  }

  // Test 7: Check preconnect and dns-prefetch optimizations
  testResourceHints() {
    const customHeadFile = path.join(this.rootDir, '_includes/custom-head.html');
    
    if (!fs.existsSync(customHeadFile)) {
      this.addResult('Resource Hints', false, 'Custom head file not found');
      return;
    }

    const content = fs.readFileSync(customHeadFile, 'utf8');
    const hasGooglePreconnect = content.includes('preconnect') && content.includes('google-analytics');
    const hasDnsPrefetch = content.includes('dns-prefetch');
    
    const isImplemented = hasGooglePreconnect && hasDnsPrefetch;

    this.addResult(
      'Resource Hints',
      isImplemented,
      isImplemented ? 'Preconnect and DNS prefetch properly configured' : 'Resource hints not fully implemented'
    );
  }

  // Run all tests
  run() {
    console.log('\n' + colors.yellow + '=== Running Performance Tests ===' + colors.reset + '\n');
    
    this.testFacebookPixelRemoved();
    this.testTalkyardLazyLoading();
    this.testLazyImageComponent();
    this.testNoMediumImages();
    this.testPerformanceMonitoring();
    this.testOptimizedImages();
    this.testResourceHints();
    
    // Summary
    const passed = this.testResults.filter(r => r.passed).length;
    const total = this.testResults.length;
    
    console.log('\n' + colors.yellow + '=== Test Summary ===' + colors.reset);
    console.log(`Total: ${total} | Passed: ${colors.green}${passed}${colors.reset} | Failed: ${colors.red}${total - passed}${colors.reset}\n`);
    
    // Exit with appropriate code
    process.exit(passed === total ? 0 : 1);
  }
}

// Run tests
const tester = new PerformanceTests();
tester.run();