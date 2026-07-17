/**
 * Netlify Identity Auth + Access Control
 * — auto-injected on all pages
 * — hides content until authorized user logs in
 * — shows login screen for unauthorized/not-logged-in users
 * — invite-only: you authorize people by inviting them via Netlify dashboard
 *
 * HOW AUTHORIZATION WORKS:
 * 1. Set Registration to "Invite-only" in Netlify Identity settings
 * 2. Invite people by email from the Identity tab in Netlify dashboard
 * 3. They get an email invitation → sign up with that email
 * 4. Only invited users can create accounts — no random signups
 * 5. Only logged-in users can see content — everyone else sees a login screen
 */

(function () {
  // 1. Inject the Netlify Identity widget script
  var s = document.createElement('script');
  s.src = 'https://identity.netlify.com/v1/netlify-identity-widget.js';
  s.async = true;
  document.head.appendChild(s);
  s.onload = function () { initAuth(); };

  // 2. Show gate immediately (before Identity loads)
  showGate();

  // 3. Also listen for DOMContentLoaded
  document.addEventListener('DOMContentLoaded', function () {
    if (window.netlifyIdentity) {
      initAuth();
    } else {
      showGate();
    }
  });
})();

function showGate() {
  if (document.getElementById('auth-gate')) return;
  if (!document.body) { setTimeout(showGate, 50); return; }

  // Hide all page content
  var style = document.createElement('style');
  style.id = 'auth-hide-style';
  style.textContent = 'body > *:not(#auth-gate) { display: none !important; }';
  document.head.appendChild(style);

  var gate = document.createElement('div');
  gate.id = 'auth-gate';
  gate.style.cssText = [
    'position: fixed', 'top: 0', 'left: 0', 'width: 100vw', 'height: 100vh',
    'background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)',
    'display: flex', 'flex-direction: column', 'align-items: center', 'justify-content: center',
    'z-index: 99999', 'font-family: Inter, -apple-system, sans-serif', 'padding: 20px',
    'box-sizing: border-box'
  ].join('; ');

  gate.innerHTML = [
    '<div style="max-width: 420px; text-align: center; width: 100%;">',
    '  <div style="font-size: 48px; margin-bottom: 16px;">📚</div>',
    '  <h1 style="color: #fff; font-size: 24px; font-weight: 800; margin-bottom: 8px; letter-spacing: -0.5px;">BPSC 72nd Prelims</h1>',
    '  <p style="color: rgba(255,255,255,0.7); font-size: 14px; margin-bottom: 24px;">Study Portal — Authorized Access Only</p>',
    '  <button id="auth-login-btn" style="',
    '    background: linear-gradient(135deg, #e94560, #c2185b);',
    '    color: #fff; border: none; padding: 14px 48px; border-radius: 12px;',
    '    font-size: 16px; font-weight: 700; cursor: pointer; font-family: inherit;',
    '    box-shadow: 0 4px 20px rgba(233,69,96,0.35); transition: all 0.2s;">',
    '    Login to Continue',
    '  </button>',
    '  <p id="auth-loading-text" style="color: rgba(255,255,255,0.5); font-size: 12px; margin-top: 16px; display: none;">Loading authentication...</p>',
    '  <p style="color: rgba(255,255,255,0.4); font-size: 11px; margin-top: 20px;">',
    '    Need access? Contact the site administrator for an invitation.',
    '  </p>',
    '</div>'
  ].join('');

  document.body.appendChild(gate);

  var loginBtn = document.getElementById('auth-login-btn');
  loginBtn.onmouseover = function () {
    this.style.transform = 'translateY(-2px)';
    this.style.boxShadow = '0 6px 28px rgba(233,69,96,0.45)';
  };
  loginBtn.onmouseout = function () {
    this.style.transform = '';
    this.style.boxShadow = '0 4px 20px rgba(233,69,96,0.35)';
  };
  loginBtn.onclick = function () {
    if (window.netlifyIdentity) {
      netlifyIdentity.open();
    } else {
      var lt = document.getElementById('auth-loading-text');
      if (lt) lt.style.display = 'block';
      setTimeout(function () {
        if (window.netlifyIdentity) netlifyIdentity.open();
      }, 1000);
    }
  };
}

function hideGate() {
  var gate = document.getElementById('auth-gate');
  var hideStyle = document.getElementById('auth-hide-style');
  if (hideStyle) hideStyle.remove();
  if (gate) gate.remove();
}

function initAuth() {
  if (!window.netlifyIdentity) return;

  // Initialize the Identity widget
  netlifyIdentity.init();

  function checkAccess() {
    var user = netlifyIdentity.currentUser();

    if (user) {
      // User is logged in — show content
      hideGate();
      addAuthButton(user);
    } else {
      // Not logged in — show gate
      showGate();
    }
  }

  // Add the floating auth button (visible only when logged in)
  function addAuthButton(user) {
    // Remove existing button if present
    var existing = document.getElementById('auth-container');
    if (existing) existing.remove();

    var authContainer = document.createElement('div');
    authContainer.id = 'auth-container';
    authContainer.style.cssText = [
      'position: fixed', 'top: 8px', 'right: 12px', 'z-index: 10000',
      'display: flex', 'align-items: center', 'gap: 8px',
      'font-family: Inter, -apple-system, sans-serif'
    ].join('; ');

    // User label
    var userLabel = document.createElement('span');
    userLabel.style.cssText = [
      'font-size: 12px', 'color: #1a1a2e', 'font-weight: 600',
      'background: #f0fdf4', 'padding: 4px 10px', 'border-radius: 6px',
      'border: 1px solid #dcfce7'
    ].join('; ');
    var name = (user.user_metadata && user.user_metadata.full_name)
      ? user.user_metadata.full_name
      : user.email || 'User';
    userLabel.textContent = '👤 ' + name;
    authContainer.appendChild(userLabel);

    // Logout button
    var logoutBtn = document.createElement('button');
    logoutBtn.style.cssText = [
      'background: linear-gradient(135deg, #475569, #334155)',
      'color: #fff', 'border: none', 'padding: 6px 16px', 'border-radius: 8px',
      'font-size: 12px', 'font-weight: 700', 'cursor: pointer',
      'font-family: inherit', 'box-shadow: 0 2px 8px rgba(71,85,105,0.25)',
      'transition: all 0.2s'
    ].join('; ');
    logoutBtn.textContent = 'Logout';
    logoutBtn.onclick = function () {
      netlifyIdentity.logout();
    };
    authContainer.appendChild(logoutBtn);

    document.body.appendChild(authContainer);
  }

  // Listen for auth events
  netlifyIdentity.on('init', checkAccess);
  netlifyIdentity.on('login', function (user) {
    checkAccess();
    netlifyIdentity.close();
  });
  netlifyIdentity.on('logout', function () {
    checkAccess();
  });

  // Initial check
  checkAccess();
}