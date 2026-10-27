# Alice → Miss Spock handoff envelope: proposed v1

**Proposal, not Miss Spock's official switchboard format.** Do not assume another agent already implements these fields.

ZIP must have one root `envelope.json` with:
`schema=ALICE_RELAY_ENVELOPE_V1`, `message_id`, `sender_agent_id`, `recipient_agent_id`, `project_id`, `task_id`, `nonce`, `created_utc` and `files` (payload path → lowercase SHA-256).

All other archive members stay under `payload/` and are SHA-256 pinned. Alice's private receiver checks expected agent IDs, project ID, CRC, duplicate paths, traversal, linked entries, exact hashes and size ceilings; it does not execute or automatically merge inbound ZIPs.

Agent IDs are distinct, including `alice.moonlight`, `miss-spock`, `lenore.alpha` and `lenore.assistant`. These names are routing labels, *not verified sender authentication*. Packages that mismatch the intended project or agent are held for Human review.

Do not send private notes or third-party project source to the public switchboard. The current public page shows only manually sanitized status summaries.
