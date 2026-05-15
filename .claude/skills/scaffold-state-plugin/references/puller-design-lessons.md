# Puller Design — Lessons Learned

When writing a `scripts/pull_<state>_court_rules.py` or
`scripts/pull_<state>_statutes.py` for a new state, apply
the patterns below. They are the result of debugging real
puller failures across the marketplace's state-specific
puller implementations.

> **Goal**: a puller that produces verbatim Markdown when
> the upstream is reachable, falls back to pointer stubs
> when blocked, never regresses substantive content to a
> stub, and runs from both developer workstations and
> GitHub Actions CI without operator handholding.

## Baseline target coverage

The puller's target catalog must include **both civil and
family content** as part of the baseline:

**Court-rules puller (`pull_<state>_court_rules.py`):**

- State's pleading-format rule
- State's civil-procedure rule set
- State's **family-court rule set** — **BASELINE**
- State's evidence code (where codified as rule)
- Court of Claims / similar specialized-court rules
- Surrogate's Court / probate rules (where applicable)
- Lower civil-court rule sets (the state's specific
  lower-civil / district / city / justice / special civil
  court rule bodies, where applicable)
- Sealing of court records
- Costs and sanctions
- Rules of Professional Conduct

**Statutes puller (`pull_<state>_statutes.py`):**

- State's civil-procedure code
- State's evidence code (where statutory)
- Limitations chapter
- Garnishment + exemptions chapter
- UCC enactment (Articles 2, 3, 9)
- Consumer protection (state UTPA analog)
- Debt collection (state mini-FDCPA)
- Real Property + summary proceedings (for L&T)
- **Family-law code** — **BASELINE**
- **Family Court / domestic-relations procedure** where
  separately codified — **BASELINE**
- General Construction / holidays for the case-calendar
  script

## 1. Probe the upstream before writing the catalog

Don't assume URL patterns, JSON shapes, locationIds, or
Part numbers from memory or secondary sources. **Verify
against the live source first** — write a one-off probe
script before committing to a target catalog.

### What to probe

- **The index URL** — find the page that lists every Part /
  Article / Chapter. CMS migrations move these around.
- **One sample content URL** — fetch it and confirm the
  response actually contains rule text, not a navigation
  index or stub.
- **JSON response shapes** — print the top-level keys and
  the shape of nested objects. Some APIs return
  `{documents: {items: [...]}}` vs. `{documents: [...]}`,
  and the difference will silently break a walker.
- **Adjacent identifiers** — when you think a Part covers
  topic X, fetch its title and verify against the live
  index. Adjacent Parts in the same numbering range often
  cover related-but-distinct courts and are easy to
  confuse from a table-of-contents skim.

### Common pitfalls

Prior puller authorship has shipped (or nearly shipped)
content with each of these classes of bugs. Verification
catches them all:

- **Wrong Part-to-court assignment** — labeling a Part
  with one specialized court's name when the actual rule
  body is for a different specialized court. Always fetch
  the canonical Part title.
- **Wrong Article identifier shape** — hyphenated
  sub-article identifiers (`A22-A`) often fail when called
  as `A22A` (and vice versa). Probe the API for the format
  it actually accepts.
- **Wrong Title vs. Article numbering** — some state
  consolidated laws use Title numbers; others use Article
  numbers. Secondary sources may name the same content
  either way. The API only resolves the canonical form.
- **Wrong law-to-topic assignment** — a topic that
  intuitively belongs to one statute may live in another.
  Verify each topic's home statute before committing to a
  target catalog.
- **Article numbering that skips** — some state codes have
  non-sequential Article numbering (e.g., Articles 32 then
  40 with nothing in between). Trusting "Article 33 must
  exist because there's Article 32 and Article 34" is a
  silent failure mode.

## 2. Cloudflare bot-fight bypass: two layers required

Many state court websites sit behind Cloudflare with
**bot-fight mode** that fingerprints two independent
signals:

1. **IP reputation** — residential / datacenter IPs get
   challenged; Cloudflare-trusted IPs pass.
2. **TLS handshake fingerprint** — `urllib`, vanilla
   `curl`, vanilla `requests` produce a fingerprint that
   Cloudflare reliably distinguishes from Chrome.

**Either layer alone is insufficient.** A `urllib` request
through a Cloudflare-Warp proxy will still be challenged
(TLS fingerprint mismatch). A `curl_cffi` request from a
residential IP will still be challenged (IP reputation).

### Recommended setup

