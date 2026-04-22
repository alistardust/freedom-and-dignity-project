/* American Renewal Project — app.js */
(function () {
  'use strict';

  /* ── NAME NOTICE BANNER ───────────────────────────── */
  (function () {
    if (sessionStorage.getItem('name-notice-dismissed')) return;
    const banner = document.createElement('div');
    banner.className = 'name-notice-banner';
    banner.innerHTML =
      '<div class="name-notice-inner">' +
        '<span class="name-notice-icon">⚠</span>' +
        '<span class="name-notice-text"><strong>Name Notice:</strong> ' +
        'It has come to our attention that the name \u201cAmerican Renewal Project\u201d is already in use by ' +
        'an existing organization with which this project has no affiliation, connection, or shared ideology. ' +
        'The current name of this project is a <strong>placeholder</strong> while a permanent name is selected. ' +
        'We apologize for any confusion.</span>' +
        '<button class="name-notice-dismiss" aria-label="Dismiss notice">\u00d7</button>' +
      '</div>';
    const nav = document.querySelector('.site-nav') || document.body.firstElementChild;
    document.body.insertBefore(banner, nav);
    banner.querySelector('.name-notice-dismiss').addEventListener('click', function () {
      banner.remove();
      sessionStorage.setItem('name-notice-dismissed', '1');
    });
  })();


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
    const aiHref = base + 'about-ai.html';
    const missionHref = base + 'mission.html';
    const constitutionHref = base + 'constitution.html';
    const isAiPage = pageName === 'about-ai';
    const isMissionPage = pageName === 'mission';
    const isConstitutionPage = pageName === 'constitution';

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

    if (navList && !navList.querySelector('a[href*="about-ai"]')) {
      const li = document.createElement('li');
      li.innerHTML = `<a href="${aiHref}"${isAiPage ? ' class="active"' : ''}>About AI</a>`;
      navList.appendChild(li);
    }

    // Inject Mission, Constitution, and About AI into footer-links
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
})();
