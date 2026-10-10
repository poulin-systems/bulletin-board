#!/usr/bin/env python3
"""Build a pre-rendered Pages site without GitHub Actions/Jekyll (PyYAML required)."""
import datetime as dt
import html
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
import yaml

ROOT = Path(__file__).resolve().parents[1]
BASE = "/bulletin-board"
HOST = "https://poulin-systems.github.io"
TITLE = "Poulin Systems Bulletin Board"

def inline(value):
    s = html.escape(value.strip())
    s = re.sub(r"\[([^\]]+)\]\((https://[^)\s]+)\)", lambda m: '<a href="'+m[2]+'">'+m[1]+'</a>', s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)
    return s

def markdown(value):
    out, para, items = [], [], []
    list_kind = None
    def flush():
        nonlocal list_kind
        if para:
            out.append("<p>"+" ".join(inline(p) for p in para)+"</p>")
            para.clear()
        if items:
            tag = "ol" if list_kind == "ol" else "ul"
            out.append("<"+tag+">"+"".join(items)+"</"+tag+">")
            items.clear()
            list_kind = None
    for source_line in value.splitlines():
        s = source_line.strip()
        if not s:
            flush()
            continue
        if s == "---":
            flush()
            out.append("<hr>")
            continue
        head = re.match(r"^(#{1,4})\s+(.+)$",s)
        if head:
            flush()
            level = len(head[1])
            out.append(f"<h{level}>"+inline(head[2])+f"</h{level}>")
            continue
        item = re.match(r"^(\d+\.\s+|-\s+)(.+)$",s)
        if item:
            if para:
                flush()
            kind = "ol" if item[1][0].isdigit() else "ul"
            if list_kind and kind != list_kind: flush()
            list_kind = kind
            items.append("<li>"+inline(item[2])+"</li>")
            continue
        if items: flush()
        para.append(s)
    flush()
    return "\n".join(out)

def postinfo(path):
    raw = path.read_text(encoding="utf-8")
    assert raw.startswith("---\n"), "Missing front matter"
    _, header, body = raw.split("---\n",2)
    meta = yaml.safe_load(header)
    stamp = meta["date"]
    if isinstance(stamp,str): stamp = dt.datetime.fromisoformat(stamp)
    assert isinstance(stamp,dt.datetime) and stamp.utcoffset() is not None
    slug = path.stem[11:]
    rel = f"/{stamp.year:04}/{stamp.month:02}/{stamp.day:02}/{slug}/"
    return {**meta, "stamp":stamp, "date_display":stamp.strftime("%B %-d, %Y"),
            "path":rel, "href":BASE+rel, "content":markdown(body)}

def document(name, description, body, path):
    esc = html.escape
    return f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light"><meta name="theme-color" content="#111e2d">
