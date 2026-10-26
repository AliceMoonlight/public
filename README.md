# Night Index — Inktober Halloween Bandcamp Research

This is the **live project source**, not a stand-alone ChatGPT plugin. Its static website is deployed at https://alicemoonlight.github.io/public/ from the public repository https://github.com/AliceMoonlight/public.

## How it works

The project maps all **31 official Inktober 2026 prompts**, in order, to Halloween-themed music on Bandcamp. Existing songs are *candidates*, not approved mix selections.

- **index.html** — all-in-one static website (HTML/CSS/JavaScript) with embedded candidate records. Browsable prompt cards, lyric summaries and brief previews, official Bandcamp embedded players, search/filter, review status, notes, shortlist.
- **candidates.json** — canonical research dataset for the Bandcamp resolver (currently 45 candidates). **Important:** the frontend still has a duplicated embedded copy; when editing songs, update both until Grok unifies them.
- **player_manifest.json** — generated metadata: confirmed numeric Bandcamp track IDs, lyric-availability flags, short excerpt, matching horror vocabulary, and resolution statuses. Last audit: **40** resolved IDs; **28** songs with published lyrics.
- **scripts/resolve_bandcamp.py** — Python script that reads candidate links, inspects public track metadata with `curl_cffi` and BeautifulSoup, and regenerates `player_manifest.json`.
- **.github/workflows/bandcamp-metadata.yml** — GitHub Actions job using Python 3.12 to run the resolver on relevant commits or manual dispatch, then commits changed player metadata.
- **GROK_HANDOFF.md, TASK.txt, ROUTING.json, CONTEXT.md** — complete instructions for the Grok ZIP relay.

### Play / review

Visit https://alicemoonlight.github.io/public/ . Review candidates by Inktober prompt and press Play on the embedded Bandcamp player. Read the lyric summary and excerpt, mark candidates, add notes. Review settings are saved to **browser localStorage** (key `night_index_v01_reviews`), not synchronized between devices. Export before clearing browser storage.

### Local development

From the repository root:

```sh
python -m http.server 8000
```

Then open `http://localhost:8000/`. Serving via HTTP ensures `player_manifest.json` can be fetched; opening `index.html` as `file://` can block file fetches.

To refresh official Bandcamp player metadata on a workstation with internet access:

```sh
python -m pip install curl_cffi beautifulsoup4
python scripts/resolve_bandcamp.py
```

To publish, commit to the repository's `main` branch. GitHub Pages is configured to deploy from `main` / `/(root)`.

### Current limits

- No full copyrighted lyric text is stored by the current code. A full-lyrics storage/display interface for material obtained with permission is an intended upgrade. Last audit covered 22/31 prompts with lyric-qualified candidates.
- Some research leads are **album** URLs rather than individual track URLs and are not resolved as playable individual tracks.
- No backend login/database currently exists; a public GitHub Pages site cannot securely store server secrets. Keep API keys out of public HTML, JSON, and commits.
- The Bandcamp resolver depends on third-party page structure; verify parsed output and don't invent song metadata.

## For Grok

Read **GROK_HANDOFF.md**, then **TASK.txt**. Modify a **copy** of these repository files. Return one `grok.reply.001.zip` containing full updated source and `REPLY.txt`, `MANIFEST.json`, `CHANGELOG.md`, and `TEST_RESULTS.txt`. Echo the task ID and nonce from `ROUTING.json`. Do **not** push to the user's live GitHub repository. Alice will inspect and integrate the changes after Human returns the ZIP.
