(function () {
  var nav = document.getElementById('site-nav');
  if (!nav) return;

  var button = nav.querySelector('button');
  var overflow = document.getElementById('navigation-overflow');
  if (!button || !overflow) return;

  function syncExpanded() {
    var expanded = !button.classList.contains('hidden') && !overflow.classList.contains('hidden');
    button.setAttribute('aria-expanded', String(expanded));
    button.classList.toggle('close', expanded);
  }

  function closeMenu() {
    overflow.classList.add('hidden');
    syncExpanded();
  }

  function refreshLayout() {
    window.updateNav();
    syncExpanded();
  }

  // The bundled priority navigation moves links and toggles the overflow list.
  button.addEventListener('click', syncExpanded);
  window.addEventListener('resize', syncExpanded);
  window.addEventListener('load', refreshLayout);
  if (document.fonts) document.fonts.ready.then(refreshLayout);
  nav.addEventListener('click', function (event) {
    if (event.target.closest('a')) closeMenu();
  });
  nav.addEventListener('keydown', function (event) {
    if (event.key === 'Escape' && button.getAttribute('aria-expanded') === 'true') {
      closeMenu();
      button.focus();
    }
  });
  syncExpanded();
})();
