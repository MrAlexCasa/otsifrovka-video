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
# Каждая страница содержит уникальный текст (H1/H2/H3), не повторяющийся
# на других страницах, и отвечает на вопросы из ТЗ для конкретного формата.
# =========================================================================
FORMAT_PAGES = {
    "vhs": {
        "title": "Оцифровка VHS в Новокузнецке — перенос VHS на флешку",
        "description": "Оцифровка VHS-кассет в Новокузнецке. Перенос старых видеозаписей VHS в цифровой формат и на флешку. Стоимость — от 200 ₽ за час записи.",
        "h1": "Оцифровка VHS в Новокузнецке",
        "crumb": "VHS",
        "image": "/assets/images/vhs.jpg",
        "image_alt": "Видеокассета VHS, подготовленная к оцифровке",
        "lead": "Перенесу записи с ваших VHS-кассет в цифровой формат — на флешку или другой удобный вам носитель. "
                "Стоимость — от 200 ₽ за час записи, точную сумму называю после просмотра кассеты.",
        "sections": [
            ("Что такое VHS", [
                "VHS — самый массовый формат видеокассет, который использовался в бытовых видеомагнитофонах "
                "с конца 1970-х и до начала 2000-х годов. Именно на VHS чаще всего записывали домашние праздники, "
                "свадьбы, детские утренники и семейные встречи.",
            ]),
            ("Кому нужна оцифровка старых VHS", [
                "Со временем магнитная лента на кассетах осыпается, а видеомагнитофоны, способные их воспроизвести, "
                "почти не встречаются в рабочем состоянии. Оцифровка старых видеокассет нужна тем, кто хочет "
                "пересмотреть семейный архив на современном телевизоре, компьютере или телефоне, а также сохранить "
                "записи, пока плёнка не испортилась окончательно.",
            ]),
            ("Как проходит оцифровка VHS", [
                "Вы передаёте кассеты — лично или другим удобным способом. Я просматриваю запись и определяю её "
                "продолжительность, после чего называю ориентировочную стоимость. После согласования выполняю "
                "оцифровку VHS и записываю результат на флешку клиента или другой согласованный носитель. "
                "Подробное описание всех шагов — на странице <a href=\"/kak-eto-rabotaet\">Как это работает</a>.",
            ]),
            ("Что происходит с готовым видео", [
                "Готовый файл передаётся клиенту в цифровом виде. Кассету можно забрать обратно — оцифровка "
                "видеокассет на флешку не портит и не стирает оригинальную запись.",
            ]),
            ("Стоимость оцифровки VHS", [
                "От 200 ₽ за каждый начатый час записи. Полную таблицу цен по всем форматам смотрите на "
                "странице <a href=\"/ceny\">Цены</a>.",
            ]),
        ],
        "faq": [
            ("Сколько времени занимает оцифровка одной кассеты?", "Зависит от продолжительности записи на кассете — точный срок обсуждается индивидуально после просмотра."),
            ("Можно ли оцифровать несколько кассет VHS сразу?", "Да, кассеты принимаются партиями, стоимость считается по суммарной продолжительности записи."),
            ("В каком качестве получится готовое видео?", "Оцифровка выполняется с сохранением исходного качества записи VHS — улучшить то, чего нет на плёнке, технически невозможно."),
        ],
        "related": ["vhs-c", "s-vhs", "hi8-video8"],
    },
    "vhs-c": {
        "title": "Оцифровка VHS-C в Новокузнецке — перенос кассет на флешку",
        "description": "Оцифровка кассет VHS-C в Новокузнецке. Перенос домашних видеозаписей VHS-C в цифровой формат. Стоимость от 200 ₽ за час записи.",
        "h1": "Оцифровка VHS-C в Новокузнецке",
        "crumb": "VHS-C",
        "image": "/assets/images/vhs-c.jpg",
        "image_alt": "Компактная видеокассета VHS-C, подготовленная к оцифровке",
        "lead": "Отдельно работаю с компактными кассетами VHS-C — переношу записи с домашних видеокамер "
                "в цифровой формат. Стоимость — от 200 ₽ за час записи.",
        "sections": [
            ("Особенности формата VHS-C", [
                "VHS-C — компактная кассета, которая по размеру заметно меньше обычной VHS, но использует ту же "
                "магнитную ленту. Такие кассеты применялись в портативных бытовых видеокамерах: их удобно было "
                "носить с собой на семейные праздники и путешествия.",
                "Из-за меньшего размера кассеты VHS-C воспроизводятся не на обычном видеомагнитофоне, а требуют "
                "камеру или адаптер под этот формат, поэтому оцифровка VHS-C — отдельная услуга, а не часть "
                "стандартной оцифровки VHS.",
            ]),
            ("Кому пригодится оцифровка VHS-C", [
                "Такие кассеты чаще всего хранятся вместе со старыми видеокамерами и содержат записи, которые "
                "нигде больше не сохранились. Если у вас есть кассеты VHS-C — стоит перенести их в цифровой вид, "
                "пока запись не осыпалась.",
            ]),
            ("Процесс и стоимость", [
                "Порядок работы такой же, как и с другими форматами: сначала просмотр кассеты и определение "
                "продолжительности записи, затем согласование стоимости и оцифровка. Итоговое видео передаю "
                "в цифровом виде на флешку или другой согласованный носитель. Цена — от 200 ₽ за начатый час "
                "записи, подробности — на странице <a href=\"/ceny\">Цены</a>.",
            ]),
        ],
        "faq": [
            ("Чем VHS-C отличается от обычной VHS?", "Это тот же формат записи, но кассета компактнее — использовалась в бытовых видеокамерах, а не в стационарных видеомагнитофонах."),
            ("Нужен ли мне адаптер для сдачи кассеты?", "Нет, кассету можно передать как есть — оборудование для считывания VHS-C у меня уже есть."),
        ],
        "related": ["vhs", "s-vhs"],
    },
    "hi8-video8": {
        "title": "Оцифровка Hi8 и Video8 в Новокузнецке — перенос видео на флешку",
        "description": "Оцифровка видеокассет Hi8 и Video8 в Новокузнецке. Перенос старых записей с видеокассет в цифровой формат. От 200 ₽ за час записи.",
        "h1": "Оцифровка Hi8 и Video8 в Новокузнецке",
        "crumb": "Hi8 и Video8",
        "image": "/assets/images/hi8.jpg",
        "image_alt": "Видеокассета Hi8, подготовленная к оцифровке",
        "lead": "Оцифровываю компактные 8-миллиметровые кассеты Video8 и Hi8 — переношу записи с домашних "
                "камкордеров в цифровой формат. Стоимость — от 200 ₽ за час записи.",
        "sections": [
            ("В чём разница между Video8 и Hi8", [
                "Video8 и Hi8 — родственные форматы компактных видеокассет для камкордеров, распространённые "
                "в 1990-х годах. Простыми словами: Video8 — более ранний и распространённый вариант, а Hi8 — "
                "его улучшенная версия с более чёткой картинкой. Кассеты выглядят почти одинаково, а определить "
                "формат точно можно по надписи на самой кассете.",
                "Для оцифровки разница между форматами не критична — оборудование считывает оба варианта, "
                "а результат сохраняется в том качестве, в котором была сделана исходная запись.",
            ]),
            ("Как проходит оцифровка", [
                "Сначала смотрю кассету и определяю продолжительность записи, затем называю ориентировочную "
                "стоимость. После согласования переношу видео с Hi8 или Video8 в цифровой вид и записываю "
                "на флешку клиента или другой согласованный носитель. Подробнее об этапах — на странице "
                "<a href=\"/kak-eto-rabotaet\">Как это работает</a>.",
            ]),
            ("Стоимость", [
                "От 200 ₽ за каждый начатый час записи — как и для остальных форматов кассет. Полная таблица "
                "цен — на странице <a href=\"/ceny\">Цены</a>.",
            ]),
        ],
        "faq": [
            ("Как узнать, Video8 у меня кассета или Hi8?", "Обычно формат указан прямо на наклейке кассеты. Если сомневаетесь — пришлите фото в Телеграм, подскажу."),
            ("Кассета долго хранилась без присмотра — можно ли её оцифровать?", "В большинстве случаев да, кассету можно посмотреть и оценить состояние записи перед началом работы."),
        ],
        "related": ["minidv-digital8", "vhs"],
    },
    "minidv-digital8": {
        "title": "Оцифровка MiniDV и Digital8 в Новокузнецке",
        "description": "Оцифровка MiniDV и Digital8 в Новокузнецке. Перенос видеозаписей с кассет MiniDV и Digital8 в цифровой формат. От 200 ₽ за час.",
        "h1": "Оцифровка MiniDV и Digital8 в Новокузнецке",
        "crumb": "MiniDV и Digital8",
        "image": "/assets/images/minidv.jpg",
        "image_alt": "Видеокассета MiniDV, подготовленная к оцифровке",
        "lead": "Переношу записи с цифровых кассет MiniDV и Digital8 на флешку или другой удобный носитель. "
                "Стоимость — от 200 ₽ за час записи.",
        "sections": [
            ("Формат MiniDV", [
                "MiniDV — маленькая кассета, которая использовалась в цифровых камкордерах конца 1990-х — 2000-х "
                "годов. Запись на ней уже цифровая, но хранится на самой кассете и требует специального "
                "устройства для воспроизведения и переноса файлов на компьютер или флешку.",
            ]),
            ("Формат Digital8", [
                "Digital8 — переходный формат: кассета внешне похожа на Video8 и Hi8, но запись на ней выполняется "
                "в цифровом виде, как на MiniDV. Такие камкордеры выпускались, чтобы владельцы старых кассет "
                "Video8 могли продолжать снимать в привычном формате, но уже с цифровым качеством записи.",
            ]),
            ("Зачем переносить файлы, если запись уже цифровая", [
                "Несмотря на цифровую запись, сами кассеты MiniDV и Digital8 читаются только специальными "
                "камкордерами или плеерами, которых почти не осталось в рабочем состоянии. Оцифровка в этом "
                "случае — это перенос файлов с кассеты на флешку или другой носитель, чтобы видео можно было "
                "смотреть на современных устройствах.",
            ]),
            ("Процесс и стоимость", [
                "Порядок работы стандартный: просмотр кассеты, определение продолжительности записи, согласование "
                "стоимости и перенос файлов. Цена — от 200 ₽ за начатый час записи, подробности — на странице "
                "<a href=\"/ceny\">Цены</a>, этапы работы — на странице <a href=\"/kak-eto-rabotaet\">Как это работает</a>.",
            ]),
        ],
        "faq": [
            ("MiniDV и Digital8 — это одно и то же?", "Нет, это разные по размеру кассеты, но обе используют цифровую запись, поэтому переносятся похожим способом."),
            ("Файлы с MiniDV теряют качество при переносе?", "Перенос выполняется без дополнительного сжатия сверх исходной записи на кассете."),
        ],
        "related": ["hi8-video8", "s-vhs"],
    },
    "s-vhs": {
        "title": "Оцифровка S-VHS в Новокузнецке — перенос видеокассет",
        "description": "Оцифровка кассет S-VHS в Новокузнецке. Перенос видеозаписей в цифровой формат. Стоимость от 200 ₽ за час записи.",
        "h1": "Оцифровка S-VHS в Новокузнецке",
        "crumb": "S-VHS",
        "image": "/assets/images/s-vhs.jpg",
        "image_alt": "Видеокассета S-VHS, подготовленная к оцифровке",
        "lead": "Оцифровываю кассеты S-VHS — переношу видеозаписи в цифровой формат на флешку или другой "
                "согласованный носитель. Стоимость — от 200 ₽ за час записи.",
        "sections": [
            ("Чем S-VHS отличается от обычного VHS", [
                "S-VHS (Super VHS) — формат, разработанный как улучшенная версия обычного VHS: кассеты и "
                "видеомагнитофоны S-VHS были рассчитаны на более чёткую картинку по сравнению со стандартным "
                "VHS. Внешне кассеты похожи, но отличаются маркировкой и требуют совместимой техники для "
                "воспроизведения.",
                "Важно понимать: итоговое качество оцифровки всегда зависит от состояния конкретной плёнки "
                "и того, как была сделана исходная запись. Оцифровка переносит запись в цифровой вид в том "
                "качестве, в котором она сохранилась на кассете, — гарантировать улучшение картинки сверх "
                "исходного уровня невозможно.",
            ]),
            ("Как проходит оцифровка S-VHS", [
                "Как и с другими форматами: сначала просмотр кассеты и оценка продолжительности записи, затем "
                "согласование стоимости и перенос видео в цифровой вид. Подробное описание шагов — на странице "
                "<a href=\"/kak-eto-rabotaet\">Как это работает</a>.",
            ]),
            ("Стоимость", [
                "От 200 ₽ за каждый начатый час записи. Таблица цен по всем форматам — на странице "
                "<a href=\"/ceny\">Цены</a>.",
            ]),
        ],
        "faq": [
            ("Можно ли улучшить качество записи при оцифровке S-VHS?", "Оцифровка сохраняет исходное качество записи с кассеты — заново «дорисовать» отсутствующие детали изображения технически невозможно."),
            ("Подойдёт ли обычный видеомагнитофон для просмотра S-VHS?", "Не всегда — для наилучшего считывания нужна техника, совместимая с S-VHS, поэтому оцифровку лучше доверить тому, у кого такое оборудование уже есть."),
        ],
        "related": ["vhs", "vhs-c"],
    },
}

