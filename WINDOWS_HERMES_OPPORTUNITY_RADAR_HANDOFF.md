# Windows 11 Hermes Opportunity Radar: Destination-Agent Handoff

## Role and authority

You are taking over an existing, privacy-sensitive opportunity-radar project for **Farzaneh Fayazbakhsh** on a Windows 11 laptop that stays online for scheduled work. The user has already installed Hermes and configured the Telegram integration. You must configure the remaining project environment, validate the pipeline, create the required Hermes schedules, and leave the system operating safely.

Work directly in the extracted project at:

```text
C:\projects\job-hunter
```

If the bundle was extracted elsewhere, move it to that exact path before configuring schedules. Do not assume a shell path convention: Hermes on native Windows executes terminal commands through Git Bash, while native Windows executables need `C:/...` paths.

The archive intentionally excludes credentials, Hermes profile backups, virtual environments, caches, transient rendering output, and Git metadata. Do not ask the user to place a token, password, OAuth credential, Telegram chat ID, connection string, or API key in this project. Do not print secrets in messages, files, commits, reports, scheduler prompts, or logs.

## Completion target

Operate a high-recall, auditable Stockholm/Solna/Uppsala opportunity radar for Farzaneh that:

1. discovers relevant PhD roles and realistic research-related jobs;
2. deterministically enumerates the configured official vacancy sources;
3. uses search engines, lab pages, aggregators, and boards for discovery/reconciliation only;
4. accepts a listing only after verifying its current official employer vacancy/application page;
5. deduplicates by employer reference or canonical official URL;
6. ranks roles using explainable CV-fit evidence and explicit gaps, not probability claims;
7. creates truthful tailored RenderCV YAML/PDF artifacts for accepted roles;
8. generates a static, responsive GitHub Pages report;
9. delivers a transparent daily Telegram summary; and
10. never labels an incomplete refresh as complete or publishes partial/stale data as current.

The report is public at the existing repository’s GitHub Pages site. Treat public publishing as deliberate: the report exposes tailored CV PDFs, which may contain personal and reference information.

## Non-negotiable data and privacy rules

- `data/master_profile/master_cv.yml` is the immutable master CV. **Never overwrite it.** Tailored copies only belong under `data/tailored/`.
- Preserve the master CV’s content, ordering, dates, links, publications, references, YAML semantics, `design`, and `locale` fields.
- The master profile is intentionally bundled although it is not committed to the public repository. Do not add it, generated master PDFs, local credentials, or private source material to Git.
- `data/seen_positions.json` is an append-only identity ledger. Never remove an ID merely because a listing expires.
- `data/positions.json` holds active report records. Do not remove a record due only to a source-fetch failure; remove it only for confirmed expiry/unavailability according to the active-data policy.
- Never fabricate qualifications, experience, degrees, dates, research results, publication status, eligibility, source status, or delivery results.
- Farzaneh’s SLU bioinformatics MSc is ongoing. Do not describe it as completed.
- Tailored personal statements must use simple, natural language: emphasize established cellular/molecular-biology research and publications, then honestly connect newer bioinformatics skills to collaboration between experimental and computational researchers. Do not overstate machine-learning, multiomics, clinical, or deep-learning experience.
- Name tailored artifacts deterministically as `<stable_position_id>_<short_underscore_title>.yml` and `.pdf`. Manual application packages use the same ID convention in their own folder.

## Existing project state to preserve

The bundle includes the source code, current active positions, permanent seen ledger, tailored artifacts, the private master profile, RenderCV guide, source registry, tests, and the standalone `KTH_960383_multiomics_cancer_bioinformatics` application package.

The pipeline’s designed scope is:

- geography: **Stockholm, Solna, Uppsala**;
- primary opportunity types: **PhD positions** and **realistic research-related jobs**;
- mandatory official-source verification for accepted listings;
- PhD inclusion may cover relevant adjacent disciplines; non-PhD jobs use stricter realistic-fit gating;
- SLU is a required Uppsala/Ultuna priority because Farzaneh is studying there.

The official source registry is `data/source_registry.json`. It currently defines KI, KTH, Uppsala University (PhD and all vacancies), Stockholm University Chemistry, Stockholm University Molecular Biosciences/Wenner-Gren, SciLifeLab, and SLU. Its source health is evidence only for that explicit registry—not proof that all regional employers have been covered.

Important limitation: SLU’s public vacancy index is client-rendered. The harvester marks it `dynamic`, meaning web reconciliation is required. Do not interpret static zero listing links as no SLU vacancies. Implement a tested official dynamic feed/API extractor only after you can verify its behavior. Until then, unresolved required dynamic coverage must produce `STATUS: partial`.

