"""Regenerate every derived composite artifact from one place (Phase 3, v2).

Inputs : the five dimension score columns in PSAI_CompositeScores_Rebuilt.xlsx (A:F), weights 30/28/22/15/5.
Writes : cached composite values and the Ranked column inside the workbook (so it opens with numbers
         even before recalculation), docs/psai_phase2_scores.csv (rank, composite, tier, zero count, D4 status
         for D.C.), and the DATA array and no-JavaScript table in docs/results.html.
Then run robustness.py and alternatives.py (see README) so every figure comes from the same data.
Standard library only. Run from the repo root: python3 composite/regenerate.py
"""
import csv, json, pathlib, re, shutil, sys, zipfile, tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "composite"))
from robustness import load, tier, comp, ranks, W

XLSX = ROOT / "composite" / "PSAI_CompositeScores_Rebuilt.xlsx"
CSV = ROOT / "docs" / "psai_phase2_scores.csv"
HTML = ROOT / "docs" / "results.html"

# D.C. is not in the Digital States survey. D4's rule: never default D.C. to zero. v2 scores D.C.'s D4 on the
# PD half alone (pd_points = 70); see d4-investment-in-people/dimension4_pd_revised.csv.
DC_D4 = 70.0


def patch_xlsx(order, comps):
    z = zipfile.ZipFile(XLSX)
    x = z.read("xl/worksheets/sheet1.xml").decode()

    def fix_row(m):
        row = m.group(0)
        r = int(m.group(1))
        if r == 1:
            return row
        name = re.search(r"<c r=\"A\d+\"[^>]*><is><t>([^<]*)</t>", row).group(1)
        if name == "District of Columbia":
            row = re.sub(r"(<c r=\"E%d\" t=\"n\"><v>)[^<]*(</v>)" % r, r"\g<1>%s\2" % DC_D4, row)
        row = re.sub(r"(<c r=\"G%d\"><f>[^<]*</f>)<v ?/>" % r, r"\g<1><v>%s</v>" % repr(comps[name]), row)
        row = re.sub(r"(<c r=\"I%d\" t=\"inlineStr\"><is><t>)[^<]*(</t>)" % r, r"\g<1>%s\2" % order[r - 2], row)
        return row

    x = re.sub(r"<row r=\"(\d+)\"[^>]*>.*?</row>", fix_row, x, flags=re.S)
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
    with zipfile.ZipFile(tmp.name, "w", zipfile.ZIP_DEFLATED) as out:
        for i in z.infolist():
            out.writestr(i, x if i.filename == "xl/worksheets/sheet1.xml" else z.read(i.filename))
    shutil.move(tmp.name, XLSX)


def main():
    data = load(XLSX)
    if data["District of Columbia"][3] == 0.0:
        data["District of Columbia"][3] = DC_D4
    comps = {s: comp(v, W) for s, v in data.items()}
    rk = ranks(comps)
    order = sorted(comps, key=rk.get)
    patch_xlsx(order, comps)

    rows = list(csv.DictReader(open(CSV)))
    fields = list(rows[0].keys())
    for r in rows:
        s = r["state"]
        r["composite"] = f"{comps[s]:.1f}"
        r["tier"] = tier(comps[s])
        r["zero_filled_dimensions"] = str(sum(1 for v in data[s] if v == 0.0))
        r["rank"] = str(rk[s])
        if s == "District of Columbia":
            r["d4_score"] = f"{DC_D4:.1f}"
            r["d4_status"] = "partial"
            r["d4_indicators_confirmed"] = "2"
            r["d4_indicators_total"] = "3"
    rows.sort(key=lambda r: int(r["rank"]))
    with open(CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        w.writeheader(); w.writerows(rows)

    h = HTML.read_text()
    m = re.search(r"const DATA = (\[.*?\]);\n", h, re.S)
    old = json.loads(m.group(1))
    new = []
    for s in order:
        o = next(d for d in old if d["state"] == s)
        o.update(composite=round(comps[s], 1), tier=tier(comps[s]), rank=rk[s],
                 d4=data[s][3], zeros=sum(1 for v in data[s] if v == 0.0))
        new.append(o)
    h = h.replace(m.group(0), "const DATA = " + json.dumps(new) + ";\n")
    tr = "".join("<tr><td>%d</td><td>%s</td><td>%.1f</td><td>%s</td>%s</tr>" % (
        d["rank"], d["state"], d["composite"], d["tier"], "".join("<td>%.1f</td>" % d[k] for k in ("d1", "d2", "d3", "d4", "d5"))) for d in new)
    h = re.sub(r"(<noscript><div class=\"table-wrap\"><table><thead>.*?</thead><tbody>).*?(</tbody>)", lambda mm: mm.group(1) + tr + mm.group(2), h, count=1, flags=re.S)
    HTML.write_text(h)


if __name__ == "__main__":
    main()
