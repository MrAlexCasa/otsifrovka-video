// Общий скрипт навигации для многостраничного сайта
document.addEventListener('DOMContentLoaded', function () {
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.querySelector('.main-nav');

  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var isOpen = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });

    // Закрывать меню при клике на обычную ссылку (не на элемент с подменю)
    nav.querySelectorAll('a.main-nav__link').forEach(function (link) {
      link.addEventListener('click', function () {
        if (window.innerWidth <= 900) {
          nav.classList.remove('is-open');
          toggle.setAttribute('aria-expanded', 'false');
        }
      });
    });
  }

  // Мобильный тап по пункту с подменю — раскрыть/закрыть список
  document.querySelectorAll('.main-nav__item--has-dropdown > a.main-nav__link').forEach(function (parentLink) {
    parentLink.addEventListener('click', function (e) {
      if (window.innerWidth <= 900) {
        e.preventDefault();
        parentLink.parentElement.classList.toggle('is-open');
      }
    });
  });
});
