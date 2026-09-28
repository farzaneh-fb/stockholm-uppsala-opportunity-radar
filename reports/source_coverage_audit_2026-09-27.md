# Weekly opportunity-source coverage audit — 2026-09-27

Scope: Stockholm / Solna / Uppsala; PhD and research jobs. Registry was inspected but not modified. Baseline: `data/source_registry.json`; latest manifest: `data/discovery_manifest.json`, generated 2026-09-26 09:02 UTC.

## SOURCE_UNIVERSE_COVERAGE

**Status: incomplete.** The registry has 8 source records covering 6 organisations/partner networks: KI, KTH, Uppsala University (two overlapping indexes), Stockholm University (two department pages), SciLifeLab, and SLU. The latest manifest reports 6 `ok`, 1 `failed` (KTH), and 1 `dynamic` (SLU), with 59 distinct candidate URLs.

The most consequential universe gap is Stockholm University: the official central jobs route is not registered even though it states that it carries current openings, including doctoral positions, and links to the university-wide Varbi index.[1] The registry instead samples only Chemistry and MBW. The central route should be authoritative; department and faculty pages should be secondary discovery/reconciliation feeds.

The employer universe also omits several official research-employer routes.

FOI currently publishes many vacancies, including Stockholm/Kista entries, while IVL’s official careers page leads to a Teamtailor jobs index.[12][18][19]

RISE has an official careers index and has advertised research roles available in Stockholm.[17][21]

The two regional employers have central vacancy routes capable of carrying clinical or applied-research jobs; Region Stockholm has published an official researcher vacancy on that route.[13][14][20]

SEI’s official opportunities route should also be monitored with an SEI Headquarters/Stockholm location filter.[11]

Södertörn University has an official vacancy index and says doctoral positions are advertised collectively once per year, but its campus is in Flemingsberg.[9][10] It should remain outside the strict city-level universe unless “Stockholm” is explicitly defined as Stockholm County/metro rather than the municipality.

## HEALTH_GAPS

| Severity | Source / official URL | Organisation · geography · role scope | Evidence and manifest reconciliation | Recommended source type / requiredness | Extraction or reconciliation method | Why this closes the gap |
|---|---|---|---|---|---|---|
| **Critical** | https://www.kth.se/lediga-jobb?l=en | KTH · Stockholm · PhD, postdoc, researcher, research engineer | Latest manifest: `failed`, 0 candidates, WinError 10060. The official index is nevertheless indexed with live vacancy rows, so the failure is transport-specific rather than evidence of no jobs.[5] | Keep `official_vacancy_index`, `required: true` | Retry with exponential backoff and a browser/extractor fallback; if the index still times out, reconcile official `kth.se/lediga-jobb/<id>?l=en` results discovered through the configured official-domain query. Require a positive completeness check against index row count before status `ok`. | Prevents a whole required employer from silently contributing zero candidates. |
| **Critical** | https://www.su.se/english/about-the-university/work-at-su/available-jobs and linked https://su.varbi.com/en/what:findjob/?showresult=1&categories=1&checklist=1&orglevel=1&ref=1&nologin=1&nocity=1&nocounty=1&nocountry=1&nolocalefield=1&nolocalegroup=1&hideColumns=town&norefsearch=1 | Stockholm University · Stockholm · all PhD/research jobs | Not in registry/manifest. The official page says the university-wide route contains current jobs and that applications, including doctoral positions, use Varbi.[1] Current DSV and Public Health official pages expose 10 PhD vacancies absent from the manifest.[3][4] | Add central route as `official_vacancy_index`, `required: true`; retain department pages as optional reconciliation sources | Harvest direct Varbi index. Match both `su.varbi.com/what:job/jobID:` **and** `su.varbi.com/en/what:job/jobID:`; normalize `/en/`; paginate until no unseen job IDs. | Replaces two-department sampling with university-wide coverage and fixes the current pattern’s inability to match `/en/what:job/` links. |
| **Critical** | https://www.uu.se/en/about-uu/join-us/jobs-and-vacancies?query=PhD | Uppsala University · Uppsala · PhD | Official search reports **38 hits but renders 10 initially**; latest PhD manifest has 11 candidates. Current official IDs `971937` and `970239` are absent from the manifest.[7] The “all vacancies” manifest source also contains only 10 candidates. | Keep official indexes `required: true`; add explicit completeness metadata | Reproduce the site’s “Show more hits” request/API rather than trying inert `page=` parameters; continue until harvested count equals the page’s declared total. Deduplicate on numeric `query=` ID and fail closed if `observed < declared`. | Detects and eliminates first-page truncation masquerading as a successful harvest. |
| **Critical** | https://www.slu.se/en/about-slu/work-at-slu/jobs-and-vacancies?filters=OccupationArea%24%24string%7CPhD | SLU · Uppsala/Ultuna · PhD | Latest manifest is `dynamic` with one expired Uppsala vacancy. The official filtered index currently shows 5 PhD hits, including an Uppsala PhD in Arctic freshwater ecology due 12 October.[8] | Add filtered route as `official_dynamic_vacancy_index`, `required: true` | Fetch/render the filtered page; parse job cards and location/deadline. Reconcile all official slugs weekly, not a hard-coded candidate list. Assert filtered result count and inventory every Uppsala/Ultuna card. | Replaces stale manual reconciliation that currently misses active Uppsala calls. |
| **High** | https://ki.se/en/about-ki/jobs-at-ki/available-positions-at-ki | KI · Stockholm/Solna · PhD and research jobs | Registry still uses `https://ki.se/en/vacancies`. The current canonical page shows **1–25 of 87 hits**; latest manifest has 24 candidates and omits first-page research IDs `966110` and `967691`.[6] The old URL still returns HTTP 200, so this is a canonical-route and pagination issue, not a hard 404. | Update primary URL to canonical `official_vacancy_index`, `required: true`; retain old URL as fallback | Paginate through all result pages or harvest both KI Varbi namespaces directly; assert `observed >= displayed_total` after URL deduplication. Normalize duplicate rows and preserve `ki.varbi.com` vs `kidoktorand.varbi.com`. | Avoids alias drift and first-page-only collection as KI’s result set changes. |
| **Medium** | https://www.scilifelab.se/careers | SciLifeLab · Stockholm/Solna/Uppsala · partner research roles | Manifest is healthy technically, but its 10 candidates include Linköping, Örebro and Chalmers/Gothenburg entries outside the declared geography. | Keep `official_partner_careers_page`, `required: true` | Parse employer/location from each card before triage; accept only Stockholm/Solna/Uppsala, then resolve every accepted partner listing to the employer’s official application page. | Stops national partner-board content from inflating local source coverage. |

