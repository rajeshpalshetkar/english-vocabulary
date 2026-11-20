#!/usr/bin/env python3
"""Build static, SEO-ready lesson and catalogue pages from GitHub JSON."""
import json, re, shutil, html, os
from pathlib import Path
from common import markdown_to_safe_html, word_count

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"dist"
CFG=json.loads((ROOT/"site/config.json").read_text(encoding="utf-8"))
CAT=json.loads((ROOT/CFG["catalogue_path"]).read_text(encoding="utf-8"))
LESSONS=ROOT/CFG["lessons_path"]
BASE=CFG["site_url"].rstrip("/")

def slugify(text):
    s=re.sub(r"[^a-z0-9]+","-",str(text).lower()).strip("-")
    return s or "lesson"

def esc(s): return html.escape(str(s or ""), quote=True)

def page(title,description,canonical,body,extra_head=""):
    return f"""<!doctype html>
<html lang="en-IN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(description)}">
<link rel="canonical" href="{esc(canonical)}"><meta name="robots" content="index,follow">
<meta property="og:type" content="article"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}"><meta property="og:url" content="{esc(canonical)}">
<meta name="twitter:card" content="summary"><meta name="theme-color" content="#123b72">
{extra_head}<link rel="stylesheet" href="/assets/style.css"></head>
<body><header class="top"><a href="/" class="brand">English Fluency Guide</a><nav><a href="/library/">Learning Library</a><a href="/30-day-challenge/">30-Day Challenge</a><a href="/365-day-practice/">365-Day Practice</a></nav></header>
<main class="wrap">{body}</main><footer><p>© {CFG["site_name"]}. Learn, practise and improve every day.</p><a href="/about/">About</a> · <a href="/privacy/">Privacy</a> · <a href="/contact/">Contact</a></footer></body></html>"""

def write(rel,content):
    p=OUT/rel
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(content,encoding="utf-8")

def card(title,desc,url,badge="Lesson"):
    return f'<a class="card" href="{esc(url)}"><span class="badge">{esc(badge)}</span><h2>{esc(title)}</h2><p>{esc(desc)}</p><span class="more">Open lesson →</span></a>'

