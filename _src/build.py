#!/usr/bin/env python3
"""Claude & Dima, the series: followorbounce.github.io/series/ (hub) and /series/<NNN-slug> (one page per episode).

  python3 _src/export.py      # scripts from the animation project -> _src/episodes.json
  _src/encode.sh              # web videos (videos/) and poster frames (posters/)
  python3 _src/build.py       # index.html, <NNN-slug>.html, sitemap.xml, llms.txt

Each episode page: the film (720x1280, poster, plays inline), its number, length and cast, a one-line description
(_src/descriptions.json), the full English script as text, the link to The Logic of a Prompt & Life, previous/next,
and VideoObject (with transcript) + BreadcrumbList JSON-LD. Share cards and the network block come from
followorbounce.github.io engine/og_cards.py (run it after this; it keeps both). Never edit the generated pages.
"""
import html, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SITE = 'https://followorbounce.github.io/series/'
NAME = 'Claude & Dima'
LOGIC = 'https://followorbounce.github.io/logic-of-a-prompt'
CREDIT = ('Adapted, with permission, from a Russian-language series of short videos: new characters, setting, '
          'voices and sound, the dialogue translated and rewritten in places, and the original course advertisement '
          'replaced by a pointer to The Logic of a Prompt & Life.')
E = lambda s: html.escape(str(s), quote=True)
WHO = {'Dima': 'd', 'Claude': 'c', 'Codex': 'x'}