## EXTERNAL_RECONCILIATION_GAPS

1. **Stockholm University doctoral jobs are externally visible but absent from the official harvest.** EURAXESS exposes a Stockholm University doctoral vacancy with an October deadline, while the official DSV page confirms eight current PhD calls and the Public Health page confirms two more.[3][4][16] This is not a reason to ingest EURAXESS as authority; it is a signal that the missing central SU route and `/en/what:job/` pattern are causing false negatives.
2. **KTH has a zero-candidate manifest despite external discovery signals.** Academic Positions returns KTH research/PhD listings, and the official KTH index is independently discoverable with vacancy rows.[5][15] Each external signal must be resolved to `kth.se/lediga-jobb/<id>?l=en` before acceptance.
3. **KI first-page drift is already producing official omissions.** The live official index has 87 hits and contains relevant first-page items not in the 24-candidate manifest.[6] External boards are useful as alerts, but the repair is complete official pagination.
4. **No board-only active opportunity was accepted without official confirmation.** EURAXESS and Academic Positions remained discovery cross-checks, consistent with registry policy.

## PROPOSED_REGISTRY_CHANGES

Do **not** apply automatically. Recommended order:

1. **P0 — Add Stockholm University central jobs/Varbi index** (`official_vacancy_index`, `required: true`, Stockholm, PhD + research jobs). Patterns: `su.varbi.com/what:job/jobID:` and `su.varbi.com/en/what:job/jobID:`. Keep Chemistry/MBW only as optional reconciliation feeds.
2. **P0 — Repair required-source completeness:** KTH fallback/retries; Uppsala “Show more” pagination and declared-count assertion; SLU rendered filtered index and card-count assertion; KI canonical URL plus full pagination.
3. **P1 — Add official research-employer indexes:**
   - `https://www.foi.se/jobba-hos-oss.html` — FOI, Stockholm/Kista, `official_research_employer_vacancy_index`, `required: true`; select location containing `Kista`/`Stockholm` and role/title containing research/doctoral/postdoc/analyst terms; follow EasyCruit links and deduplicate by recruitment ID.[19]
   - `https://career.ri.se/en-GB/jobs` — RISE, Stockholm/Uppsala, same type, `required: false` initially; render Teamtailor, filter location, and retain research/researcher/postdoc/doctoral/scientist roles. Promote to required after two clean runs.[17][21]
   - `https://career.ivl.se/en-GB/jobs` — IVL, Stockholm, same type, `required: false` initially; parse Teamtailor `/jobs/<numeric-id>-<slug>` links and location tokens. The index currently exposes four jobs, including Stockholm-tagged opportunities.[18]
   - `https://www.sei.org/people/jobs/` — SEI, Stockholm, same type, `required: false`; filter `SEI Headquarters` or `Stockholm, Sweden`, follow `/people/jobs/<slug>`, and verify that archived/404 vacancies are dropped.[11]
   - Region Stockholm and Region Uppsala central vacancy indexes — `official_public_research_employer_index`, `required: false`; filter geography and research terms (`forskare`, `forskningsassistent`, `forskningsingenjör`, `postdoktor`, `doktorand`, `bioinformatik`, `laboratorieingenjör`) and then verify on the official detail page.[13][14]
