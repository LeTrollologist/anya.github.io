"""
gen_stars_v2.py — Real star data generator for Stargazer
Sources:
  Stars       : HYG v3.8 (Hipparcos/Yale/Gliese), GitHub
  Const. lines: Stellarium modern_iau sky culture (JSON, HIP-ID polylines)
  Star names  : Stellarium common_star_names.fab (HIP-ID → proper name)

Run: python gen_stars_v2.py 2>gen_log.txt > star_data_v2.js
"""

import csv, gzip, io, json, re, sys, urllib.request

MAG_LIMIT = 5.0

HYG_URL   = ("https://raw.githubusercontent.com/astronexus/"
             "HYG-Database/main/hyg/v3/hyg_v38.csv.gz")
IAU_URL   = ("https://raw.githubusercontent.com/Stellarium/stellarium/"
             "master/skycultures/modern_iau/index.json")
NAMES_URL = ("https://raw.githubusercontent.com/Stellarium/stellarium/"
             "master/skycultures/common_star_names.fab")

# Constellation display centers (RA°, Dec°) — label anchor
CON_CENTERS = {
    "Andromeda"         : ( 17.0,  38.0),
    "Aquarius"          : (335.0, -12.0),
    "Aquila"            : (297.0,   5.0),
    "Ara"               : (264.0, -57.0),
    "Aries"             : ( 33.0,  20.0),
    "Auriga"            : ( 90.0,  42.0),
    "Boötes"            : (220.0,  30.0),
    "Cancer"            : (130.0,  20.0),
    "Canes Venatici"    : (195.0,  40.0),
    "Canis Major"       : (105.0, -22.0),
    "Canis Minor"       : (114.0,   6.0),
    "Capricornus"       : (308.0, -18.0),
    "Carina"            : (155.0, -62.0),
    "Cassiopeia"        : ( 10.0,  60.0),
    "Centaurus"         : (210.0, -50.0),
    "Cepheus"           : (340.0,  70.0),
    "Cetus"             : ( 25.0, -10.0),
    "Columba"           : ( 84.0, -35.0),
    "Corona Australis"  : (284.0, -42.0),
    "Corona Borealis"   : (240.0,  28.0),
    "Corvus"            : (187.0, -18.0),
    "Crux"              : (187.0, -60.0),
    "Cygnus"            : (310.0,  45.0),
    "Delphinus"         : (309.0,  13.0),
    "Draco"             : (270.0,  65.0),
    "Eridanus"          : ( 55.0, -28.0),
    "Gemini"            : (113.0,  22.0),
    "Hercules"          : (258.0,  28.0),
    "Hydra"             : (180.0, -20.0),
    "Leo"               : (152.0,  15.0),
    "Lepus"             : ( 82.0, -20.0),
    "Libra"             : (230.0, -15.0),
    "Lupus"             : (232.0, -45.0),
    "Lyra"              : (283.0,  36.0),
    "Ophiuchus"         : (267.0,  -8.0),
    "Orion"             : ( 83.8,   5.0),
    "Pegasus"           : (340.0,  20.0),
    "Perseus"           : ( 57.0,  45.0),
    "Phoenix"           : (  6.6, -42.3),
    "Pisces"            : ( 10.0,  12.0),
    "Piscis Austrinus"  : (344.0, -28.0),
    "Puppis"            : (121.0, -30.0),
    "Sagitta"           : (298.0,  19.0),
    "Sagittarius"       : (285.0, -28.0),
    "Scorpius"          : (253.0, -30.0),
    "Serpens"           : (238.0,   5.0),
    "Taurus"            : ( 65.0,  20.0),
    "Triangulum"        : ( 31.0,  32.0),
    "Ursa Major"        : (165.0,  55.0),
    "Ursa Minor"        : (230.0,  78.0),
    "Virgo"             : (200.0,  -5.0),
    "Vela"              : (135.0, -45.0),
    "Vulpecula"         : (299.0,  24.0),
}

def fetch_bytes(url, label):
    print(f"  Downloading {label} ...", file=sys.stderr)
    with urllib.request.urlopen(url, timeout=45) as r:
        return r.read()

# ── 1. Stars from HYG v3.8 ───────────────────────────────────────────────────
raw_gz = fetch_bytes(HYG_URL, "HYG v3.8 star catalogue")
raw    = gzip.decompress(raw_gz).decode("utf-8")
reader = csv.DictReader(io.StringIO(raw))

all_stars   = []
hip_to_idx  = {}   # HIP int -> sorted index (filled after sort)

