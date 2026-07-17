// BPSC 72nd Prelims — Shared Navigation Bar Injector
// Automatically injects a consistent nav bar into every topic page and subpage.

(function() {
  'use strict';

  // Detect if we're in a subpage (subpages/ folder) or main page (Topics/ folder)
  var isSubpage = window.location.pathname.includes('/subpages/');
  var prefix = isSubpage ? '../' : '';

  // Topic groups for dropdown menus
  var groups = {
    'Current Affairs': { range: [1, 14], icon: '📰' },
    'Bihar Current Affairs': { range: [15, 23], icon: '🔶' },
    'Modern Indian History': { range: [24, 37], icon: '📜' },
    'Indian Polity': { range: [38, 49], icon: '⚖️' },
    'Maths & Mental Ability': { range: [50, 59], icon: '🔢' },
    'Static GK': { range: [60, 68], icon: '📖' },
    'Biology': { range: [69, 77], icon: '🧬' },
    'Economy': { range: [78, 87], icon: '💰' },
    'Bihar Geography': { range: [88, 96], icon: '🗺️' },
    'Ancient History': { range: [97, 106], icon: '🏛️' },
    'Chemistry': { range: [107, 114], icon: '⚗️' },
    'Physics': { range: [115, 122], icon: '🔭' },
    'Indian Geography': { range: [123, 130], icon: '🇮🇳' },
    'World Geography': { range: [131, 136], icon: '🌍' },
    'Medieval History': { range: [137, 142], icon: '🏰' },
    'Bihar Polity/Economy': { range: [143, 149], icon: ' Bihar' },
    'Environment': { range: [150, 154], icon: '🌿' },
    'Bihar History': { range: [155, 158], icon: ' Bihar' }
  };

  // Build dropdown HTML for a group
  function buildGroupDropdown(name, info) {
    var html = '<div class="bpsc-navbar-dropdown">';
    html += '<a class="dropdown-toggle">' + info.icon + ' ' + name + ' ▾</a>';
    html += '<div class="dropdown-menu">';
    for (var i = info.range[0]; i <= info.range[1]; i++) {
      html += '<a href="' + prefix + 'index.html#topic-' + i + '">Topic ' + i + '</a>';
    }
    html += '</div></div>';
    return html;
  }

  // Build the navbar HTML
  var navbar = document.querySelector('.bpsc-navbar');

  // If no navbar exists (topic pages), create and inject one.
  // If one exists (index.html), reuse it and just attach auto-hide behavior.
  if (!navbar) {
    navbar = document.createElement('nav');
    navbar.className = 'bpsc-navbar';

    var brand = '<div class="bpsc-navbar-brand">';
    brand += '<span class="brand-icon">🎯</span>';
    brand += '<a href="' + prefix + 'index.html">BPSC 72nd Prelims</a>';
    brand += '</div>';

    var links = '<div class="bpsc-navbar-links">';
    links += '<a href="' + prefix + 'index.html" class="active">🏠 Dashboard</a>';

    // Add dropdowns for main groups
    links += buildGroupDropdown('Current Affairs', groups['Current Affairs']);
    links += buildGroupDropdown('Bihar CA', groups['Bihar Current Affairs']);
    links += buildGroupDropdown('History', groups['Modern Indian History']);
    links += buildGroupDropdown('Polity', groups['Indian Polity']);
    links += buildGroupDropdown('Science', { range: [69, 122], icon: '🔬' });
    links += buildGroupDropdown('Geography', { range: [88, 136], icon: '🗺️' });

    links += '</div>';

    // Progress indicator
    var progress = '<div class="bpsc-navbar-progress">';
    progress += '<span class="progress-val">36</span>/158 topics • 22.8%';
    progress += '</div>';

    navbar.innerHTML = brand + links + progress;

    // Insert navbar at the very top of body
    document.body.insertBefore(navbar, document.body.firstChild);
  }

  // Remove old back-links if they exist (they're redundant with the navbar)
  var oldLinks = document.querySelectorAll('a[href="index.html"], a[href$=".html"]');
  oldLinks.forEach(function(link) {
    if (link.textContent.includes('Back to Master Dashboard') && link !== navbar.querySelector('a')) {
      link.style.display = 'none';
    }
  });

  // For subpages, also hide the "Back to Topic" link (navbar handles it)
  if (isSubpage) {
    var backLinks = document.querySelectorAll('a[href^="../"]');
    backLinks.forEach(function(link) {
      if (link.textContent.includes('Back to Topic') && link.parentElement !== navbar) {
        link.style.display = 'none';
      }
    });
  }

  // === AUTO-HIDE BEHAVIOR ===
  // Navbar vanishes when: (1) scrolling down, (2) idle for 3 seconds.
  // Navbar reappears when: (1) scrolling up, (2) mouse moves near top.

  var lastScrollY = window.scrollY;
  var idleTimer = null;
  var IDLE_DELAY = 3000; // 3 seconds of inactivity → hide
  var SCROLL_THRESHOLD = 5; // px — ignore tiny scroll jitter

  function showNavbar() {
    navbar.classList.remove('bpsc-navbar-hidden');
  }

  function hideNavbar() {
    navbar.classList.add('bpsc-navbar-hidden');
  }

  function resetIdleTimer() {
    showNavbar();
    if (idleTimer) clearTimeout(idleTimer);
    idleTimer = setTimeout(function() {
      // Only hide if page is scrolled past the very top
      if (window.scrollY > 30) {
        hideNavbar();
      }
    }, IDLE_DELAY);
  }

  // Scroll-based show/hide
  window.addEventListener('scroll', function() {
    var currentY = window.scrollY;
    var delta = currentY - lastScrollY;

    if (Math.abs(delta) < SCROLL_THRESHOLD) return; // ignore jitter

    if (delta > 0 && currentY > 30) {
      // Scrolling down → hide
      hideNavbar();
    } else {
      // Scrolling up → show
      showNavbar();
    }

    lastScrollY = currentY;
    resetIdleTimer();
  }, { passive: true });

  // Mouse near top → show (within 60px of top edge)
  document.addEventListener('mousemove', function(e) {
    if (e.clientY < 60) {
      showNavbar();
      resetIdleTimer();
    }
  });

  // Hover over navbar itself → keep visible
  navbar.addEventListener('mouseenter', function() {
    showNavbar();
    if (idleTimer) clearTimeout(idleTimer);
  });

  navbar.addEventListener('mouseleave', function() {
    resetIdleTimer();
  });

  // Start the idle timer on page load
  resetIdleTimer();
})();