def main():
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    shutil.copytree(ROOT/"site/assets",OUT/"assets",dirs_exist_ok=True)
    lesson_map={}
    for f in sorted(LESSONS.glob("*.json")):
        if f.name in {"lesson-template.json", "README.json"}: continue
        a=json.loads(f.read_text(encoding="utf-8"))
        if a.get("author_reviewed") is not True:
            print(f"Draft not published (author_reviewed is not true): {f.name}")
            continue
        required=["title","description","slug","labels","body_markdown"]
        missing=[k for k in required if not a.get(k)]
        if missing: raise ValueError(f"{f}: missing {missing}")
        slug=slugify(a["slug"])
        if slug in lesson_map: raise ValueError(f"Duplicate lesson slug: {slug}")
        lesson_map[slug]=a
    # Match planned catalogue entries by both slug and normalised lesson title.
    # The lesson file slug may be intentionally more descriptive than the catalogue title.
    def title_key(value):
        return re.sub(r"[^a-z0-9]+", "", str(value or "").lower())
    title_map={}
    for lesson_slug, lesson in lesson_map.items():
        title_map.setdefault(title_key(lesson.get("title")), (lesson_slug, lesson))
    # Explicit catalogue aliases for concise titles whose lesson titles are editorially expanded.
    catalogue_aliases = {
        title_key("Articles: A, An and The"): "articles-a-an-the",
        title_key("Prepositions: In, On and At"): "prepositions-in-on-at",
        title_key("Modal Verbs: Can, Could, Should and Would"): "modal-verbs",
        title_key("This, That, These and Those"): "this-that-these-those",
        title_key("WH Questions: What, Where, When, Why and How"): "wh-questions-what-where-when-why-how",
        title_key("Word Stress and Sentence Stress"): "word-stress-and-sentence-stress",
    }
    def find_lesson(planned_title, planned_slug):
        alias_slug = catalogue_aliases.get(title_key(planned_title))
        if alias_slug and alias_slug in lesson_map:
            return alias_slug, lesson_map[alias_slug]
        found=lesson_map.get(planned_slug)
        if found: return planned_slug, found
        found=title_map.get(title_key(planned_title))
        if found: return found
        # Catalogue titles are often shorter than editorial lesson titles
        # (for example, "Asking for Directions" vs "Asking for Directions in English").
        # Match only when all meaningful catalogue words occur in exactly one lesson slug.
        stop={"a","an","and","the","in","on","at","for","of","to","your","you","with","about"}
        wanted={w for w in re.findall(r"[a-z0-9]+", str(planned_title).lower()) if w not in stop}
        if wanted:
            candidates=[]
            for candidate_slug, candidate in lesson_map.items():
                words=set(re.findall(r"[a-z0-9]+", candidate_slug.lower()))
                if wanted.issubset(words):
                    candidates.append((candidate_slug,candidate))
            if len(candidates)==1:
                return candidates[0]
        return (None, None)

    urls=[]
    for slug,a in lesson_map.items():
        canonical=f"{BASE}/lessons/{slug}/"
        content=markdown_to_safe_html(a["body_markdown"])
        objectives=a.get("learning_objectives",[])
        faq=a.get("faq",[])
        intro=f'<p class="intro">{esc(a["description"])}</p>'
        obj=""
        if objectives:
            obj="<section><h2>What You Will Learn</h2><ul>"+"".join(f"<li>{esc(x)}</li>" for x in objectives)+"</ul></section>"
        faqhtml=""
        if faq:
            faqhtml="<section><h2>Frequently Asked Questions</h2>"+"".join(f"<h3>{esc(x.get('question'))}</h3><p>{esc(x.get('answer'))}</p>" for x in faq)+"</section>"
        crumb='<p class="crumb"><a href="/library/">Learning Library</a> / '+ " · ".join(esc(x) for x in a.get("labels",[]))+"</p>"
        body=f'{crumb}<article><h1>{esc(a["title"])}</h1><p class="meta">{esc(a.get("audience_level","All levels"))} · {int(a.get("estimated_reading_minutes",8))} min read</p>{intro}{obj}{content}{faqhtml}</article>'
        write(f"lessons/{slug}/index.html",page(a["title"],a["description"],canonical,body))
        urls.append(canonical)
    # Build topic pages; planned lessons without JSON are displayed as planned, not broken links.
    for label,titles in CAT.get("core_library",{}).items():
        items=[]
        for title in titles:
            slug=slugify(title)
            actual_slug,a=find_lesson(title,slug)
            if a: items.append(card(title,a["description"],f"/lessons/{actual_slug}/"))
            else: items.append(f'<div class="card planned"><span class="badge">Coming soon</span><h2>{esc(title)}</h2><p>This lesson is part of the learning plan.</p></div>')
        body=f'<p class="crumb"><a href="/library/">Learning Library</a></p><h1>{esc(label)}</h1><p class="intro">Explore practical {esc(label.lower())} lessons with examples and exercises.</p><div class="grid">{"".join(items)}</div>'
        u=f"{BASE}/topics/{slugify(label)}/"
        write(f"topics/{slugify(label)}/index.html",page(f"{label} Lessons | English Fluency Guide",f"Explore {label} lessons with clear explanations, examples and practice.",u,body))
        urls.append(u)
    # 30-day challenge and 52-week practice catalogues
    for route,title,key,unit in [("30-day-challenge","30-Day English Challenge","challenge_30_days","Day"),("365-day-practice","365-Day English Practice","year_practice_52_weeks","Week")]:
        entries=[]
        for i,item in enumerate(CAT.get(key,[]),1):
            name=item[0] if isinstance(item,list) else item
            slug=slugify(name)
            actual_slug,a=find_lesson(name,slug)
            if a: entries.append(card(f"{unit} {i:02d}: {name}",a["description"],f"/lessons/{actual_slug}/",f"{unit} {i}"))
            else: entries.append(f'<div class="card planned"><span class="badge">{unit} {i:02d} · Planned</span><h2>{esc(name)}</h2><p>Lesson content is not yet in the JSON library.</p></div>')
        desc=f"Structured {title.lower()} with practical daily learning tasks."
        body=f'<h1>{title}</h1><p class="intro">{desc}</p><div class="grid">{"".join(entries)}</div>'
        u=f"{BASE}/{route}/"
        write(f"{route}/index.html",page(f"{title} | English Fluency Guide",desc,u,body))
        urls.append(u)
    # Library home
    topics=[]
    for label,titles in CAT.get("core_library",{}).items():
        topics.append(card(label,f"{len(titles)} planned lessons",f"/topics/{slugify(label)}/",f"{len(titles)} lessons"))
    body=f'<section class="hero"><span class="badge">Learn at your own pace</span><h1>Build English Skills with Confidence</h1><p>Clear lessons, real-life examples, speaking tasks and regular practice.</p></section><h2>Explore Learning Topics</h2><div class="grid">{"".join(topics)}</div><section class="promo"><a href="/30-day-challenge/">Start the 30-Day Challenge →</a> <a href="/365-day-practice/">Explore 365-Day Practice →</a></section>'
    write("index.html",page("English Fluency Guide | Learn and Practise English",CFG["description"],BASE+"/",body))
    write("library/index.html",page("Learning Library | English Fluency Guide",CFG["description"],BASE+"/library/",f'<h1>Learning Library</h1><div class="grid">{"".join(topics)}</div>'))
    sitemap='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{esc(u)}</loc></url>' for u in sorted(set(urls+[BASE+"/",BASE+"/library/"])))+'</urlset>'
    write("sitemap.xml",sitemap)
    write("robots.txt","User-agent: *\nAllow: /\nSitemap: "+BASE+"/sitemap.xml\n")
    write("CNAME", BASE.split("://",1)[-1].split("/",1)[0])
    write("404.html",page("Page Not Found","The requested English lesson could not be found.",BASE+"/404.html",'<h1>Page not found</h1><p>The lesson may have moved. Visit the <a href="/library/">Learning Library</a>.</p>'))
    print(f"Built {len(lesson_map)} full lessons, {len(CAT.get('core_library',{}))} topic pages, challenge pages, sitemap and home page.")

if __name__=="__main__": main()