<meta name="description" content="{esc(description,quote=True)}">
<title>{esc(name)} · {TITLE}</title>
<link rel="stylesheet" href="{BASE}/assets/site.css">
<link rel="alternate" type="application/atom+xml" title="{TITLE}" href="{HOST}{BASE}/feed.xml">
<link rel="canonical" href="{HOST}{BASE}{path}">
</head><body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="wrap masthead">
<a class="brand" href="{BASE}/"><span class="brand-mark">P<span class="brand-dot">.</span>S</span>
<span><strong>Poulin Systems</strong><small>Bulletin Board</small></span></a>
<nav aria-label="Primary navigation"><a href="{BASE}/">Bulletins</a>
<a href="{BASE}/about/">About</a><a href="{BASE}/feed.xml">Feed ↗</a></nav>
</div></header>
<main id="main" class="wrap main-content">{body}</main>
<footer class="site-footer"><div class="wrap footer-inner">
<p>© 2026 Poulin Systems · Evidence first. People accountable.</p>
<p><a href="{BASE}/about/">Editorial policy</a> ·
<a href="https://github.com/poulin-systems">GitHub organization ↗</a></p>
</div></footer></body></html>
'''

def write(target, rel, content):
    out = target / rel
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(content, encoding="utf-8")

def atom(posts):
    xmlns = "http://www.w3.org/2005/Atom"
    ET.register_namespace("",xmlns)
    def add(parent,name,text=None,attrs=None):
        obj = ET.SubElement(parent,"{"+xmlns+"}"+name,attrs or {})
        obj.text = text
        return obj
    root = ET.Element("{"+xmlns+"}feed")
    add(root,"title",TITLE)
    add(root,"subtitle","Source-led notes on engineering and accountable AI.")
    add(root,"link",attrs={"href":HOST+BASE+"/feed.xml","rel":"self"})
    add(root,"link",attrs={"href":HOST+BASE+"/","rel":"alternate"})
    add(root,"id",HOST+BASE+"/")
    add(root,"updated",posts[0]["stamp"].isoformat())
    add(add(root,"author"),"name","Poulin Systems")
    for post in posts:
        item = add(root,"entry")
        add(item,"title",post["title"])
        add(item,"link",attrs={"href":HOST+post["href"]})
        add(item,"id",HOST+post["href"])
        add(item,"published",post["stamp"].isoformat())
        add(item,"updated",post["stamp"].isoformat())
        add(item,"summary",post["summary"])
        add(item,"content",post["content"],{"type":"html"})
    return '<?xml version="1.0" encoding="utf-8"?>\n'+ET.tostring(root,encoding="unicode")

def main(destination):
    target = Path(destination).resolve()
    assert target != ROOT and ROOT not in target.parents, "Output must be outside source"
    assert not target.exists() or not any(target.iterdir()), "Output must be empty"
    target.mkdir(parents=True,exist_ok=True)
    posts = sorted((postinfo(p) for p in (ROOT/"_posts").glob("*.md")),
                   key=lambda p:p["stamp"],reverse=True)
    assert posts, "No posts"
    cards = []
    for p in posts:
        cards.append(f'''<article class="bulletin">
        <div class="bulletin-top"><span class="category">{html.escape(p["category"])}</span>
        <time datetime="{p["stamp"].isoformat()}">{p["date_display"]}</time></div>
        <h3><a href="{p["href"]}">{html.escape(p["title"])}</a></h3>
        <p>{html.escape(p["summary"])}</p>
        <a class="read-more" href="{p["href"]}">Read bulletin ↗</a></article>''')
        content = f'''<article class="post">
        <div class="eyebrow"><a href="{BASE}/">← All bulletins</a>
        <span class="separator">/</span> {html.escape(p["category"])}</div>
        <header class="post-head"><p class="post-date"><time datetime="{p["stamp"].isoformat()}">{p["date_display"]}</time> · {html.escape(p["author"])}</p>
        <h1>{html.escape(p["title"])}</h1>
        <p class="lede">{html.escape(p["summary"])}</p></header>
        <div class="article-body">{p["content"]}</div>
        <aside class="editorial-note" aria-label="Editorial information">
        <strong>Editorial note</strong>
        <p>This is Poulin Systems commentary, not a statement from the organizations referenced.
        Prepared with AI drafting assistance; the human publisher owns factual responsibility.</p>
        </aside><p class="back-link"><a href="{BASE}/">← Return to bulletin board</a></p>
        </article>'''
        write(target,p["path"].lstrip("/")+"index.html",document(p["title"],p["summary"],content,p["path"]))
    home = f'''<section class="hero">
    <p class="kicker">POULIN SYSTEMS / PUBLIC NOTES</p>
    <h1>Ideas worth examining.<br><em>Evidence worth keeping.</em></h1>
    <p>Research notes, engineering observations, and responsible-AI commentary from an independent
    builder's perspective. Facts, interpretation, and unresolved questions belong in different sentences.</p>
    </section><section class="board" aria-labelledby="latest-title">
    <div class="section-heading"><h2 id="latest-title">Latest bulletins</h2><span>{len(posts)} posted</span></div>
    {"".join(cards)}</section>
    <section class="about-strip"><div><strong>Public thinking, accountable writing.</strong>
    <p>We link to original sources, identify our interpretations, and correct mistakes.
    We do not publish private infrastructure details here.</p></div>
    <a href="{BASE}/about/">How we publish ↗</a></section>'''
    write(target,"index.html",document("Bulletins","Sourced commentary from Poulin Systems",home,"/"))
    about = (ROOT/"about.md").read_text(encoding="utf-8").split("---\n",2)[2]
    write(target,"about/index.html",document("About","Editorial standards",markdown(about),"/about/"))
    write(target,"feed.xml",atom(posts))
    (target/"assets").mkdir(exist_ok=True)
    shutil.copy(ROOT/"assets/site.css",target/"assets/site.css")
    write(target,"404.html",document("Not found","Page not found",
          f'<div class="hero"><h1>Page not found</h1><p>Return to the <a href="{BASE}/">bulletin board</a>.</p></div>',"/404.html"))
    write(target,".nojekyll","")
    head = subprocess.check_output(["git","-C",str(ROOT),"rev-parse","origin/main"],text=True).strip()
    write(target,"build-provenance.json",json.dumps({
        "source":"poulin-systems/bulletin-board",
        "source_commit":head,
        "generator":"scripts/build_static.py",
        "note":"Static deploy with .nojekyll because organization Actions policy is disabled."
    },indent=2)+"\n")
    ET.fromstring((target/"feed.xml").read_text())
    for page in target.rglob("*.html"):
        s = page.read_text()
        assert ('{{' not in s and '{%' not in s), f"Unrendered template: {page}"
        assert BASE+"/" in s
    print("STATIC_BUILD_PASS",len(posts),"bulletin(s)",head)
    for p in sorted(target.rglob("*")):
        if p.is_file(): print(str(p.relative_to(target)))

if __name__=="__main__":
    assert len(sys.argv)==2, "usage: build_static.py EMPTY_OUTPUT_DIR"
    main(sys.argv[1])