4. **P1 — Add coordinated-call monitors:** Stockholm University Faculty of Science news/call pages as `official_faculty_call_feed`, `required: false`. The 2026 faculty call bundled 31 PhD positions and linked each official Varbi job, showing why burst-call reconciliation is useful even after the central index is added.[2]
5. **P2 — Geography decision:** if Stockholm means county/metro, add Södertörn’s vacancy index as required and its annual collective doctoral-call page as optional; otherwise document Flemingsberg/Huddinge as excluded.[9][10]
6. **Query-policy update:** add weekly official-domain queries for the SU central route, FOI, RISE, IVL, SEI, and the two regions. Keep EURAXESS/Academic Positions queries explicitly labelled reconciliation-only.

## WARNINGS

- This is a source-coverage audit, not a claim that all opportunities are covered.
- The latest manifest is one day old and is materially incomplete for KTH, SU, UU, SLU and KI; `status: ok` does not currently prove pagination completeness.
- `scripts/harvest_sources.py` only parses anchor tags from one fetched HTML response; it has no pagination, declared-total check, JavaScript rendering, retry policy, or fallback execution. Those limitations explain several false-success/false-empty states.
- `scripts/reconcile_manifest.py` hard-codes SLU candidates and one Uppsala candidate; this cannot establish complete weekly coverage.
- SciLifeLab candidates receive `SLU_...` fallback stable IDs in the current reconciliation script, which risks organisation-ID collisions and should be corrected independently of registry changes.
- FOI vacancies generally require Swedish citizenship because positions are security-classified.[19] Source inclusion should not imply applicant eligibility.
- Search engines and external boards can be stale; all accepted opportunities must resolve to a live official employer/application page.
- No credentials were accessed or disclosed.

## Sources

[1] https://www.su.se/english/about-the-university/work-at-su/available-jobs — Stockholm University — Available jobs
[2] https://www.su.se/english/news/articles/2026-03-30-the-faculty-of-science-announces-31-phd-positions — Stockholm University Faculty of Science — 31 PhD positions
[3] https://www.su.se/english/divisions/department-of-computer-and-systems-sciences/about-the-department/work-with-us — Stockholm University DSV — Work with us
[4] https://www.su.se/english/divisions/department-of-public-health-sciences/news/articles/2026-09-17-two-new-phd-positions-in-current-public-health-sciences-research — Stockholm University Public Health — two PhD positions
[5] https://www.kth.se/lediga-jobb?l=en — KTH — Vacancies
[6] https://ki.se/en/about-ki/jobs-at-ki/available-positions-at-ki — Karolinska Institutet — Available positions
[7] https://www.uu.se/en/about-uu/join-us/jobs-and-vacancies?query=PhD — Uppsala University — PhD search
[8] https://www.slu.se/en/about-slu/work-at-slu/jobs-and-vacancies?filters=OccupationArea%24%24string%7CPhD — SLU — PhD vacancies
[9] https://www.sh.se/english/sodertorn-university/meet-sodertorn-university/this-is-sodertorn-university/vacant-positions — Södertörn University — Vacant positions
[10] https://www.sh.se/english/sodertorn-university/research/doctoral-level-education/interested-in-doctoral-studies — Södertörn University — Interested in doctoral studies
[11] https://www.sei.org/people/jobs — Stockholm Environment Institute — Opportunities
[12] https://www.ivl.se/english/ivl/career.html — IVL — Careers
[13] https://www.regionstockholm.se/jobb/lediga-jobb — Region Stockholm — Vacancies
[14] https://regionuppsala.se/jobb-och-utbildning/lediga-tjanster — Region Uppsala — Vacancies
[15] https://academicpositions.com/jobs/country/sweden — Academic Positions — Sweden jobs
[16] https://euraxess.ec.europa.eu/jobs/465219 — EURAXESS — Stockholm University doctoral vacancy
[17] https://career.ri.se/en-GB/jobs — RISE — Open job positions
[18] https://career.ivl.se/en-GB/jobs — IVL — Job openings
[19] https://www.foi.se/jobba-hos-oss.html — FOI — Jobba hos oss
[20] https://www.regionstockholm.se/jobb/lediga-jobb/stockholms-lans-sjukvardsomrade/forskare-sokes-till-projekt-som-ska-utveckla-varden-for-aldre — Region Stockholm — Researcher vacancy
[21] https://www.ri.se/en/about-rise/work-with-us/open-job-positions/researcher-electric-power-systems-1 — RISE — Researcher Electric Power Systems
