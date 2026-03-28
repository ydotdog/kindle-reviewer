# Kindle Clippings Reviewer

A lightweight, self-contained web app to review your Kindle highlights and notes — randomly, by book, or through search.

![HTML](https://img.shields.io/badge/HTML-CSS--JS-orange)
![No Dependencies](https://img.shields.io/badge/dependencies-zero-green)

## Features

- **Random Review** — Shuffled flashcard-style review (no repeats until all clippings shown). Press `Space` or `→` to advance.
- **Browse by Book** — Filter clippings by book via dropdown, sorted by clipping count.
- **Full-text Search** — Real-time search across content, book titles, and authors with match highlighting.
- **Favorites** — Star clippings to save them for later. Persisted in `localStorage`.
- **Highlight / Note Distinction** — Visual badges and color accents differentiate highlights (orange) from notes (blue).
- **Statistics Dashboard** — Total counts, top books bar chart, and monthly reading timeline.

## Quick Start

### 1. Parse your clippings

Connect your Kindle and run:

```bash
python3 parse_clippings.py /Volumes/Kindle/documents/My\ Clippings.txt
```

This generates `data.js` with all parsed clippings.

### 2. Open the app

Simply open `index.html` in your browser:

```bash
open index.html
```

If the page appears blank (rare `file://` restriction), start a local server:

```bash
python3 -m http.server 8000
# then visit http://localhost:8000
```

## File Structure

```
kindle-reviewer/
├── index.html            # The web app (HTML + CSS + JS, self-contained)
├── parse_clippings.py    # Python parser for Kindle's My Clippings.txt
├── data.js               # Parsed clippings data (generated, gitignored)
└── README.md
```

## Notes

- `data.js` is gitignored since it contains personal reading data. Run the parser to generate your own.
- Zero external dependencies — no frameworks, no CDN, no build step.
- Favorites are stored in your browser's `localStorage`.
- The parser handles both English and Chinese Kindle metadata formats.
