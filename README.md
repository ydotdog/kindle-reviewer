# Kindle Clippings Reviewer

A lightweight, self-contained web app for rereading your Kindle highlights and notes: shuffled, by book, or through search.

![HTML](https://img.shields.io/badge/HTML-CSS--JS-orange)
![No Dependencies](https://img.shields.io/badge/dependencies-zero-green)

## Features

- **Review** — Flashcard-style shuffled review with no repeats until a round is finished. Go back with Prev, and pick up where you left off after a reload. Review everything, your favorites, clippings with notes, or a single book.
- **Clean library** — Titles that came from file names (`书名_副标题_作者_译者`, `Title (Kindle Edition)`) are split into title, subtitle and author. Sort by clippings, recent activity or title, and filter as you type.
- **No duplicates** — Kindle keeps every version of a passage you highlight twice or extend later. They are merged into the longest one.
- **Notes in context** — Notes appear under the highlight they belong to instead of as separate cards.
- **Book pages** — Every clipping of a book in reading order, with a filter, "Review this book" and Markdown export.
- **Search** — Every word has to match; put a phrase in "quotes" to match it exactly. Matching books are listed first, and each search has its own link (`#/search/…`).
- **Favorites** — Star with `F` or the star button, then review them or export them as Markdown. Stars from the previous version carry over.
- **Stats** — Highlights, notes, active days, longest streak, busiest day and month, clippings per month, most clipped books and a by-year table.
- **Light, dark or system theme**, and a phone layout with a bottom tab bar and swiping between cards.
- **Token auth** — Nginx cookie-based token protection for self-hosted deployments.

### Keyboard shortcuts

| Key | Action |
| --- | --- |
| `→` / `J` / `Space` | Next clipping |
| `←` / `K` / `Shift`+`Space` | Previous clipping |
| `F` / `S` | Star or unstar |
| `C` | Copy |
| `O` | Open in its book |
| `/` | Search |
| `Esc` | Clear the search |

The clipping shortcuts work in Review. On a touch screen, swipe the card left or right.

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
├── auth.html             # Token login page for self-hosted deployments
├── parse_clippings.py    # Python parser for Kindle's My Clippings.txt
├── data.js               # Parsed clippings data (generated, gitignored)
└── README.md
```

## Notes

- `data.js` is gitignored since it contains personal reading data. Run the parser to generate your own.
- Zero external dependencies — no frameworks, no CDN, no build step.
- Title cleanup, duplicate merging and note matching happen in the browser, so `data.js` stays a plain export of My Clippings.txt.
- Favorites, review progress and the theme are stored in your browser's `localStorage`, so each browser keeps its own.
- The parser handles both English and Chinese Kindle metadata formats.