FORMAT_LABELS = dict(NAV_SERVICES)  # slug -> label


def related_links_html(slugs, extra=None, heading="Смотрите также"):
    links = []
    for slug in slugs:
        label = FORMAT_LABELS.get(slug, slug)
        links.append('<li><a href="/{slug}">{label}</a></li>'.format(slug=slug, label=label))
    if extra:
        for href, label in extra:
            links.append('<li><a href="{href}">{label}</a></li>'.format(href=href, label=label))
    return """
<div class="related-links">
  <h3>{heading}</h3>
  <ul>{links}</ul>
</div>
""".format(heading=heading, links="".join(links))


def sections_html(sections):
    parts = []
    for heading, paragraphs in sections:
        paras = "".join("<p>{}</p>".format(p) for p in paragraphs)
        parts.append('<h2>{heading}</h2>{paras}'.format(heading=heading, paras=paras))
    return "".join(parts)


def faq_html(items):
    if not items:
        return ""
    cards = "".join(
        '<div class="faq-item"><h3>{q}</h3><p>{a}</p></div>'.format(q=q, a=a)
        for q, a in items
    )
    return """
<section class="section section--shade">
  <div class="container">
    <h2>Частые вопросы</h2>
    <div class="faq-list">{cards}</div>
  </div>
</section>
""".format(cards=cards)