for row in reader:
    try:
        mag = float(row["mag"])
    except ValueError:
        continue
    if mag > MAG_LIMIT:
        continue

    hip_str = row.get("hip", "").strip()
    hip     = int(hip_str) if hip_str.isdigit() else 0

    try:
        ra_deg = float(row["ra"]) * 15.0   # hours -> degrees
        dec    = float(row["dec"])
    except ValueError:
        continue

    try:
        bv = round(float(row["ci"]), 2)
    except (ValueError, KeyError):
        bv = 0.6

    all_stars.append({
        "ra" : round(ra_deg, 4),
        "dec": round(dec,    4),
        "mag": round(mag,    2),
        "bv" : bv,
        "hip": hip,
        "name": "",              # filled below
    })

all_stars.sort(key=lambda s: s["mag"])
for i, s in enumerate(all_stars):
    if s["hip"]:
        hip_to_idx[s["hip"]] = i

print(f"  {len(all_stars)} stars (mag ≤ {MAG_LIMIT})", file=sys.stderr)

# ── 2. Star names from Stellarium common_star_names.fab ─────────────────────
# Format: <HIP>|_("<Name>") <rank>
names_raw = fetch_bytes(NAMES_URL, "star names").decode("utf-8")
for line in names_raw.splitlines():
    m = re.match(r'\s*(\d+)\|_\("([^"]+)"\)', line)
    if not m:
        continue
    hip, name = int(m.group(1)), m.group(2)
    if hip in hip_to_idx:
        all_stars[hip_to_idx[hip]]["name"] = name

named_count = sum(1 for s in all_stars if s["name"])
print(f"  {named_count} named stars", file=sys.stderr)

# ── 3. Constellation lines from Stellarium modern_iau ───────────────────────
iau_data = json.loads(fetch_bytes(IAU_URL, "IAU constellation lines"))

constellations = []
for con in iau_data.get("constellations", []):
    # Use Latin (native) name for matching and display
    cn   = con.get("common_name", {})
    name = cn.get("native", "").strip()
    if not name:
        continue

    if name not in CON_CENTERS:
        continue                   # skip southern-only / unlisted ones

    # Convert polylines (chains of HIP IDs) -> flat segment pairs [a,b,a,b,...]
    segs = []
    for polyline in con.get("lines", []):
        for k in range(len(polyline) - 1):
            ha, hb = int(polyline[k]), int(polyline[k + 1])
            if ha in hip_to_idx and hb in hip_to_idx:
                segs.extend([hip_to_idx[ha], hip_to_idx[hb]])

    if not segs:
        print(f"  WARNING: no matched stars for {name}", file=sys.stderr)
        continue

    cra, cdec = CON_CENTERS[name]
    constellations.append([name, cra, cdec, segs])

constellations.sort(key=lambda c: c[1])
print(f"  {len(constellations)} constellations", file=sys.stderr)

# ── 4. Emit JS ───────────────────────────────────────────────────────────────
out = []
out.append("// AUTO-GENERATED by gen_stars_v2.py")
out.append(f"// {len(all_stars)} REAL stars from HYG v3.8 (Hipparcos-based, mag ≤ {MAG_LIMIT})")
out.append(f"// {len(constellations)} IAU constellations (Stellarium modern_iau lines, HIP-verified)")
out.append("")

# SG_STAR_DATA: flat array [ra,dec,vmag,bv, ra,dec,vmag,bv, ...]
vals = []
for s in all_stars:
    vals.extend([s["ra"], s["dec"], s["mag"], s["bv"]])

STARS_PER_LINE = 8          # 32 numbers per text line
out.append("var SG_STAR_DATA=[")
for i in range(0, len(vals), STARS_PER_LINE * 4):
    chunk = vals[i : i + STARS_PER_LINE * 4]
    out.append("  " + ",".join(str(v) for v in chunk) + ",")
out.append("];")
out.append("")

# SG_STAR_NAMES: {idx: "Name", ...}
out.append("var SG_STAR_NAMES={")
for i, s in enumerate(all_stars):
    if s["name"]:
        safe = s["name"].replace('"', '\\"')
        out.append(f'  {i}:"{safe}",')
out.append("};")
out.append("")

# SG_CONSTELLATIONS: [[name, cRA, cDec, [seg pairs...]], ...]
out.append("var SG_CONSTELLATIONS=[")
for con in constellations:
    seg_str = ",".join(str(x) for x in con[3])
    out.append(f'  ["{con[0]}",{con[1]},{con[2]},[{seg_str}]],')
out.append("];")
out.append("")

sys.stdout.reconfigure(encoding="utf-8")
sys.stdout.write("\n".join(out))
print(f"\nDone — {len(all_stars)} stars, {len(constellations)} constellations.",
      file=sys.stderr)