## Project files and responsibility map

| Path | Purpose |
|---|---|
| `data/master_profile/master_cv.yml` | Immutable RenderCV master CV; private, not for Git. |
| `data/master_profile/RENDERCV_RENDERING_GUIDE.md` | Exact styling and structural preservation guide. |
| `data/positions.json` | Active report entries. |
| `data/seen_positions.json` | Permanent deduplication ledger. |
| `data/source_registry.json` | Governed official-source coverage map. |
| `scripts/harvest_sources.py` | Deterministic official-index harvester producing `data/discovery_manifest.json`. |
| `scripts/reconcile_manifest.py` | Current reconciliation helper; inspect before using and do not treat it as a complete dynamic-source solution. |
| `build_test_report.py` | Report-generation helpers and position-CV renderer. |
| `refresh_report.py` | Rebuilds `index.html` from active records; it does not discover positions. |
| `tests/test_harvest_sources.py` | Harvester/health/governance regression tests. |
| `tests/test_rendering_guide.py` | RenderCV environment and style-preservation tests. |
| `tests/validate_tailored_pdfs.py` | PDF text/structure/contact-sheet validation. |
| `tests/test_report_e2e.py` | Browser report test, including tabs, localStorage state, theme, and mobile overflow. |
| `index.html` | Generated static report. Do not hand-edit unless intentionally changing the report generator. |

## Environment to create

Use isolated project-local environments; do not copy one from another computer.

1. Confirm tools and project state:

```bash
cd /c/projects/job-hunter
hermes doctor
python --version
uv --version
git --version
git status --short
```

2. Create the renderer environment with exactly Python 3.12 and RenderCV 2.8:

```bash
uv venv --python 3.12 .rendercv-venv
uv pip install --python .rendercv-venv/Scripts/python.exe "rendercv[full]==2.8"
```

3. Create a separate local test environment (or an equivalent environment that does not contaminate Hermes) and install only dependencies actually imported by the project tests:

```bash
uv venv --python 3.12 .venv
uv pip install --python .venv/Scripts/python.exe pytest ruamel.yaml pypdf pymupdf pillow playwright
.venv/Scripts/python.exe -m playwright install chromium
```

4. Inspect the current tests before changing any paths. `tests/test_report_e2e.py` currently points at a Windows Chrome executable. Prefer a robust, installed Chromium/Playwright executable; make the smallest tested compatibility edit needed for the new machine.

5. Do not copy `.rendercv-venv`, `.venv`, `.env`, `__pycache__`, `data/.render_work`, `data/test_output`, or browser caches into Git.

## RenderCV baseline: must remain identical in intent

- Library: `rendercv[full]==2.8`
- Renderer: RenderCV using Typst
- Theme: `classic`
- Default page size: US Letter
- Locale: English

The master YAML must preserve this configuration exactly:

```yaml
design:
  theme: "classic"
  page:
    top_margin: "0.55in"
    bottom_margin: "0.55in"
    left_margin: "0.55in"
    right_margin: "0.55in"
  typography:
    alignment: "left"
    font_size:
      body: "9.5pt"
      name: "28pt"
      headline: "9.5pt"
      connections: "9.5pt"
      section_titles: "1.35em"
  entries:
    date_and_location_width: "2.4cm"
  templates:
    education_entry:
      main_column: "**INSTITUTION**, AREA\nLOCATION\nSUMMARY\nHIGHLIGHTS"
      date_and_location_column: "DATE"
    experience_entry:
      main_column: "**COMPANY**, POSITION\nLOCATION\nSUMMARY\nHIGHLIGHTS"
      date_and_location_column: "DATE"
    normal_entry:
      main_column: "**NAME**\nLOCATION\nSUMMARY\nHIGHLIGHTS"
      date_and_location_column: "DATE"

locale:
  language: "english"
```

Keep all other RenderCV classic defaults. Preserve literal `\n` template line breaks; unquoted year-only dates such as `date: 2024`; quoted display ranges such as `date: "2025–present"`; bold `**Farzaneh Fayazbakhsh**` author names; escaped equal-contribution asterisks; and reference entries using `#linebreak()` and `mailto:`.

Use the supported command form, never the obsolete `--output-folder-name` option:

```bash
.rendercv-venv/Scripts/rendercv.exe render "C:/projects/job-hunter/data/tailored/example.yml" --output-folder "C:/projects/job-hunter/data/.render_work/example"
```