CSS = """:root{--bg:#0f1115;--panel:#171a21;--panel2:#1e222b;--ink:#e9e6df;--muted:#a3a09a;--faint:#6f6c66;--line:#2a2e38;
--dima:#9db4cf;--claude:#e08a5f;--codex:#4fc2b3;--acc:#e08a5f;--font:'IBM Plex Sans',system-ui,sans-serif;--mono:'IBM Plex Mono',ui-monospace,monospace;
--display:'IBM Plex Sans Condensed','IBM Plex Sans',system-ui,sans-serif}
@media (prefers-color-scheme: light){:root:not([data-theme="dark"]){--bg:#f4f2ec;--panel:#ffffff;--panel2:#ece9e1;--ink:#1b1c20;--muted:#5d5b55;--faint:#8f8c84;--line:#d9d5ca;--dima:#3d5f86;--claude:#b4532b;--codex:#16786b;--acc:#b4532b}}
:root[data-theme="light"]{--bg:#f4f2ec;--panel:#ffffff;--panel2:#ece9e1;--ink:#1b1c20;--muted:#5d5b55;--faint:#8f8c84;--line:#d9d5ca;--dima:#3d5f86;--claude:#b4532b;--codex:#16786b;--acc:#b4532b}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--font);font-size:16px;line-height:1.6}
a{color:inherit}
.wrap{max-width:1180px;margin:0 auto;padding-inline:max(16px,env(safe-area-inset-left)) max(16px,env(safe-area-inset-right))}
header{border-bottom:1px solid var(--line);padding:max(12px,env(safe-area-inset-top)) 0 12px}
header .wrap{display:flex;gap:12px;align-items:center;justify-content:space-between;flex-wrap:wrap}
.brand{font-family:var(--mono);font-size:12px;letter-spacing:.14em;text-transform:uppercase;text-decoration:none;border:1px solid var(--line);padding:6px 10px}
header nav{display:flex;gap:4px;flex-wrap:wrap}
header nav a{font-family:var(--mono);font-size:12px;text-decoration:none;color:var(--muted);padding:0 10px;min-height:44px;display:inline-flex;align-items:center}
header nav a:hover,header nav a[aria-current]{color:var(--ink)}
h1,h2,h3{font-family:var(--display);font-weight:600;margin:0;line-height:1.1}
.eyebrow{font-family:var(--mono);font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--acc)}
.hero{padding:clamp(28px,6vw,56px) 0 24px}
.hero h1{font-size:clamp(2.4rem,7vw,4.4rem);margin:10px 0 12px}
.hero p{color:var(--muted);max-width:62ch;margin:0}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,180px),1fr));gap:18px;padding:12px 0 48px;list-style:none;margin:0}
.grid a{display:block;text-decoration:none}
.grid img{display:block;width:100%;height:auto;aspect-ratio:9/16;object-fit:cover;border:1px solid var(--line);background:var(--panel)}
.grid .n{font-family:var(--mono);font-size:12px;color:var(--faint);margin-top:8px}
.grid b{display:block;font-family:var(--display);font-size:1.12rem;font-weight:600;line-height:1.2;margin-top:2px}
.grid span.d{display:block;font-size:13px;color:var(--muted);line-height:1.45;margin-top:4px}
.grid a:hover img,.grid a:focus-visible img{border-color:var(--acc)}
.ep{display:grid;grid-template-columns:minmax(0,420px) minmax(0,1fr);gap:clamp(20px,4vw,48px);padding:24px 0 40px;align-items:start}
.film{position:sticky;top:16px}
.film video{display:block;width:100%;height:auto;aspect-ratio:9/16;max-height:calc(100vh - 32px);background:#000;border:1px solid var(--line)}
.ep h1{font-size:clamp(2rem,5vw,3.2rem);margin:8px 0 12px}
.facts{font-family:var(--mono);font-size:13px;color:var(--muted);display:flex;flex-wrap:wrap;gap:6px 18px;margin-bottom:14px}
.lede{font-size:1.15rem;margin:0 0 26px;max-width:46ch}
.script h2{font-family:var(--mono);font-size:12px;font-weight:500;letter-spacing:.12em;text-transform:uppercase;color:var(--faint);margin:0 0 10px}
.script ol{list-style:none;margin:0;padding:0;border-top:1px solid var(--line)}
.script li{display:grid;grid-template-columns:4.5em 4.6em minmax(0,1fr);gap:4px 10px;padding:9px 0;border-bottom:1px solid var(--line)}
.script time{font-family:var(--mono);font-size:12px;color:var(--faint);padding-top:3px}
.script button.t{font:inherit;font-family:var(--mono);font-size:12px;color:var(--faint);background:none;border:0;padding:3px 0 0;text-align:left;cursor:pointer;min-height:24px}
.script button.t:hover{color:var(--ink);text-decoration:underline}
.script .who{font-family:var(--mono);font-size:12px;font-weight:600;padding-top:3px}
.who.d{color:var(--dima)} .who.c{color:var(--claude)} .who.x{color:var(--codex)}
.script li.on{background:color-mix(in srgb,var(--acc) 10%,transparent)}
.cta{display:block;margin-top:26px;border:1px solid var(--acc);padding:16px 18px;text-decoration:none;background:var(--panel)}
.cta b{display:block;font-family:var(--display);font-size:1.2rem}
.cta span{color:var(--muted);font-size:14px}
.pn{display:flex;justify-content:space-between;gap:12px;border-top:1px solid var(--line);padding:16px 0;font-family:var(--mono);font-size:13px}
.pn a{text-decoration:none;min-height:44px;display:inline-flex;align-items:center;max-width:48%}
.pn a:hover{text-decoration:underline}
footer{border-top:1px solid var(--line);padding:22px 0 calc(22px + env(safe-area-inset-bottom));font-size:13px;color:var(--faint)}
footer p{max-width:80ch}
@media (max-width:760px){.ep{grid-template-columns:1fr}.film{position:static;max-width:420px;margin:0 auto}.script li{grid-template-columns:3.8em 4.4em minmax(0,1fr)}}"""

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="{ogtype}">
<meta property="og:site_name" content="{name}">
<meta property="og:title" content="{ogtitle}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}">
{extra}{ld}<meta name="theme-color" content="#0f1115">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Sans+Condensed:wght@600&display=swap" rel="stylesheet">
<script src="/assets/theme-toggle.js"></script>
<style>
{css}
</style>
<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{{"token": "bba4e16a7d9b4d9985eda0cda2624e60"}}'></script>
</head>
<body>
<header><div class="wrap"><a class="brand" href="/">Follow or Bounce</a>
<nav aria-label="Series"><a href="./"{cur_all}>All episodes</a><a href="{logic}">The Logic of a Prompt</a></nav></div></header>
"""

FOOT = """<footer><div class="wrap"><p>{credit}</p><p>Dima and Claude are voxel characters; the voices are synthetic (offline text-to-speech).
Claude is shown as the Claude Code mascot. Part of <a href="/">Follow or Bounce</a>.</p></div></footer>
</body>
</html>
"""


def ld(items):
    return ''.join('<script type="application/ld+json">%s</script>\n' % json.dumps(dict({'@context': 'https://schema.org'}, **i), ensure_ascii=False,
                                                                                 separators=(',', ':')).replace('</', '<\\/') for i in items)


def iso_dur(s):
    s = int(round(s))
    return 'PT%dM%dS' % (s // 60, s % 60) if s >= 60 else 'PT%dS' % s


def mmss(s):
    return '%d:%02d' % (int(s) // 60, int(s) % 60)


def episode(e, i, eps, desc):
    url = SITE + e['slug']
    prev, nxt = eps[i - 1] if i else None, eps[i + 1] if i + 1 < len(eps) else None
    lines = ''.join(
        '<li data-t="%s"><button class="t" type="button" aria-label="Play from %s">%s</button><span class="who %s">%s</span><span>%s</span></li>'
        % (l['t'], mmss(l['t']), mmss(l['t']), WHO[l['who']], E(l['who']), E(l['text'])) for l in e['lines'])
    transcript = '\n'.join('%s: %s' % (l['who'], l['text']) for l in e['lines'])
    title = '%s · %s, episode %d' % (e['title'], NAME, int(e['num']))
    video = {'@type': 'VideoObject', 'name': '%s (%s, episode %d)' % (e['title'], NAME, int(e['num'])), 'description': desc,
             'thumbnailUrl': SITE + 'posters/%s.jpg' % e['slug'], 'uploadDate': e['made'], 'duration': iso_dur(e['duration']),
             'contentUrl': SITE + 'videos/%s.mp4' % e['slug'], 'embedUrl': url, 'inLanguage': 'en', 'transcript': transcript,
             'width': 720, 'height': 1280, 'isFamilyFriendly': True,
             'partOfSeries': {'@type': 'CreativeWorkSeries', 'name': NAME, 'url': SITE},
             'publisher': {'@type': 'Organization', 'name': 'Follow or Bounce', 'url': 'https://followorbounce.github.io/'}}
    crumbs = {'@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': 'Follow or Bounce', 'item': 'https://followorbounce.github.io/'},
        {'@type': 'ListItem', 'position': 2, 'name': NAME, 'item': SITE},
        {'@type': 'ListItem', 'position': 3, 'name': e['title'], 'item': url}]}
    extra = ('<meta property="og:video" content="%s">\n<meta property="og:video:type" content="video/mp4">\n'
             '<meta property="og:video:width" content="720">\n<meta property="og:video:height" content="1280">\n' % (SITE + 'videos/%s.mp4' % e['slug']))
    head = HEAD.format(title=E(title), desc=E(desc), canon=url, ogtype='video.episode', name=NAME, ogtitle=E(e['title']),
                       extra=extra, ld=ld([video, crumbs]), css=CSS, cur_all='', logic=LOGIC)
    end = ''
    body = f'''<main class="wrap">
<div class="ep">
  <div class="film">
    <video id="v" controls playsinline preload="metadata" poster="posters/{e['slug']}.jpg" width="720" height="1280">
      <source src="videos/{e['slug']}.mp4" type="video/mp4">
      Your browser can't play this video. <a href="videos/{e['slug']}.mp4">Download it</a>.
    </video>
  </div>
  <div>
    <div class="eyebrow">{NAME} · Episode {int(e['num'])} of {len(eps)}</div>
    <h1>{E(e['title'])}</h1>
    <div class="facts"><span>{mmss(e['duration'])}</span><span>{' · '.join(E(c) for c in e['cast'])}</span><span>720 × 1280, English</span></div>
    <p class="lede">{E(desc)}</p>
    <section class="script" aria-labelledby="script-h"><h2 id="script-h">The script</h2><ol id="lines">{lines}</ol></section>
    <a class="cta" href="{LOGIC}"><b>The Logic of a Prompt &amp; Life →</b><span>Twenty-one parts of a clear request, the things Dima keeps leaving out.</span></a>
  </div>
</div>
<nav class="pn" aria-label="Previous and next episode">{('<a href="%s">← %d · %s</a>' % (prev['slug'], int(prev['num']), E(prev['title']))) if prev else '<span></span>'}{('<a href="%s">%d · %s →</a>' % (nxt['slug'], int(nxt['num']), E(nxt['title']))) if nxt else '<a href="./">All episodes →</a>'}</nav>
</main>
<script>
(function () {{
  // the script follows the film; a line's time plays the film from there
  var v = document.getElementById('v'), items = [].slice.call(document.querySelectorAll('#lines li')), cur = -1;
  v.addEventListener('timeupdate', function () {{
    var t = v.currentTime, k = -1;
    for (var i = 0; i < items.length; i++) if (parseFloat(items[i].getAttribute('data-t')) <= t + 0.05) k = i;
    if (k !== cur) {{ if (cur >= 0) items[cur].classList.remove('on'); if (k >= 0) items[k].classList.add('on'); cur = k; }}
  }});
  document.getElementById('lines').addEventListener('click', function (e) {{
    var b = e.target.closest('button.t'); if (!b) return;
    v.currentTime = parseFloat(b.parentNode.getAttribute('data-t')); v.play();
  }});
}})();
</script>
'''
    return head + body + FOOT.format(credit=E(CREDIT))


def hub(eps, descs):
    total = sum(e['duration'] for e in eps)
    desc = ('%d short comedy episodes about a developer, Dima, and Claude, the AI that works with him: limits, prompts, '
            'deleted databases and dates. Each about a minute, with the full script.') % len(eps)
    cards = ''.join('<li><a href="%s"><img src="posters/%s.jpg" width="720" height="1280" alt="" loading="lazy" decoding="async">'
                    '<div class="n">%s · %s</div><b>%s</b><span class="d">%s</span></a></li>'
                    % (e['slug'], e['slug'], e['num'], mmss(e['duration']), E(e['title']), E(descs[e['num']])) for e in eps)
    series = {'@type': 'CreativeWorkSeries', 'name': NAME, 'url': SITE, 'description': desc, 'inLanguage': 'en',
              'hasPart': [{'@type': 'VideoObject', 'name': e['title'], 'url': SITE + e['slug']} for e in eps],
              'publisher': {'@type': 'Organization', 'name': 'Follow or Bounce', 'url': 'https://followorbounce.github.io/'}}
    crumbs = {'@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': 'Follow or Bounce', 'item': 'https://followorbounce.github.io/'},
        {'@type': 'ListItem', 'position': 2, 'name': NAME, 'item': SITE}]}
    head = HEAD.format(title='%s: a comedy series about vibe coding · Follow or Bounce' % NAME, desc=E(desc), canon=SITE, ogtype='website',
                       name=NAME, ogtitle=NAME, extra='', ld=ld([series, crumbs]), css=CSS, cur_all=' aria-current="page"', logic=LOGIC)
    body = f'''<main class="wrap">
<section class="hero"><div class="eyebrow">A series · {len(eps)} episodes · {int(total // 60)} minutes</div><h1>{NAME}</h1>
<p>{E(desc)} Every episode ends where most prompts go wrong, and the fix is usually the same: say clearly what you want.</p></section>
<ol class="grid">{cards}</ol>
</main>
'''
    return head + body + FOOT.format(credit=E(CREDIT))


def main():
    eps = json.load(open(os.path.join(HERE, 'episodes.json'), encoding='utf-8'))
    descs = json.load(open(os.path.join(HERE, 'descriptions.json'), encoding='utf-8'))
    missing = [e['num'] for e in eps if e['num'] not in descs]
    assert not missing, 'no description for %s' % missing
    for i, e in enumerate(eps):
        page = episode(e, i, eps, descs[e['num']])
        p = os.path.join(ROOT, e['slug'] + '.html')
        old = open(p, encoding='utf-8').read() if os.path.exists(p) else ''
        open(p, 'w', encoding='utf-8').write(keep_network(old, page))
    p = os.path.join(ROOT, 'index.html')
    old = open(p, encoding='utf-8').read() if os.path.exists(p) else ''
    open(p, 'w', encoding='utf-8').write(keep_network(old, hub(eps, descs)))
    with open(os.path.join(ROOT, 'sitemap.xml'), 'w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n  <url><loc>%s</loc></url>\n' % SITE +
                ''.join('  <url><loc>%s%s</loc></url>\n' % (SITE, e['slug']) for e in eps) + '</urlset>\n')
    with open(os.path.join(ROOT, 'llms.txt'), 'w') as f:
        f.write('# %s\n\n> %d short English comedy episodes about Dima, a developer, and Claude, the AI that works with him. Each page has the video and its full script.\n\n## Episodes\n\n' % (NAME, len(eps)) +
                ''.join('- [%s](%s%s): %s\n' % (e['title'], SITE, e['slug'], descs[e['num']]) for e in eps))
    print('wrote index + %d episode pages' % len(eps))


def keep_network(old, new):
    """Keep what engine/og_cards.py added to a page (share-image tags, network block) across rebuilds."""
    tags = re.findall(r'<meta (?:property="og:image[^"]*"|name="twitter:(?:card|image)") content="[^"]*">\n', old)
    if tags:
        new = new.replace('<meta name="theme-color"', ''.join(tags) + '<meta name="theme-color"', 1)
    net = re.search(r'<!-- fob-network -->[\s\S]*?<!-- /fob-network -->\n?', old)
    if net:
        new = new.replace('</body>', net.group(0) + '</body>', 1)
    return new


if __name__ == '__main__':
    main()
