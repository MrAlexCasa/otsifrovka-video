#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор многостраничного сайта "Оцифровка видеокассет в Новокузнецке".
Создаёт статические HTML-страницы с единым header/nav/footer,
на базе фирменного стиля (assets/css/site.css).

Запуск: python3 build_pages.py
"""
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))

SITE_NAME = "Оцифровка видеокассет в Новокузнецке"
SITE_URL = "https://otsifrovka-video.ru"
TELEGRAM_URL = "https://t.me/+ldEclZqRNDs2Njgy"
AVITO_URL = "https://www.avito.ru/novokuznetsk/predlozheniya_uslug/otsifrovka_videokasset_vhs_vhs-c_hi8_minidv_dvd_837292697"
OK_URL = "https://ok.ru/otsifrovka.noz1"
ADDRESS = "г. Новокузнецк, Кемеровская обл. Кирова 84"

# -------------------------------------------------------------------------
# Структура страниц: slug -> (nav_label, <title> заголовок, meta description)
# -------------------------------------------------------------------------
NAV_SERVICES = [
    ("vhs", "Оцифровка VHS"),
    ("vhs-c", "Оцифровка VHS-C"),
    ("hi8-video8", "Оцифровка Hi8 и Video8"),
    ("minidv-digital8", "Оцифровка MiniDV и Digital8"),
    ("s-vhs", "Оцифровка S-VHS"),
]

NAV_MAIN = [
    ("/", "Главная"),
    ("__services__", "Форматы кассет"),  # dropdown placeholder
    ("/ceny", "Цены"),
    ("/kak-eto-rabotaet", "Как это работает"),
    ("/kontakty", "Контакты"),
]


def nav_html(active_path):
    """Строит HTML для <nav class="main-nav">."""
    items = []
    for href, label in NAV_MAIN:
        if href == "__services__":
            sub_items = "".join(
                '<li><a href="/{slug}">{label}</a></li>'.format(slug=slug, label=label)
                for slug, label in NAV_SERVICES
            )
            is_active_dropdown = active_path.strip("/") in [s for s, _ in NAV_SERVICES]
            items.append(
                '<li class="main-nav__item main-nav__item--has-dropdown{active_cls}">'
                '<a href="#" class="main-nav__link" aria-haspopup="true" aria-expanded="false">Форматы кассет ▾</a>'
                '<ul class="main-nav__dropdown">{sub}</ul>'
                '</li>'.format(
                    active_cls=" is-open" if is_active_dropdown else "",
                    sub=sub_items,
                )
            )
            continue
        is_active = (href == active_path) or (href == "/" and active_path == "/")
        items.append(
            '<li class="main-nav__item"><a href="{href}" class="main-nav__link{active_cls}"{aria}>{label}</a></li>'.format(
                href=href,
                label=label,
                active_cls=" is-active" if is_active else "",
                aria=' aria-current="page"' if is_active else "",
            )
        )
    return "".join(items)


def header_html(active_path):
    return """
<a class="skip-link" href="#main-content">Перейти к содержанию</a>
<header class="site-header">
  <div class="container site-header__inner">
    <a href="/" class="site-logo">Оцифровка видеокассет<span>в Новокузнецке</span></a>
    <nav class="main-nav" aria-label="Основная навигация">
      <ul class="main-nav__list">
        {nav_items}
      </ul>
      <a href="{telegram}" target="_blank" rel="noreferrer noopener" class="header-cta">Написать в Телеграм</a>
    </nav>
    <button type="button" class="nav-toggle" aria-label="Открыть меню" aria-expanded="false">
      <span class="nav-toggle__bar"></span>
      <span class="nav-toggle__bar"></span>
      <span class="nav-toggle__bar"></span>
    </button>
  </div>
