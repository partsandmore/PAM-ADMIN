# -*- coding: utf-8 -*-
"""Copy index.html's trimmed sidebar onto every page the sidebar links to.

Each page marks its own entry as current and expands the group that entry
lives in - not always Start. hr-dashboard.html opens with Uebersicht
expanded, voice-call.html with Anwendungen, and so on. The group is found by
walking up from the matching link to its enclosing <li class="submenu">,
rather than assuming a position.

Only the sidebar's <ul> is replaced. Nothing else on the page is touched.
"""
import re, sys, os

SRC = "index.html"
TRIGGER = '<a href="javascript:void(0);"'
UL_O, UL_C = re.compile(r"<ul\b[^>]*>", re.I), re.compile(r"</ul\s*>", re.I)
LI_O, LI_C = re.compile(r"<li\b[^>]*>", re.I), re.compile(r"</li\s*>", re.I)


def extent(s, st, op, cl):
    m = op.match(s, st)
    if not m: raise ValueError(f"not an open tag at {st}: {s[st:st+40]!r}")
    d, i = 1, m.end()
    while d:
        o, c = op.search(s, i), cl.search(s, i)
        if not c: raise ValueError("unbalanced")
        if o and o.start() < c.start(): d += 1; i = o.end()
        else:                            d -= 1; i = c.end()
    return i


def sidebar_span(s):
    a = s.find('<div id="sidebar-menu"')
    if a < 0: return None
    st = s.find("<ul", a)
    return st, extent(s, st, UL_O, UL_C)


def mark_current(nav, page):
    """Mark `page`'s link current and expand the group it sits in."""
    nav = re.sub(r'\s+class="active"', "", nav)
    nav = nav.replace(f'{TRIGGER} class="active subdrop">', f"{TRIGGER}>")

    link = re.search(rf'<a href="{re.escape(page)}"(?=[ >])', nav)
    if not link:
        # page is not in the sidebar at all - leave every group collapsed
        return nav, None

    # expand the enclosing <li class="submenu">, if there is one
    group_start = nav.rfind('<li class="submenu">', 0, link.start())
    label = None
    if group_start != -1 and extent(nav, group_start, LI_O, LI_C) > link.start():
        head_end = nav.find("</a>", group_start)
        head = nav[group_start:head_end]
        lab = re.search(r"<span>([^<]+)</span>", head)
        label = lab.group(1) if lab else None
        new_head = head.replace(f"{TRIGGER}>", f'{TRIGGER} class="active subdrop">', 1)
        nav = nav[:group_start] + new_head + nav[head_end:]
        link = re.search(rf'<a href="{re.escape(page)}"(?=[ >])', nav)

    nav = nav[:link.end()] + ' class="active"' + nav[link.end():]
    return nav, label


def main(dry=False):
    src = open(SRC, encoding="utf-8", errors="surrogateescape").read()
    a, b = sidebar_span(src)
    NAV = src[a:b]
    pages = sorted({h for h in re.findall(r'<a href="([^"#]+\.html)"', NAV)})
    print(f"  source nav: {len(NAV)} bytes, {len(pages)} linked pages\n")

    done = skipped = 0
    for p in pages:
        if p == SRC:
            # index.html is the source, and it is deliberately set to open on
            # Start rather than on the Uebersicht group that links to it
            print(f"  {p:<34} SKIP - source page"); skipped += 1; continue
        if not os.path.exists(p):
            print(f"  {p:<34} SKIP - not on disk"); skipped += 1; continue
        s = open(p, encoding="utf-8", errors="surrogateescape").read()
        span = sidebar_span(s)
        if not span:
            print(f"  {p:<34} SKIP - no #sidebar-menu"); skipped += 1; continue
        st, en = span
        nav, label = mark_current(NAV, p)
        if not dry:
            open(p, "w", encoding="utf-8", errors="surrogateescape").write(s[:st] + nav + s[en:])
        print(f"  {p:<34} {en-st:6d}b -> {len(nav):5d}b   group: {label or '-'}")
        done += 1
    print(f"\n  {done} page(s) synced, {skipped} skipped")


if __name__ == "__main__":
    main("--dry" in sys.argv)
