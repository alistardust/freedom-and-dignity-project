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
    const missionHref = base + 'problem.html';
    const rightsHref = base + 'rights.html';
    const classificationHref = base + 'classification.html';
    const getInvolvedHref = base + 'get-involved.html';
    const roadmapHref    = base + 'roadmap.html';
    const letterHref     = base + 'letter-from-the-founder.html';
    const isAiPage = pageName === 'about-ai';
    const isLetterPage = pageName === 'letter-from-the-founder';
    const isRoadmapPage = pageName === 'roadmap';
    const isMissionPage = pageName === 'mission';
    const isRightsPage = pageName === 'rights';
    const isAboutUsPage = pageName === 'about-us';
    const isClassificationPage = pageName === 'classification';
    const isGetInvolvedPage = pageName === 'get-involved';
    const approachHref = base + 'approach.html';
    const isApproachPage = pageName === 'approach';
    const policyLibraryHref = base + 'policy-library.html';
    const isPolicyLibraryPage = pageName === 'policy-library';
    const platformHref = base + 'platform.html';
    const isPlatformPage = pageName === 'platform';
    if (navList && !navList.querySelector('a[href*="mission"]')) {
      const li = document.createElement('li');
      li.innerHTML = `<a href="${missionHref}"${isMissionPage ? ' class="active"' : ''}>Problem</a>`;
      navList.appendChild(li);
    }

    if (navList && !navList.querySelector('a[href*="approach"]')) {
      const li = document.createElement('li');
      li.innerHTML = `<a href="${approachHref}"${isApproachPage ? ' class="active"' : ''}>Approach</a>`;
      navList.appendChild(li);
    }

    if (navList && !navList.querySelector('a[href*="policy-library"]')) {
      const li = document.createElement('li');
      li.innerHTML = `<a href="${policyLibraryHref}"${isPolicyLibraryPage ? ' class="active"' : ''}>Policy Library</a>`;
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

    // Inject links into footer-links
    const footerLinks = document.querySelector('ul.footer-links');
    if (footerLinks && !footerLinks.querySelector('a[href*="platform"]')) {
      const fli = document.createElement('li');
      fli.innerHTML = `<a href="${platformHref}">Platform</a>`;
      footerLinks.appendChild(fli);
    }
    if (footerLinks && !footerLinks.querySelector('a[href*="rights"]')) {
      const fli = document.createElement('li');
      fli.innerHTML = `<a href="${rightsHref}">Rights</a>`;
      footerLinks.appendChild(fli);
    }
    if (footerLinks && !footerLinks.querySelector('a[href*="policy-library"]')) {
      const fli = document.createElement('li');
      fli.innerHTML = `<a href="${policyLibraryHref}">Policy Library</a>`;
      footerLinks.appendChild(fli);
    }
    if (footerLinks && !footerLinks.querySelector('a[href*="mission"]')) {
      const fli = document.createElement('li');
      fli.innerHTML = `<a href="${missionHref}">Problem</a>`;
      footerLinks.appendChild(fli);
    }
    if (footerLinks && !footerLinks.querySelector('a[href*="approach"]')) {
      const fli = document.createElement('li');
      fli.innerHTML = `<a href="${approachHref}">Approach</a>`;
      footerLinks.appendChild(fli);
    }
    if (footerLinks && !footerLinks.querySelector('a[href*="rights"]')) {
      const fli = document.createElement('li');
      fli.innerHTML = `<a href="${rightsHref}">Rights</a>`;
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

  /* ── SKIP LINK ───────────────────────────────────── */
  (function () {
    const skip = document.createElement('a');
    skip.href = '#main-content';
    skip.className = 'skip-link sr-only focusable';
    skip.textContent = 'Skip to main content';
    document.body.insertAdjacentElement('afterbegin', skip);

    // Wire the skip target to the first <section> after the nav
    const firstSection = document.querySelector('section, [role="main"]');
    if (firstSection && !firstSection.id) {
      firstSection.id = 'main-content';
    } else if (firstSection && firstSection.id !== 'main-content') {
      firstSection.setAttribute('tabindex', '-1');
      const anchor = document.createElement('span');
      anchor.id = 'main-content';
      anchor.setAttribute('tabindex', '-1');
      anchor.setAttribute('aria-hidden', 'true');
      firstSection.insertAdjacentElement('beforebegin', anchor);
    }
  })();

  /* ── HAMBURGER SITE TREE ─────────────────────────── */
  (function () {
    const inSubdir = /\/(pillars|compare)\//.test(location.pathname);
    const base = inSubdir ? '../' : '';

    function buildTree() {
      const foundations = (window.siteData && siteData.foundations) ? siteData.foundations : [];
      const policyLibraryChildren = foundations.map(f => ({
        label: f.title,
        href: base + 'policy-library.html#' + f.id,
      }));
      const comparePages = [
        { label: 'Republican Party',                 href: base + 'compare/republican-party.html' },
        { label: 'Democratic Party',                 href: base + 'compare/democratic-party.html' },
        { label: 'Green Party',                      href: base + 'compare/green-party.html' },
        { label: 'Libertarian Party',                href: base + 'compare/libertarian-party.html' },
        { label: 'Working Families Party',           href: base + 'compare/working-families-party.html' },
        { label: 'Democratic Socialists of America', href: base + 'compare/dsa.html' },
      ];
      return [
        { label: 'Home',         href: base + 'index.html' },
        { label: 'The Problem',  href: base + 'problem.html' },
        { label: 'Our Approach', href: base + 'approach.html' },
        { label: 'The Platform', children: [
          { label: 'Rights',          href: base + 'rights.html' },
          { label: 'Policy Library',  href: base + 'policy-library.html', children: policyLibraryChildren },
          { label: 'Platform Overview', href: base + 'platform.html' },
        ]},
        { label: 'Get Involved', href: base + 'get-involved.html' },
        { label: 'Roadmap',      href: base + 'roadmap.html' },
        { label: 'About', children: [
          { label: 'About Us',                href: base + 'about-us.html' },
          { label: 'Letter from the Founder', href: base + 'letter-from-the-founder.html' },
          { label: 'On the Use of AI',        href: base + 'about-ai.html' },
        ]},
        { label: 'Compare Platforms', children: comparePages },
      ];
    }

    function makeTreeNode(item, level) {
      const li = document.createElement('li');
      li.className = 'st-node' + (item.children && item.children.length ? ' st-parent' : '');
      li.setAttribute('role', 'treeitem');
      li.setAttribute('aria-level', level);
      if (item.children && item.children.length) {
        li.setAttribute('aria-expanded', 'false');
        const btn = document.createElement('button');
        btn.className = 'st-toggle';
        btn.setAttribute('aria-label', 'Expand ' + item.label);
        const labelSpan = document.createElement('span');
        labelSpan.className = 'st-label';
        if (item.href) {
          const a = document.createElement('a');
          a.href = item.href;
          a.textContent = item.label;
          a.className = 'st-item-link';
          labelSpan.appendChild(a);
        } else {
          labelSpan.textContent = item.label;
        }
        const chevron = document.createElement('span');
        chevron.className = 'st-chevron';
        chevron.setAttribute('aria-hidden', 'true');
        chevron.textContent = '›';
        btn.appendChild(labelSpan);
        btn.appendChild(chevron);
        li.appendChild(btn);
        const ul = document.createElement('ul');
        ul.className = 'st-children';
        ul.setAttribute('role', 'group');
        item.children.forEach(child => ul.appendChild(makeTreeNode(child, level + 1)));
        li.appendChild(ul);
        btn.addEventListener('click', function (e) {
          e.stopPropagation();
          const expanded = li.getAttribute('aria-expanded') === 'true';
          li.setAttribute('aria-expanded', String(!expanded));
          btn.setAttribute('aria-label', (expanded ? 'Expand ' : 'Collapse ') + item.label);
        });
      } else {
        const a = document.createElement('a');
        a.href = item.href;
        a.className = 'st-item-link st-leaf';
        a.textContent = item.label;
        a.setAttribute('role', 'treeitem');
        a.setAttribute('aria-level', String(level));
        a.addEventListener('click', closeTree);
        li.setAttribute('role', 'none');
        li.appendChild(a);
      }
      return li;
    }

    function closeTree() {
      const panel = document.querySelector('.site-tree');
      const burger = document.querySelector('.nav-hamburger');
      if (panel) panel.classList.remove('st-open');
      if (burger) {
        burger.setAttribute('aria-expanded', 'false');
        burger.setAttribute('aria-label', 'Open site menu');
      }
    }

    function buildPanel() {
      const nav = document.querySelector('.site-nav');
      if (!nav) return;
      const panel = document.createElement('nav');
      panel.id = 'site-tree';
      panel.className = 'site-tree';
      panel.setAttribute('aria-label', 'Site navigation tree');
      const header = document.createElement('div');
      header.className = 'st-header';
      const closeBtn = document.createElement('button');
      closeBtn.className = 'st-close';
      closeBtn.setAttribute('aria-label', 'Close site menu');
      closeBtn.textContent = '✕';
      closeBtn.addEventListener('click', closeTree);
      header.appendChild(closeBtn);
      panel.appendChild(header);
      const ul = document.createElement('ul');
      ul.className = 'st-root';
      ul.setAttribute('role', 'tree');
      buildTree().forEach(item => ul.appendChild(makeTreeNode(item, 1)));
      panel.appendChild(ul);
      const overlay = document.createElement('div');
      overlay.className = 'st-overlay';
      overlay.addEventListener('click', closeTree);
      document.body.appendChild(overlay);
      nav.insertAdjacentElement('afterend', panel);
    }

    buildPanel();

    const burger = document.querySelector('.nav-hamburger');
    if (burger) {
      burger.setAttribute('aria-expanded', 'false');
      burger.setAttribute('aria-controls', 'site-tree');
      burger.addEventListener('click', function () {
        const panel = document.querySelector('.site-tree');
        const open = panel && panel.classList.toggle('st-open');
        burger.setAttribute('aria-expanded', open ? 'true' : 'false');
        burger.setAttribute('aria-label', open ? 'Close site menu' : 'Open site menu');
        if (open) {
          const firstLink = panel.querySelector('.st-item-link, .st-toggle');
          if (firstLink) firstLink.focus();
        }
      });
    }

    document.addEventListener('keydown', function (e) {
      const panel = document.querySelector('.site-tree.st-open');
      if (!panel) return;
      if (e.key === 'Escape') { closeTree(); burger && burger.focus(); return; }
      const focusable = Array.from(panel.querySelectorAll('.st-item-link, .st-toggle'));
      const idx = focusable.indexOf(document.activeElement);
      if (e.key === 'ArrowDown') { e.preventDefault(); focusable[(idx + 1) % focusable.length].focus(); }
      if (e.key === 'ArrowUp')   { e.preventDefault(); focusable[(idx - 1 + focusable.length) % focusable.length].focus(); }
    });

    document.addEventListener('click', function (e) {
      const panel = document.querySelector('.site-tree.st-open');
      if (!panel) return;
      if (!panel.contains(e.target) && e.target !== burger) closeTree();
    });
  })();

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
