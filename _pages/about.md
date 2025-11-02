---
layout: post
title: "About"
permalink: /about/
---

I have worked in startups, management consulting, and Private Equity. For my day job, I work as a Product Manager in FB's Seattle office.

<nav class="social-links-nav" aria-label="Social media links">
  <a class="social-link" target="_blank" rel="noopener noreferrer" aria-label="Visit my Twitter profile" href="https://twitter.com/zeroplustwo_" title="Twitter profile">
    <svg class="niftybutton-twitter" data-tag="twi" data-name="Twitter" viewBox="0 0 512 512" preserveAspectRatio="xMidYMid meet">
      <path d="M419.6 168.6c-11.7 5.2-24.2 8.7-37.4 10.2 13.4-8.1 23.8-20.8 28.6-36 -12.6 7.5-26.5 12.9-41.3 15.8 -11.9-12.6-28.8-20.6-47.5-20.6 -42 0-72.9 39.2-63.4 79.9 -54.1-2.7-102.1-28.6-134.2-68 -17 29.2-8.8 67.5 20.1 86.9 -10.7-0.3-20.7-3.3-29.5-8.1 -0.7 30.2 20.9 58.4 52.2 64.6 -9.2 2.5-19.2 3.1-29.4 1.1 8.3 25.9 32.3 44.7 60.8 45.2 -27.4 21.4-61.8 31-96.4 27 28.8 18.5 63 29.2 99.8 29.2 120.8 0 189.1-102.1 185-193.6C399.9 193.1 410.9 181.7 419.6 168.6z" />
    </svg>
  </a>
  <a class="social-link" target="_blank" rel="noopener noreferrer" aria-label="Visit my LinkedIn profile" href="https://www.linkedin.com/in/bmakanju/" title="LinkedIn profile">
    <svg class="niftybutton-linkedin" data-tag="lin" data-name="LinkedIn" viewBox="0 0 512 512" preserveAspectRatio="xMidYMid meet">
      <path d="M186.4 142.4c0 19-15.3 34.5-34.2 34.5 -18.9 0-34.2-15.4-34.2-34.5 0-19 15.3-34.5 34.2-34.5C171.1 107.9 186.4 123.4 186.4 142.4zM181.4 201.3h-57.8V388.1h57.8V201.3zM273.8 201.3h-55.4V388.1h55.4c0 0 0-69.3 0-98 0-26.3 12.1-41.9 35.2-41.9 21.3 0 31.5 15 31.5 41.9 0 26.9 0 98 0 98h57.5c0 0 0-68.2 0-118.3 0-50-28.3-74.2-68-74.2 -39.6 0-56.3 30.9-56.3 30.9v-25.2H273.8z" />
    </svg>
  </a>
</nav>

&nbsp;

<form
  class="contact-form"
  action="https://formspree.io/mgezoeeg"
  method="POST"
  id="contact-form"
  novalidate
  aria-label="Contact form"
>
  <!-- Honeypot field for spam protection -->
  <div class="honeypot-field">
    <input type="text" name="website_url" tabindex="-1" autocomplete="off" aria-hidden="true" />
  </div>

  <fieldset class="contact-fieldset">
    <legend class="contact-legend">Get in touch with me</legend>

    <div class="form-group">
      <label for="contact-name" class="form-label">Name:</label>
      <input
        class="form-input"
        type="text"
        id="contact-name"
        name="name"
        required
        aria-required="true"
        aria-describedby="name-error"
      />
      <small class="form-help-text">Your full name is required</small>
    </div>

    <div class="form-group">
      <label for="contact-email" class="form-label">Email:</label>
      <input
        class="form-input"
        type="email"
        id="contact-email"
        name="_replyto"
        required
        aria-required="true"
        aria-describedby="email-error"
      />
      <small class="form-help-text">So I can respond to your message</small>
    </div>

    <div class="form-group">
      <label for="contact-message" class="form-label">Message:</label>
      <textarea
        class="form-textarea"
        id="contact-message"
        name="message"
        rows="5"
        required
        aria-required="true"
        aria-describedby="message-error"
      ></textarea>
      <small class="form-help-text">Please share your thoughts (at least 5 characters)</small>
    </div>

    <button
      class="form-button"
      type="submit"
      aria-label="Send contact form"
    >
      Send
    </button>
  </fieldset>
  <input type="hidden" value="/thanks/" name="_next" />
  <input type="hidden" name="_captcha" value="false" />
</form>

<script>
(function() {
  'use strict';
  var form = document.getElementById('contact-form');
  if (!form) return;

  // Honeypot validation
  var honeypot = form.querySelector('input[name="website_url"]');

  form.addEventListener('submit', function(e) {
    // Validate honeypot field (should be empty)
    if (honeypot && honeypot.value.trim() !== '') {
      console.warn('Spam detection: honeypot field filled');
      e.preventDefault();
      alert('Form submission failed. Please try again.');
      return false;
    }

    // Basic form validation
    var name = form.querySelector('input[name="name"]').value.trim();
    var email = form.querySelector('input[name="_replyto"]').value.trim();
    var message = form.querySelector('textarea[name="message"]').value.trim();

    // Validate name
    if (name.length === 0) {
      e.preventDefault();
      alert('Please enter your name.');
      return false;
    }

    // Validate email format
    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      e.preventDefault();
      alert('Please enter a valid email address.');
      return false;
    }

    // Validate message length
    if (message.length < 5) {
      e.preventDefault();
      alert('Please enter a message with at least 5 characters.');
      return false;
    }

    // Prevent excessive URLs in message (common spam indicator)
    var urlCount = (message.match(/https?:\/\//g) || []).length;
    if (urlCount > 2) {
      e.preventDefault();
      alert('Your message contains too many links. Please reduce the number of URLs.');
      return false;
    }

    // All validations passed
    return true;
  });
})();
</script>

<br>&nbsp;

*This is a personal blog. Any views or opinions represented in this blog are mine and mine only. They do not represent those of people, institutions or organizations that I may or may not be associated with in professional or personal capacity, unless explicitly stated. Any views or opinions are not intended to malign any religion, ethnic group, club, organization, company, or individual.*