```python
from curl_cffi import requests

def http_get_bytes(url):
    proxies = None
    proxy_env = os.environ.get("<STATE>_RULES_PROXY", "").strip()
    if proxy_env:
        proxies = {"http": proxy_env, "https": proxy_env}
    r = requests.get(
        url,
        impersonate="chrome",          # TLS fingerprint
        proxies=proxies,               # IP reputation (optional)
        timeout=30,
        headers={...},
    )
    if _looks_like_cf_challenge(r.content):
        raise CloudflareChallenge(url)
    return r.content
```

Install dependency: `pip install --break-system-packages
curl_cffi`. The workflow yaml runs the install step before
the puller step.

### Proxy env var is developer-local

The proxy env var (e.g., `NY_RULES_PROXY`) typically points
at a LAN address (a docker-compose warpsocks container at
`http://192.168.8.21:9091`). **GitHub Actions runners can't
reach LAN addresses.** Do NOT reference the proxy as a
workflow secret unless you have a publicly-routable proxy.

Instead, document the proxy as **developer-local**: the
canonical refresh path is for an operator to run the puller
from a workstation with their proxy set and commit the
diff. The CI run does a heartbeat / date-bump and relies on
the regression-protection check to preserve verbatim
content.

### Cloudflare-challenge detector

```python
def _looks_like_cf_challenge(body: bytes) -> bool:
    head = body[:4096].decode("utf-8", errors="replace").lower()
    return ("just a moment" in head
            or "cf_chl_opt" in head
            or "challenge-platform" in head)
```

## 3. API-key-gated pullers — conditional pattern

If the state's statute publisher offers a JSON API behind a
free API key (which many state legislative or judicial
publishers do):

- Read the key from an env var (`<STATE>_API_KEY` or
  similar).
- When the key is set: use the API path and emit verbatim
  Markdown.
- When the key is unset: emit well-formed **pointer stubs**
  that record the canonical URL and the API URL. This keeps
  the corpus's shape honest about the gap.
- Wire the env var into the workflow yaml as a repo secret.

## 4. Prefetch-and-slice the law tree

For statute APIs that return per-law trees with `?full=true`
(or an equivalent parameter that includes text bodies in
the tree response), fetch each unique `lawId` **once** and
walk the in-memory tree to find each target
article / chapter / section. This collapses N per-target
HTTP calls into M per-law calls (where M = unique law IDs).

```python
# Example: 36 article-targets across 11 unique law IDs
# collapses to 11 HTTP calls (instead of 36 with the
# per-target endpoint pattern).
unique_law_ids = sorted({t.law_id for t in targets})
law_cache = {}
for lid in unique_law_ids:
    law_cache[lid] = fetch_law(lid, api_key)  # ?full=true
for t in targets:
    root = law_cache[t.law_id][0]
    subtree = find_subtree(root, t.location_id)
    sections = collect_sections(subtree)
    render_and_write(t, sections)
```

## 5. Decode embedded escape sequences in API text fields

API JSON responses sometimes embed **literal `\n`** (two
characters: backslash + 'n') in their text fields rather
than JSON-escaped newlines. After `json.loads()` the body
still contains the literal sequence and renders as one
unbroken line.

The fix:

```python
def _decode_text(raw: str) -> str:
    out = raw.replace("\\n", "\n") \
              .replace("\\r", "\n") \
              .replace("\\t", "\t")
    out = "\n".join(line.rstrip() for line in out.split("\n"))
    out = re.sub(r"\n{3,}", "\n\n", out)
    return out.strip()
```

Apply per-section before rendering Markdown.

### Strip duplicate section-heading prefixes

Some statute APIs return each section's text body with the
section header already prepended: `"§ 3101. Scope of
disclosure. (a) Generally..."`. If your renderer emits a
`## § 3101. Scope of disclosure` heading AND the body, the
heading repeats. Strip the prefix:

```python
duplicate_prefix = f"§ {section_marker}. {title}".rstrip(".")
if body.lstrip().startswith(duplicate_prefix):
    body = body.lstrip()[len(duplicate_prefix):].lstrip(". \n\t")
```

## 6. Regression protection — `_file_is_stub`

When the puller would write a stub but a verbatim file
already exists at the target path, **keep the existing
file** rather than overwriting:

