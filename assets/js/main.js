/* No build system, dependencies, analytics, or network requests at page load. */
(() => {
  'use strict';

  // Mobile navigation: native links continue to work without JavaScript.
  const menuButton = document.querySelector('.menu-toggle');
  const navigation = document.getElementById('site-navigation');
  function closeMenu() {
    menuButton?.setAttribute('aria-expanded', 'false');
    navigation?.classList.remove('open');
  }
  menuButton?.addEventListener('click', () => {
    const expanded = menuButton.getAttribute('aria-expanded') === 'true';
    menuButton.setAttribute('aria-expanded', String(!expanded));
    navigation.classList.toggle('open', !expanded);
  });
  navigation?.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menuButton?.getAttribute('aria-expanded') === 'true') {
      closeMenu();
      menuButton.focus();
    }
  });
  document.addEventListener('click', event => {
    if (!event.target.closest('.site-header')) closeMenu();
  });
  if ('IntersectionObserver' in window) {
    const links = Array.from(navigation?.querySelectorAll('a') || []);
    const visibleSections = new Set();
    const observer = new IntersectionObserver(entries => {
      for (const entry of entries) {
        if (entry.isIntersecting) visibleSections.add(entry.target.id);
        else visibleSections.delete(entry.target.id);
      }
      // At a section boundary, highlight the later section in document order.
      const current = links.slice().reverse().find(link => visibleSections.has(link.hash.slice(1)));
      links.forEach(link => {
        const active = link === current;
        link.classList.toggle('active', active);
        if (active) link.setAttribute('aria-current', 'location');
        else link.removeAttribute('aria-current');
      });
    }, { rootMargin: '-10% 0px -65% 0px', threshold: 0 });
    links.forEach(link => {
      const section = document.querySelector(link.hash);
      if (section) observer.observe(section);
    });
  }

  function setText(id, value) {
    const element = document.getElementById(id);
    if (element) element.textContent = value;
  }

  // Accessible gallery tabs with Arrow / Home / End navigation.
  const tabs = Array.from(document.querySelectorAll('.gallery-tabs [role="tab"]'));
  function activateTab(tab, focus = false) {
    tabs.forEach(item => {
      const selected = item === tab;
      item.setAttribute('aria-selected', String(selected));
      item.tabIndex = selected ? 0 : -1;
      const panel = document.getElementById(item.getAttribute('aria-controls'));
      if (panel) panel.hidden = !selected;
    });
    if (focus) tab.focus();
  }
  if (tabs.length) {
    activateTab(tabs[0]);
    tabs.forEach((tab, index) => {
      tab.addEventListener('click', () => activateTab(tab));
      tab.addEventListener('keydown', event => {
        let next;
        if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
        else if (event.key === 'ArrowLeft') next = (index - 1 + tabs.length) % tabs.length;
        else if (event.key === 'Home') next = 0;
        else if (event.key === 'End') next = tabs.length - 1;
        else return;
        event.preventDefault();
        activateTab(tabs[next], true);
      });
    });
  }

  // Native modal dialog supplies keyboard focus containment and Escape behavior.
  const dialog = document.getElementById('figure-dialog');
  const figureImage = document.getElementById('lightbox-image');
  let lightboxTrigger = null;
  if (dialog && typeof dialog.showModal === 'function') {
    document.querySelectorAll('[data-lightbox]').forEach(link => {
      link.addEventListener('click', event => {
        if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
        event.preventDefault();
        lightboxTrigger = link;
        const caption = link.dataset.caption || link.querySelector('img')?.alt || 'Research figure';
        dialog.dataset.plot = String(link.getAttribute("href").startsWith("assets/plots/"));
        figureImage.src = link.href;
        figureImage.alt = caption;
        setText('lightbox-caption', caption);
        document.getElementById('lightbox-original').href = link.href;
        dialog.showModal();
        document.body.classList.add('modal-open');
        document.getElementById('close-lightbox').focus();
      });
    });
    document.getElementById('close-lightbox')?.addEventListener('click', () => dialog.close());
    dialog.addEventListener('click', event => {
      if (event.target !== dialog) return;
      const box = dialog.getBoundingClientRect();
      if (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom) dialog.close();
    });
    dialog.addEventListener('close', () => {
      document.body.classList.remove('modal-open');
      lightboxTrigger?.focus({ preventScroll: true });
    });
  }

  // The video currently disables external embedding. The direct link is the default.
  // Set data-embed="true" in index.html after allowing embedding on YouTube.
  // With embedding enabled, load YouTube only after an explicit visitor action.
  const play = document.getElementById('play-demo');
  if (play?.dataset.embed === 'true') play.addEventListener('click', event => {
    if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    const frame = document.createElement('iframe');
    frame.src = 'https://www.youtube-nocookie.com/embed/NO25k2dfSFE?autoplay=1&rel=0';
    frame.title = 'No Cones, No Duals — NRSfM reconstruction demo';
    frame.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
    frame.allowFullscreen = true;
    frame.referrerPolicy = 'strict-origin-when-cross-origin';
    document.getElementById('video-frame').replaceChildren(frame);
    frame.focus();
  });

  // Copy with a fallback for local-file browsing or clipboard restrictions.
  const copyButton = document.getElementById('copy-citation');
  const bibtex = document.getElementById('bibtex');
  let copyTimer;
  copyButton?.addEventListener('click', async () => {
    const text = bibtex.textContent.trim();
    let success = false;
    try {
      if (navigator.clipboard?.writeText && window.isSecureContext) {
        await navigator.clipboard.writeText(text);
        success = true;
      }
    } catch (_) { /* Try the browser's selection-based copy next. */ }
    if (!success) {
      const range = document.createRange();
      range.selectNodeContents(bibtex);
      const selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
      try { success = document.execCommand('copy'); } catch (_) { success = false; }
      if (success) selection.removeAllRanges();
    }
    copyButton.querySelector('span').textContent = success ? 'Copied!' : 'Citation selected';
    setText('copy-status', success ? 'BibTeX copied to clipboard.' : 'Press Ctrl+C / ⌘C to copy the selected citation.');
    clearTimeout(copyTimer);
    copyTimer = setTimeout(() => {
      copyButton.querySelector('span').textContent = 'Copy citation';
      setText('copy-status', '');
    }, 5000);
  });
})();
