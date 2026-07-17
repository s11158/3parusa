# -*- coding: utf-8 -*-
"""Генерирует /faq.html (RU) с FAQPage JSON-LD + патчит sitemap и llms.txt."""
import io, os, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

QA = [
("💰 Цена и оплата", [
("Сколько стоит тур на яхте?", "Место в каюте — от €1 100 за неделю, каюта целиком (на двоих) — от €2 200. Вся яхта (4 каюты, до 8 гостей) — от €6 700 за неделю. Экзотика (Сейшелы, Карибы) — от €12 000. Точная цена зависит от страны, сезона и яхты — напишите, посчитаю под ваши даты."),
("Что входит в стоимость?", "Каюта DBL с собственным санузлом, авторский маршрут, работа капитана, постельное бельё и полотенца, WiFi (60 ГБ), трансфер аэропорт—марина и наша поддержка 24/7."),
("Что оплачивается отдельно?", "Авиаперелёт и судовая касса — общие расходы на борту: питание, топливо, стоянки в маринах. Собираем её в начале тура, в конце показываю полный расчёт по чекам. По желанию: повар (€1 200), фотограф (€1 000), SUP (€100), удочка (€75)."),
("Как можно оплатить?", "Как вам удобнее: наличные (евро, доллары, лиры), перевод, рубли на российскую карту, крипта (USDT). Карты «Мир» за границей работают через раз — лучше иметь запас наличных, остальное решим."),
("Что за страховой депозит?", "Возвратный залог чартерной компании за яхту (≈€500 с человека). Если с лодкой всё в порядке — возвращается полностью. Часто вместо депозита можно купить полную страховку (~€330 на яхту) — тогда замораживать ничего не нужно; подскажу, что выгоднее в вашем случае."),
]),
("📅 Даты и бронирование", [
("Как забронировать место?", "Пишете нам → подбираем тур и каюту → предоплата фиксирует место → остаток до старта. Всё прозрачно: суммы, сроки и что куда идёт — проговариваем сразу."),
("Можно ли оплатить в рассрочку?", "Да, разбиваем оплату на части до начала тура."),
("Что, если я не смогу поехать?", "Обсуждаем индивидуально: можно передать место, перенести на другие даты или найти замену — стараемся, чтобы никто не потерял деньги."),
]),
("🛏 Каюты и яхта", [
("Что за яхта?", "VIP-катамаран 100–150 м²: 4 каюты-«отельных номера», каждая со своим санузлом и душем, несколько палуб, зоны для отдыха. Ход ровный и устойчивый — это не «болтанка на яхточке»."),
("Мы пара — у нас будет своя каюта?", "Да, каюта только ваша, с собственным санузлом. Уединение на борту — легко: палуб и уголков хватает."),
]),
("🍽 Питание", [
("Как устроено питание на борту?", "Завтраки и часть обедов готовим на борту (продукты — из судовой кассы), ужины — чаще в прибрежных ресторанчиках с местной кухней: рыбный рынок в Фетхие, устрицы в Стоне, винодельни. Можно взять повара на борт (€1 200/нед) — тогда вообще ни о чём думать не надо."),
("У меня аллергия или особая диета — как быть?", "Пишите заранее — учтём при закупке продуктов и выборе ресторанов."),
]),
("✈️ Дорога и документы", [
("Как добраться и встретят ли меня?", "Вы покупаете перелёт, всё остальное — наше: встречаем в аэропорту, довозим до марины и обратно (трансфер включён)."),
("Нужна ли виза?", "Зависит от направления: Турция — без визы, Европа — шенген, Сейшелы/Таиланд — штамп по прилёту. Перед туром присылаю памятку под вашу страну."),
("Нужна ли страховка?", "Да, обычная туристическая страховка нужна каждому гостю — оформляется за один день онлайн. Подскажу проверенные варианты."),
]),
("🎒 Что взять с собой", [
("Какие вещи брать на яхту?", "Мягкую сумку (не чемодан — его некуда ставить), купальники, лёгкие вещи, ветровку на вечер, обувь со светлой подошвой для палубы, крем SPF, головной убор. Полотенца и бельё уже на борту. Перед туром пришлю полный чек-лист."),
]),
("⛵ Опыт и безопасность", [
("Я ни разу не был(а) на яхте. Справлюсь?", "Конечно! Опыт не нужен вообще: всю работу делает капитан, вы — отдыхаете. Захотите — научу стоять за штурвалом и работать с парусами; не захотите — просто загорайте."),
("А если укачает?", "Мы специально строим маршруты короткими переходами: больше стоим в бухтах, купаемся и загораем, чем идём. На стоянках качки нет. Морская болезнь сегодня решается легко — таблетки, браслеты, да и ром на закате ещё никто не отменял 🙂 Для чувствительных подбираем самый «лайтовый» маршрут."),
("Это безопасно?", "Капитан — лицензированный (IYT/ICC), за плечами 20 000+ миль и 100+ туров. Маршруты только по проверенным акваториям с учётом прогноза. Для новичков выбираем закрытые спокойные акватории."),
]),
("🌤 Погода и сезон", [
("Когда лучше ехать?", "Турция и Греция — май–октябрь (бархатный сезон в Турции — сентябрь–ноябрь, для новичков в мае лучше всего Турция). Сейшелы и Таиланд — наша зима. Под ваши даты подскажу, где в это время лучшее море."),
]),
("👨‍👩‍👧 Дети", [
("Можно ли с детьми?", "Нужно! Семейные туры — наш любимый формат: 50% спокойного отдыха, 50% программы для детей, и компанию подбираем так, чтобы на борту были другие семьи с детьми. Детские жилеты и постоянный присмотр — само собой."),
]),
]

