# GROK HANDOFF — NIGHT INDEX CODING ZIP RELAY

**TO:** GROK  
**FROM:** ALICE TEST / Human  
**TASK_ID:** NIGHTINDEX-GROK-20261026-001  
**NONCE:** NI-20261026-8C62E29A110E  
**RETURN ZIP:** grok.reply.001.zip

## Purpose
This ZIP contains the complete live Night Index project as downloaded from AliceMoonlight/public (main). Review actual code; do not pretend it is an already installed ChatGPT/Grok/Quin plugin. This is a static GitHub Pages music research website plus a Python Bandcamp metadata resolver and GitHub Actions workflow.

The Human needs 31 Inktober 2026 prompts filled with *lyric-bearing* Halloween-themed song candidates. Human should see track, artist/band description, release date, actual playback, and lyrical information **inside the website** without manually hunting for embeds or editing anything.

## Existing code
- index.html: frontend and embedded dataset.
- candidates.json: 45 research records (some non-qualifying).
- player_manifest.json: automated track ID & lyric metadata (last audit 40 resolved, 28 with lyrics).
- scripts/resolve_bandcamp.py: fetches metadata from Bandcamp via curl_cffi/BeautifulSoup.
- .github/workflows/bandcamp-metadata.yml: runs resolver, commits manifest.
- README.md: operating directions, current limitations.

## Update requirements
1. Keep the **31 prompts in official order**, unique candidate IDs, existing links and research notes.
2. Make `candidates.json` a single source of truth instead of separately copied candidate JSON embedded in index.html.
3. Build an **in-app lyric storage and display** feature, including a durable schema/ingestion adapter for material sourced with permission or from authorized providers, track/provenance attribution, permissions flag, and a readable full-text panel. Avoid mislabeling an excerpt/summary as full lyrics.
4. Keep **automatic working Bandcamp players**. No user-entered embed codes.
5. Include artist, title, date, band description and meaningful lyric evidence on the same card.
6. Protect data and secrets: public Pages cannot store private API keys or private full-text material. Put any privileged storage/API integration in an appropriate service rather than in public JS. No credentials should enter ZIP or commits.
7. Add sensible tests: candidate JSON validation; correct prompt order; ID uniqueness; Bandcamp URL validity; player manifest mappings; full-text import/display using permitted fixture material; browser search, status and notes.
8. Update README, clear changelog, and test results. Flag assumptions and any remaining limitations explicitly.

## Integration contract
Work only inside this project. Do not change Quin, Alice's private workshop, unrelated repositories, account settings, credentials, or the live GitHub repository.

Return a **single** `grok.reply.001.zip` containing:
- REPLY.txt: what changed, what works, anything blocked.
- MANIFEST.json: fields below plus hashes of all modified/new files.
- CHANGELOG.md, TEST_RESULTS.txt.
- Complete updated project files (not only snippets/patches).

Required MANIFEST.json minimum:
```json
{
  "to": "ALICE TEST",
  "from": "GROK",
  "task_id": "NIGHTINDEX-GROK-20261026-001",
  "nonce": "NI-20261026-8C62E29A110E",
  "status": "completed",
  "changed_files": [
    {"path": "index.html", "sha256": "<64 hexadecimal characters>"}
  ]
}
```

Use `status: "blocked"` if blocked; explain why in REPLY.txt. The Human will return the ZIP to Alice. Alice verifies this nonce, checks changes/tests, then incorporates approved files. Do not demand that Human merge files or perform metadata work.

## End-to-end use
1. Human sends this GitHub repository ZIP to Grok.
2. Grok unpacks and reads this document and TASK.txt.
3. Grok codes/tests and returns one reply ZIP.
4. Human uploads reply ZIP to Alice.
5. Alice audits the manifest and code and deploys accepted changes.