Do not shrink margins or fonts, delete publication content, force fewer pages, or strip `design`/`locale` fields just to make a CV fit. Inspect every rendered page before claiming visual success.

## Required validation before scheduling

Do not change code blindly. First inspect definitions and usages. Then run these focused checks from the project root, adapting only the Python environment prefix if needed:

```bash
.venv/Scripts/python.exe -m pytest tests/test_harvest_sources.py tests/test_rendering_guide.py -q
.venv/Scripts/python.exe tests/test_report_e2e.py
.venv/Scripts/python.exe tests/validate_tailored_pdfs.py
```

Also run `scripts/harvest_sources.py` once and inspect `data/discovery_manifest.json`. Confirm each required source is explicitly `ok`, `dynamic`, `empty`, or `failed`; do not collapse these conditions into “healthy.” Verify that no source index/navigation URL was accepted as a vacancy candidate.

Before any document or report operation, calculate and record the SHA-256 of `data/master_profile/master_cv.yml`; verify it remains unchanged afterward. Do not place that hash in a public report if it would identify private material unnecessarily.

## Daily refresh policy

The daily job must be self-contained because cron runs have no current chat context. It must:

1. Work in `C:\projects\job-hunter`.
2. Run `scripts/harvest_sources.py` first, creating a fresh manifest.
3. Preserve source-health totals: total, ok, dynamic, empty, failed, and candidate URLs.
4. Triage every deterministic candidate title locally before expensive browsing.
5. Use official-domain search and external boards only to discover/reconcile candidates; accept only after verifying a live official vacancy/application page.
6. Check expiry/deadline, geography, opportunity kind, degree/eligibility gates, canonical URL, and employer reference.
7. Deduplicate against the permanent seen ledger before calling a position new.
8. Apply explainable fit scoring with concrete reasons and honest gaps; do not use a score as a probability.
9. Create a tailored YAML/PDF only for accepted, active opportunities. Preserve the master CV and validate the PDF.
10. Rebuild `index.html`, run relevant tests, and verify generated artifact paths.
11. Commit and push only verified complete report updates, if GitHub authentication and explicit publication authorization are available.
12. Fetch the deployed Pages report and at least one hosted artifact after publishing before claiming it succeeded.
13. If any required source failed/was empty, dynamic reconciliation remains unresolved, candidate triage is incomplete, rendering/tests fail, or publishing cannot be verified: return `STATUS: partial` (or `failed` when appropriate), preserve last-known-good hosted content, and do **not** publish partial data as current.

Use this compact machine-readable output contract at the end of every daily run:

```text
REFRESH_DATE: YYYY-MM-DD
DISCOVERY_SOURCES_TOTAL: integer
DISCOVERY_SOURCES_OK: integer
DISCOVERY_SOURCES_DYNAMIC: integer
DISCOVERY_SOURCES_FAILED: integer
DISCOVERY_SOURCES_EMPTY: integer
DISCOVERY_CANDIDATE_URLS: integer
NEW_COUNT: integer
NEW_IDS: comma-separated stable IDs or NONE
ACTIVE_COUNT: integer
PHD_COUNT: integer
JOB_COUNT: integer
PAGES_URL: URL or NOT_PUBLISHED
STATUS: success|partial|failed
WARNINGS: concise text or NONE
```

Never claim universal completeness. State coverage only relative to the configured source universe, and call out known gaps such as dynamic SLU coverage or incomplete registry scope.

## Scheduled jobs to create

First verify the user’s Hermes ChatGPT/OpenAI authentication and Telegram integration are already working. Do not request, reveal, or save the Telegram token or numeric chat ID. Create the Telegram delivery target through Hermes’s configured integration and verify its authorization with a manually run test.

Configure the timezone as **Europe/Stockholm** and create these distinct jobs. Pin exact provider/model values only if those models are available in the destination Hermes installation; otherwise stop and ask the user which available model to use rather than silently changing quality/cost behavior.

### 1. Daily opportunity refresh

- Name: `Daily Stockholm–Uppsala opportunity refresh`
- Schedule: `0 11 * * *` (11:00 Europe/Stockholm)
- Model/provider: `gpt-5.6-terra` / `openai-codex`
- Reasoning effort: medium
- Toolsets: web, terminal, file
- Skills: `grounded-citations`, `github-repo-management`, `opportunity-monitoring`
- Workdir: `C:\projects\job-hunter`
- Delivery: local
- Continuity: enabled

