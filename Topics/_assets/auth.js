/**
 * Netlify Identity Auth — auto-injected on all pages
 * Adds login/signup/logout button to the navbar
 * Works with Netlify Identity widget (free, up to 1,000 users)
 */

// 1. Inject the Netlify Identity widget script
(function () {
  var s = document.createElement('script');
  s.src = 'https://identity.netlify.com/v1/netlify-identity-widget.js';
  s.async = true;
  document.head.appendChild(s);

  s.onload = function () {
    initAuth();
  };
})();

// 2. Also listen for DOMContentLoaded in case script loads fast
document.addEventListener('DOMContentLoaded', function () {
  if (window.netlifyIdentity) {
    initAuth();
  }
});

function initAuth() {
  if (!window.netlifyIdentity) return;

  // Initialize the widget
  netlifyIdentity.init();

  // Create auth button container
  var authContainer = document.createElement('div');
  authContainer.id = 'auth-container';
  authContainer.style.cssText = `
    position: fixed;
    top: 8px;
    right: 12px;
    z-index: 10000;
    display: flex;
    align-items: center;
    gap: 8px;
    font-family: 'Inter', -apple-system, sans-serif;
  `;

  // User display name (hidden by default)
  var userLabel = document.createElement('span');
  userLabel.id = 'auth-user-label';
  userLabel.style.cssText = `
    font-size: 12px;
    color: #1a1a2e;
    font-weight: 600;
    display: none;
    background: #f0fdf4;
    padding: 4px 10px;
    border-radius: 6px;
    border: 1px solid #dcfce7;
  `;
  authContainer.appendChild(userLabel);

  // Login/Logout button
  var authBtn = document.createElement('button');
  authBtn.id = 'auth-btn';
  authBtn.style.cssText = `
    background: linear-gradient(135deg, #e94560, #c2185b);
    color: #fff;
    border: none;
    padding: 6px 16px;
    border-radius: 8px;
    font-size: 12px;
    font-weight: 700;
    cursor: pointer;
    font-family: 'Inter', -apple-system, sans-serif;
    transition: all 0.2s;
    box-shadow: 0 2px 8px rgba(233,69,96,0.25);
  `;
  authBtn.textContent = 'Login';
  authBtn.onclick = function () {
    if (netlifyIdentity.currentUser()) {
      netlifyIdentity.logout();
    } else {
      netlifyIdentity.open();
    }
  };
  authContainer.appendChild(authBtn);

  // Append to body (works on all pages, stays on top)
  document.body.appendChild(authContainer);

  // Update UI based on auth state
  function updateAuthUI() {
    var user = netlifyIdentity.currentUser();
    var btn = document.getElementById('auth-btn');
    var label = document.getElementById('auth-user-label');

    if (user) {
      // Logged in
      var name = user.user_metadata && user.user_metadata.full_name
        ? user.user_metadata.full_name
        : user.email || 'User';
      btn.textContent = 'Logout';
      btn.style.background = 'linear-gradient(135deg, #475569, #334155)';
      label.textContent = '👤 ' + name;
      label.style.display = 'inline-block';
    } else {
      // Logged out
      btn.textContent = 'Login';
      btn.style.background = 'linear-gradient(135deg, #e94560, #c2185b)';
      label.style.display = 'none';
    }
  }

  // Listen for auth events
  netlifyIdentity.on('init', updateAuthUI);
  netlifyIdentity.on('login', function (user) {
    updateAuthUI();
    netlifyIdentity.close();
  });
  netlifyIdentity.on('logout', function () {
    updateAuthUI();
  });

  // Initial update
  updateAuthUI();
}