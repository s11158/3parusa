(function () {
  "use strict";

  var IMAGE_ROOT = "/assets/brand/images/";
  var LOGO_SRC = "/assets/static.tildacdn.com/tild3431-6664-4435-b466-386137613935/photo.png";

  var DESTINATION_IMAGES = {
    turkey: "turkey.webp",
    greece: "greece.webp",
    italy: "italy.webp",
    croatia: "croatia.webp",
    ibiza: "ibiza.webp",
    "canary-islands": "canary.webp",
    seychelles: "seychelles.webp",
    thailand: "thailand.webp",
    caribbean: "caribbean.webp"
  };

  var OFFER_IMAGES = {
    corporate: "corporate.webp",
    "kids-camp": "kids.webp",
    "captains-school": "captain.webp",
    "b2b-charter": "b2b.webp",
    devichnik: "devichnik.webp",
    malchishnik: "malchishnik.webp"
  };

  var ARTICLE_HERO_IMAGES = {
    "barhatnyy-sezon-turcia": "turkey.webp",
    "bezopasno-li-na-yahte": "yacht-aerial.webp",
    "chto-esli-shtorm": "lifestyle-7.webp",
    "chto-vzyat-s-soboy-na-yahtu": "lifestyle-5.webp",
    "detskiy-lager-pod-parusom": "kids.webp",
    "greciya-na-yahte": "greece.webp",
    "horvatiya-na-yahte": "croatia.webp",
    "internet-i-rabota-na-yahte": "lifestyle-6.webp",
    "italiya-na-yahte-amalfi-sardiniya": "italy.webp",
    "kak-dobratsya-dalaman-fethiye": "turkey.webp",
    "kak-oplatit-tur-iz-rossii": "lifestyle-3.webp",
    "kak-vybrat-yahtu": "yacht-aerial.webp",
    "kayuty-i-razmeshchenie-na-katamarane": "lifestyle-2.webp",
    "korporativ-na-yahte": "corporate.webp",
    "lazurnyy-bereg-na-yahte": "lifestyle-8.webp",
    "malchishnik-na-yahte": "malchishnik.webp",
    "marshrut-fethiye-gocek": "turkey.webp",
    "odin-v-tur-na-yahte": "lifestyle-1.webp",
    "pervyy-raz-na-yahte": "lifestyle-4.webp",
    "semeyniy-otdyh-s-detmi": "kids.webp",
    "seyshely-kogda-sezon": "seychelles.webp",
    "seyshely-na-katamarane": "seychelles.webp",
    "skolko-stoit-tur-na-yahte": "lifestyle-3.webp",
    "sudovaya-kassa-chto-eto": "lifestyle-2.webp",
    "tailand-na-yahte-zimoy": "thailand.webp",
    "ukachivaet-li-na-katamarane": "lifestyle-6.webp",
    "yahta-ili-otel": "lifestyle-8.webp"
  };

  var LIFESTYLE_IMAGES = [
    "lifestyle-1.webp",
    "lifestyle-2.webp",
    "lifestyle-3.webp",
    "lifestyle-4.webp",
    "lifestyle-5.webp",
    "lifestyle-6.webp",
    "lifestyle-7.webp",
    "lifestyle-8.webp"
  ];

  var EYEBROWS = {
    destination: "Авторский маршрут · 3Parusa",
    offer: "Частный формат · Под ключ",
    faq: "Перед выходом в море",
    "blog-index": "Бортовой журнал",
    "blog-article": "Блог капитана",
    privacy: "Документы · 3Parusa",
    "not-found": "Навигация · 3Parusa",
    secondary: "Путешествия под парусом"
  };

  var HEADER_LINKS = [
    { href: "/#rec695697372", label: "Маршруты" },
    { href: "/#rec662235809", label: "Программа" },
    { href: "/#rec695421651", label: "Стоимость" },
    { href: "/#rec662235811", label: "Флот" },
    { href: "/#rec662235814", label: "Отзывы" },
    { href: "/blog/", label: "Блог", current: "blog" },
    { href: "/faq.html", label: "FAQ", current: "faq" }
  ];

  function normalisePath(pathname) {
    var value = pathname || "/";

    try {
      value = decodeURIComponent(value);
    } catch (error) {
      /* Keep the browser-provided value when a path has malformed escapes. */
    }

    value = value.replace(/\\/g, "/").replace(/\/{2,}/g, "/").toLowerCase();
    if (value.length > 1) {
      value = value.replace(/\/+$/, "");
    }
    return value || "/";
  }

  function slugFromPath(path) {
    var pieces = path.split("/");
    var last = pieces[pieces.length - 1] || "index";
    return last.replace(/\.html?$/i, "") || "index";
  }

  function classifyPage(pathname) {
    var path = normalisePath(pathname);
    var slug = slugFromPath(path);

    if (path === "/") {
      return null;
    }
    if (path === "/blog" || path === "/blog/index" || path === "/blog/index.html") {
      return { kind: "blog-index", slug: "blog", path: path };
    }
    if (path.indexOf("/blog/") === 0) {
      return { kind: "blog-article", slug: slug, path: path };
    }
    if (Object.prototype.hasOwnProperty.call(DESTINATION_IMAGES, slug)) {
      return { kind: "destination", slug: slug, path: path };
    }
    if (Object.prototype.hasOwnProperty.call(OFFER_IMAGES, slug)) {
      return { kind: "offer", slug: slug, path: path };
    }
    if (slug === "faq") {
      return { kind: "faq", slug: slug, path: path };
    }
    if (slug === "privacy") {
      return { kind: "privacy", slug: slug, path: path };
    }
    if (slug === "404") {
      return { kind: "not-found", slug: slug, path: path };
    }
    return { kind: "secondary", slug: slug, path: path };
  }

  function hashString(value) {
    var hash = 0;
    var index;
    for (index = 0; index < value.length; index += 1) {
      hash = (hash * 31 + value.charCodeAt(index)) >>> 0;
    }
    return hash;
  }

  function imageUrl(filename) {
    return IMAGE_ROOT + filename;
  }

  function cssImage(filename) {
    return 'url("' + imageUrl(filename) + '")';
  }

  function buildImagePlan(info) {
    var seed = hashString(info.slug);
    var hero = "yacht-aerial.webp";
    var inlineIndex = (seed + 2) % LIFESTYLE_IMAGES.length;
    var galleryIndexes = [
      (seed + 1) % LIFESTYLE_IMAGES.length,
      (seed + 4) % LIFESTYLE_IMAGES.length,
      (seed + 6) % LIFESTYLE_IMAGES.length
    ];

    if (info.kind === "destination") {
      hero = DESTINATION_IMAGES[info.slug];
    } else if (info.kind === "offer") {
      hero = OFFER_IMAGES[info.slug];
    } else if (info.kind === "faq") {
      hero = "faq.webp";
    } else if (info.kind === "blog-index") {
      hero = "blog.webp";
    } else if (info.kind === "blog-article") {
      hero = ARTICLE_HERO_IMAGES[info.slug] || LIFESTYLE_IMAGES[seed % LIFESTYLE_IMAGES.length];
    }

    if (LIFESTYLE_IMAGES[inlineIndex] === hero) {
      inlineIndex = (inlineIndex + 1) % LIFESTYLE_IMAGES.length;
    }

    return {
      hero: hero,
      inline: LIFESTYLE_IMAGES[inlineIndex],
      gallery: galleryIndexes.map(function (index) {
        return LIFESTYLE_IMAGES[index];
      })
    };
  }

  function setImageVariables(plan) {
    var root = document.documentElement;
    root.style.setProperty("--brand-hero-image", cssImage(plan.hero));
    root.style.setProperty("--brand-inline-image", cssImage(plan.inline));
    root.style.setProperty("--brand-gallery-image-1", cssImage(plan.gallery[0]));
    root.style.setProperty("--brand-gallery-image-2", cssImage(plan.gallery[1]));
    root.style.setProperty("--brand-gallery-image-3", cssImage(plan.gallery[2]));
  }

  function makeElement(tagName, className, text) {
    var element = document.createElement(tagName);
    if (className) {
      element.className = className;
    }
    if (typeof text === "string") {
      element.textContent = text;
    }
    return element;
  }

  function appendLink(parent, className, href, text) {
    var link = makeElement("a", className, text);
    link.href = href;
    parent.appendChild(link);
    return link;
  }

  function createHeader(info) {
    var header = makeElement("header", "brand-header");
    var inner = makeElement("div", "brand-header__inner");
    var logo = makeElement("a", "brand-header__logo");
    var logoImage = makeElement("img");
    var toggle = makeElement("button", "brand-header__toggle");
    var toggleLabel = makeElement("span", "brand-header__toggle-label", "Меню");
    var toggleLines = makeElement("span", "brand-header__toggle-lines");
    var drawer = makeElement("div", "brand-header__drawer");
    var nav = makeElement("nav", "brand-header__nav");
    var actions = makeElement("div", "brand-header__actions");

    header.setAttribute("data-brand-generated", "header");
    logo.href = "/";
    logo.setAttribute("aria-label", "3Parusa — на главную");
    logoImage.src = LOGO_SRC;
    logoImage.alt = "3Parusa";
    logoImage.width = 190;
    logoImage.decoding = "async";
    logoImage.setAttribute("fetchpriority", "high");
    logo.appendChild(logoImage);

    toggle.type = "button";
    toggle.setAttribute("aria-expanded", "false");
    toggle.setAttribute("aria-controls", "brand-site-menu");
    toggle.appendChild(toggleLabel);
    toggle.appendChild(toggleLines);

    drawer.id = "brand-site-menu";
    nav.id = "brand-primary-navigation";
    nav.setAttribute("aria-label", "Основная навигация");

    HEADER_LINKS.forEach(function (item) {
      var link = appendLink(nav, "", item.href, item.label);
      if ((item.current === "blog" && info.kind.indexOf("blog-") === 0) ||
          (item.current === "faq" && info.kind === "faq")) {
        link.setAttribute("aria-current", "page");
      }
    });

    appendLink(actions, "brand-header__phone", "tel:+79104651420", "+7 910 465-14-20");
    var telegram = appendLink(actions, "brand-header__telegram", "https://t.me/stas_kochukov", "Telegram");
    telegram.target = "_blank";
    telegram.rel = "noopener";
    var whatsapp = appendLink(actions, "brand-header__whatsapp", "https://wa.me/79104651420", "WhatsApp");
    whatsapp.target = "_blank";
    whatsapp.rel = "noopener";

    drawer.appendChild(nav);
    drawer.appendChild(actions);
    inner.appendChild(logo);
    inner.appendChild(toggle);
    inner.appendChild(drawer);
    header.appendChild(inner);
    return header;
  }

  function bindHeader(header) {
    var toggle = header.querySelector(".brand-header__toggle");
    var drawer = header.querySelector(".brand-header__drawer");

    if (!toggle || !drawer || header.getAttribute("data-brand-bound") === "true") {
      return;
    }
    header.setAttribute("data-brand-bound", "true");

    function closeMenu(returnFocus) {
      header.classList.remove("is-open");
      toggle.setAttribute("aria-expanded", "false");
      if (returnFocus) {
        toggle.focus();
      }
    }

    toggle.addEventListener("click", function () {
      var willOpen = toggle.getAttribute("aria-expanded") !== "true";
      header.classList.toggle("is-open", willOpen);
      toggle.setAttribute("aria-expanded", willOpen ? "true" : "false");
    });

    drawer.addEventListener("click", function (event) {
      if (event.target.closest && event.target.closest("a")) {
        closeMenu(false);
      }
    });

    document.addEventListener("click", function (event) {
      if (header.classList.contains("is-open") && !header.contains(event.target)) {
        closeMenu(false);
      }
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && header.classList.contains("is-open")) {
        closeMenu(true);
      }
    });
  }

  function ensureHeader(info) {
    var existingBrandHeader = document.querySelector(".brand-header");
    var originalHeader;
    var header;

    if (existingBrandHeader) {
      bindHeader(existingBrandHeader);
      return existingBrandHeader;
    }

    header = createHeader(info);
    originalHeader = document.querySelector("body > header, body > .top");
    if (originalHeader && originalHeader.parentNode) {
      originalHeader.parentNode.replaceChild(header, originalHeader);
    } else if (document.body) {
      document.body.insertBefore(header, document.body.firstChild);
    }
    bindHeader(header);
    return header;
  }

  function createEyebrow(text) {
    var eyebrow = makeElement("span", "brand-eyebrow", text);
    eyebrow.setAttribute("data-brand-generated", "eyebrow");
    return eyebrow;
  }

  function enhanceHero(info) {
    var hero = document.querySelector(".hero");
    var panel;
    var heading;

    if (!hero) {
      return null;
    }

    panel = hero.querySelector(".hero-panel");
    if (!panel) {
      panel = makeElement("div", "hero-panel");
      panel.setAttribute("data-brand-generated", "hero-panel");
      while (hero.firstChild) {
        panel.appendChild(hero.firstChild);
      }
      hero.appendChild(panel);
    }

    heading = panel.querySelector("h1");
    if (heading) {
      if (!heading.id) {
        heading.id = "brand-page-title";
      }
      hero.setAttribute("aria-labelledby", heading.id);
      if (!panel.querySelector(".brand-eyebrow")) {
        panel.insertBefore(createEyebrow(EYEBROWS[info.kind] || EYEBROWS.secondary), heading);
      }
    }
    return hero;
  }

  function directChildrenByClass(root, classNames) {
    var matches = [];
    var child = root ? root.firstElementChild : null;
    while (child) {
      if (classNames.some(function (className) { return child.classList.contains(className); })) {
        matches.push(child);
      }
      child = child.nextElementSibling;
    }
    return matches;
  }

  function getContentRoot(info) {
    if (info.kind === "destination") {
      return document.querySelector(".wrap");
    }
    return document.querySelector("main") || document.querySelector(".wrap");
  }

  function pageHeadingText() {
    var heading = document.querySelector("h1");
    return heading ? heading.textContent.trim() : "Путешествие 3Parusa";
  }

  function makeEditorialFigure() {
    var figure = makeElement("figure", "brand-editorial");
    var image = makeElement("div", "brand-editorial__image");
    var caption = makeElement("figcaption", "", "Жизнь под парусом");
    image.setAttribute("role", "img");
    image.setAttribute("aria-label", "Фотография к странице «" + pageHeadingText() + "»");
    figure.setAttribute("data-brand-generated", "editorial");
    figure.appendChild(image);
    figure.appendChild(caption);
    return figure;
  }

  function insertEditorialImage(info, root) {
    var headings;
    var headingIndex;
    var anchor;
    var following;
    var categories;

    if (!root || root.querySelector(".brand-editorial") || info.kind === "blog-index") {
      return;
    }

    if (info.kind === "faq") {
      categories = root.querySelectorAll(".cat");
      if (categories.length) {
        categories[0].insertAdjacentElement("afterend", makeEditorialFigure());
      }
      return;
    }

    headings = Array.prototype.filter.call(root.querySelectorAll("h2"), function (heading) {
      return heading.parentElement === root;
    });
    if (!headings.length) {
      return;
    }

    headingIndex = info.kind === "destination" ? 0 : Math.min(1, headings.length - 1);
    anchor = headings[headingIndex];
    following = anchor.nextElementSibling;
    if (following && !/^(H1|H2|H3|SECTION)$/i.test(following.tagName) &&
        !following.classList.contains("cta") && !following.classList.contains("box")) {
      anchor = following;
    }
    anchor.insertAdjacentElement("afterend", makeEditorialFigure());
  }

  function makeGallery() {
    var gallery = makeElement("section", "brand-gallery");
    var label = makeElement("div", "brand-gallery__label", "Моменты путешествия");
    var grid = makeElement("div", "brand-gallery__grid");
    var index;

    gallery.setAttribute("data-brand-generated", "gallery");
    gallery.setAttribute("aria-label", "Фотографии путешествий 3Parusa");
    for (index = 1; index <= 3; index += 1) {
      var item = makeElement("div", "brand-gallery__item");
      item.setAttribute("role", "img");
      item.setAttribute("aria-label", "Путешествие под парусом, фотография " + index);
      grid.appendChild(item);
    }
    gallery.appendChild(label);
    gallery.appendChild(grid);
    return gallery;
  }

  function insertGallery(info, root) {
    var candidates;
    var target;

    if (!root || root.querySelector(".brand-gallery") ||
        info.kind === "privacy" || info.kind === "not-found" || info.kind === "secondary") {
      return;
    }

    candidates = directChildrenByClass(root, ["cta", "box"]);
    target = candidates.length ? candidates[candidates.length - 1] : null;
    if (target) {
      root.insertBefore(makeGallery(), target);
    } else {
      root.appendChild(makeGallery());
    }
  }

  function slugFromHref(href) {
    try {
      return slugFromPath(normalisePath(new URL(href, window.location.origin).pathname));
    } catch (error) {
      return "article";
    }
  }

  function articleImage(slug, index) {
    return ARTICLE_HERO_IMAGES[slug] || LIFESTYLE_IMAGES[index % LIFESTYLE_IMAGES.length];
  }

  function enhanceBlogIndex(info) {
    var main;
    var list;

    if (info.kind !== "blog-index") {
      return;
    }
    main = document.querySelector("main");
    list = main ? main.querySelector("ul") : null;
    if (!list || list.getAttribute("data-brand-cards") === "true") {
      return;
    }

    list.setAttribute("data-brand-cards", "true");
    list.classList.add("brand-blog-grid");
    Array.prototype.forEach.call(list.children, function (item, index) {
      var link = item.querySelector("a[href]");
      var media;
      var title;
      var meta;
      var slug;
      var nodes;

      if (!link) {
        return;
      }
      item.classList.add("brand-blog-card");
      link.classList.add("brand-blog-card__link");
      slug = slugFromHref(link.getAttribute("href"));
      media = makeElement("span", "brand-blog-card__media");
      media.setAttribute("aria-hidden", "true");
      media.style.setProperty("--brand-card-image", cssImage(articleImage(slug, index)));
      title = makeElement("span", "brand-blog-card__title");
      meta = makeElement("span", "brand-blog-card__meta", "Бортовой журнал");

      nodes = Array.prototype.slice.call(link.childNodes);
      nodes.forEach(function (node) {
        title.appendChild(node);
      });
      link.appendChild(media);
      link.appendChild(title);
      link.appendChild(meta);
    });
  }

  function enhanceUtilityPage(info) {
    var root;
    var heading;
    var card;
    var child;

    if (info.kind === "privacy") {
      root = document.querySelector(".wrap");
      heading = root ? root.querySelector("h1") : null;
      if (root && heading && !root.querySelector(".brand-eyebrow")) {
        root.insertBefore(createEyebrow(EYEBROWS.privacy), heading);
      }
      return;
    }

    if (info.kind !== "not-found") {
      return;
    }
    child = document.body ? document.body.firstElementChild : null;
    while (child) {
      if (child.tagName === "DIV" && !child.classList.contains("float-contacts")) {
        card = child;
        break;
      }
      child = child.nextElementSibling;
    }
    if (!card) {
      return;
    }
    card.classList.add("brand-not-found");
    if (!card.querySelector(".brand-eyebrow")) {
      card.insertBefore(createEyebrow(EYEBROWS["not-found"]), card.firstChild);
    }
  }

  function initialise() {
    var body = document.body;
    var info;
    var imagePlan;
    var contentRoot;

    if (!body || body.getAttribute("data-brand-enhanced") === "true") {
      return;
    }
    info = classifyPage(window.location.pathname);
    if (!info) {
      return;
    }

    body.setAttribute("data-brand-enhanced", "true");
    body.setAttribute("data-page-kind", info.kind);
    body.classList.add("brand-enhanced", "brand-kind-" + info.kind);
    document.documentElement.classList.add("brand-enhanced-root");

    imagePlan = buildImagePlan(info);
    setImageVariables(imagePlan);
    ensureHeader(info);
    enhanceHero(info);
    enhanceBlogIndex(info);
    enhanceUtilityPage(info);

    contentRoot = getContentRoot(info);
    insertEditorialImage(info, contentRoot);
    insertGallery(info, contentRoot);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initialise, { once: true });
  } else {
    initialise();
  }
}());