</header>
""".format(nav_items=nav_html(active_path), telegram=TELEGRAM_URL)


def breadcrumbs_html(items):
    """items: список (label, href|None). Последний — текущая страница (href=None)."""
    parts = []
    for i, (label, href) in enumerate(items):
        if i > 0:
            parts.append('<span class="sep">/</span>')
        if href:
            parts.append('<a href="{href}">{label}</a>'.format(href=href, label=label))
        else:
            parts.append('<span aria-current="page">{label}</span>'.format(label=label))
    return '<nav class="breadcrumbs container" aria-label="Хлебные крошки">{}</nav>'.format("".join(parts))


def footer_html():
    return """
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <h4>{site_name}</h4>
        <p>Бережно сохраняем ваши семейные сокровища и теплые воспоминания.</p>
        <p class="footer-share-heading">Поделиться в соцсетях</p>
        <div class="footer-share-row">
          <a href="https://connect.ok.ru/offer?url={url_enc}&amp;title={title_enc}" target="_blank" rel="noreferrer noopener" aria-label="Поделиться в Одноклассниках" title="Поделиться в Одноклассниках" style="background-color:#EE8208;">
            <svg viewBox="0 0 24 24" fill="#fff" xmlns="http://www.w3.org/2000/svg"><path d="M12 2a4 4 0 100 8 4 4 0 000-8zm0 6a2 2 0 110-4 2 2 0 010 4zm5.2 5.4a1 1 0 00-1.4-.2 8 8 0 01-7.6 0 1 1 0 00-1.2 1.6c.7.5 1.5 1 2.3 1.3l-2.6 2.6a1 1 0 001.4 1.4L11 17.3v3.7a1 1 0 002 0v-3.7l2.9 2.8a1 1 0 001.4-1.4l-2.6-2.6c.8-.3 1.6-.8 2.3-1.3a1 1 0 00.2-1.4z"/></svg>
          </a>
          <a href="https://vk.com/share.php?url={url_enc}&amp;title={title_enc}" target="_blank" rel="noreferrer noopener" aria-label="Поделиться в ВКонтакте" title="Поделиться в ВКонтакте" style="background-color:#0077FF;">
            <svg viewBox="0 0 24 24" fill="#fff" xmlns="http://www.w3.org/2000/svg"><path d="M2 12.5C2 6.7 6.7 2 12.5 2S23 6.7 23 12.5 18.3 23 12.5 23 2 18.3 2 12.5zm9.8 4.6h1c.3 0 .4-.1.4-.4 0-.6.5-1.3 1.4.2.6 1 .9 1.1 1.7 1.1H17c.2 0 .4-.2.3-.5-.2-.5-1.5-1.9-1.6-2.1-.2-.3-.1-.5 0-.7.2-.4 1.5-2.1 1.6-2.9.1-.3-.1-.5-.4-.5h-1.3c-.3 0-.5.2-.6.4-.4 1-1.5 2.8-1.9 2.8-.2 0-.3-.1-.3-.5v-2c0-.4-.1-.6-.5-.6h-2c-.3 0-.5.2-.5.4 0 .3.5.4.5 1.4v1.7c0 .4-.1.5-.2.5-.4 0-1.4-1.8-2-3.1-.1-.3-.2-.4-.6-.4H7.4c-.3 0-.4.2-.4.4 0 .3 1.5 3.6 3.5 5.4.6.7 1.4.7 1.3.7z"/></svg>
          </a>
          <a href="https://wa.me/?text={share_wa}" target="_blank" rel="noreferrer noopener" aria-label="Поделиться в WhatsApp" title="Поделиться в WhatsApp" style="background-color:#25D366;">
            <svg viewBox="0 0 24 24" fill="#fff" xmlns="http://www.w3.org/2000/svg"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.85.5 3.58 1.36 5.06L2 22l5.2-1.44a9.9 9.9 0 004.84 1.25h.01c5.46 0 9.9-4.45 9.9-9.91C21.96 6.45 17.5 2 12.04 2zm5.8 14a8.2 8.2 0 01-4.16 1.14h-.01a8.2 8.2 0 01-4.17-1.13l-.3-.18-2.9.8.8-2.83-.19-.3a8.14 8.14 0 01-1.24-4.4c0-4.52 3.68-8.2 8.21-8.2a8.16 8.16 0 018.2 8.2 8.2 8.2 0 01-4.24 6.9z"/></svg>
          </a>
          <a href="https://max.ru/:share?text={share_wa}" target="_blank" rel="noreferrer noopener" aria-label="Поделиться в MAX" title="Поделиться в MAX" style="background-color:#8F3E1E;">
            <span style="color:#fff;font-weight:700;font-size:12px;">MAX</span>
          </a>
        </div>
      </div>
      <div>
        <h4>Контакты</h4>
        <p>{address}</p>
      </div>
      <div>
        <h4>Мы в соцсетях</h4>
        <ul class="footer-social-list">
          <li><a href="{telegram}" target="_blank" rel="noreferrer noopener">Телеграм</a></li>
          <li><a href="{avito}" target="_blank" rel="noreferrer noopener">Авито</a></li>
          <li><a href="{ok}" target="_blank" rel="noreferrer noopener">Одноклассники</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      &copy; 2026. Сохраняем лучшее.
    </div>
  </div>
