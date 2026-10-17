# Rural Broadband Fix — Oregon: data notes

Built 2026-10-16. Every number on the dashboard traces to a source below.
Nothing is invented. Estimates are labeled as estimates.

## What the page shows

| Display | Value | Source | Date verified |
|---|---|---|---|
| Starlink kit | $349 | starlink.com | read Sep 7 & Oct 13, 2026 |
| Starlink kit rental alt | $0 upfront + $10/mo | Starlink rental model | launched June 2026 |
| Starlink monthly | $130 (Residential Max) | starlink.com via Talk Android, Prism News, RV Mobile Internet Resource Center | price rise effective June 18, 2026 |
| Starlink 2-yr total | $3,469 ($349 + $130×24) | computed from above | — |
| Fiber per location | $9,421 | Oregon BEAD Final Proposal: $517,187,064 ÷ 54,895 locations | NTIA-approved Feb 4, 2026 |
| Satellite per location (BEAD) | $550 | Oregon BEAD Final Proposal: $26,743,750 ÷ 48,631 locations | NTIA-approved Feb 4, 2026 |
| Oregon BEAD total | $689M, 104,654 locations | Business Oregon press release; Benton Institute | Feb 4, 2026 |
| Tech mix | 52.5% fiber / 46.4% satellite / 1.1% fixed wireless | Oregon Legislature committee briefing on Final Proposal (2026R1) | 2026 |
| Build deadline | ~Sep 2030 (4 yrs from Sep 2026 contracts) | IIJA §60102(h)(4)(C); OBO: contracts by Sep 18, 2026, most construction late 2026 | 2026 |
| FCC benchmark | 100/20 Mbps | FCC 24-27 (Mar 14, 2024); confirmed current Apr 29, 2026 (DOC-421212A1) | 2024–2026 |
| "Unserved / underserved" | <25/3 / <100/20 | IIJA + NTIA BEAD NOFO | statute |
| LA benchmark (secondary) | $3,902/location (blended) | ConnectLA revised final proposal, NTIA-approved Nov 2025, via BroadbandBreakfast / Pelican Policy Institute | Nov 2025 |
| ZIP → county / land area | Census 2023 Gazetteer + 2020 ZCTA-county file | U.S. Census Bureau (public domain) | 2020–2023 |

## Statewide cost comparison (shown on page)

- Starlink for all 104,654: 104,654 × $3,469 = **$363,044,726** (~$363.0M)
- Fiber for all 104,654: 104,654 × $9,421 = **$985,945,334** (~$985.9M)
- Difference: **$622,900,608** (~$622.9M)

## What's estimated vs measured

- **Measured:** all cost figures, program totals, timeline, benchmark, ZIP geography.
- **Estimated (labeled on page):** the rural/suburban/urban tag per ZIP — a rough
  read from land area (≥50 sq mi = rural, 10–50 = suburban/small-town, <10 = urban),
  NOT a Census urban/rural designation.
- **Not present:** per-ZIP counts of unserved homes. See below.

## The per-ZIP data gap (honest account)

The original concept called for per-ZIP unserved counts from the FCC Broadband
Data Collection (BDC) fixed-availability file, aggregated to ZIP.

What I tried (Oct 16, 2026):
1. FCC bulk download (broadbandmap.fcc.gov/data-download) — **Akamai bot-blocked**.
2. FCC BDC Public Data API (`/api/public/map/...`) — reachable, but the manifest
   and download endpoints require a **registered FCC account** (username + hash).
   Per third-party docs, registration may ask for an SSN/EIN (FRN registration).
3. Old keyless map API (`/api/public/map/listAvailability`) — **retired** (per
   point998/livably research, June 2026).
4. FCC Open Data on Socrata (opendata.fcc.gov) — only 2021 Form 477 data (pre-BDC,
   block-level, outdated). Not usable.
5. Public mirrors of Oregon BDC location data — none found.
6. Oregon's per-District-Grant-Area CSVs — behind the interactive Oregon Broadband
   Map (JS app); 212 separate downloads, location IDs without ZIPs.

The BDC files also carry **no ZIP column** — geography is census block GEOID only,
so aggregation needs a block→ZIP crosswalk (documented in build_data.py).

**Upgrade path:** a human creates the free FCC account, downloads the Oregon
fixed-availability ZIPs (~150–300 MB), and runs `build_data.py`, which implements
the per-location 100/20 classification (satellite excluded, matching BEAD practice)
and the block→tract→ZIP aggregation via the HUD-USPS crosswalk. The page's
`lookup()` will use per-ZIP counts automatically once `data.json` has them.

Latest BDC vintage as of Oct 2026: **as of Dec 31, 2025** ("D25", released Jun 23, 2026).
Next vintage (as of Jun 30, 2026) expected ~Dec 2026.

## The opt-in counter (added Oct 16, 2026)

**What it is:** a voluntary "show of hands." After seeing the fiber timeline, a
visitor can tap "Count me in" to register that their household would take
Starlink rather than wait. Displayed as per-ZIP and statewide running totals —
advocacy-grade demand evidence, not a government program signup.

**Privacy design:**
- The ONLY thing transmitted/stored is a ZIP code. No name, email, phone,
  address, IP, or any identifier. The backend (`counter-backend/Code.gs`)
  persists nothing but `{zips: {ZIP: count}, total: N}` in Apps Script
  Properties. No request metadata is kept.
