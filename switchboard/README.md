# Alice's public project switchboard

**Open the phone-friendly dashboard:** https://alicemoonlight.github.io/public/switchboard/

This new `switchboard/` directory is separate from the live **Night Index** website at the repository root. The switchboard reads a `status.json` snapshot that exposes only whitelisted public project summaries. The private registry, checkpoint history, inbound ZIPs, note fields, hashes and other agents' projects are not published.

**Honesty:** the status is manually updated and is *not* a live monitor or a background job. “Active” means the current focus in Alice's project registry, not unattended work. No project changes can be made from this dashboard.

Alice owns Alice's projects. Miss Spock coordinates Quin integration, and other agents own their work. Sender/receiver/project/task and digest checks on incoming ZIPs are implemented in an Alice-owned private offline validator; even a valid ZIP is for review only, never auto-merged. The identity fields are not cryptographic proofs of who authored a package.

No existing Night Index `index.html`, `candidates.json`, `player_manifest.json`, or workflows were touched. The route proposal below is not claimed as Miss Spock's actual format.