</footer>
<a href="{telegram}" target="_blank" rel="noreferrer noopener" class="floating-cta" aria-label="Написать в Телеграм"><span aria-hidden="true">&#128172;</span><span class="floating-cta__label">Написать в Телеграм</span></a>
<script src="/assets/js/site.js"></script>
""".format(
        site_name=SITE_NAME,
        address=ADDRESS,
        telegram=TELEGRAM_URL,
        avito=AVITO_URL,
        ok=OK_URL,
        url_enc="https%3A%2F%2Fotsifrovka-video.ru%2F",
        title_enc="%D0%9E%D1%86%D0%B8%D1%84%D1%80%D0%BE%D0%B2%D0%BA%D0%B0%20%D0%B2%D0%B8%D0%B4%D0%B5%D0%BE%D0%BA%D0%B0%D1%81%D1%81%D0%B5%D1%82%20%D0%B2%20%D0%9D%D0%BE%D0%B2%D0%BE%D0%BA%D1%83%D0%B7%D0%BD%D0%B5%D1%86%D0%BA%D0%B5",
        share_wa="%D0%9E%D1%86%D0%B8%D1%84%D1%80%D0%BE%D0%B2%D0%BA%D0%B0%20%D0%B2%D0%B8%D0%B4%D0%B5%D0%BE%D0%BA%D0%B0%D1%81%D1%81%D0%B5%D1%82%20%D0%B2%20%D0%9D%D0%BE%D0%B2%D0%BE%D0%BA%D1%83%D0%B7%D0%BD%D0%B5%D1%86%D0%BA%D0%B5%20https%3A%2F%2Fotsifrovka-video.ru%2F",
    )


def page_shell(active_path, title, description, body, canonical_path, extra_head=""):
    canonical = SITE_URL.rstrip("/") + canonical_path
    return """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="{site_name}">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<link rel="stylesheet" href="/assets/css/site.css">
{extra_head}
</head>
<body>
{header}
<main id="main-content">
{body}
</main>
{footer}
</body>
</html>
""".format(
        title=title,
        description=description,
        canonical=canonical,
        site_name=SITE_NAME,
        extra_head=extra_head,
        header=header_html(active_path),
        body=body,
        footer=footer_html(),
    )


def write_page(rel_path, html):
    """rel_path: '/vhs' -> vhs/index.html ; '/' -> index generated separately."""
    slug = rel_path.strip("/")
    out_dir = os.path.join(ROOT, slug)
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "index.html")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html)
    print("Written:", os.path.relpath(out_file, ROOT))


# =========================================================================
# СТРАНИЦЫ УСЛУГ (форматы кассет)
# =========================================================================
FORMAT_PAGES = {
    "vhs": {
        "title": "Оцифровка VHS в Новокузнецке — перенос кассет на флешку",
        "description": "Оцифровка видеокассет VHS в Новокузнецке. Аккуратно переношу записи с VHS на флешку или в облако. Цена — от 200 ₽ за час записи.",
        "h1": "Оцифровка VHS в Новокузнецке",
        "image": "/assets/images/vhs.jpg",
        "intro": "VHS — самый распространённый формат домашних видеокассет 1980–2000-х годов. "
                 "Если у вас сохранились кассеты VHS с записями праздников, свадеб или домашнего архива — "
                 "я аккуратно перенесу их в цифровой формат, сохранив оригинальное качество записи.",
        "related": ["vhs-c", "s-vhs"],
    },
    "vhs-c": {
        "title": "Оцифровка VHS-C в Новокузнецке — компактные видеокассеты",
        "description": "Оцифровка видеокассет VHS-C в Новокузнецке. Перенос записей с компактных кассет VHS-C на флешку. Точная стоимость — после просмотра кассет.",
        "h1": "Оцифровка VHS-C в Новокузнецке",
        "image": "/assets/images/vhs-c.jpg",
        "intro": "VHS-C — компактная версия VHS, использовавшаяся в бытовых видеокамерах. "
                 "Несмотря на маленький размер кассеты, для оцифровки требуется специальный адаптер и оборудование. "
                 "Я работаю с VHS-C и переношу записи в современный цифровой формат.",
        "related": ["vhs", "s-vhs"],
    },
    "hi8-video8": {
        "title": "Оцифровка Hi8 и Video8 в Новокузнецке",
        "description": "Оцифровка кассет Hi8 и Video8 в Новокузнецке. Перенос видеозаписей с камкордерных кассет 8 мм на флешку или в облако.",
        "h1": "Оцифровка Hi8 и Video8 в Новокузнецке",
        "image": "/assets/images/hi8.jpg",
        "intro": "Hi8 и Video8 — форматы компактных видеокассет для камкордеров, популярные в 1990-х годах. "
                 "Записи на этих кассетах со временем портятся, поэтому их стоит оцифровать как можно раньше. "
                 "Я перенесу ваши записи с Hi8 и Video8 в цифровой формат.",
        "related": ["minidv-digital8", "vhs"],
    },
    "minidv-digital8": {
        "title": "Оцифровка MiniDV и Digital8 в Новокузнецке",
        "description": "Оцифровка кассет MiniDV и Digital8 в Новокузнецке. Перенос цифровых видеозаписей с камкордеров на флешку.",
        "h1": "Оцифровка MiniDV и Digital8 в Новокузнецке",
        "image": "/assets/images/minidv.jpg",
        "intro": "MiniDV и Digital8 — цифровые форматы видеокассет, которые использовались в камкордерах 2000-х годов. "
                 "Хотя запись на них цифровая, для просмотра на современных устройствах требуется перенос файлов на флешку или в облако. "
                 "Я помогу извлечь и сохранить ваши записи с MiniDV и Digital8.",
        "related": ["hi8-video8", "s-vhs"],
    },
    "s-vhs": {
        "title": "Оцифровка S-VHS в Новокузнецке — улучшенный формат VHS",
        "description": "Оцифровка видеокассет S-VHS в Новокузнецке. Перенос записей с кассет улучшенного формата VHS на флешку с сохранением качества.",
        "h1": "Оцифровка S-VHS в Новокузнецке",
        "image": "/assets/images/s-vhs.jpg",
        "intro": "S-VHS (Super VHS) — улучшенная версия формата VHS с более высоким качеством изображения. "
                 "Кассеты S-VHS требуют аккуратной оцифровки, чтобы сохранить их преимущество в качестве картинки. "
                 "Я оцифровываю S-VHS с максимальным сохранением исходного качества.",
        "related": ["vhs", "vhs-c"],
    },
}

FORMAT_LABELS = dict(NAV_SERVICES)  # slug -> label


def related_links_html(slugs, extra=None):
    links = []
    for slug in slugs:
        label = FORMAT_LABELS.get(slug, slug)
        links.append('<li><a href="/{slug}">{label}</a></li>'.format(slug=slug, label=label))
    if extra:
        for href, label in extra:
            links.append('<li><a href="{href}">{label}</a></li>'.format(href=href, label=label))
    return """
