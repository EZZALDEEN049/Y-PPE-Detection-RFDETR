"""Offline secondary summary; no API requests, raw images or identities."""
import csv, json, random, statistics as st
from collections import defaultdict
from pathlib import Path

root = Path(__file__).resolve().parent
rows = list(csv.DictReader((root / "v38b_targets_pseudonymous.csv").open(encoding="utf8")))
groups = defaultdict(list)
classes = defaultdict(list)
for row in rows:
    groups[row["image_cluster"]].append(row)
    classes[row["class_name"]].append(row)
assert len(rows) == 48 and len(groups) == 24 and all(len(v) == 2 for v in groups.values())
assert [r["target_id"] for r in rows if not r["rho"]] == ["T05", "T30", "T47"]
values = [float(r["rho"]) for r in rows if r["rho"]]
image_means = [st.mean(float(r["rho"]) for r in g if r["rho"]) for g in groups.values()]
rng = random.Random("seer-ppe/v38b-image-block-bootstrap-2026-11-23")
n = len(image_means)
bootstrap = sorted(st.mean(image_means[rng.randrange(n)] for _ in range(n)) for _ in range(5000))
lo = bootstrap[int(.025 * 4999)]
hi = bootstrap[int(.975 * 4999)]
loo = [st.mean(float(r["rho"]) for r in rows if r["rho"] and r["image_cluster"] != group) for group in groups]
m = len(rows) - len(values)
bounds = [(sum(values) - m) / len(rows), (sum(values) + m) / len(rows)]
assert abs(st.mean(values) - .6489788814589973) < 1e-12
assert abs(st.mean(image_means) - .6507583876423197) < 1e-12
assert abs(lo - .5949574145556713) < 1e-12 and abs(hi - .7043504901960784) < 1e-12
assert abs(min(loo) - .6409970510480615) < 1e-12 and abs(max(loo) - .6648684600767892) < 1e-12
assert all(abs(a-b)<1e-12 for a,b in zip(bounds,[.5459177013678099,.6709177013678099]))
print(json.dumps({"images":n,"targets":len(rows),"estimable":len(values),"target_mean":st.mean(values),"image_balanced_mean":st.mean(image_means),"descriptive_bootstrap":[lo,hi],"target_weighted_leave_one_image_out":[min(loo),max(loo)],"hypothetical_completion_bounds":bounds,"classes":{k:{"images":len({r["image_cluster"] for r in g}),"targets":len(g),"estimable":sum(bool(r["rho"]) for r in g)} for k,g in sorted(classes.items())}},indent=2))