Use the daily refresh policy above verbatim in its cron prompt. The prompt must explicitly command the harvester, mandate official verification, prohibit publishing partial work, and emit the machine-readable output contract.

### 2. Noon Telegram summary

- Name: `Noon opportunity radar summary`
- Schedule: `0 12 * * *` (12:00 Europe/Stockholm)
- Model/provider: `gpt-5.6-luna` / `openai-codex`
- Reasoning effort: low
- Toolsets: file, terminal
- Workdir: `C:\projects\job-hunter`
- Delivery: the already configured authorized Telegram chat
- Context: the daily refresh job’s most recent completed output

The summary must read the latest daily result and `data/positions.json`, cross-check counts programmatically, then send a concise message that includes: date, `STATUS`, verified new IDs/count, active PhD/job counts, report URL only when hosted content is confirmed current, and material warnings. If the refresh was partial or failed, say clearly that hosted Pages may be stale and do not imply newly local roles were published. It must never report the source-universe coverage as complete.

### 3. Weekly source-coverage audit

- Name: `Weekly opportunity-source coverage audit`
- Schedule: every Sunday at 09:30 Europe/Stockholm
- Model/provider: use the available substantive research model; prefer `gpt-5.6-terra` / `openai-codex`
- Reasoning effort: medium
- Toolsets: web, terminal, file
- Skills: `grounded-citations`, `opportunity-monitoring`
- Workdir: `C:\projects\job-hunter`
- Delivery: local
- Continuity: enabled

The audit reviews the source universe, source health, omissions, broken URL patterns, dynamic source behavior, external-discovery misses, and proposed registry changes. It must produce a reviewable proposal with official URLs and rationale, but **must not automatically edit** `data/source_registry.json` or silently broaden/reduce scope. The user must approve new required sources, source removals, geography changes, or relevance-policy changes.

## GitHub Pages and source-control policy

The existing remote is:

```text
https://github.com/farzaneh-fb/stockholm-uppsala-opportunity-radar.git
```

Do not push until GitHub authentication is explicitly available and the working tree has been reviewed. Do not commit the master profile, credentials, virtual environments, caches, local Hermes configuration, or generated transient files. Keep the public report privacy implications visible to the user.

Before enabling routine publication:

1. inspect `.gitignore` and ensure private materials remain excluded;
2. run `git status --short` and inspect every intended change;
3. run focused tests and report E2E;
4. push only a verified complete refresh;
5. read back the exact GitHub Pages URL and one hosted tailored PDF; and
6. compare that artifact to local content or hash before declaring publication successful.

## Always-on operation and recovery

The destination laptop is the **single active scheduled runner and Telegram polling gateway**. Do not leave the old laptop’s gateway or identical schedules enabled against the same Telegram bot; duplicate polling/schedules can conflict and duplicate messages or pushes.

After successful manual validation, configure Hermes gateway auto-start using the current official Hermes commands and verify with `hermes gateway status`. On Windows, test actual restart recovery—not merely installation output. Keep the machine plugged in, awake while connected to AC power, online, and logged in near scheduled runtime. Configure Windows sleep/hibernation and lid-close behavior accordingly. Inspect Hermes logs after each failure and after reboot.

## Required acceptance tests and completion report

Do not stop at a plan or a successful command exit. Complete a real, controlled verification sequence:

1. Confirm the project is in `C:\projects\job-hunter` and the master-CV hash stays unchanged.
2. Confirm RenderCV 2.8 / classic / Typst and focused tests are working.
3. Run a live harvester and inspect the manifest/source-health semantics.
4. Run a report build and report browser E2E; inspect desktop and mobile screenshots.
5. Render and validate at least one tailored CV without fabricating content.
6. Create all three schedules and list them back, including timezone/schedule, workdir, model, delivery mode, enabled state, and next run.
7. Manually run the refresh job. Read its actual final output; distinguish `success`, `partial`, and `failed`.
8. If and only if the refresh actually publishes, read back the live Pages report and one hosted PDF.
9. Manually run the noon summary; confirm Hermes reports Telegram delivery to the configured authorized chat. Do not repeat the chat ID in the report.
10. Restart the laptop or test the configured startup route, then verify gateway/scheduler status and next runs.

At the end, report only verified facts: files configured, test results, current active/local vs hosted counts, job IDs/schedules (but not Telegram identifiers), Pages verification state, and unresolved warnings. If blocked by missing authorization, a source failure, a dynamic source, incomplete triage, or startup limitations, state the blocker plainly and preserve last-known-good public state.
