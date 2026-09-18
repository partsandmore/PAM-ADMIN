# -*- coding: utf-8 -*-
"""Localise dates and clock times in the demo content.

Runs after apply.py on the same footing: text nodes and whitelisted
attributes only, never scripts, comments or attribute values that carry
behaviour. Invoice and project IDs (INV-1454, PRJ-154) are deliberately left
alone - they are identifiers, not prose.

  "Thu, 15 Feb 2025"     -> "Do, 15. Feb. 2025"
  "Mar 15, 2025"         -> "15. Mär. 2025"
  "14 Jan 2024, 04:27 AM"-> "14. Jan. 2024, 04:27"
  "09:21 Hrs"            -> "09:21 Std."
"""
import re, sys

sys.path.insert(0, "tools/i18n")
from apply import PAGES, protected_spans, TEXT, ATTRS

MONTH = {"Jan": "Jan.", "Feb": "Feb.", "Mar": "Mär.", "Apr": "Apr.", "May": "Mai",
         "Jun": "Jun.", "Jul": "Jul.", "Aug": "Aug.", "Sep": "Sep.", "Oct": "Okt.",
         "Nov": "Nov.", "Dec": "Dez.",
         "January": "Januar", "February": "Februar", "March": "März",
         "April": "April", "June": "Juni", "July": "Juli", "August": "August",
         "September": "September", "October": "Oktober", "November": "November",
         "December": "Dezember"}
DAY = {"Mon": "Mo", "Tue": "Di", "Wed": "Mi", "Thu": "Do",
       "Fri": "Fr", "Sat": "Sa", "Sun": "So"}

MON_RE = "|".join(sorted(MONTH, key=len, reverse=True))
DAY_RE = "|".join(DAY)


def to24(h, m, ampm):
    h = int(h)
    if ampm.upper() == "AM": h = 0 if h == 12 else h
    else:                    h = 12 if h == 12 else h + 12
    return f"{h:02d}:{m}"


def localise(t):
    # "Mar 15, 2025" -> "15. Mär. 2025"
    t = re.sub(rf"\b({MON_RE})\s+(\d{{1,2}}),\s*(\d{{4}})",
               lambda m: f"{int(m.group(2))}. {MONTH[m.group(1)]} {m.group(3)}", t)
    # "15 Apr 2024" -> "15. Apr. 2024"
    t = re.sub(rf"\b(\d{{1,2}})\s+({MON_RE})\b(?=[\s,]|$)",
               lambda m: f"{int(m.group(1))}. {MONTH[m.group(2)]}", t)
    # weekday abbreviations
    t = re.sub(rf"\b({DAY_RE})\b", lambda m: DAY[m.group(1)], t)
    # 12-hour clock -> 24-hour
    t = re.sub(r"\b(\d{1,2}):(\d{2})(?::(\d{2}))?\s*([AaPp][Mm])\b",
               lambda m: to24(m.group(1), m.group(2), m.group(4))
                         + (f":{m.group(3)}" if m.group(3) else ""), t)
    # units
    t = re.sub(r"\bHrs\b", "Std.", t)
    t = re.sub(r"\bhrs\b", "Std.", t)
    t = re.sub(r"\bmins ago\b", "Minuten", t)
    return t


def run(path, dry=False):
    s = open(path, encoding="utf-8", errors="surrogateescape").read()
    spans = protected_spans(s)
    hits = 0

    def sub_text(m):
        nonlocal hits
        raw = m.group(1)
        new = localise(raw)
        if new != raw: hits += 1
        return ">" + new + "<"

    def sub_attr(m):
        nonlocal hits
        new = localise(m.group(2))
        if new != m.group(2): hits += 1
        return f'{m.group(1)}="{new}"'

    out, cursor = [], 0
    for a, b in sorted(spans) + [(len(s), len(s))]:
        if a > cursor:
            chunk = TEXT.sub(sub_text, s[cursor:a])
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
    total = 0
    for p in PAGES:
        n = run(p, dry); total += n
        print(f"  {p:<20} {n:5d} date/time fixes")
    print(f"\n  {total} total")
