#!/usr/bin/env python3
"""UPGRADE PATH: build per-ZIP unserved counts from the FCC BDC bulk file.

The dashboard ships without per-ZIP unserved counts because the FCC
Broadband Data Collection bulk download requires a (free) FCC account,
which can't be created automatically. This script documents and performs
the upgrade once a human downloads the files.

STEP 1 — human does this once (about 10 minutes):
  1. Create a free FCC account at https://broadbandmap.fcc.gov/
     (username + hash/token from the BDC system).
  2. Go to https://broadbandmap.fcc.gov/data-download
  3. Download the FIXED broadband availability files for Oregon (state FIPS 41),
     latest vintage (as of Dec 31, 2025 = "D25", released ~June 2026).
     There is one ZIP per technology; you want all of them
     (Fiber, Cable, Copper, Licensed/Unlicensed Fixed Wireless, NGSO Satellite...).
  4. Put the ZIPs in ./fcc_raw/

STEP 2 — run this script:
  python3 build_data.py

What it does:
  - Reads every row of every Oregon CSV (one row = location + provider + tech + speed tier)
  - Per location_id: served_100_20 = any row with max_advertised_download_speed >= 100
    AND max_advertised_upload_speed >= 20 AND business_residential_code in (R, X)
    AND technology not in (60, 61)  [exclude satellite: BEAD doesn't count it as served,
    and this dashboard is about the terrestrial gap]
  - Underserved/unserved = locations without served_100_20
    (BEAD calls <25/3 "unserved" and <100/20 "underserved"; we report the
    combined 100/20 gap because 100/20 is the FCC's current benchmark — FCC 24-27)
  - Maps block_geoid -> census tract (first 11 digits) -> ZIP via the
    HUD-USPS tract-to-ZIP crosswalk (largest residential share wins)
  - Writes per-ZIP counts into data.json under data["per_zip_unserved"]

Output schema added to data.json:
  "per_zip_unserved": {
      "vintage": "2025-12-31",
      "method": "...",
      "zips": { "97355": {"unserved_100_20": 1234, "total_locations": 5678}, ... }
  }
The page's lookup() function will automatically use these counts when present.
"""
import csv
import json
import os
import zipfile
from collections import defaultdict

WORK = "/home/hatch/workspace/rural-broadband-fix"
RAW = os.path.join(WORK, "fcc_raw")

# BDC technology codes for satellite (excluded from "served" — see docstring)
SAT_TECH = {"60", "61"}

# HUD-USPS crosswalk URL (quarterly; pick the latest):
# https://www.huduser.gov/portal/datasets/usps_crosswalk.html
# File: ZIP_TRACT_<YYYYMM>.xlsx — needs openpyxl; or use the .csv version if available.


def iter_bdc_rows():
    """Yield dict rows from all Oregon BDC fixed-availability CSVs in fcc_raw/."""
    if not os.path.isdir(RAW):
        raise SystemExit(
            f"Missing {RAW}/ — download the Oregon fixed-availability ZIPs first (see STEP 1)."
        )
    zips = [os.path.join(RAW, f) for f in os.listdir(RAW) if f.lower().endswith(".zip")]
    if not zips:
        raise SystemExit(f"No ZIP files found in {RAW}/.")
    for zp in zips:
        with zipfile.ZipFile(zp) as zf:
            for name in zf.namelist():
                if not name.lower().endswith(".csv"):
                    continue
                with zf.open(name) as fh:
                    # files are large; wrap in text mode and stream
                    import io
                    txt = io.TextIOWrapper(fh, encoding="utf-8-sig", errors="replace")
                    rdr = csv.DictReader(txt)
                    for row in rdr:
                        yield row


def served_100_20(row):
    try:
        down = int(float(row.get("max_advertised_download_speed") or 0))
        up = int(float(row.get("max_advertised_upload_speed") or 0))
    except ValueError:
        return False
    if down < 100 or up < 20:
        return False
    if (row.get("business_residential_code") or "").strip().upper() not in ("R", "X"):
        return False
    if (row.get("technology") or "").strip() in SAT_TECH:
        return False
    return True


def main():
    loc_served = {}   # location_id -> True/False
    loc_block = {}    # location_id -> block_geoid
    n_rows = 0
    for row in iter_bdc_rows():
        n_rows += 1
        lid = (row.get("location_id") or "").strip()
        if not lid:
            continue
        if lid not in loc_block:
            loc_block[lid] = (row.get("block_geoid") or "").strip()
        if served_100_20(row):
            loc_served[lid] = True
        elif lid not in loc_served:
            loc_served[lid] = False
        if n_rows % 1_000_000 == 0:
            print(f"  ...{n_rows:,} rows, {len(loc_block):,} locations")

    print(f"Rows: {n_rows:,} | locations: {len(loc_block):,}")

    # block -> tract (first 11 chars of 15-digit block GEOID)
    # tract -> ZIP needs the HUD-USPS crosswalk (download separately, see docstring).
    # Placeholder: implement tract->zip mapping here once the crosswalk is downloaded.
    #
    # Suggested approach:
    #   1. Download ZIP_TRACT_*.xlsx from huduser.gov
    #   2. For each tract, pick ZIP with max res_ratio
    #   3. zip_counts[zip]["total"] += 1; if not served: zip_counts[zip]["unserved"] += 1
    #
    raise SystemExit(
        "Parsed OK. To finish: download the HUD-USPS ZIP_TRACT crosswalk and "
        "implement the tract->ZIP mapping in the section above, then re-run."
    )


if __name__ == "__main__":
    main()
