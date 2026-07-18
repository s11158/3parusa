# -*- coding: utf-8 -*-
"""Генерирует /faq.html (RU): FAQPage JSON-LD, фирменный стиль главной, аккордеон.
Голос — «мы / наша команда» (компания, не один человек). Без морского сленга.
Также патчит sitemap.xml и llms.txt."""
import io, os, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERO = "/assets/static.tildacdn.com/tild3662-3766-4663-a466-383465653737/_.jpg"

QA = [
("💰", "Цена и оплата", [
("Сколько стоит тур на яхте?", "Место в каюте — от €1 100 за неделю, каюта целиком (на двоих) — от €2 200. Вся яхта (4 каюты, до 8 гостей) — от €6 700 за неделю. Дальние направления (Сейшелы, Карибы) — от €12 000. Точная цена зависит от страны, сезона и яхты — напишите нам, и мы посчитаем под ваши даты."),
("Что входит в стоимость?", "Двухместная каюта с собственным санузлом, продуманный маршрут, работа капитана, постельное бельё и полотенца, WiFi (60 ГБ), трансфер аэропорт—марина и наша поддержка 24/7."),
("Что оплачивается отдельно?", "Авиаперелёт и судовая касса — это общие расходы на борту: еда, топливо, стоянки в портах. Собираем её в начале тура, а в конце показываем полный расчёт по чекам. По желанию: повар (€1 200), фотограф (€1 000), сапборд (€100), удочка (€75)."),
("Как можно оплатить?", "Как вам удобнее: наличными (евро, доллары, турецкие лиры), банковским переводом, рублями на российскую карту или криптовалютой (USDT). Карты «Мир» за границей работают не везде — лучше иметь с собой запас наличных, остальное подскажем."),
("Что такое страховой депозит?", "Это возвратный залог за яхту, который берёт компания-владелец лодки (около €500 с человека). Если с яхтой всё в порядке — а так почти всегда — залог возвращается полностью. Часто вместо залога можно оформить страховку (примерно €330 на всю яхту) — тогда замораживать деньги не нужно. Подскажем, что выгоднее в вашем случае."),
]),
("📅", "Даты и бронирование", [
("Как забронировать место?", "Вы пишете нам → мы подбираем тур и каюту → предоплата закрепляет за вами место → остаток вносится до старта. Всё прозрачно: суммы, сроки и что за что — проговариваем сразу."),
("Можно ли оплатить в рассрочку?", "Да, оплату можно разбить на части до начала тура."),
("Что, если я не смогу поехать?", "Решаем индивидуально: можно передать своё место другому человеку, перенести поездку на другие даты или найти замену — мы стараемся, чтобы никто не потерял деньги."),
]),
("🛏", "Каюты и яхта", [
("Что за яхта?", "Это VIP-катамаран площадью 100–150 м²: четыре каюты уровня хорошего отельного номера, у каждой свой санузел с душем, несколько палуб и зон для отдыха. Катамаран идёт ровно и устойчиво — это не качка, как на маленькой лодке."),
("Мы пара — у нас будет своя каюта?", "Да, каюта будет только вашей, с отдельным санузлом. Уединиться на борту легко — палуб и укромных уголков хватает."),
]),
("🍽", "Питание", [
("Как устроено питание на борту?", "Завтраки и часть обедов готовим прямо на яхте (продукты берём из судовой кассы), а ужинать чаще ходим в прибрежные ресторанчики с местной кухней. Можно взять на борт повара (€1 200 за неделю) — тогда о еде вообще можно не думать."),
("У меня аллергия или особая диета — как быть?", "Напишите нам заранее — учтём это при закупке продуктов и выборе ресторанов."),
]),
("✈️", "Дорога и документы", [
("Как добраться и встретят ли меня?", "Вы покупаете авиабилеты, всё остальное — на нас: встречаем в аэропорту, довозим до причала и обратно (трансфер включён в стоимость)."),
("Нужна ли виза?", "Зависит от направления: Турция — без визы, Европа — по шенгену, Сейшелы и Таиланд — штамп прямо по прилёту. Перед поездкой пришлём памятку под вашу страну."),
("Нужна ли страховка?", "Да, обычная туристическая страховка нужна каждому гостю — её можно оформить онлайн за один день. Подскажем проверенные варианты."),
]),
("🎒", "Что взять с собой", [
("Какие вещи брать на яхту?", "Мягкую сумку вместо чемодана (чемодан на яхте некуда ставить), купальники, лёгкую одежду, ветровку на вечер, обувь на светлой мягкой подошве для палубы, крем от солнца и головной убор. Полотенца и бельё уже есть на борту. Перед поездкой пришлём полный список."),
]),
("⛵", "Опыт и безопасность", [
("Я ни разу не был(а) на яхте. Справлюсь?", "Конечно! Опыт не нужен совсем: всю работу с яхтой делает капитан, а вы отдыхаете. Захотите — научим стоять за штурвалом и управлять парусами; не захотите — просто загорайте."),
("А если укачает?", "Мы специально строим маршрут короткими переходами: больше времени стоим в бухтах, купаемся и загораем, чем плывём. На стоянке качки нет вообще. С морской болезнью сегодня легко справиться — есть таблетки и специальные браслеты. А для тех, кто переживает, подбираем самый спокойный маршрут по закрытым бухтам."),
("Это безопасно?", "Капитан — с международной лицензией (IYT/ICC), за плечами больше 20 000 морских миль и 100+ проведённых туров. Маршрут прокладываем только по проверенным местам и всегда сверяемся с прогнозом погоды. Для новичков выбираем спокойные закрытые бухты."),
]),
("🌤", "Погода и сезон", [
("Когда лучше ехать?", "Турция и Греция — с мая по октябрь (бархатный сезон в Турции — сентябрь–ноябрь; новичкам приятнее всего май в Турции). Сейшелы и Таиланд — наша зима. Скажите свои даты — подскажем, где в это время самое лучшее море."),
]),
("👨‍👩‍👧", "Дети", [
("Можно ли с детьми?", "Не только можно — нужно! Семейные туры — наш любимый формат: половина времени спокойный отдых, половина — программа для детей. Компанию подбираем так, чтобы на борту были и другие семьи с детьми. Детские спасательные жилеты и постоянный присмотр — само собой."),
]),
]