- **Spam guard is client-side:** localStorage key `rbf_optins` records which
  ZIPs this browser already tapped; the button disables after one tap per ZIP.
  This is a soft guard — it stops casual double-tapping, not a determined
  actor clearing storage. Stated honestly on the page ("one tap per browser
  per ZIP (saved on your device)").
- **No backend configured = no fake numbers:** `COUNTER_ENDPOINT` ships empty.
  Until a real Apps Script URL is pasted in, the page runs in local-only mode:
  the tap is recorded on-device and the totals panel says plainly that live
  district totals appear once the counter service is connected. It never
  displays invented shared counts.
- **Transport:** JSONP (dynamic script tag) for both reads and increments, so
  the static page works without CORS configuration. Callback names are
  validated server-side (`/^[A-Za-z_$][A-Za-z0-9_$]*$/`). ZIPs are validated
  against the embedded 428-ZIP Oregon list; anything else is rejected.
- **Concurrency:** `LockService` around the read-modify-write so simultaneous
  taps don't lose increments.

**Deploy (human, ~5 min):** paste `counter-backend/Code.gs` into a new Apps
Script project → Deploy as Web App (Execute as: Me, access: Anyone) → paste the
/exec URL into `COUNTER_ENDPOINT` in index.html → redeploy the site.

## New sections added Oct 16, 2026 (sections 6–9)

| Display | Value | Source | Date verified |
|---|---|---|---|
| Starlink ship time | 1–2 weeks (U.S.) | satellitesnetwork.com 2026 U.S. guide; consistent w/ starlink.com checkout | Oct 2026 |
| CAF II auction | $1.488B / 10 yrs; 103 bidders; 713,176 locations; 45 states | USAC (usac.org/high-cost/funds/caf-phase-ii-auction) — primary | Oct 2026 |
| CAF II speeds | as low as 25/3 Mbps | FCC auction service tiers (via USAC) | 2018 |
| RDOF total | $20.4B / 10 yrs | FCC (Jan 2020 Report & Order), via Computer Weekly/Light Reading | 2020 |
| LTD Broadband award revoked | $1,320,920,718.60 | FCC Aug 10, 2022 order (via Light Reading, SpaceNews, The Register) | 2022 |
| Starlink award revoked | $885,509,638.40 | FCC Aug 10, 2022 order (same) | 2022 |
| RDOF authorized to date | >$5B to 3M+ locations, 47 states | FCC via SpaceNews | ~2025 |
| Household broadband value | $1,950/yr; $68.2B lost / 6.3M co-op households | NRECA study via Broadband Communities (bbcmag.com) — secondary | Oct 2026 |
| Rural hospital telemedicine gap | $370,000/yr per hospital (24 hospitals) | USDA ERS report ERR-78 (ers.usda.gov) — primary | report |
| Broadband ↔ rural income | associated w/ higher median income, more proprietors | Oklahoma State economist, peer-reviewed — via secondary summary only | Oct 2026 |
| Rain degradation | −52.27% uplink / −37.84% downlink median; availability >98.5% | VTT / Univ. of Oulu, arXiv 2505.04772 — primary (peer-track paper) | 2025 |
| Heavy rain attenuation | 2–3 dB Ku-band | cited within arXiv 2603.14008 literature review — secondary | 2026 |
| Latency ranges | Starlink 20–60 ms; fiber 5–20 ms | Ookla Feb 2023 U.S. medians via secondary; 2025–26 comparison tests | 2023–2026 |
| Upload comparison | Starlink 10–20 Mbps; fiber symmetrical gigabit | same as above | 2023–2026 |
| Dish lifespan | ~5–7 years | industry-standard figure — **no primary source verified** | — |
| Fiber lifespan | 30–50 years | industry-standard figure — **no primary source verified** | — |

### Could not verify (new items, Oct 16, 2026)

- Dish 5–7 year and fiber 30–50 year lifespan figures: widely repeated in industry
  press but I found no manufacturer spec sheet or standards document stating them
  directly. Labeled on the page as "roughly" / industry-standard. Starlink's own
  warranty is 1–2 years depending on region — not the same as lifespan.
- Oklahoma State broadband-income study: cited from a secondary statistics
  roundup (thenetworkinstallers.com); the primary paper was not pulled. The page
  says "a peer-reviewed study by an Oklahoma State economist" — accurate to the
  secondary, but primary verification is an open item.
- NRECA $68.2B / $1,950 figures: from Broadband Communities' reporting of the
  NRECA study, not the NRECA report PDF itself. The numbers are consistent across
  multiple outlets but primary-document verification is open.
- CAF II actual buildout completion (how many of the 713,176 locations were
  actually served by the 6-year deadline): not verified. The page presents only
  the award figures, which is the honest scope.
- RDOF "authorized >$5B to 3M+ locations" is a ~2025 figure; current cumulative
  may differ. Page presents it as reported.

## Could not verify

- Whether Starlink's $10/mo kit rental is waived at any specific Oregon address
  (address-dependent, shown only at checkout).
- Per-address fiber arrival dates — **confirmed not publicly available** (Oregon's
  District Grant Area Tool shows technology + provider per address, not dates).
- The direct URL of Oregon's District Grant Area Tool (linked only from the BEAD
  homepage): https://www.oregon.gov/biz/programs/BEAD/
- A handful of Oregon ZCTAs that cross state lines are assigned to their primary
  (largest-overlap) county; border ZIPs may show the neighboring state's county
  if most of the ZCTA's land is across the border.