def build_format_page(slug, data):
    active_path = "/" + slug
    breadcrumbs = breadcrumbs_html([
        ("Главная", "/"),
        (data["crumb"], None),
    ])
    body = """
{breadcrumbs}
<section class="hero hero--page">
  <div class="container">
    <h1>{h1}</h1>
    <p class="lead">{lead}</p>
    <div class="btn-row">
      <a href="{telegram}" target="_blank" rel="noreferrer noopener" class="btn btn-primary">Написать в Телеграм</a>
      <a href="/ceny" class="btn btn-secondary">Узнать цены</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div style="display:flex;gap:32px;flex-wrap:wrap;align-items:flex-start;">
      <img src="{image}" alt="{image_alt}" style="max-width:320px;border-radius:14px;flex-shrink:0;">
      <div style="flex:1;min-width:260px;">
        {sections}
      </div>
    </div>
  </div>
</section>

{faq}

<section class="section{shade_class}">
  <div class="container">
    {related}
  </div>
</section>
""".format(
        breadcrumbs=breadcrumbs,
        h1=data["h1"],
        lead=data["lead"],
        telegram=TELEGRAM_URL,
        image=data["image"],
        image_alt=data["image_alt"],
        sections=sections_html(data["sections"]),
        faq=faq_html(data.get("faq")),
        shade_class="" if data.get("faq") else " section--shade",
        related=related_links_html(
            data["related"],
            extra=[("/", "Главная"), ("/ceny", "Цены"), ("/kak-eto-rabotaet", "Как проходит оцифровка"), ("/kontakty", "Контакты")],
        ),
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
    <p class="lead">Стоимость — 200 ₽ за начатый час записи. Точную сумму я называю после бесплатного просмотра кассеты.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <h2>Как рассчитывается стоимость</h2>
    <p>Цена оцифровки зависит от продолжительности видеозаписи на кассете, а не от количества самих кассет. Любой начатый час записи оплачивается как полный. Например:</p>
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
    <p class="price-note">Точную длительность записи заранее знают не все — поэтому перед началом работы я бесплатно просматриваю кассету, определяю продолжительность записи и только после этого называю ориентировочную стоимость. Подробнее о порядке работы — на странице <a href="/kak-eto-rabotaet">Как это работает</a>.</p>
    <div class="btn-row">
      <a href="{telegram}" target="_blank" rel="noreferrer noopener" class="btn btn-primary">Узнать точную стоимость</a>
      <a href="/kak-eto-rabotaet" class="btn btn-secondary">Как это работает</a>
    </div>
  </div>
</section>

<section class="section section--shade">
  <div class="container">
    <h2>Поддерживаемые форматы кассет</h2>
    <table class="price-table">
      <thead>
        <tr><th>Формат</th><th>Стоимость</th></tr>
      </thead>
      <tbody>
        <tr><td><a href="/vhs">VHS</a></td><td rowspan="9" style="vertical-align:middle;">200 ₽ за начатый час записи</td></tr>
        <tr><td><a href="/vhs-c">VHS-C</a></td></tr>
        <tr><td><a href="/s-vhs">S-VHS</a></td></tr>
        <tr><td><a href="/hi8-video8">Video8</a></td></tr>
        <tr><td><a href="/hi8-video8">Hi8</a></td></tr>
        <tr><td><a href="/minidv-digital8">Digital8</a></td></tr>
        <tr><td><a href="/minidv-digital8">MiniDV</a></td></tr>
        <tr><td>DVD</td></tr>
        <tr><td>CD</td></tr>
      </tbody>
    </table>
    <p class="price-note">Дополнительных тарифов и скрытых доплат нет — стоимость одинаково рассчитывается по продолжительности записи для всех форматов.</p>
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
        telegram=TELEGRAM_URL,
        format_links="".join(
            '<li><a href="/{slug}">{label}</a></li>'.format(slug=slug, label=label)
            for slug, label in NAV_SERVICES
        ),
    )
    html = page_shell(
        active_path,
        "Цены на оцифровку видеокассет в Новокузнецке",
        "Цены на оцифровку VHS, VHS-C, S-VHS, Video8, Hi8, Digital8 и MiniDV в Новокузнецке. Стоимость — 200 ₽ за начатый час записи.",
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
        ("1", "Клиент передаёт кассету", "Кассету можно передать лично или согласовать другой удобный способ."),
        ("2", "Выполняется предварительный просмотр", "Я смотрю запись, чтобы убедиться в её состоянии перед началом работы. Просмотр — бесплатный."),
        ("3", "Определяется продолжительность записи", "От продолжительности записи, а не от количества кассет, зависит итоговая стоимость."),
        ("4", "Сообщается ориентировочная стоимость", "Стоимость называю после просмотра — из расчёта 200 ₽ за каждый начатый час записи."),
        ("5", "После согласования выполняется оцифровка", "Приступаю к переносу записи в цифровой формат только после того, как стоимость согласована."),
        ("6", "Готовое видео передаётся клиенту в цифровом виде", "Результат записываю на флешку клиента или на другой согласованный с ним носитель."),
    ]
    steps_html = "".join(
        '<li><span class="step-num">{num}</span><div><h3 style="margin:0 0 6px;font-size:17px;">{title}</h3><p style="margin:0;">{text}</p></div></li>'.format(num=n, title=t, text=d)
        for n, t, d in steps
    )
    body = """
{breadcrumbs}
<section class="hero hero--page">
  <div class="container">
    <h1>Как проходит оцифровка видеокассет</h1>
    <p class="lead">Понятная последовательность действий — от передачи кассеты до получения готового видео в цифровом виде.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <h2>Шесть шагов оцифровки</h2>
    <ul class="steps-list">
      {steps}
    </ul>
  </div>
</section>

<section class="section section--shade">
  <div class="container">
    <h2>Почему сначала просмотр, а потом стоимость</h2>
    <p>Продолжительность записи на разных кассетах отличается, поэтому точную стоимость невозможно назвать заранее — только после того, как кассета просмотрена и определена длительность видео. Это тот же принцип расчёта, что описан на странице <a href="/ceny">Цены</a>.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <h2>Не знаете формат своей кассеты?</h2>
    <p>Отправьте фотографию кассеты в Телеграм — я помогу определить формат и расскажу, что нужно для оцифровки.</p>
    <div class="btn-row">
      <a href="{telegram}" target="_blank" rel="noreferrer noopener" class="btn btn-primary">📷 Отправить фото кассеты</a>
      <a href="/ceny" class="btn btn-secondary">Узнать цены</a>
    </div>
  </div>
</section>

<section class="section section--shade">
  <div class="container">
    <div class="related-links">
      <h3>Форматы кассет, с которыми я работаю</h3>
      <ul>
        {format_links}
        <li><a href="/kontakty">Контакты</a></li>
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
        "Как проходит оцифровка видеокассет в Новокузнецке",
        "Как проходит оцифровка VHS, Hi8, Video8, MiniDV и других видеокассет. Предварительный просмотр, оценка продолжительности и перенос видео в цифровой формат.",
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
    <p class="lead">Свяжитесь удобным способом, чтобы обсудить оцифровку видеокассет в Новокузнецке — отвечаю в Телеграме, Авито и Одноклассниках.</p>
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
      <p style="margin-top:8px;">Новокузнецк и регионы РФ.</p>
    </div>
  </div>
</section>

<section class="section section--shade">
  <div class="container">
    <div class="related-links">
      <h3>Также вам может быть полезно</h3>
      <ul>
        <li><a href="/">Главная</a></li>
        <li><a href="/ceny">Цены</a></li>
        <li><a href="/kak-eto-rabotaet">Как проходит оцифровка</a></li>
      </ul>
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
        "Контакты — оцифровка видеокассет в Новокузнецке",
        "Контакты для заказа оцифровки видеокассет в Новокузнецке. VHS, VHS-C, S-VHS, Hi8, Video8, Digital8 и MiniDV.",
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