METRICA = """<script type="text/javascript">(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window, document, "script", "https://mc.yandex.ru/metrika/tag.js", "ym");ym(110049558, 'init', {ssr:true, webvisor:true, clickmap:true, ecommerce:"dataLayer", accurateTrackBounce:true, trackLinks:true});</script><noscript><div><img src="https://mc.yandex.ru/watch/110049558" style="position:absolute; left:-9999px;" alt="" /></div></noscript>"""

schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
    for _, items in QA for q, a in items]}

sections = []
for title, items in QA:
    block = "<h2>%s</h2>" % title
    for q, a in items:
        block += '<h3 class="q">%s</h3><p>%s</p>' % (q, a)
    sections.append(block)
body = "\n".join(sections)

html = """<!DOCTYPE html><html lang="ru"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Вопросы и ответы о яхтенных турах — FAQ | 3Parusa</title>
<meta name="description" content="21 самый частый вопрос о турах на яхте: цены, оплата, каюты, питание, визы, укачивание, дети, безопасность. Отвечает капитан Стас Кочуков.">
<link rel="canonical" href="https://3parusa.ru/faq.html">
<meta property="og:title" content="Вопросы и ответы о яхтенных турах — FAQ | 3Parusa"><meta property="og:description" content="21 самый частый вопрос о турах на яхте: цены, оплата, каюты, питание, визы, укачивание, дети, безопасность."><meta property="og:type" content="website">
<script type="application/ld+json">%s</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&family=Inter:wght@300;400;500;600&display=swap&subset=cyrillic" rel="stylesheet">
<style>
:root{--dark:#191f28;--navy:#06112a;--gold:#d3aa31;--gold2:#d6a000;--sand:#eddba6;--txt:#454545;--bg2:#f8f8f8}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Inter',Arial,sans-serif;font-weight:300;color:var(--txt);line-height:1.7;background:#fff}
h1,h2,h3,.logo{font-family:'Montserrat',Arial,sans-serif}
header{background:#fff;padding:16px 24px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;border-bottom:1px solid #eee;position:sticky;top:0;z-index:10}
header a.logo{color:var(--dark);font-size:21px;text-decoration:none;font-weight:700;letter-spacing:.5px}
header nav a{color:var(--dark);text-decoration:none;margin-left:18px;font-size:14px;font-weight:500;font-family:'Montserrat',Arial,sans-serif}
header nav a:hover{color:var(--gold2)}
.hero{background:var(--dark);color:#fff;padding:64px 20px 52px;text-align:center}
.hero h1{font-size:clamp(26px,4.5vw,44px);font-weight:700;max-width:860px;margin:0 auto 16px;line-height:1.25}
.hero p{max-width:680px;margin:0 auto;font-size:18px;font-weight:300;color:#d9dee6}
.cta{display:inline-block;margin-top:26px;background:var(--gold);color:var(--dark);padding:16px 42px;border-radius:100px;text-decoration:none;font-weight:600;font-family:'Montserrat',Arial,sans-serif;font-size:15px;transition:background .2s}
.cta:hover{background:var(--gold2)}
main{max-width:740px;margin:0 auto;padding:40px 20px 20px}
main h2{color:var(--dark);margin:36px 0 10px;font-size:25px;font-weight:600}
main h3.q{color:var(--navy);margin:20px 0 6px;font-size:18px;font-weight:600}
main p, main li{font-size:17px;margin-bottom:12px}
main a{color:var(--gold2)}
.box{background:var(--bg2);border-left:4px solid var(--gold);padding:18px 20px;border-radius:8px;margin:22px 0}
footer{background:var(--dark);color:#aab3bf;text-align:center;padding:30px 20px;margin-top:48px;font-size:14px}
footer a{color:var(--sand);text-decoration:none}
</style>%s</head><body>
<header><a class="logo" href="/">⛵ 3Parusa</a><nav><a href="/#rec">Туры</a><a href="/blog/">Блог</a><a href="/faq.html">FAQ</a><a href="https://t.me/stas_kochukov">Telegram</a></nav></header>
<div class="hero"><h1>Вопросы и ответы</h1><p>21 вопрос, которые мне задают гости десять лет подряд. Ответы — из 10 000+ реальных переписок, слово в слово как я отвечаю лично.</p><a class="cta" href="https://wa.me/79104651420">Задать свой вопрос</a></div>
<main>%s
<div class="box"><b>Остались вопросы? Напишите капитану напрямую:</b> <a href="https://wa.me/79104651420">WhatsApp +7 910 465-14-20</a> · <a href="https://t.me/stas_kochukov">Telegram @stas_kochukov</a>. Отвечаю сам. — Стас Кочуков, капитан 3Parusa</div>
<p>Подробные разборы — в <a href="/blog/">блоге капитана</a>: <a href="/blog/skolko-stoit-tur-na-yahte.html">сколько стоит тур</a>, <a href="/blog/kak-oplatit-tur-iz-rossii.html">как оплатить из России</a>, <a href="/blog/sudovaya-kassa-chto-eto.html">судовая касса</a>, <a href="/blog/ukachivaet-li-na-katamarane.html">про укачивание</a>.</p>
</main>
<footer>3Parusa — авторские яхтенные туры по всему миру · 20 000 миль · 20+ стран · 1000 довольных гостей<br><a href="/">3parusa.ru</a> · <a href="/privacy.html">Политика конфиденциальности</a></footer>
</body></html>""" % (json.dumps(schema, ensure_ascii=False), METRICA, body)

io.open(os.path.join(ROOT, "faq.html"), "w", encoding="utf-8", newline="\n").write(html)

sm_path = os.path.join(ROOT, "sitemap.xml")
sm = io.open(sm_path, encoding="utf-8").read()
if "3parusa.ru/faq.html" not in sm:
    sm = sm.replace("</urlset>", "<url><loc>https://3parusa.ru/faq.html</loc></url></urlset>")
    io.open(sm_path, "w", encoding="utf-8", newline="\n").write(sm)

llms_path = os.path.join(ROOT, "llms.txt")
llms = io.open(llms_path, encoding="utf-8").read()
if "3parusa.ru/faq.html" not in llms:
    llms = llms.rstrip("\n") + "\n- FAQ (21 вопрос-ответ): https://3parusa.ru/faq.html\n"
    io.open(llms_path, "w", encoding="utf-8", newline="\n").write(llms)
print("faq ok")