METRICA = """<script type="text/javascript">(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window, document, "script", "https://mc.yandex.ru/metrika/tag.js", "ym");ym(110049558, 'init', {ssr:true, webvisor:true, clickmap:true, ecommerce:"dataLayer", accurateTrackBounce:true, trackLinks:true});</script><noscript><div><img src="https://mc.yandex.ru/watch/110049558" style="position:absolute; left:-9999px;" alt="" /></div></noscript>"""

schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
    for _, _, items in QA for q, a in items]}

# навигация-чипсы + секции-аккордеоны
chips, sections = [], []
for i, (emoji, title, items) in enumerate(QA):
    cid = "cat%d" % i
    chips.append('<a class="chip" href="#%s">%s %s</a>' % (cid, emoji, title))
    block = '<section id="%s" class="cat"><h2><span class="ce">%s</span>%s</h2>' % (cid, emoji, title)
    for q, a in items:
        block += '<details class="qa"><summary>%s</summary><div class="a"><p>%s</p></div></details>' % (q, a)
    block += '</section>'
    sections.append(block)
chips_html = "\n".join(chips)
body = "\n".join(sections)

html = """<!DOCTYPE html><html lang="ru"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Вопросы и ответы о яхтенных турах — FAQ | 3Parusa</title>
<meta name="description" content="21 самый частый вопрос о турах на яхте: цены, оплата, каюты, питание, визы, укачивание, дети, безопасность. Простые ответы от команды 3Parusa.">
<link rel="canonical" href="https://3parusa.ru/faq.html">
<link rel="alternate" hreflang="ru" href="https://3parusa.ru/faq.html">
<link rel="alternate" hreflang="en" href="https://3parusa.com/faq.html">
<meta property="og:title" content="Вопросы и ответы о яхтенных турах — FAQ | 3Parusa"><meta property="og:description" content="21 самый частый вопрос о турах на яхте: цены, оплата, каюты, питание, визы, укачивание, дети, безопасность."><meta property="og:type" content="website"><meta property="og:image" content="https://3parusa.ru@@HERO@@">
<script type="application/ld+json">@@SCHEMA@@</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&family=Inter:wght@300;400;500;600&display=swap&subset=cyrillic" rel="stylesheet">
<style>
:root{--dark:#191f28;--navy:#06112a;--gold:#d3aa31;--gold2:#d6a000;--sand:#eddba6;--txt:#454545;--bg2:#f8f8f8}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Inter',Arial,sans-serif;font-weight:300;color:var(--txt);line-height:1.7;background:#fff}
h1,h2,h3,.logo,summary,.chip{font-family:'Montserrat',Arial,sans-serif}
header{background:#fff;padding:16px 24px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;border-bottom:1px solid #eee;position:sticky;top:0;z-index:20}
header a.logo{color:var(--dark);font-size:21px;text-decoration:none;font-weight:700;letter-spacing:.5px}
header nav a{color:var(--dark);text-decoration:none;margin-left:18px;font-size:14px;font-weight:500;font-family:'Montserrat',Arial,sans-serif}
header nav a:hover,header nav a.active{color:var(--gold2)}
.hero{position:relative;color:#fff;padding:88px 20px 78px;text-align:center;background:linear-gradient(rgba(15,20,28,.62),rgba(15,20,28,.72)),url('@@HERO@@') center/cover no-repeat}
.hero h1{font-size:clamp(28px,5vw,46px);font-weight:700;max-width:860px;margin:0 auto 16px;line-height:1.22;text-shadow:0 2px 18px rgba(0,0,0,.35)}
.hero p{max-width:640px;margin:0 auto;font-size:18px;font-weight:300;color:#eef1f5}
.cta{display:inline-block;margin-top:28px;background:var(--gold);color:var(--dark);padding:16px 42px;border-radius:100px;text-decoration:none;font-weight:600;font-family:'Montserrat',Arial,sans-serif;font-size:15px;transition:background .2s}
.cta:hover{background:var(--gold2)}
.nav{position:sticky;top:59px;z-index:15;background:#fff;border-bottom:1px solid #eee;padding:14px 16px}
.nav-in{max-width:900px;margin:0 auto;display:flex;flex-wrap:wrap;gap:9px;justify-content:center}
.chip{font-size:13px;font-weight:500;color:var(--dark);text-decoration:none;border:1px solid #e3d9bf;background:#fbf7ea;padding:7px 15px;border-radius:100px;transition:all .18s}
.chip:hover{background:var(--gold);border-color:var(--gold)}
main{max-width:760px;margin:0 auto;padding:44px 20px 20px}
.cat{margin-bottom:34px;scroll-margin-top:130px}
.cat h2{color:var(--dark);font-size:24px;font-weight:600;display:flex;align-items:center;gap:12px;margin-bottom:14px;padding-bottom:10px;border-bottom:2px solid #f0ead7}
.cat h2 .ce{font-size:26px}
.qa{border:1px solid #ececec;border-radius:12px;margin-bottom:12px;background:#fff;overflow:hidden;transition:box-shadow .2s,border-color .2s}
.qa[open]{border-color:var(--gold);box-shadow:0 6px 22px rgba(25,31,40,.07)}
.qa summary{list-style:none;cursor:pointer;padding:18px 52px 18px 22px;font-size:17px;font-weight:600;color:var(--navy);position:relative;user-select:none}
.qa summary::-webkit-details-marker{display:none}
.qa summary::after{content:"+";position:absolute;right:20px;top:50%;transform:translateY(-50%);font-size:24px;font-weight:400;color:var(--gold2);transition:transform .2s}
.qa[open] summary::after{content:"–";transform:translateY(-50%) rotate(0)}
.qa summary:hover{color:var(--gold2)}
.qa .a{padding:0 22px 20px}
.qa .a p{font-size:16.5px;margin:0;color:var(--txt)}
.box{background:var(--bg2);border-left:4px solid var(--gold);padding:20px 22px;border-radius:8px;margin:30px 0 8px}
.box b{color:var(--dark)}
.more{font-size:15.5px;margin-top:18px}
footer{background:var(--dark);color:#aab3bf;text-align:center;padding:30px 20px;margin-top:44px;font-size:14px}
footer a{color:var(--sand);text-decoration:none}
@media(max-width:640px){.hero{padding:64px 18px 56px}.nav{top:57px}.cat{scroll-margin-top:150px}.qa summary{font-size:16px;padding:16px 46px 16px 18px}}
</style>@@METRICA@@</head><body>
<header><a class="logo" href="/">⛵ 3Parusa</a><nav><a href="/#rec">Туры</a><a href="/blog/">Блог</a><a href="/faq.html" class="active">FAQ</a><a href="https://t.me/stas_kochukov">Telegram</a></nav></header>
<div class="hero"><h1>Вопросы и ответы</h1><p>21 вопрос, который нам задают чаще всего. Ответы — из тысяч реальных переписок с нашими гостями, простыми словами и по делу.</p><a class="cta" href="https://wa.me/79104651420">Задать свой вопрос</a></div>
<div class="nav"><div class="nav-in">@@CHIPS@@</div></div>
<main>@@BODY@@
<div class="box"><b>Остались вопросы?</b> Напишите нам напрямую — отвечаем быстро и по делу: <a href="https://wa.me/79104651420">WhatsApp +7 910 465-14-20</a> · <a href="https://t.me/stas_kochukov">Telegram @stas_kochukov</a>. — Команда 3Parusa
<p class="more">Хотите подробнее? Загляните в <a href="/blog/">блог</a>: <a href="/blog/skolko-stoit-tur-na-yahte.html">сколько стоит тур</a>, <a href="/blog/kak-oplatit-tur-iz-rossii.html">как оплатить из России</a>, <a href="/blog/sudovaya-kassa-chto-eto.html">что такое судовая касса</a>, <a href="/blog/ukachivaet-li-na-katamarane.html">про укачивание</a>.</p></div>
</main>
<footer>3Parusa — авторские яхтенные туры по всему миру · 20 000 миль · 20+ стран · 1000 довольных гостей<br><a href="/">3parusa.ru</a> · <a href="/privacy.html">Политика конфиденциальности</a></footer>
</body></html>"""
html = (html.replace("@@SCHEMA@@", json.dumps(schema, ensure_ascii=False))
            .replace("@@METRICA@@", METRICA).replace("@@CHIPS@@", chips_html)
            .replace("@@BODY@@", body).replace("@@HERO@@", HERO))

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
print("faq ru ok")