```python
def _file_is_stub(path: Path) -> bool:
    """Detect whether an existing MD file is a pointer-stub."""
    try:
        head = path.read_text(encoding="utf-8")[:1024]
    except Exception:
        return True
    return "(stub" in head or "Format:** pointer stub" in head


def write_with_regression_guard(target, out_path, fetched_iso, reason):
    if out_path.exists() and not _file_is_stub(out_path):
        return WriteResult(..., error=f"{reason} (kept existing file)",
                            stub=False)
    # otherwise write fresh stub
    out_path.write_text(render_stub(target, fetched_iso, reason))
```

This is critical for CI safety. The quarterly refresh on a
runner that can't pass Cloudflare must not regress the
verbatim corpus that a developer committed from their
workstation.

## 7. Clean up renamed-target leftovers

When you fix a wrong label (e.g., `CVP-Article-33-Trial.md`
→ `CVP-Article-40-Trial.md`, `GBS-Article-22A-Deceptive.md`
→ `GBS-Article-22-A-Deceptive.md`), the old files do not
get cleaned up automatically. Either:

- Add explicit `rm` calls in the commit cleaning up old
  paths.
- Run a glob over the output directory and delete files
  not in the current target catalog.

The puller writes new files at the new label paths; the
old files persist alongside as stale stubs unless removed.

## 8. JSON-escape quotes inside long description strings

When writing long `plugin.json` description strings or
`marketplace.json` description strings, any literal double
quote inside the string must be backslash-escaped:

```json
"description": "...the \"serious injury\" threshold under..."
```

NOT:

```json
"description": "...the "serious injury" threshold under..."  // INVALID
```

This trips an `Expecting ',' delimiter` JSON parse error
that's easy to miss until the marketplace fails to load.
Test with `python3 -m json.tool` after every edit.

## 9. Workflow yaml — install dependencies in the step

The `refresh-references.yml` step that runs the puller must
install third-party Python deps inline because the runner
doesn't carry a virtualenv between steps:

```yaml
- name: <state> — court rules
  if: matrix.target == '<state>'
  continue-on-error: true
  timeout-minutes: 15
  run: |
    pip3 install --break-system-packages curl_cffi
    python3 scripts/pull_<state>_court_rules.py --workers 4
```

`continue-on-error: true` and `timeout-minutes` are
non-negotiable — a stuck or 4xx-failed puller must not
abort the rest of the matrix.

## 10. Document what's a stub and why

Some content has no free authoritative HTML source —
paywalled secondary sources (West, LexisNexis), interactive
forms, PDF-only publications. Ship those as **pointer
stubs** with:

- The canonical URL
- A one-paragraph scope description
- A `_(stub — fetch deferred)_` status marker
- A "How to retrieve verbatim text" section explaining
  what's needed (API key, paid subscription, etc.)

A pointer stub is not a failure — it's an honest
documentation of the gap. Common categories of unavoidable
stubs:

- **Paywalled rule sets** — e.g., Rules of Professional
  Conduct published commercially by West / LexisNexis
  without a free HTML mirror
- **PDF-only style manuals** — citation manuals that the
  publisher distributes only as PDF
- **Interactive-page-only local rules** — per-court
  procedural manuals served as JavaScript apps without
  scrapeable HTML
- **Per-judge / per-justice Part Rules** — published
  individually with no consolidated HTML index

## Summary checklist

When writing a new state puller, verify each item:

- [ ] Probed the live upstream for actual URL pattern and
      ID structure before committing the target catalog
- [ ] Verified adjacent identifiers (no Part-N vs Part-N+1
      confusion)
- [ ] Used `curl_cffi` with Chrome TLS impersonation
- [ ] Supports `<STATE>_RULES_PROXY` env var for
      Cloudflare-Warp proxy routing (developer-local)
- [ ] Falls back to pointer stubs on Cloudflare challenge
      / 4xx / API-key-missing
- [ ] `_file_is_stub` check prevents regression of verbatim
      content to stubs
- [ ] If the upstream is a JSON API: prefetches per-law trees
      with `?full=true` and slices in memory
- [ ] If the upstream returns literal `\n`: decoded with
      `_decode_text` before rendering
- [ ] If the upstream embeds section-header prefix in body:
      stripped before rendering
- [ ] Workflow yaml `pip install`s third-party deps inline
- [ ] Workflow yaml uses `continue-on-error: true` and a
      `timeout-minutes` cap
- [ ] Long description strings in plugin.json /
      marketplace.json have escaped quotes
- [ ] Cleaned up legacy-named files when renaming targets
- [ ] Documented honest stubs for content with no free
      authoritative HTML source
