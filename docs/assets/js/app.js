/* Freedom and Dignity Project — app.js */
(function () {
  'use strict';


  (function () {
    const page = location.pathname.split('/').pop() || 'index.html';
    // Normalize: strip .html for comparison (serve redirects clean URLs, so
    // /about-ai.html becomes /about-ai, making page = 'about-ai' not 'about-ai.html')
    const pageName = page.replace(/\.html$/, '') || 'index';
    document.querySelectorAll('.nav-links a').forEach(a => {
      const href = a.getAttribute('href');
      const hrefName = href ? href.replace(/\.html$/, '').replace(/^\.\.\//, '') : '';
      if (hrefName === pageName || (pageName === 'index' && href === 'index.html')) {
        a.classList.add('active');
      }
    });

    // Inject nav links (path-aware for subdirectories)
    const navList = document.querySelector('ul.nav-links');
    // Check for actual subdirectory pages (pillars/, compare/) not just path depth.
    // Depth-counting breaks on GitHub Pages because the repo base path adds a segment.
    const inSubdir = /\/(pillars|compare)\//.test(location.pathname);
    const base = inSubdir ? '../' : '';
    const aboutUsHref = base + 'about-us.html';
    const aiHref = base + 'about-ai.html';
    const missionHref = base + 'mission.html';
    const constitutionHref = base + 'constitution.html';
    const classificationHref = base + 'classification.html';
    const getInvolvedHref = base + 'get-involved.html';
    const roadmapHref    = base + 'roadmap.html';
    const letterHref     = base + 'letter-from-the-founder.html';
    const isAiPage = pageName === 'about-ai';
    const isLetterPage = pageName === 'letter-from-the-founder';
    const isRoadmapPage = pageName === 'roadmap';
    const isMissionPage = pageName === 'mission';
    const isConstitutionPage = pageName === 'constitution';
    const isAboutUsPage = pageName === 'about-us';
    const isClassificationPage = pageName === 'classification';
    const isGetInvolvedPage = pageName === 'get-involved';

    if (navList && !navList.querySelector('a[href*="mission"]')) {
      const li = document.createElement('li');
      li.innerHTML = `<a href="${missionHref}"${isMissionPage ? ' class="active"' : ''}>Mission</a>`;
      navList.appendChild(li);
    }

    if (navList && !navList.querySelector('a[href*="constitution"]')) {
      const li = document.createElement('li');
      li.innerHTML = `<a href="${constitutionHref}"${isConstitutionPage ? ' class="active"' : ''}>Constitution</a>`;
      navList.appendChild(li);
    }

    if (navList && !navList.querySelector('a[href*="classification"]')) {
      const li = document.createElement('li');
      li.innerHTML = `<a href="${classificationHref}"${isClassificationPage ? ' class="active"' : ''}>Classification</a>`;
      navList.appendChild(li);
    }

    if (navList && !navList.querySelector('a[href*="about-us"]')) {
      const li = document.createElement('li');
      li.innerHTML = `<a href="${aboutUsHref}"${isAboutUsPage ? ' class="active"' : ''}>About Us</a>`;
      navList.appendChild(li);
    }

    if (navList && !navList.querySelector('a[href*="letter-from-the-founder"]')) {
      const li = document.createElement('li');
      li.innerHTML = `<a href="${letterHref}"${isLetterPage ? ' class="active"' : ''}>Letter from the Founder</a>`;
      navList.appendChild(li);
    }

    if (navList && !navList.querySelector('a[href*="get-involved"]')) {
      const li = document.createElement('li');
      li.innerHTML = `<a href="${getInvolvedHref}"${isGetInvolvedPage ? ' class="active"' : ''}>Get Involved</a>`;
      navList.appendChild(li);
    }

    if (navList && !navList.querySelector('a[href*="roadmap"]')) {
      const li = document.createElement('li');
      li.innerHTML = `<a href="${roadmapHref}"${isRoadmapPage ? ' class="active"' : ''}>Roadmap</a>`;
      navList.appendChild(li);
    }

    if (navList && !navList.querySelector('a[href*="about-ai"]')) {
      const li = document.createElement('li');
      li.innerHTML = `<a href="${aiHref}"${isAiPage ? ' class="active"' : ''}>About AI</a>`;
      navList.appendChild(li);
    }

    // Inject Mission, Constitution, Classification, About Us, and About AI into footer-links
    const footerLinks = document.querySelector('ul.footer-links');
    if (footerLinks && !footerLinks.querySelector('a[href*="mission"]')) {
      const fli = document.createElement('li');
      fli.innerHTML = `<a href="${missionHref}">Mission</a>`;
      footerLinks.appendChild(fli);
    }
    if (footerLinks && !footerLinks.querySelector('a[href*="constitution"]')) {
      const fli = document.createElement('li');
      fli.innerHTML = `<a href="${constitutionHref}">Constitution</a>`;
      footerLinks.appendChild(fli);
    }
    if (footerLinks && !footerLinks.querySelector('a[href*="classification"]')) {
      const fli = document.createElement('li');
      fli.innerHTML = `<a href="${classificationHref}">Classification</a>`;
      footerLinks.appendChild(fli);
    }
    if (footerLinks && !footerLinks.querySelector('a[href*="about-us"]')) {
      const fli = document.createElement('li');
      fli.innerHTML = `<a href="${aboutUsHref}">About Us</a>`;
      footerLinks.appendChild(fli);
    }
    if (footerLinks && !footerLinks.querySelector('a[href*="letter-from-the-founder"]')) {
      const fli = document.createElement('li');
      fli.innerHTML = `<a href="${letterHref}">Letter from the Founder</a>`;
      footerLinks.appendChild(fli);
    }
    if (footerLinks && !footerLinks.querySelector('a[href*="get-involved"]')) {
      const fli = document.createElement('li');
      fli.innerHTML = `<a href="${getInvolvedHref}">Get Involved</a>`;
      footerLinks.appendChild(fli);
    }
    if (footerLinks && !footerLinks.querySelector('a[href*="roadmap"]')) {
      const fli = document.createElement('li');
      fli.innerHTML = `<a href="${roadmapHref}">Roadmap</a>`;
      footerLinks.appendChild(fli);
    }
    if (footerLinks && !footerLinks.querySelector('a[href*="about-ai"]')) {
      const fli = document.createElement('li');
      fli.innerHTML = `<a href="${aiHref}">About AI</a>`;
      footerLinks.appendChild(fli);
    }
  })();

  /* ── HAMBURGER ────────────────────────────────────── */
  const burger = document.querySelector('.nav-hamburger');
  const navList = document.querySelector('.nav-links');
  if (burger && navList) {
    burger.addEventListener('click', () => navList.classList.toggle('open'));
    document.addEventListener('click', e => {
      if (!burger.contains(e.target) && !navList.contains(e.target)) navList.classList.remove('open');
    });
  }

  /* ── PILLAR FILTER + RENDER ───────────────────────── */
  const pillarGrid = document.getElementById('pillar-grid');
  if (pillarGrid && window.siteData) {
    const filterBar = document.getElementById('pillar-filters');

    /* Build filter buttons */
    const allBtn = makeBtn('all', 'All Pillars', null);
    allBtn.classList.add('active');
    filterBar.appendChild(allBtn);
    siteData.foundations.forEach(f => filterBar.appendChild(makeBtn(f.id, f.title, f.color)));

    /* Render all cards initially */
    renderPillars('all');

    function makeBtn(id, label, color) {
      const btn = document.createElement('button');
      btn.className = 'pillar-filter-btn';
      btn.dataset.filter = id;
      btn.textContent = label;
      if (color) btn.dataset.color = color;
      btn.addEventListener('click', () => {
        document.querySelectorAll('.pillar-filter-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        renderPillars(id);
      });
      return btn;
    }

    function renderPillars(filterId) {
      const list = filterId === 'all' ? siteData.pillars : siteData.pillars.filter(p => p.foundation === filterId);
      pillarGrid.innerHTML = '';
      list.forEach(p => {
        const f = siteData.getFoundation(p.foundation);
        const card = document.createElement('article');
        card.className = 'pillar-card';
        card.style.borderTopColor = f ? f.color : 'var(--red)';
        card.innerHTML = `
          <div class="pc-foundation" style="color:${f ? f.color : 'var(--gold)'};">${f ? f.title : ''}</div>
          <div class="pc-title">${p.title.replace(/_/g,' ')}</div>
          <p class="pc-summary">${p.summary}</p>
          <ul class="pc-points">${p.points.map(pt => `<li>${pt}</li>`).join('')}</ul>`;
        pillarGrid.appendChild(card);
      });
    }
  }

  /* ── POLICY ENFORCEMENT HIGHLIGHT ───────────────── */
  // Wraps strong enforcement words in red-bold spans within policy content areas.
  (function () {
    const ENFORCE_RE = /\b(ban(s|ned|ning)?|prohibit(s|ed|ing|ion)?|restriction(s)?|restrict(s|ed|ing)?|mandate(s|d|ing)?|mandatory|criminalize[sd]?|criminalizing|abolish(es|ed|ing)?|outlaw(s|ed|ing)?)\b/gi;
    const SELECTORS = [
      '.rule-title', '.rule-stmt', '.rule-notes',
      '.ai-compare-table td', '.compare-table td',
      '.pillar-intro p', '.pi-desc', '.pi-summary',
      '.pillar-summary', '.section-intro p'
    ].join(', ');

    function highlightNode(el) {
      const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, null);
      const toReplace = [];
      let node;
      while ((node = walker.nextNode())) {
        if (ENFORCE_RE.test(node.nodeValue)) toReplace.push(node);
        ENFORCE_RE.lastIndex = 0;
      }
      toReplace.forEach(function (tn) {
        const frag = document.createDocumentFragment();
        let last = 0, m;
        ENFORCE_RE.lastIndex = 0;
        while ((m = ENFORCE_RE.exec(tn.nodeValue)) !== null) {
          if (m.index > last) frag.appendChild(document.createTextNode(tn.nodeValue.slice(last, m.index)));
          const span = document.createElement('span');
          span.className = 'policy-strong';
          span.textContent = m[0];
          frag.appendChild(span);
          last = m.index + m[0].length;
        }
        if (last < tn.nodeValue.length) frag.appendChild(document.createTextNode(tn.nodeValue.slice(last)));
        tn.parentNode.replaceChild(frag, tn);
      });
    }

    document.querySelectorAll(SELECTORS).forEach(highlightNode);
  })();

  /* ── BACK-TO-TOP BUTTON ──────────────────────────── */
  (function () {
    const btn = document.createElement('button');
    btn.id = 'back-to-top';
    btn.setAttribute('aria-label', 'Back to top');
    btn.innerHTML = '&#8679;';
    document.body.appendChild(btn);
    window.addEventListener('scroll', () => {
      btn.classList.toggle('btt-visible', window.scrollY > 400);
    }, { passive: true });
    btn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
  })();

  /* ── SMOOTH SECTION REVEAL ───────────────────────── */
  if ('IntersectionObserver' in window) {
    const obs = new IntersectionObserver(entries => {
      entries.forEach(e => {
        if (e.isIntersecting) { e.target.classList.add('visible'); obs.unobserve(e.target); }
      });
    // threshold: 0 fires as soon as any pixel of the section enters the viewport.
  // A higher threshold (e.g. 0.08) breaks for very tall sections (like #pil-policy)
  // because 8% of a 5000px section never fits in the viewport, keeping it invisible.
  }, { threshold: 0 });
    document.querySelectorAll('section').forEach(s => {
      s.style.opacity = '0';
      s.style.transform = 'translateY(18px)';
      s.style.transition = 'opacity .5s ease, transform .5s ease';
      obs.observe(s);
    });
    document.head.insertAdjacentHTML('beforeend', '<style>.visible{opacity:1!important;transform:none!important}</style>');
  }

  /* ── PILLAR SECTION SCROLLSPY ───────────────────────── */
  // Highlights the active section in the sticky pillar sub-nav.
  // Replaces the inline <script> block that was repeated in every pillar HTML file.
  (function () {
    const nav = document.getElementById('pil-snav');
    if (!nav) return;
    const links    = nav.querySelectorAll('a[href^="#"]');
    const sections = Array.from(links).map(a => document.querySelector(a.getAttribute('href'))).filter(Boolean);
    function onScroll() {
      const y      = window.scrollY + 120;
      let   active = sections[0];
      sections.forEach(s => { if (s.offsetTop <= y) active = s; });
      links.forEach(a => a.classList.toggle('active', a.getAttribute('href') === '#' + active.id));
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  })();

  /* ── WIP / PRE-1.0 BANNER ───────────────────────────── */
  (function () {
    if (document.getElementById('wip-banner')) return;
    if (sessionStorage.getItem('wip-banner-dismissed')) return;
    const nav = document.querySelector('.site-nav');
    if (!nav) return;
    const _base = /\/(pillars|compare)\//.test(location.pathname) ? '../' : '';
    const banner = document.createElement('div');
    banner.id = 'wip-banner';
    banner.className = 'wip-banner';
    banner.innerHTML =
      '<strong>Pre-1.0 — Work in Progress</strong> &nbsp;·&nbsp; ' +
      'This platform is a living document, intentionally updated as policy develops. ' +
      'We have not yet reached our 1.0 release — language, structure, and positions will evolve.' +
      ' &nbsp;<a href="' + _base + 'roadmap.html">View Roadmap →</a>' +
      '<button class="wip-banner-dismiss" aria-label="Dismiss banner">✕</button>';
    banner.querySelector('.wip-banner-dismiss').addEventListener('click', function () {
      sessionStorage.setItem('wip-banner-dismissed', '1');
      banner.remove();
    });
    nav.insertAdjacentElement('afterend', banner);
  })();

  /* ── DYNAMIC COUNTS ─────────────────────────────────── */
  // Fills [data-dynamic] elements from live siteData and DOM.
  // Usage: <span data-dynamic="pillar-count">23</span>  ← fallback shown if JS disabled
  (function () {
    if (!window.siteData) return;
    const pillarCount     = siteData.pillars.length;
    const foundationCount = siteData.foundations.length;
    const ruleCount       = document.querySelectorAll('.policy-card').length;
    const families        = new Set();
    document.querySelectorAll('.policy-card[id]').forEach(card => {
      const m = card.id.match(/^([A-Z]+-[A-Z]+)/);
      if (m) families.add(m[1]);
    });
    const familyCount = families.size;
    document.querySelectorAll('[data-dynamic]').forEach(el => {
      switch (el.dataset.dynamic) {
        case 'pillar-count':     el.textContent = pillarCount;                   break;
        case 'foundation-count': el.textContent = foundationCount;               break;
        case 'policy-count':       if (ruleCount)   el.textContent = ruleCount;    break;
        case 'family-count':     if (familyCount) el.textContent = familyCount;  break;
      }
    });
  })();

  /* ── POLICY CARD EXPAND / TRUNCATE ─────────────────── */
  (function () {
    document.querySelectorAll('.policy-card').forEach(function (card) {
      const bodies = card.querySelectorAll('.rule-body');
      if (!bodies.length) return;
      const lastBody = bodies[bodies.length - 1];

      // Enable truncation via CSS class, then measure clamping.
      card.classList.add('card-clamped-active');
      const isClamped = lastBody.scrollHeight > lastBody.clientHeight;

      if (!isClamped) {
        // Text fits within 4 lines — no toggle needed.
        card.classList.remove('card-clamped-active');
        return;
      }

      const toggle = document.createElement('button');
      toggle.className = 'card-expand-toggle';
      toggle.setAttribute('aria-expanded', 'false');
      toggle.textContent = 'Read more';
      lastBody.insertAdjacentElement('afterend', toggle);

      toggle.addEventListener('click', function (e) {
        e.stopPropagation();
        const expanded = card.classList.toggle('expanded');
        toggle.setAttribute('aria-expanded', String(expanded));
        toggle.textContent = expanded ? 'Show less' : 'Read more';
      });

      // Clicking anywhere on the card (except the toggle itself) also toggles.
      card.addEventListener('click', function (e) {
        if (e.target === toggle) return;
        const expanded = card.classList.toggle('expanded');
        toggle.setAttribute('aria-expanded', String(expanded));
        toggle.textContent = expanded ? 'Show less' : 'Read more';
      });
    });
  })();

  /* ── NAME / AFFILIATION NOTICE ─────────────────────── */
  (function () {
    if (sessionStorage.getItem('name-notice-dismissed')) return;
    if (document.querySelector('.name-notice-banner')) return;
    const wip = document.getElementById('wip-banner');
    const banner = document.createElement('div');
    banner.className = 'name-notice-banner';
    banner.style.cssText =
      'background:#1a2744;color:rgba(255,255,255,.82);font-family:"Libre Franklin",sans-serif;' +
      'font-size:.8rem;padding:.6rem 1.5rem;display:flex;align-items:center;gap:1rem;flex-wrap:wrap;' +
      'border-top:1px solid rgba(255,255,255,.1);position:relative;z-index:199;';
    banner.innerHTML =
      '<span><strong style="color:#c9952a">Note:</strong> "Freedom and Dignity Project" is a working-title ' +
      '<strong>placeholder</strong> — this platform has <strong>no affiliation</strong> with any political ' +
      'party, candidate, or organization.</span>' +
      '<button class="name-notice-dismiss" style="margin-left:auto;background:none;border:1px solid ' +
      'rgba(255,255,255,.3);color:rgba(255,255,255,.6);border-radius:3px;padding:.2rem .7rem;' +
      'cursor:pointer;font-size:.75rem;white-space:nowrap;">Dismiss</button>';
    banner.querySelector('.name-notice-dismiss').addEventListener('click', function () {
      sessionStorage.setItem('name-notice-dismissed', '1');
      banner.remove();
    });
    if (wip) {
      wip.insertAdjacentElement('afterend', banner);
    } else {
      const nav = document.querySelector('.site-nav');
      if (nav) nav.insertAdjacentElement('afterend', banner);
    }
  })();

  /* ── HOMEPAGE SECTION ACCORDIONS ────────────────────── */
  if (document.querySelector('.section-accordion')) {
    document.querySelectorAll('.section-accordion').forEach(function (details) {
      const summary = details.querySelector('summary');
      const content = details.querySelector('section');
      if (!content || !summary) return;

      // Start collapsed — JS controls visibility from here
      content.style.overflow = 'hidden';
      content.style.transition = 'max-height .4s ease';
      content.style.maxHeight = '0';

      summary.addEventListener('click', function (e) {
        e.preventDefault();

        if (details.open) {
          // Animate close: capture current height, then transition to 0
          content.style.maxHeight = content.scrollHeight + 'px';
          void content.offsetHeight; // force reflow
          content.style.maxHeight = '0';
          content.addEventListener('transitionend', function handler() {
            details.removeAttribute('open');
            content.removeEventListener('transitionend', handler);
          }, { once: true });
        } else {
          // Animate open: set open first so scrollHeight is measurable, then transition
          details.setAttribute('open', '');
          content.style.maxHeight = content.scrollHeight + 'px';
          content.addEventListener('transitionend', function handler() {
            content.style.maxHeight = 'none'; // allow dynamic resizing once fully open
            content.removeEventListener('transitionend', handler);
          }, { once: true });
        }
      });
    });
  }

  /* ── PILLARS INDEX ACCORDION ANIMATION ─────────────── */
  (function () {
    if (!document.querySelector('.pil-foundation-accordion')) return;
    document.querySelectorAll('.pil-foundation-accordion').forEach(function (details) {
      details.addEventListener('click', function (e) {
        if (!e.target.closest('summary')) return;
        e.preventDefault();
        if (details.open) {
          const grid = details.querySelector('.pil-pillar-grid');
          if (!grid) { details.removeAttribute('open'); return; }
          grid.classList.add('pil-grid-closing');
          grid.addEventListener('animationend', function () {
            grid.classList.remove('pil-grid-closing');
            details.removeAttribute('open');
          }, { once: true });
        } else {
          details.setAttribute('open', '');
        }
      });
    });
  })();

})();
