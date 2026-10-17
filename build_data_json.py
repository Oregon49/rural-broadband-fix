#!/usr/bin/env python3
"""Assemble data.json for the Rural Broadband Fix dashboard.

Combines:
- or_zips.json (Census ZCTA -> county/area, built by build_zip_data.py)
- Sourced cost + program constants (see DATA_NOTES.md for provenance)

All figures are from public sources; see "sources" in output.
Per-ZIP unserved counts are NOT included: the FCC BDC bulk file requires
a free FCC account to download (see build_data.py for the upgrade path).
"""
import json

WORK = "/home/hatch/workspace/rural-broadband-fix"

STARLINK_KIT = 349            # starlink.com, verified Sep 7 & Oct 13, 2026
STARLINK_RENTAL_UPFRONT = 0   # since June 2026: $0 upfront + $10/mo kit rental
STARLINK_RENTAL_MO = 10
STARLINK_MO = 130             # Residential Max, since June 18, 2026 billing cycle
STARLINK_MONTHS = 24
STARLINK_TOTAL = STARLINK_KIT + STARLINK_MO * STARLINK_MONTHS  # 3469

FIBER_PER_LOCATION = 9421    # Oregon BEAD Final Proposal: $517,187,064 / 54,895 BSLs
LEO_PER_LOCATION = 550       # Oregon BEAD: $26,743,750 / 48,631 BSLs
OR_LOCATIONS = 104654        # NTIA-approved eligible locations, Final Proposal
OR_ALLOCATION = 689_000_000  # ~$688.9M

data = {
    "meta": {
        "title": "Rural Broadband Fix — Oregon",
        "data_date": "2026-10-16",
        "program": "Oregon BEAD (Broadband Equity, Access, and Deployment)",
        "note": (
            "Per-ZIP unserved-location counts are not yet included. They require "
            "the FCC Broadband Data Collection bulk file, which needs a free FCC "
            "account to download (see build_data.py). ZIP lookup currently shows "
            "county, area, and rural character from Census data; cost math uses "
            "verified statewide figures."
        ),
    },
    "sources": {
        "fcc_benchmark": "FCC 24-27 (Mar 14, 2024): 100/20 Mbps benchmark; confirmed current Apr 29, 2026 (DOC-421212A1)",
        "bead_definitions": "IIJA / NTIA BEAD NOFO: unserved = <25/3 Mbps; underserved = <100/20 Mbps",
        "oregon_bead_plan": "Oregon BEAD Final Proposal, NTIA-approved Feb 4, 2026 (Business Oregon press release; Benton Institute)",
        "oregon_tech_mix": "Oregon Legislature committee briefing on Final Proposal (2026R1)",
        "oregon_timeline": "IIJA 60102(h)(4)(C) 4-year build requirement; OBO: contracts signed by Sep 18, 2026; most construction late 2026",
        "starlink_kit": "starlink.com, read Sep 7 and Oct 13, 2026",
        "starlink_monthly": "Starlink price increase effective June 18, 2026 (Talk Android, Prism News, RV Mobile Internet Resource Center)",
        "starlink_rental": "Starlink hardware rental model launched June 2026",
        "louisiana_bead": "ConnectLA revised final proposal, NTIA-approved Nov 2025 (via BroadbandBreakfast, Pelican Policy Institute)",
        "zip_geography": "U.S. Census Bureau: 2023 Gazetteer (ZCTA land area/centroid); 2020 ZCTA-to-County relationship file",
    },
    "oregon_bead": {
        "allocation_usd": OR_ALLOCATION,
        "eligible_locations": OR_LOCATIONS,
        "final_proposal_approved": "2026-02-04",
        "contracts_signed_by": "2026-09-18",
        "construction_starts": "late 2026",
        "federal_completion_deadline": "~2030-09",
        "tech_mix": [
            {"tech": "Fiber", "locations": 54895, "award_usd": 517187064,
             "per_location_usd": FIBER_PER_LOCATION, "share_pct": 52.5},
            {"tech": "LEO satellite", "locations": 48631, "award_usd": 26743750,
             "per_location_usd": LEO_PER_LOCATION, "share_pct": 46.4},
            {"tech": "Fixed wireless / hybrid", "locations": 1128,
             "award_usd": None, "per_location_usd": None, "share_pct": 1.1},
        ],
    },
    "costs": {
        "starlink": {
            "kit_usd": STARLINK_KIT,
            "kit_rental_alt": {"upfront_usd": STARLINK_RENTAL_UPFRONT,
                               "per_month_usd": STARLINK_RENTAL_MO,
                               "note": "Since June 2026; address-dependent, sometimes waived"},
            "monthly_usd": STARLINK_MO,
            "plan": "Residential Max (400+ Mbps), widest availability",
            "months": STARLINK_MONTHS,
            "total_per_location_usd": STARLINK_TOTAL,
        },
        "fiber": {
            "per_location_usd": FIBER_PER_LOCATION,
            "basis": "Oregon BEAD approved average ($517.2M / 54,895 locations)",
            "secondary_benchmark": {
                "per_location_usd": 3902,
                "basis": "Louisiana revised BEAD plan average (blended across technologies), NTIA-approved Nov 2025",
            },
        },
        "statewide_comparison": {
            "locations": OR_LOCATIONS,
            "starlink_total_usd": OR_LOCATIONS * STARLINK_TOTAL,
            "fiber_total_usd": OR_LOCATIONS * FIBER_PER_LOCATION,
            "difference_usd": OR_LOCATIONS * FIBER_PER_LOCATION - OR_LOCATIONS * STARLINK_TOTAL,
        },
    },
    "links": {
        "oregon_bead": "https://www.oregon.gov/biz/programs/BEAD/",
        "oregon_address_tool": "https://www.oregon.gov/biz/programs/BEAD/",
        "fcc_map": "https://broadbandmap.fcc.gov/",
        "fcc_data_download": "https://broadbandmap.fcc.gov/data-download",
        "house_lookup": "https://www.house.gov/representatives/find-your-representative",
        "senate_lookup": "https://www.senate.gov/senators/senators-contact.htm",
    },
}

with open(f"{WORK}/or_zips.json") as f:
    zips = json.load(f)
data["zips"] = zips
data["meta"]["zip_count"] = len(zips)

with open(f"{WORK}/data.json", "w") as f:
    json.dump(data, f)

print(f"Wrote data.json: {len(zips)} ZIPs")
sw = data["costs"]["statewide_comparison"]
print(f"Statewide Starlink: ${sw['starlink_total_usd']:,}")
print(f"Statewide fiber:    ${sw['fiber_total_usd']:,}")
print(f"Difference:         ${sw['difference_usd']:,}")