<div class="related-links">
  <h3>Смотрите также</h3>
  <ul>{links}</ul>
</div>
""".format(links="".join(links))


def build_format_page(slug, data):
    active_path = "/" + slug
    breadcrumbs = breadcrumbs_html([
        ("Главная", "/"),
        (data["h1"].split(" в ")[0], None),
    ])
    body = """
{breadcrumbs}
<section class="hero hero--page">
  <div class="container">
    <h1>{h1}</h1>
    <p class="lead">{intro}</p>
    <div class="btn-row">
      <a href="{telegram}" target="_blank" rel="noreferrer noopener" class="btn btn-primary">Написать в Телеграм</a>
      <a href="/ceny" class="btn btn-secondary">Узнать цены</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div style="display:flex;gap:32px;flex-wrap:wrap;align-items:flex-start;">
      <img src="{image}" alt="{h1}" style="max-width:320px;border-radius:14px;flex-shrink:0;">
      <div style="flex:1;min-width:260px;">
        <h2>Как проходит оцифровка</h2>
        <ol style="padding-left:20px;">
          <li>Вы приносите или присылаете кассеты</li>
          <li>Я проверяю их и просматриваю записи</li>
          <li>Определяю продолжительность и сообщаю точную стоимость</li>
          <li>Оцифровываю видео</li>
          <li>Вы получаете готовые файлы на флешке или в облаке</li>
        </ol>
        <p><a href="/kak-eto-rabotaet">Подробнее о процессе оцифровки →</a></p>
      </div>
    </div>
  </div>
