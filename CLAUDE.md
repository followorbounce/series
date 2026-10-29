# Claude & Dima — the series

GitHub Pages site at https://followorbounce.github.io/series/ : a hub and one page per episode (29) of the voxel
comedy shorts made in /home/none/git/animation (Dima and Claude, sometimes Codex). Reach plan B3.

- **Generated, never hand-edit the pages.** `python3 _src/export.py` snapshots the scripts from the animation project
  (story.py for 001, episodes/epNNN.py) into `_src/episodes.json` (English only; the Russian originals stay there);
  `_src/encode.sh` re-encodes the films to `videos/` (libopenh264 600k + AAC 96k mono, faststart; ~5–6 MB each, checked
  side by side with the masters) and takes a poster frame at 1 s into `posters/`; `python3 _src/build.py` writes
  `index.html`, `<NNN-slug>.html`, `sitemap.xml`, `llms.txt`. A new episode: render it in the animation project, add
  its one-line description to `_src/descriptions.json`, run all three, then `engine/og_cards.py series` in the
  followorbounce.github.io repo (share cards in `og/`, the poster as art; the network block). build.py keeps both.
- Each page: the video (plays inline, poster), number/length/cast, the description, the full English script (each
  line's time plays the film from there; the current line is highlighted while it plays), a link to The Logic of a
  Prompt & Life, prev/next, VideoObject (with transcript) + BreadcrumbList JSON-LD.
- **Rights:** the episodes adapt another creator's Russian-language shorts; the owner has permission (2026-10-28). Every
  page carries the credit line `CREDIT` in build.py; add the original author's name there when the owner wants it.
- Listed in the hub's sitemap index (`PROJECT_SITEMAPS`), its llms.txt, the new-pages feed, and linked from the
  homepage mascots ("Watch them").
