import argparse, pandas as pd
from pathlib import Path
ap=argparse.ArgumentParser(); ap.add_argument("--summary",required=True,help="CSV: model,energy_j_per_frame,violation_recall"); ap.add_argument("--out",required=True); ap.add_argument("--small",default="nano"); ap.add_argument("--large",default="medium"); ap.add_argument("--min-saving",type=float,default=.10); a=ap.parse_args(); d=pd.read_csv(a.summary).set_index("model"); s=d.loc[a.small]; l=d.loc[a.large]; saving=1-float(s.energy_j_per_frame)/float(l.energy_j_per_frame); gap=float(l.violation_recall)-float(s.violation_recall)
if saving>=a.min_saving and gap>0: decision="GO"; why=f"{a.small} is {saving:.1%} lower-energy than {a.large}, while {a.large} improves violation recall by {gap:.3f}."
elif saving>0 and gap>=0: decision="MODIFY"; why=f"Some separation exists (energy saving {saving:.1%}, recall gap {gap:.3f}); test another model pair/routing target."
else: decision="NO-GO"; why=f"No useful safety-energy separation (saving={saving:.1%}, recall gap={gap:.3f})."
txt=f"# EcoSafe Pilot Decision\n\n**{decision}**\n\n{why}\n\nPilot decision only; not a final paper conclusion.\n"; Path(a.out).write_text(txt,encoding="utf-8"); print(txt)
