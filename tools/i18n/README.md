# German translation tooling

The glossary that turned the English SmartHR template into German. Kept in
the repo so the remaining pages can be translated the same way rather than
by hand.

| file | purpose |
|---|---|
| `glossary.py`  | first pass: navigation, actions, labels, statuses, modules |
| `glossary2.py` | second pass: compound labels the first pass missed |
| `people.py`    | demo people, companies and mailboxes, curated by hand |
| `apply.py`     | applies the glossary to the pages listed in `PAGES` |
| `dates.py`     | date and clock formats, run after `apply.py` |

## Running it

```bash
python tools/i18n/apply.py --dry     # report only, writes nothing
python tools/i18n/apply.py
python tools/i18n/dates.py
```

`apply.py` writes `tools/i18n/untranslated.json` listing every string it did
not recognise, which is how you find what to add next. Both scripts are
idempotent: German text does not match the English keys, so a second run is
a no-op.

## What it will and will not touch

Rewritten: text nodes, and the `placeholder`, `title`, `alt` and
`aria-label` attributes.

Never touched: `href`, `src`, `class`, `id`, `data-*`, inline `<script>` and
`<style>` blocks, and HTML comments. That is what keeps links and CSS
selectors intact - verify after any run with a structural-attribute diff
against the previous commit.

## To translate more pages

Add filenames to `PAGES` in `apply.py`, run the dry pass, add whatever shows
up in `untranslated.json` to `glossary2.py`, then run for real.

## Known gap

`assets/plugins/apexchart/chart-data.js` holds the chart labels. It is shared
by 148 pages and mixes display strings with element ids and ApexCharts config
values (`'donut'`, `'smooth'`, `'attendance-chart'`), so it cannot be run
through a blanket replace - the display strings have to be picked out first.
