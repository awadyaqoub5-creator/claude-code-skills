"""Builds the blog: blog/index.html + blog/<slug>.html from blog/data/*.json."""
import json, glob, os, html, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
TITLE_TAG = "خبير الذكاء الاصطناعي"

posts = []
for f in sorted(glob.glob(os.path.join(HERE, "data", "batch-*.json"))):
    posts += json.load(open(f, encoding="utf-8"))

# Paperclip guide lives on its own site
EXTERNAL = [{
    "slug": None, "url": "https://awadyaqoub5-creator.github.io/paperclip-guide/",
    "title": "Paperclip: شغّل فريق agents كأنك صاحب شركة", "tag": "Claude Code", "minutes": 8,
    "summary": "دليل كامل: تثبيت Paperclip، كتابة هدف الشركة، تعيين الفريق، وحط ميزانية وموافقات قبل أول تشغيل.",
    "img": "../img/agents-team-768.webp",
}]

# real publish date of these batches (from git); give later articles their own "date" in the JSON
SITE = "https://awadyaqoub5-creator.github.io/claude-code-skills/"
PUBLISHED = datetime.date(2026, 11, 21)
MONTHS = ["يناير","فبراير","مارس","أبريل","مايو","يونيو","يوليو","أغسطس","سبتمبر","أكتوبر","نوفمبر","ديسمبر"]
def ar_date(d): return f"{d.day} {MONTHS[d.month-1]} {d.year}"

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;700&family=Readex+Pro:wght@500;700&family=JetBrains+Mono:wght@400;600&display=swap">'

TT = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M16.6 5.8A4.3 4.3 0 0 1 15.5 3h-3.1v12.4a2.6 2.6 0 1 1-2.6-2.6c.3 0 .5 0 .8.1V9.7a5.7 5.7 0 1 0 4.9 5.7V9.1a7.4 7.4 0 0 0 4.3 1.4V7.4a4.3 4.3 0 0 1-3.2-1.6z"/></svg>'
WA = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.9 11.9 0 0 0 4.5 4c1.7.7 2.4.8 3.2.7a2.8 2.8 0 0 0 1.8-1.3 2.3 2.3 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3z"/></svg>'
PH = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.2 11.4 11.4 0 0 0 3.6.6 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1 11.4 11.4 0 0 0 .6 3.6 1 1 0 0 1-.3 1z"/></svg>'
SOCIAL = f'''<div class="social">
      <a class="soc tt" href="https://www.tiktok.com/@yaqoubaldhafeeri1" target="_blank" rel="noopener">{TT}تيك توك</a>
      <a class="soc wa" href="https://wa.me/966544956205" target="_blank" rel="noopener">{WA}واتساب</a>
      <a class="soc ph" href="tel:+966544956205">{PH}اتصال</a>
    </div>'''

def head(title, desc, path, img, published=None):
    url, image = SITE + path, SITE + img
    ld = {"@context": "https://schema.org", "@type": "BlogPosting" if published else "Blog",
          "headline": title.split(" | ")[0], "description": desc, "url": url, "image": image, "inLanguage": "ar",
          "author": {"@type": "Person", "name": "يعقوب الظفيري", "url": SITE}}
    if published:
        ld["datePublished"] = published
    ld_json = json.dumps(ld, ensure_ascii=False).replace("<", chr(92) + "u003c")
    return f'''<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{"article" if published else "website"}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{image}">
<script type="application/ld+json">{ld_json}</script>
{FONTS}
<link rel="stylesheet" href="blog.css">
</head>
<body>'''

def header(active):
    blog = ' aria-current="page"' if active == "blog" else ""
    return f'''
  <header class="top">
    <a class="brand" href="../"><img src="../img/yaqoub.webp" width="42" height="42" alt=""><span>يعقوب الظفيري<small>{TITLE_TAG}</small></span></a>
    <nav aria-label="روابط الموقع"><a href="../">الأدوات</a><a href="./"{blog}>المدونة</a></nav>
  </header>'''

AUTHOR = f'''
  <section class="author" aria-label="عن الكاتب">
    <img src="../img/yaqoub.webp" width="96" height="96" alt="صورة يعقوب الظفيري" loading="lazy">
    <div>
      <h2>يعقوب الظفيري</h2>
      <p>{TITLE_TAG}. أشرح أدوات الذكاء الاصطناعي بالعربي وبشكل عملي.</p>
      {SOCIAL}
    </div>
  </section>'''

FOOTER = f'''
  <footer><span><strong>يعقوب الظفيري</strong> · {TITLE_TAG}</span><span>© 2026</span></footer>'''

