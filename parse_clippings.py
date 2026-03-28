#!/usr/bin/env python3
"""Parse Kindle My Clippings.txt and output data.js for the web reviewer."""

import json
import re
import sys
from datetime import datetime
from pathlib import Path


def extract_book_author(title_line):
    depth = 0
    last_open = -1
    last_close = -1

    for i in range(len(title_line) - 1, -1, -1):
        if title_line[i] == ')':
            if depth == 0:
                last_close = i
            depth += 1
        elif title_line[i] == '(':
            depth -= 1
            if depth == 0:
                last_open = i
                break

    if last_open > 0 and last_close > last_open:
        book = title_line[:last_open].strip()
        author = title_line[last_open + 1:last_close].strip()
    else:
        book = title_line.strip()
        author = ''

    book = clean_book_name(book)
    return book, author


def clean_book_name(name):
    name = re.sub(r'\s*\(z-lib\.org\)', '', name, flags=re.IGNORECASE)
    name = re.sub(r'\s*\(Z-Library\)', '', name, flags=re.IGNORECASE)
    name = re.sub(r'[_\-]z[_\-]lib[_\-]org$', '', name, flags=re.IGNORECASE)
    name = re.sub(r'[_\-]Z[_\-]Library$', '', name, flags=re.IGNORECASE)
    name = name.strip().rstrip('-').rstrip('_').strip()
    return name


def parse_metadata(meta_line):
    clip_type = None
    if 'Your Highlight' in meta_line:
        clip_type = 'highlight'
    elif 'Your Note' in meta_line:
        clip_type = 'note'
    elif 'Your Bookmark' in meta_line:
        clip_type = 'bookmark'
    elif '标注' in meta_line or '高亮' in meta_line:
        clip_type = 'highlight'
    elif '笔记' in meta_line:
        clip_type = 'note'
    elif '书签' in meta_line:
        clip_type = 'bookmark'

    if not clip_type:
        return None, '', '', ''

    page_match = re.search(r'page\s+(\S+)', meta_line, re.IGNORECASE)
    if not page_match:
        page_match = re.search(r'第\s*(\S+)\s*页', meta_line)
    page = page_match.group(1).rstrip('|') if page_match else ''

    loc_match = re.search(r'Location\s+(\S+)', meta_line, re.IGNORECASE)
    if not loc_match:
        loc_match = re.search(r'位置\s*#?(\S+)', meta_line)
    location = loc_match.group(1).rstrip('|') if loc_match else ''

    date_str = ''
    date_match = re.search(r'Added on\s+(.+)$', meta_line)
    if not date_match:
        date_match = re.search(r'添加于\s+(.+)$', meta_line)

    if date_match:
        raw_date = date_match.group(1).strip()
        for fmt in [
            '%A, %B %d, %Y %I:%M:%S %p',
            '%A, %B %d, %Y %H:%M:%S',
        ]:
            try:
                dt = datetime.strptime(raw_date, fmt)
                date_str = dt.strftime('%Y-%m-%d')
                break
            except ValueError:
                continue
        if not date_str:
            date_str = raw_date

    return clip_type, page, location, date_str


def parse_clippings(filepath):
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        content = f.read()

    blocks = content.split('==========')
    clippings = []
    clip_id = 0

    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) < 2:
            continue

        title_line = lines[0].strip().lstrip('\ufeff')
        if not title_line:
            continue

        meta_line = lines[1].strip() if len(lines) > 1 else ''

        content_lines = []
        skip_blank = True
        for line in lines[2:]:
            if skip_blank and line.strip() == '':
                skip_blank = False
                continue
            skip_blank = False
            content_lines.append(line)

        content_text = '\n'.join(content_lines).strip()

        if not content_text:
            continue
        if 'clipping limit' in content_text.lower():
            continue

        book, author = extract_book_author(title_line)
        clip_type, page, location, date_str = parse_metadata(meta_line)

        if not clip_type or clip_type == 'bookmark':
            continue

        clip_id += 1
        clippings.append({
            'id': clip_id,
            'book': book,
            'author': author,
            'type': clip_type,
            'page': page,
            'location': location,
            'date': date_str,
            'content': content_text,
        })

    return clippings


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else '/Volumes/Kindle/documents/My Clippings.txt'
    out_dir = Path(__file__).parent

    clippings = parse_clippings(src)

    data_js = f'const CLIPPINGS_DATA = {json.dumps(clippings, ensure_ascii=False)};'
    (out_dir / 'data.js').write_text(data_js, encoding='utf-8')

    books = set(c['book'] for c in clippings)
    highlights = sum(1 for c in clippings if c['type'] == 'highlight')
    notes = sum(1 for c in clippings if c['type'] == 'note')

    print(f'Parsed {len(clippings)} clippings from {len(books)} books')
    print(f'  Highlights: {highlights}')
    print(f'  Notes: {notes}')
    print(f'  Output: {out_dir / "data.js"}')


if __name__ == '__main__':
    main()
