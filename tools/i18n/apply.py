# -*- coding: utf-8 -*-
"""Apply the German glossary to the template pages.

Only two things are ever rewritten:
  * text nodes  - the characters between > and <
  * a whitelist of attributes: placeholder, title, alt, aria-label

Everything else is left exactly as it was. href, src, class, id, data-*,
inline scripts, stylesheets and HTML comments are never touched, so no link
or selector can break. Matching is done on the whitespace-normalised node,
because the template wraps long labels across several tab-indented lines,
and the original leading/trailing whitespace is put back afterwards.

Running it twice is a no-op: German text does not match the English keys.
"""
import re, sys, json, collections

sys.path.insert(0, "tools/i18n")
from glossary import GLOSSARY
from people import PERSON_MAP
from glossary2 import EXTRA

PAGES = ["index.html", "email.html", "calendar.html", "todo.html", "notes.html",
         "file-manager.html", "invoices.html", "kanban-view.html"]

TABLE = {}
TABLE.update(GLOSSARY)
TABLE.update(PERSON_MAP)
TABLE.update(EXTRA)

ATTRS = re.compile(r'\b(placeholder|title|alt|aria-label)="([^"]*)"')
TEXT  = re.compile(r">([^<>]+)<")
norm  = lambda t: " ".join(t.split())


def protected_spans(s):
    """Character ranges that must not be rewritten."""
    spans = []
    for pat in (r"<!--.*?-->", r"<(script|style)\b.*?</\1\s*>"):
        for m in re.finditer(pat, s, re.S | re.I):
            spans.append((m.start(), m.end()))
    return spans


def inside(spans, i):
    return any(a <= i < b for a, b in spans)


def translate(path, dry=False, stats=None):
    s = open(path, encoding="utf-8", errors="surrogateescape").read()
    spans = protected_spans(s)
    out, pos, hits = [], 0, 0

    def sub_text(m):
        nonlocal hits
        raw = m.group(1)
        key = norm(raw)
        new = TABLE.get(key)
        if new is None:
            if stats is not None and re.search(r"[A-Za-z]{3}", key):
                stats[key] += 1
            return m.group(0)
        hits += 1
        lead = raw[:len(raw) - len(raw.lstrip())]
        tail = raw[len(raw.rstrip()):]
        return ">" + lead + new + tail + "<"

    def sub_attr(m):
        nonlocal hits
        new = TABLE.get(norm(m.group(2)))
        if new is None:
            return m.group(0)
        hits += 1
        return f'{m.group(1)}="{new}"'

    # walk the document, skipping protected regions wholesale
    cursor = 0
    for a, b in sorted(spans) + [(len(s), len(s))]:
        if a > cursor:
            chunk = s[cursor:a]
            chunk = TEXT.sub(sub_text, chunk)
            chunk = ATTRS.sub(sub_attr, chunk)
            out.append(chunk)
        out.append(s[a:b])
        cursor = b
    new_s = "".join(out)

    if not dry and new_s != s:
        open(path, "w", encoding="utf-8", errors="surrogateescape").write(new_s)
    return hits


if __name__ == "__main__":
    dry = "--dry" in sys.argv
    leftover = collections.Counter()
    total = 0
    print(f"  glossary: {len(TABLE)} entries\n")
    for p in PAGES:
        n = translate(p, dry, leftover)
        total += n
        print(f"  {p:<20} {n:5d} replacements")
    print(f"\n  {total} replacements across {len(PAGES)} pages")
    json.dump(leftover.most_common(), open("tools/i18n/untranslated.json", "w",
              encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"  {len(leftover)} distinct strings left untranslated "
          f"-> tools/i18n/untranslated.json")
