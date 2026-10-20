# MAIS site

Front end for the [MAIS open-problem registry](https://github.com/Math-for-AI-Safety/MAIS). Plain HTML, CSS and JavaScript, with no build step.

- `index.html`, `problems.html`, `agendas.html`, `fields.html`, `about.html`
- `assets/data.js`: snapshot of the registry (92 problems, 8 agendas) taken from the MAIS repository
- `assets/art.js`, `assets/site.css`, `assets/site.js`: drawings, styles and helpers

Served through GitHub Pages from `main`, root.

## Refresh full wiki statements

The wiki embeds the complete problem Markdown at build time; reading it needs no GitHub request. Source authorship, references, and a pinned source revision are retained. Other problem links stay inside the wiki; agenda source documents and references link to the pinned upstream revision.

```sh
python3 -m venv .venv
.venv/bin/pip install -r scripts/requirements.txt
.venv/bin/python scripts/sync-wiki.py /path/to/MAIS
```

Review the generated `wiki/p/` changes before committing. The script updates existing problem pages and preserves their navigation and metadata; adding problems or refreshing registry metadata is a separate step.
