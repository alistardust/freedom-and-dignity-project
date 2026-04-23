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
    const isAiPage = pageName === 'about-ai';
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
  if (pillarGrid && window.ARP) {
    const filterBar = document.getElementById('pillar-filters');

    /* Build filter buttons */
    const allBtn = makeBtn('all', 'All Pillars', null);
    allBtn.classList.add('active');
    filterBar.appendChild(allBtn);
    ARP.foundations.forEach(f => filterBar.appendChild(makeBtn(f.id, f.title, f.color)));

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
      const list = filterId === 'all' ? ARP.pillars : ARP.pillars.filter(p => p.foundation === filterId);
      pillarGrid.innerHTML = '';
      list.forEach(p => {
        const f = ARP.getFoundation(p.foundation);
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

  /* ── WIP / PRE-1.0 BANNER ───────────────────────────── */
  (function () {
    if (document.getElementById('wip-banner')) return;
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
      ' &nbsp;<a href="' + _base + 'roadmap.html">View Roadmap →</a>';
    nav.insertAdjacentElement('afterend', banner);
  })();

  /* ── DYNAMIC COUNTS ─────────────────────────────────── */
  // Fills [data-dynamic] elements from live ARP data and DOM.
  // Usage: <span data-dynamic="pillar-count">23</span>  ← fallback shown if JS disabled
  (function () {
    if (!window.ARP) return;
    const pillarCount     = ARP.pillars.length;
    const foundationCount = ARP.foundations.length;
    const ruleCount       = document.querySelectorAll('.rule-card').length;
    const families        = new Set();
    document.querySelectorAll('.rule-card[id]').forEach(card => {
      const m = card.id.match(/^([A-Z]+-[A-Z]+)/);
      if (m) families.add(m[1]);
    });
    const familyCount = families.size;
    document.querySelectorAll('[data-dynamic]').forEach(el => {
      switch (el.dataset.dynamic) {
        case 'pillar-count':     el.textContent = pillarCount;                   break;
        case 'foundation-count': el.textContent = foundationCount;               break;
        case 'rule-count':       if (ruleCount)   el.textContent = ruleCount;    break;
        case 'family-count':     if (familyCount) el.textContent = familyCount;  break;
      }
    });
  })();

})();
