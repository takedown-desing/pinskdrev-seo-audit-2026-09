import sys, re, base64, os, markdown
from markdown.extensions.toc import slugify_unicode
src, out = sys.argv[1], sys.argv[2]
base = os.path.dirname(os.path.abspath(src))
md_text = open(src, encoding='utf-8').read()
def embed(m):
    alt, path = m.group(1), m.group(2)
    p = os.path.join(base, path)
    if os.path.exists(p):
        b = base64.b64encode(open(p,'rb').read()).decode()
        ext = 'png' if p.endswith('.png') else 'jpeg'
        return f'<figure><img src="data:image/{ext};base64,{b}" alt="{alt}" loading="lazy"><figcaption>{alt}</figcaption></figure>'
    return m.group(0)
md_text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', embed, md_text)
md = markdown.Markdown(extensions=['tables','toc','sane_lists'], extension_configs={'toc':{'slugify':slugify_unicode,'toc_depth':'1-3','separator':'-'}})
html = md.convert(md_text)
tokens = md.toc_tokens
def render(items, level=1):
    if not items: return ''
    s = '<ul>'
    for it in items:
        name = it['name']
        if level == 1 and name.startswith('Комплексный SEO-аудит'): name = 'Начало и резюме'
        s += f'<li class="l{it["level"]}"><a href="#{it["id"]}">{name}</a>{render(it.get("children",[]), level+1)}</li>'
    return s + '</ul>'
toc_html = render(tokens)
title = re.search(r'^# (.+)$', md_text, re.M).group(1) if re.search(r'^# (.+)$', md_text, re.M) else 'Аудит'
css = """
:root{--nav:300px;--accent:#b5651d;--line:#e2ddd6;--soft:#faf7f3}
*{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:16px}
body{font-family:-apple-system,'Segoe UI',Roboto,Arial,sans-serif;margin:0;color:#1a1a1a;line-height:1.55;font-size:15px;background:#fff}
nav.toc{position:fixed;top:0;left:0;bottom:0;width:var(--nav);overflow-y:auto;background:var(--soft);border-right:1px solid var(--line);padding:18px 14px 40px;font-size:13px;z-index:20}
nav.toc .toc-title{font-weight:700;font-size:13px;letter-spacing:.04em;text-transform:uppercase;color:#6b6259;margin:0 0 10px 6px}
nav.toc ul{list-style:none;margin:0;padding:0}
nav.toc ul ul{padding-left:12px}
nav.toc li.l1>a{font-weight:700;color:#1a1a1a;margin-top:10px}
nav.toc li.l2>a{color:#2a2a2a}
nav.toc li.l3>a{color:#5c5650;font-size:12.5px}
nav.toc a{display:block;padding:4px 8px;border-radius:5px;text-decoration:none;line-height:1.35;border-left:2px solid transparent}
nav.toc a:hover{background:#f0e9e1}
nav.toc a.active{background:#f0e6d9;border-left-color:var(--accent);color:#000;font-weight:600}
main{margin-left:var(--nav);padding:40px 40px 80px;max-width:calc(var(--nav) + 980px)}
main>*{max-width:940px}
#toc-toggle{display:none;position:fixed;left:14px;bottom:14px;z-index:30;background:var(--accent);color:#fff;border:0;border-radius:24px;padding:10px 16px;font-size:14px;box-shadow:0 4px 14px rgba(0,0,0,.25);cursor:pointer}
h1{font-size:28px;border-bottom:3px solid var(--accent);padding-bottom:8px} h2{font-size:22px;margin-top:40px;border-bottom:1px solid #ddd;padding-bottom:6px} h3{font-size:18px;margin-top:28px}
table{border-collapse:collapse;width:100%;margin:14px 0;font-size:13.5px} th,td{border:1px solid #ccc;padding:6px 8px;vertical-align:top} th{background:#f3ede6;text-align:left}
figure{margin:18px 0} figure img{max-width:100%;border:1px solid #ddd;border-radius:4px} figcaption{font-size:12.5px;color:#555;margin-top:6px}
code{background:#f5f5f5;padding:1px 4px;border-radius:3px;font-size:13px} pre{background:#f5f5f5;padding:12px;overflow:auto;font-size:12.5px}
blockquote{border-left:4px solid var(--accent);margin:0;padding:4px 16px;color:#444;background:var(--soft)}
@media (max-width:1100px){nav.toc{transform:translateX(-100%);transition:transform .2s;width:min(320px,86vw)} nav.toc.open{transform:none;box-shadow:0 0 30px rgba(0,0,0,.25)} main{margin-left:0;padding:24px 16px 80px} #toc-toggle{display:block}}
@media print{nav.toc,#toc-toggle{display:none!important} main{margin:0;padding:0;max-width:none;font-size:12.5px} figure{page-break-inside:avoid} tr{page-break-inside:avoid}}
"""
js = """
(function(){
  var nav=document.querySelector('nav.toc'), btn=document.getElementById('toc-toggle');
  btn.addEventListener('click',function(){nav.classList.toggle('open');});
  nav.addEventListener('click',function(e){ if(e.target.tagName==='A' && window.innerWidth<=1100) nav.classList.remove('open'); });
  var links=[].slice.call(nav.querySelectorAll('a[href^="#"]'));
  var heads=links.map(function(a){return document.getElementById(decodeURIComponent(a.getAttribute('href').slice(1)));});
  function update(){
    var y=window.scrollY+120, idx=0;
    for(var i=0;i<heads.length;i++){ if(heads[i] && heads[i].offsetTop<=y) idx=i; }
    links.forEach(function(a,i){a.classList.toggle('active',i===idx);});
    var act=links[idx]; if(act){var r=act.getBoundingClientRect(); if(r.top<0||r.bottom>window.innerHeight) act.scrollIntoView({block:'center'});}
  }
  window.addEventListener('scroll',update,{passive:true}); window.addEventListener('load',update); update();
})();
"""
doc = f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex, nofollow"><base href="https://takedown-desing.github.io/pinskdrev-seo-audit-2026-09/"><title>{title}</title><style>{css}</style></head><body>
<nav class="toc"><div class="toc-title">Оглавление</div>{toc_html}</nav>
<button id="toc-toggle" type="button">Оглавление</button>
<main>{html}</main>
<script>{js}</script></body></html>'''
open(out,'w',encoding='utf-8').write(doc)
print('written', out, os.path.getsize(out)//1024, 'KB | toc items:', len(re.findall(r'<li class="l', toc_html)))