</section>

<section class="section section--shade">
  <div class="container">
    {related}
  </div>
</section>
""".format(
        breadcrumbs=breadcrumbs,
        h1=data["h1"],
        intro=data["intro"],
        telegram=TELEGRAM_URL,
        image=data["image"],
        related=related_links_html(data["related"], extra=[("/ceny", "Цены"), ("/kontakty", "Контакты")]),
    )
    html = page_shell(active_path, data["title"], data["description"], body, active_path)
    write_page(active_path, html)


# =========================================================================
# СТРАНИЦА "ЦЕНЫ"
# =========================================================================
def build_prices_page():
    active_path = "/ceny"
    breadcrumbs = breadcrumbs_html([("Главная", "/"), ("Цены", None)])
    body = """
{breadcrumbs}
<section class="hero hero--page">
  <div class="container">
    <h1>Цены на оцифровку видеокассет</h1>
    <p class="lead">Минимальный заказ — 1 час (200 ₽). Любое начатое время свыше часа округляется в большую сторону.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <table class="price-table">
      <thead>
        <tr><th>Продолжительность записи</th><th>Стоимость</th></tr>
      </thead>
      <tbody>
        <tr><td>1 час</td><td>200 ₽</td></tr>
        <tr><td>1 час 10 минут</td><td>400 ₽</td></tr>
        <tr><td>2 часа</td><td>400 ₽</td></tr>
        <tr><td>2 часа 5 минут</td><td>600 ₽</td></tr>
      </tbody>
    </table>
    <p class="price-note">Стоимость рассчитывается по продолжительности видеозаписи. Точную сумму я сообщаю после просмотра кассет и определения общей длительности.</p>
    <div class="btn-row">
      <a href="{telegram}" target="_blank" rel="noreferrer noopener" class="btn btn-primary">Узнать точную стоимость</a>
      <a href="/kak-eto-rabotaet" class="btn btn-secondary">Как это работает</a>
    </div>
  </div>
</section>

<section class="section section--shade">
  <div class="container">
    <div class="related-links">
      <h3>Форматы кассет, с которыми я работаю</h3>
      <ul>
        {format_links}
      </ul>
    </div>
  </div>
</section>
""".format(
        breadcrumbs=breadcrumbs,
        telegram=TELEGRAM_URL,
        format_links="".join(
            '<li><a href="/{slug}">{label}</a></li>'.format(slug=slug, label=label)
            for slug, label in NAV_SERVICES
        ),
    )
    html = page_shell(
        active_path,
        "Цены на оцифровку видеокассет в Новокузнецке",
        "Стоимость оцифровки видеокассет в Новокузнецке — от 200 ₽ за час записи. Минимальный заказ 1 час, точная цена после просмотра кассет.",
        body,
        active_path,
    )
    write_page(active_path, html)


# =========================================================================
# СТРАНИЦА "КАК ЭТО РАБОТАЕТ"
# =========================================================================
def build_how_it_works_page():
    active_path = "/kak-eto-rabotaet"
    breadcrumbs = breadcrumbs_html([("Главная", "/"), ("Как это работает", None)])
    steps = [
        ("1", "Вы приносите или присылаете кассеты"),
        ("2", "Я проверяю их и просматриваю записи"),
        ("3", "Определяю продолжительность"),
        ("4", "Сообщаю точную стоимость"),
        ("5", "Оцифровываю видео"),
        ("6", "Вы получаете готовые файлы"),
    ]
    steps_html = "".join(
        '<li><span class="step-num">{num}</span><p>{text}</p></li>'.format(num=n, text=t)
        for n, t in steps
    )
    body = """
{breadcrumbs}
<section class="hero hero--page">
  <div class="container">
    <h1>Как проходит оцифровка видеокассет</h1>
    <p class="lead">Процесс простой и прозрачный — от передачи кассет до получения готовых файлов.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <ul class="steps-list">
      {steps}
    </ul>
  </div>
