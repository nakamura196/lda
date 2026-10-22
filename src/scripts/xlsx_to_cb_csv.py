#!/usr/bin/env python3
"""Convert src/data/metadata.xlsx into a CollectionBuilder metadata CSV.

One row per article (the parent). An article printed on more than one spread
becomes a compound object, with one child row per spread (`parentid` = the
article). A spread shared by several articles appears as a child row of each
of them, with the same `object_location`. An article on a single spread has its own
`object_location`. Every article's page shows its IIIF manifest
(display_template iiif), made by static_iiif.

Which spreads an article covers is taken from the manifests of the site
before CollectionBuilder (docs/iiif/3/<id>/manifest.json at commit OLD, read
from git). The start/end columns of the Excel sheet are compared with them and
differences are reported.

The annotations of that site (docs/iiif/3/<id>/list/*.json) are written to
iiif/annotations/<id>.csv, which static_iiif adds to the manifests it makes.

This is a one-time conversion: after it, _data/yanesen.csv and
iiif/annotations/ are the data to edit.

Usage: python3 src/scripts/xlsx_to_cb_csv.py
"""
import csv
import json
import re
import subprocess
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parents[2]
XLSX = ROOT / "src/data/metadata.xlsx"
OLD = "2780558fe8"  # the last commit of the site before CollectionBuilder
OUT = ROOT / "_data/yanesen.csv"
ANNOTATIONS = ROOT / "iiif/annotations"

BASE = "https://nakamura196.github.io/lda"
RIGHTS = "CC BY 4.0"

COLUMNS = [
    "objectid", "parentid", "title", "issue", "creator", "subject",
    "description", "references", "note", "latitude", "longitude",
    "rights", "rightsstatement", "viewing_direction",
    "display_template", "object_location", "image_small", "image_thumb",
    "image_alt_text", "format",
]


def split_list(value):
    """'a,b,,c' -> 'a; b; c' (CollectionBuilder separates values with ';')."""
    if not value:
        return ""
    return "; ".join(v.strip() for v in re.split(r"[,，、]", str(value)) if v.strip())


def old_file(path):
    """A file of the old site, or None."""
    r = subprocess.run(["git", "-C", str(ROOT), "show", f"{OLD}:docs/{path}"], capture_output=True)
    return r.stdout.decode("utf-8") if r.returncode == 0 else None


def old_manifest(item_id):
    return json.loads(old_file(f"iiif/3/{item_id}/manifest.json"))


def canvases(item_id):
    m = old_manifest(item_id)
    paths = []
    for canvas in m["items"]:
        for page in canvas["items"]:
            for anno in page["items"]:
                paths.append("/" + anno["body"]["id"].split(BASE + "/", 1)[1])
    return paths


def thumb(original):
    return original.replace("/files/original/", "/files/medium/")


def excel_range(row, ix):
    """Spreads from the sheet's start/end columns (AC, AD), as file names."""
    start, end = row[ix["_start"]], row[ix["_end"]]
    if not (isinstance(start, str) and isinstance(end, str)):
        return None
    prefix, a = start.rsplit("-", 1)
    _, b = end.rsplit("-", 1)
    return [f"{prefix}-{n:03d}.jpg" for n in range(int(a[:3]), int(b[:3]) + 1)]


def main():
    ws = openpyxl.load_workbook(XLSX, data_only=True, read_only=True)["Sheet1"]
    rows = list(ws.iter_rows(values_only=True))
    header = rows[0]
    ix = {k: i for i, k in enumerate(header) if k}
    # unnamed columns AC, AD: first and last spread of the article
    ix["_start"], ix["_end"] = 28, 29

    annotated = [i["id"].split("/")[-2]
                 for i in json.loads(old_file("iiif/collection/3/annotated.json"))["items"]]

    out, diffs = [], []
    for r in rows[4:]:
        if not r[ix["ID"]]:
            continue
        item_id = r[ix["ID"]].replace("/", "_")
        issue = int(r[ix["ID"]].split("/")[1])
        images = canvases(item_id)

        expected = excel_range(r, ix)
        if expected and [Path(p).name for p in images] != expected:
            diffs.append((item_id, expected, [Path(p).name for p in images]))

        lat = lon = ""
        if r[ix["spatial"]]:
            lat, lon = (s.strip() for s in str(r[ix["spatial"]]).split(","))

        parent = {
            "objectid": item_id,
            "title": r[ix["title"]],
            "issue": f"第{issue}号",
            "creator": split_list(r[ix["creator"]]),
            "subject": split_list(r[ix["subject"]]),
            "description": r[ix["description"]] or "",
            "references": split_list(r[ix["references"]]),
            "note": r[ix["備考"]] or "",
            "latitude": lat,
            "longitude": lon,
            "rights": RIGHTS,
            "rightsstatement": r[ix["license"]],
            "viewing_direction": r[ix["viewingDirection"]],
            "image_thumb": thumb(images[0]),
        }
        if len(images) == 1:
            parent.update(display_template="iiif", object_location=images[0],
                          image_alt_text=r[ix["title"]], format="image/jpeg")
            out.append(parent)
            continue

        # still a compound object for CollectionBuilder (child rows), but the item
        # page shows the manifest, where the spreads are turned in the viewer
        parent["display_template"] = "iiif"
        out.append(parent)
        for n, path in enumerate(images, 1):
            out.append({
                "objectid": f"{item_id}_p{n}",
                "parentid": item_id,
                "title": f"{r[ix['title']]} [{n}]",
                "rights": RIGHTS,
                "rightsstatement": r[ix["license"]],
                "display_template": "image",
                "object_location": path,
                "image_thumb": thumb(path),
                "image_alt_text": f"{r[ix['title']]} [{n}]",
                "format": "image/jpeg",
            })

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        for row in out:
            w.writerow(row)

    n_annos = sum(write_annotations(item_id) for item_id in annotated)

    parents = [o for o in out if not o.get("parentid")]
    print(f"{OUT.relative_to(ROOT)}: {len(parents)} articles "
          f"({sum(1 for o in parents if not o.get('object_location'))} compound), "
          f"{len(out) - len(parents)} child rows, "
          f"{len({o['object_location'] for o in out if o.get('object_location')})} distinct images; "
          f"{n_annos} annotations on {len(annotated)} articles")
    for item_id, expected, actual in diffs:
        print(f"  sheet != manifest: {item_id} sheet={expected} manifest={actual}")



def write_annotations(item_id):
    """The old site's annotations of one article -> iiif/annotations/<id>.csv."""
    m = old_manifest(item_id)
    rows = []
    for n, canvas in enumerate(m["items"], 1):
        for ref in canvas.get("annotations", []):
            page = json.loads(old_file(ref["id"].split(BASE + "/", 1)[1]))
            for a in page["items"]:
                target = a["target"] if isinstance(a["target"], str) else a["target"]["id"]
                if target.split("#")[0] != canvas["id"]:
                    raise SystemExit(f"{item_id}: annotation not on canvas {n}: {target}")
                xywh = target.split("#xywh=", 1)[1] if "#xywh=" in target else ""
                rows.append({"canvas": n, "xywh": xywh, "text": a["body"]["value"]})
    ANNOTATIONS.mkdir(parents=True, exist_ok=True)
    with (ANNOTATIONS / f"{item_id}.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["canvas", "xywh", "text", "motivation"])
        w.writeheader()
        w.writerows(rows)
    return len(rows)


if __name__ == "__main__":
    main()
