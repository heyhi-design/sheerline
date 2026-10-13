# Build & Preview — multi-page coded prototypes

*ui-studio reference. Load when a build produces 3+ structurally similar pages, or when handing a coded multi-page prototype to a user for browser review. Promoted from `skill-updates/ui-studio/build-and-preview-techniques-2026-06-17.md` on 2026-07-02; both techniques proven on a full multi-page client website prototype build (2026-06-16 session). Stack-agnostic; applies to any coded, build-and-hold prototype.*

---

## 1. Generate N near-identical pages from the approved exemplar; never hand-copy

When a coded build needs many structurally-identical pages (a service-page set, a location-page set, a product grid), do not hand-author each one. They drift — a missed class, a stale value in one of the schema blocks, an inconsistent footer.

**Technique:**
1. Get **one** page approved by the client first — the exemplar. It is the contract for structure, classes, and tokens.
2. Write a small data-driven generator in the engagement's `working/` dir (Node, no deps): one template function faithful to the exemplar + a per-item data array (slug, name, headings, the few per-page content fields). It emits **static** HTML — no build step for the developer or client.
3. Do **not** regenerate or overwrite the approved exemplar. Generate the *other* pages; leave the exemplar as the hand-authored source of truth it was approved as.
4. Build structured data (JSON-LD) inside the generator with `JSON.stringify` rather than hand-writing JSON strings — it guarantees valid JSON and keeps visible content and schema in sync from one data source.
5. Verify fidelity: read one generated page in full against the exemplar, and run a link/consistency verify script across all of them.

**Why a generator and not the Edit tool:** 9+ near-identical large files via Edit is token-expensive and error-prone; the generator amortizes one careful template across all of them and makes a later change (a new nav item, a palette-independent structural tweak) a data edit + one re-run, not an N-file hand-sweep.

**Threshold (rule of thumb):** 3+ pages sharing a section skeleton tips to the generator; below that, or when per-page structure is mostly bespoke, hand-author.

**Rewiring rule — change the generator, not the output.** When placeholder links later resolve to real pages (or any site-wide link change), update the generator's shared header/footer/CTA and **regenerate**; for the hand-authored pages, use `replace_all` on the href substring where the same target recurs identically (nav + footer + body CTA). A single placeholder page that names the clicked destination via a `?page=` query is a good prototype pattern for not-yet-built links; once everything is built, repurpose that page as the branded 404 (point the host's 404 handler at it) since nothing links to it anymore.

**Open improvement hook:** should the generator's data file carry a JSON schema so per-item fields are validated before emit?

---

## 2. To let the user review a coded multi-page prototype, serve the folder

A static multi-page prototype only renders correctly when served from its **directory root**. Relative `assets/…` and cross-page links break in a single-file preview, so the page looks unstyled or empty and the reviewer thinks it's broken.

**Technique:** start a local static server over the prototype dir and give the user the URL:

```bash
python3 -m http.server <port> --bind 127.0.0.1   # run from the prototype dir, backgrounded
# → user opens http://127.0.0.1:<port>/
```

Now styles, assets, and every cross-page link resolve; the reviewer clicks straight through Home → a service → Contact.

**Caveat (agent-specific):** the agent can *start* the server but cannot *fetch* `localhost` to self-verify it — the sandbox can't reach a user-local server. Don't loop trying to curl it; trust the server and let the user confirm. The static files also open directly via `file://` (buildless), but a served root is the robust path for cross-page navigation.

**Cross-reference:** the SKILL.md delivery-handoff note "Serving a prototype for browser review" is the short form of this technique; this reference is canonical for the full pattern. Document the serve command in the engagement README so the user can restart the server without the agent.

**Open improvement hook:** port-collision / cleanup story — does the backgrounded server linger across sessions, and who stops it?

---

*HeyHi Internal Use Only*