</section>

<section class="section section--shade">
  <div class="container">
    <h2>Не знаете формат своей кассеты?</h2>
    <p>Отправьте фотографию кассеты в Телеграм — я помогу определить формат и расскажу, что нужно для оцифровки.</p>
    <div class="btn-row">
      <a href="{telegram}" target="_blank" rel="noreferrer noopener" class="btn btn-primary">📷 Отправить фото кассеты</a>
      <a href="/ceny" class="btn btn-secondary">Узнать цены</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="related-links">
      <h3>Форматы кассет, с которыми я работаю</h3>
      <ul>
        {format_links}
      </ul>
    </div>
  </div>
</section>
""".format(
        breadcrumbs=breadcrumbs,
        steps=steps_html,
        telegram=TELEGRAM_URL,
        format_links="".join(
            '<li><a href="/{slug}">{label}</a></li>'.format(slug=slug, label=label)
            for slug, label in NAV_SERVICES
        ),
    )
    html = page_shell(
        active_path,
        "Как проходит оцифровка видеокассет — Новокузнецк",
        "Пошаговый процесс оцифровки видеокассет в Новокузнецке: от передачи кассет до получения готовых цифровых файлов.",
        body,
        active_path,
    )
    write_page(active_path, html)


# =========================================================================
# СТРАНИЦА "КОНТАКТЫ"
# =========================================================================
def build_contacts_page():
    active_path = "/kontakty"
    breadcrumbs = breadcrumbs_html([("Главная", "/"), ("Контакты", None)])
    body = """
{breadcrumbs}
<section class="hero hero--page">
  <div class="container">
    <h1>Контакты</h1>
    <p class="lead">Свяжитесь со мной удобным способом — отвечаю быстро.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="contact-methods">
      <div class="contact-card">
        <h3>Телеграм</h3>
        <p>Самый быстрый способ связи. Можно сразу отправить фото кассеты.</p>
        <a href="{telegram}" target="_blank" rel="noreferrer noopener" class="btn btn-primary">Написать в Телеграм</a>
      </div>
      <div class="contact-card">
        <h3>Авито</h3>
        <p>Смотрите отзывы и пишите через Авито.</p>
        <a href="{avito}" target="_blank" rel="noreferrer noopener" class="btn btn-secondary">Я на Авито</a>
      </div>
      <div class="contact-card">
        <h3>Одноклассники</h3>
        <p>Также на связи в Одноклассниках.</p>
        <a href="{ok}" target="_blank" rel="noreferrer noopener" class="btn btn-secondary">Написать в Одноклассники</a>
      </div>
    </div>
    <div class="related-links">
      <h3>Где я работаю</h3>
      <p style="margin:0;">{address}</p>
      <p style="margin-top:8px;">Новокузнецк и регионы РФ (кассеты можно отправить почтой).</p>
    </div>
  </div>
</section>
""".format(
        breadcrumbs=breadcrumbs,
        telegram=TELEGRAM_URL,
        avito=AVITO_URL,
        ok=OK_URL,
        address=ADDRESS,
    )
    html = page_shell(
        active_path,
        "Контакты — Оцифровка видеокассет в Новокузнецке",
        "Контакты для заказа оцифровки видеокассет в Новокузнецке: Телеграм, Авито, Одноклассники.",
        body,
        active_path,
    )
    write_page(active_path, html)


if __name__ == "__main__":
    for slug, data in FORMAT_PAGES.items():
        build_format_page(slug, data)
    build_prices_page()
    build_how_it_works_page()
    build_contacts_page()
    print("\nВсе подстраницы созданы.")