# --- article pages
for i, p in enumerate(posts):
    p["img"] = f"img/{p['slug']}-640.webp"
    d = datetime.date.fromisoformat(p["date"]) if p.get("date") else PUBLISHED
    p["iso"] = d.isoformat()
    p["date"] = ar_date(d)
    page = head(f"{p['title']} | يعقوب الظفيري", p["summary"], "blog/" + p["slug"] + ".html", "blog/img/" + p["slug"] + ".webp", p["iso"]) + f'''
<div class="wrap">{header("post")}
  <article>
    <div class="meta"><span class="tag">{html.escape(p["tag"])}</span><span>{p["date"]}</span><span>قراءة {p["minutes"]} دقائق</span></div>
    <h1>{html.escape(p["title"])}</h1>
    <p class="lead">{html.escape(p["summary"])}</p>
    <img class="cover" src="img/{p["slug"]}.webp" srcset="img/{p["slug"]}-640.webp 640w, img/{p["slug"]}.webp 1280w" sizes="(max-width:760px) 100vw, 760px" width="1280" height="716" alt="">
    {p["body"]}
    <a class="back" href="./">→ رجوع لكل المقالات</a>
  </article>{AUTHOR}{FOOTER}
</div>
</body>
</html>
'''
    open(os.path.join(HERE, p["slug"] + ".html"), "w", encoding="utf-8").write(page)

# --- index
cards = []
for p in EXTERNAL + posts:
    url = p.get("url") or (p["slug"] + ".html")
    ext = ' target="_blank" rel="noopener"' if p.get("url") else ""
    visual = f'<img src="{p["img"]}" alt="" loading="lazy" width="640" height="358">' if p.get("img") else f'<div class="ph" aria-hidden="true">AI</div>'
    meta = f'<span class="tag">{html.escape(p["tag"])}</span><span>قراءة {p["minutes"]} دقائق</span>'
    cards.append(f'''    <li class="post" data-tag="{html.escape(p["tag"])}"><a href="{url}"{ext}>{visual}<div class="b"><div class="meta">{meta}</div><h2>{html.escape(p["title"])}</h2><p>{html.escape(p["summary"])}</p><span class="more">اقرأ المقال ←</span></div></a></li>''')

tags = []
for p in EXTERNAL + posts:
    if p["tag"] not in tags: tags.append(p["tag"])
chips = '<button class="chip" type="button" data-f="all" aria-pressed="true">الكل</button>' + "".join(
    f'<button class="chip" type="button" data-f="{html.escape(t)}" aria-pressed="false">{html.escape(t)}</button>' for t in tags)

index = head("مدونة الذكاء الاصطناعي | يعقوب الظفيري", "مقالات عملية بالعربي عن Claude وأدوات الذكاء الاصطناعي.", "blog/", "img/agents-team-768.webp") + f'''
<style>
.chips{{display:flex;gap:8px;flex-wrap:wrap;margin-top:22px}}
.chip{{font:500 14px var(--f-body);color:var(--fg);background:var(--surface);border:1px solid var(--line);border-radius:999px;min-height:40px;padding:0 16px;cursor:pointer;transition:background-color .2s,border-color .2s}}
.chip:hover{{border-color:var(--accent)}}
.chip[aria-pressed="true"]{{background:var(--accent);border-color:var(--accent);color:var(--surface)}}
</style>
<div class="wrap wide">{header("blog")}
  <section class="intro">
    <h1>مدونة الذكاء الاصطناعي</h1>
    <p>{len(cards)} مقال عملي بالعربي: Claude وClaude Code، البرومبتات، الإنتاجية، المحتوى، والتصميم.</p>
    <div class="chips" id="chips" role="group" aria-label="فلترة المقالات">{chips}</div>
  </section>
  <ul class="posts" id="posts">
{chr(10).join(cards)}
  </ul>{AUTHOR}{FOOTER}
</div>
<script>
document.getElementById('chips').addEventListener('click',function(e){{
  var b=e.target.closest('.chip'); if(!b) return; var f=b.dataset.f;
  document.querySelectorAll('.chip').forEach(function(x){{x.setAttribute('aria-pressed',x===b)}});
  document.querySelectorAll('#posts .post').forEach(function(li){{li.hidden=!(f==='all'||li.dataset.tag===f)}});
}});
</script>
</body>
</html>
'''
open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(index)
NL = chr(10)
locs = [SITE, SITE + "blog/"] + [SITE + "blog/" + p["slug"] + ".html" for p in posts]
open(os.path.join(HERE, "..", "sitemap.xml"), "w", encoding="utf-8").write(
    '<?xml version="1.0" encoding="UTF-8"?>' + NL + '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + NL
    + "".join(f"<url><loc>{u}</loc></url>{NL}" for u in locs) + "</urlset>" + NL)
print("built", len(posts), "articles +", len(EXTERNAL), "external; total cards", len(cards))
