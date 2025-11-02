# Accessibility Checklist for bankole.org

Quick reference guide for maintaining and improving accessibility on the blog.

## Before Publishing New Content

### Images
- [ ] All meaningful images have descriptive alt text
  - Describe the content and function, not just "image"
  - Example: "Screenshot of GitHub pull request diff showing line-by-line changes" ✅
  - NOT: "Screenshot" ❌
- [ ] Decorative images use empty alt text: `alt=""`
- [ ] Complex images (charts, diagrams) have extended descriptions in surrounding text
- [ ] Alt text is concise (typically 125 characters or less)
- [ ] Alt text doesn't start with "image of" or "picture of"

### Links
- [ ] All links have descriptive text (no "click here" or "read more" alone)
  - Example: "Read my article on accessibility in web design" ✅
  - NOT: "Click here" ❌
- [ ] Links that open in new windows have title attribute: `title="Opens in new window"`
- [ ] External links use `rel="noopener noreferrer"` for security

### Headings
- [ ] Use proper heading hierarchy (h1 → h2 → h3, not h1 → h3)
- [ ] Don't skip heading levels
- [ ] Each page has only one h1
- [ ] Headings describe content that follows

### Forms (if adding new ones)
- [ ] All form inputs have associated `<label>` elements
- [ ] Labels use `for` attribute matching input `id`
- [ ] Required fields marked with `required` attribute AND `aria-required="true"`
- [ ] Error messages are associated with fields using `aria-describedby`
- [ ] Form inputs have sufficient size (at least 16px font)

### Videos
- [ ] YouTube embeds include title parameter for accessibility
  ```liquid
  {% include youtube.html
    youtube_id="VIDEO_ID"
    title="Descriptive title of video"
  %}
  ```

## Testing Before Commit

### Keyboard Navigation
1. Open the post/page in a browser
2. Press `Tab` repeatedly to navigate through all elements
3. Press `Shift+Tab` to navigate backward
4. Verify:
   - [ ] Focus indicator is always visible (purple outline)
   - [ ] Focus order is logical (left-to-right, top-to-bottom)
   - [ ] No keyboard traps (you can Tab out of every element)
   - [ ] All interactive elements are reachable

### Links and Buttons
- [ ] Press `Enter` on focused link navigates to URL
- [ ] Press `Enter` or `Space` on focused button activates it
- [ ] Link text is descriptive without context

### Forms
- [ ] Tab moves focus to next form field
- [ ] Shift+Tab moves focus to previous form field
- [ ] Submit button is reachable via Tab
- [ ] Required field validation works via keyboard

## Lighthouse Accessibility Audit

### How to Run in Chrome DevTools:
1. Open Chrome DevTools (F12 or Cmd+Option+I)
2. Click "Lighthouse" tab
3. Select "Accessibility"
4. Click "Analyze page load"
5. Review the report

### Target Score: 90+

Current areas to maintain:
- [ ] Color contrast is sufficient (9.2:1 for purple)
- [ ] Images have alt text
- [ ] Form fields are labeled
- [ ] Heading hierarchy is proper
- [ ] All buttons and links are keyboard accessible

## Common Issues to Avoid

### Don't:
❌ Use color alone to convey information
❌ Set focus outline to "none" without replacement
❌ Use `<div>` instead of semantic HTML (`<button>`, `<nav>`, `<section>`)
❌ Have images without alt text
❌ Create keyboard traps (focus stuck in an element)
❌ Use very small text without sufficient sizing
❌ Disable zoom or set `user-scalable=no`
❌ Rely on hover states without focus states
❌ Embed large text as images

### Do:
✅ Provide alternative text for images
✅ Use semantic HTML elements
✅ Ensure keyboard access to all interactive elements
✅ Maintain visible focus indicators
✅ Use sufficient color contrast
✅ Test with actual screen readers
✅ Include form labels and error messages
✅ Use descriptive link text
✅ Test on actual devices and browsers

## Post Template Accessibility Checklist

Use this when creating a new post:

```markdown
---
layout: post
title: "Your Post Title"
date: YYYY-MM-DD
---

<!--
  Accessibility Checklist:
  [ ] All images have descriptive alt text
  [ ] Links have descriptive text (no "click here")
  [ ] Heading hierarchy is correct (h1 → h2 → h3)
  [ ] No heading levels are skipped
  [ ] All code examples are properly formatted
  [ ] Videos have title parameter if using YouTube embed
  [ ] Color contrast is sufficient
  [ ] No content conveyed by color alone
-->

Your post content here...
```

## Form Accessibility Best Practices

When adding forms, ensure:

```html
<!-- Good Form Markup -->
<form aria-label="Contact form">
  <fieldset>
    <legend>Contact Information</legend>

    <div>
      <label for="name">Name:</label>
      <input
        id="name"
        name="name"
        type="text"
        required
        aria-required="true"
      />
    </div>

    <div>
      <label for="email">Email:</label>
      <input
        id="email"
        name="email"
        type="email"
        required
        aria-required="true"
      />
    </div>

    <button type="submit">Submit</button>
  </fieldset>
</form>
```

## Image Alt Text Examples

### Good Alt Text:
✅ "Portrait of Margaret Mead, anthropologist, in profile facing left"
✅ "Graph showing blog traffic increase from January to December 2023"
✅ "Screenshot of GitHuib pull request merge button"
✅ "Aerial view of Manhattan skyline at sunset with Hudson River"

### Poor Alt Text:
❌ "Photo"
❌ "Image 1"
❌ "Logo" (what product/company?)
❌ "Chart" (of what?)
❌ "Picture of something"

## Useful Resources

- [WCAG 2.1 Quick Reference](https://www.w3.org/WAI/WCAG21/quickref/)
- [WebAIM: Web Accessibility in Mind](https://webaim.org/)
- [A11y Project Checklist](https://www.a11yproject.com/checklist/)
- [MDN: Accessibility](https://developer.mozilla.org/en-US/docs/Web/Accessibility)
- [Color Contrast Checker](https://webaim.org/resources/contrastchecker/)

## Tools for Testing

- **Chrome DevTools:** Lighthouse Accessibility
- **Color Contrast:** WebAIM Contrast Checker
- **Screen Readers:**
  - macOS/iOS: VoiceOver (built-in)
  - Windows: NVDA (free) or JAWS
  - Linux: Orca
- **Automated Testing:** axe DevTools, WAVE, Lighthouse CI

## Questions?

For accessibility-related questions, refer to:
- `/Users/bankole/Documents/Coding_Projects/brm444.github.io/ACCESSIBILITY_IMPROVEMENTS.md` - Detailed improvement documentation
- Comments in individual component files (e.g., `_layouts/post.html`)
- Component documentation in `_includes/*.html` files

---

**Last Updated:** November 2024
**WCAG Target:** 2.1 Level AA
