import json, re, sys
from pathlib import Path
import bleach, markdown
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))
from config import CANONICAL_LABELS, MAX_DESCRIPTION_LENGTH, MAX_TITLE_LENGTH, MIN_PAGE_WORDS, MIN_POST_WORDS

def load_article(path):
    p=Path(path)
    if not p.is_absolute(): p=ROOT/p
    with p.open("r",encoding="utf-8") as f: return json.load(f)

def word_count(text):
    return len(re.findall(r"\b[\w'-]+\b", text or ""))

def markdown_to_safe_html(source):
    raw=markdown.markdown(source,extensions=["extra","sane_lists","smarty"],output_format="html5")
    tags=set(bleach.sanitizer.ALLOWED_TAGS)|{"p","h1","h2","h3","h4","hr","br","ul","ol","li","blockquote","table","thead","tbody","tr","th","td","pre","code","img","figure","figcaption","details","summary"}
    attrs={**bleach.sanitizer.ALLOWED_ATTRIBUTES,"a":["href","title","rel","target"],"img":["src","alt","title","width","height","loading"],"th":["scope","colspan","rowspan"],"td":["colspan","rowspan"]}
    clean=bleach.clean(raw,tags=tags,attributes=attrs,protocols={"http","https","mailto"},strip=True)
    return bleach.linkifier.Linker(callbacks=[]).linkify(clean)

def article_to_html(article):
    desc=bleach.clean(article["description"])
    parts=[f'<div class="efg-article"><p class="efg-intro"><strong>{desc}</strong></p>']
    objectives=article.get("learning_objectives",[])
    if objectives:
        parts.append("<h2>What You Will Learn</h2><ul>")
        parts.extend(f"<li>{bleach.clean(str(x))}</li>" for x in objectives)
        parts.append("</ul>")
    parts.append(markdown_to_safe_html(article["body_markdown"]))
    faq=article.get("faq",[])
    if faq:
        parts.append("<h2>Frequently Asked Questions</h2>")
        for item in faq:
            q=bleach.clean(str(item.get("question","")))
            a=bleach.clean(str(item.get("answer","")))
            if q and a: parts.append(f"<h3>{q}</h3><p>{a}</p>")
    parts.append("</div>")
    return "\n".join(parts)

def validation_errors(a):
    errors=[]
    required=["kind","title","description","slug","labels","primary_keyword","audience_level","learning_objectives","body_markdown","faq","references"]
    for k in required:
        if k not in a: errors.append(f"Missing required field: {k}")
    if errors: return errors
    if a["kind"] not in {"post","page"}: errors.append("kind must be post or page")
    if not isinstance(a["title"],str) or not a["title"].strip() or len(a["title"])>MAX_TITLE_LENGTH: errors.append("Invalid title length")
    if not isinstance(a["description"],str) or not a["description"].strip() or len(a["description"])>MAX_DESCRIPTION_LENGTH: errors.append("Description must be 1-160 characters")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*",str(a["slug"])): errors.append("Invalid slug")
    labels=a.get("labels",[])
    if not isinstance(labels,list) or (a["kind"]=="post" and not labels): errors.append("Post requires labels")
    elif set(labels)-CANONICAL_LABELS: errors.append("Unknown labels: "+", ".join(sorted(set(labels)-CANONICAL_LABELS)))
    minimum=MIN_POST_WORDS if a["kind"]=="post" else MIN_PAGE_WORDS
    if word_count(a["body_markdown"])<minimum: errors.append(f"Content is below minimum {minimum} words")
    if len(a.get("learning_objectives",[]))<2: errors.append("Add at least two learning objectives")
    if not isinstance(a.get("faq"),list) or not isinstance(a.get("references"),list): errors.append("faq and references must be lists")
    if a.get("author_reviewed") is not True: errors.append("Human review required: set author_reviewed=true only after checking the article")
    return errors
