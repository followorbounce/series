#!/usr/bin/env python3
"""Snapshot the 29 episodes from the animation project (/home/none/git/animation: story.py for 001, episodes/epNNN.py
for 002-029) into _src/episodes.json: number, slug, title, English lines (time, speaker, text) and the end card.
The Russian originals stay in the animation project. Run when an episode's script changes, then build.py."""
import glob, importlib.util, json, os, re, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
ANIM = '/home/none/git/animation'
NAMES = {'D': 'Dima', 'C': 'Claude', 'X': 'Codex'}


def load(path):
    spec = importlib.util.spec_from_file_location('m', path)
    m = importlib.util.module_from_spec(spec)
    src = open(path, encoding='utf-8').read()
    if path.endswith('story.py'):                        # the first film's script runs code at import; read only its tables
        ns = {}
        exec(src[src.index('LENGTH'):src.index('\n', src.index('LENGTH'))], ns)
        i = src.index('LINES = ['); exec(src[i:src.index('\n]\n', i) + 3], ns)
        return {'num': '001', 'slug': 'production-old-do-not-delete', 'title': 'production-old-DO-NOT-DELETE'}, ns['LINES'], None
    spec.loader.exec_module(m)
    return m.META, m.LINES, m.END_CARD


eps = []
for path in [os.path.join(ANIM, 'story.py')] + sorted(glob.glob(os.path.join(ANIM, 'episodes', 'ep*.py'))):
    meta, lines, end = load(path)
    video = os.path.join(ANIM, 'out', '%s-%s.mp4' % (meta['num'], meta['slug']))
    dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', video],
                               capture_output=True, text=True, check=True).stdout)
    eps.append({'num': meta['num'], 'slug': '%s-%s' % (meta['num'], meta['slug']), 'title': meta['title'],
                'duration': round(dur, 1), 'end_card': list(end) if end else None,
                'cast': [NAMES[w] for w in sorted({l[2] for l in lines}, key='DCX'.index)],
                'lines': [{'t': round(l[0], 1), 'who': NAMES[l[2]], 'text': l[3]} for l in lines],
                'made': '2026-10-27'})
json.dump(eps, open(os.path.join(HERE, 'episodes.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(eps), 'episodes,', sum(len(e['lines']) for e in eps), 'lines')
