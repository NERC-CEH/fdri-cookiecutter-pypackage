# After generation

```bash
cd <package_name>
uv sync              # install all dependencies
make install-hooks   # configure git to use .githooks/
make qa              # format, lint, type-check, test
```

If you chose `sphinx` docs, preview them locally:

```bash
make docs-serve  # serves at http://localhost:8000
```

## Citation metadata (`CITATION.cff`)

The template generates a `CITATION.cff` at the project root, with some fields pre-filled from your prompt answers
(title, author, email, affiliation, repo URL, version, licence). GitHub renders a **Cite this repository** button
when this file is present, and tools like Zenodo and Zotero read it automatically.

Before your first tagged release, review the `CITATION.cff` file and update:

- **ORCID** for each author ([orcid.org](https://orcid.org/))
- **Keywords** as NERC vocabulary URIs (e.g. `http://onto.nerc.ac.uk/vocab/...`)
- Split `given-names` / `family-names` if your full name wasn't split cleanly (the template splits on the last space)

After depositing in a catalogue (EIDC, Zenodo, etc.), also add:

- `doi`
- `repository`
- `date-released`

Full guidance: [NERC-CEH CFF guidelines](https://github.com/NERC-CEH/repo-guidance/blob/main/cff-guidance/citation-cff_guidelines.md).

## Writing docs

The generated `docs/source/` directory contains `.rst` files to get you started, but you can use Markdown (`.md`) or
reStructuredText (`.rst`) - or mix both. [MyST-Parser](https://myst-parser.readthedocs.io/) is installed and
configured so Sphinx handles both formats automatically.

**Markdown example** - create `docs/source/my-page.md`:

```markdown
# My page

Some content here.
```

**reStructuredText example** - create `docs/source/my-page.rst`:

```rst
My page
=======

Some content here.
```

Then add the page to the table of contents in `docs/source/index.rst`:

```rst
.. toctree::

    my-page
```

Either format works - Sphinx resolves the filename regardless of extension.
