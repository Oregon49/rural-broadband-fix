#!/usr/bin/env python3
"""Build per-ZIP lookup data for Oregon from Census bulk files.

Sources (all public domain, U.S. Census Bureau):
- 2023 Gazetteer, ZCTA national file: land area (sq mi), centroid lat/lon
- 2020 ZCTA-to-County relationship file: primary county per ZCTA
  (primary = county with largest AREALAND_PART overlap)

Output: or_zips.json — one record per Oregon ZCTA:
  {zip, county_name, county_fips, land_sqmi, lat, lon, rural_class}

rural_class is derived from land area + county and labeled approximate:
  - "rural": land area >= 50 sq mi
  - "suburban/small-town": 10-50 sq mi
  - "urban": < 10 sq mi
This is a rough geographic read, NOT a Census urban/rural designation.
"""
import csv
import json
from collections import defaultdict

WORK = "/home/hatch/workspace/rural-broadband-fix"

# Oregon county FIPS -> name (2020). Built from relationship file instead.
def load_gazetteer():
    gaz = {}
    with open(f"{WORK}/2023_Gaz_zcta_national.txt", newline="") as f:
        r = csv.DictReader(f, delimiter="\t")
        # header fields carry trailing whitespace; normalize them
        r.fieldnames = [fn.strip() for fn in r.fieldnames]
        for row in r:
            row = {k.strip(): (v or "").strip() for k, v in row.items()}
            z = row["GEOID"].strip()
            try:
                gaz[z] = {
                    "land_sqmi": float(row["ALAND_SQMI"]),
                    "lat": float(row["INTPTLAT"]),
                    "lon": float(row["INTPTLONG"]),
                }
            except ValueError:
                continue
    return gaz


def load_county_xwalk():
    # ZCTA -> list of (county_geoid, county_name, arealand_part)
    xw = defaultdict(list)
    with open(f"{WORK}/zcta_county.txt", newline="", encoding="utf-8-sig") as f:
        r = csv.DictReader(f, delimiter="|")
        for row in r:
            z = (row.get("GEOID_ZCTA5_20") or "").strip()
            cg = (row.get("GEOID_COUNTY_20") or "").strip()
            cn = (row.get("NAMELSAD_COUNTY_20") or "").strip()
            if not z or not cg:
                continue
            try:
                part = float(row.get("AREALAND_PART") or 0)
            except ValueError:
                part = 0
            xw[z].append((cg, cn, part))
    # primary county = largest land overlap
    primary = {}
    for z, lst in xw.items():
        lst.sort(key=lambda t: t[2], reverse=True)
        cg, cn, _ = lst[0]
        primary[z] = (cg, cn)
    return primary


def rural_class(land_sqmi):
    if land_sqmi >= 50:
        return "rural"
    if land_sqmi >= 10:
        return "suburban/small-town"
    return "urban"


def main():
    gaz = load_gazetteer()
    primary = load_county_xwalk()
    out = {}
    for z, g in gaz.items():
        if z not in primary:
            continue
        cg, cn = primary[z]
        if not cg.startswith("41"):  # Oregon state FIPS
            continue
        out[z] = {
            "zip": z,
            "county_name": cn,
            "county_fips": cg,
            "land_sqmi": round(g["land_sqmi"], 1),
            "lat": round(g["lat"], 4),
            "lon": round(g["lon"], 4),
            "rural_class": rural_class(g["land_sqmi"]),
        }
    with open(f"{WORK}/or_zips.json", "w") as f:
        json.dump(out, f)
    print(f"Wrote {len(out)} Oregon ZCTA records")
    # sanity samples
    for z in ["97355", "97205", "97701", "97850"]:
        if z in out:
            print(z, out[z])


if __name__ == "__main__":
    main()
