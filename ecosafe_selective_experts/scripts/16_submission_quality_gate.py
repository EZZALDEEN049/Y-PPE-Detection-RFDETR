#!/usr/bin/env python3
"""Offline manuscript source gate. Editorial checks are NOT peer review or validation."""
from __future__ import annotations
import json,re,xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PACK=ROOT/"submission"/"automation_in_construction"
MAN=ROOT/"docs"/"ECOSAFE_WORKING_MANUSCRIPT_2026-10-17.md"
HIL=PACK/"HIGHLIGHTS_2026-10-18.txt"
AGG=PACK/"LOCKED_FIGURE_AGGREGATES_2026-10-18.json"
F1=ROOT/"figures"/"FIG1_CHECKPOINT_RECALL_FP_2026-10-18.svg"
F2=ROOT/"figures"/"FIG2_INCREMENTAL_FP_PER_RECOVERED_GT_2026-10-18.svg"

def check_abstract(md):
    m=re.search(r"(?ms)^## Abstract[^\n]*\n(.*?)(?=^## 1\.)",md)
    if not m:
        raise ValueError("Missing standalone abstract section")
    text=re.split(r"(?m)^\*\*Keywords",m.group(1),maxsplit=1)[0]
    text=re.sub(r"\*","",text).replace(chr(96),"").strip()
    count=len(re.findall(r"\b[\w]+(?:[-'][\w]+)*\b",text))
    if not 1<=count<=250 or "validation" not in text.lower() or "energy" not in text.lower():
        raise ValueError("Abstract invalid, >250 words or hides evidence limits")
    if "http://" in text or "https://" in text:
        raise ValueError("Abstract should be citation-free")
    return count

def check_highlights(content):
    xs=[x.strip()[2:].strip() for x in content.splitlines() if x.strip().startswith(("• ","- "))]
    if not 3<=len(xs)<=5 or any(not x or len(x)>85 for x in xs) or len(set(xs))!=len(xs):
        raise ValueError("Elsevier highlights count, length or uniqueness failed")
    return list(map(len,xs))

def check_data(obj):
    if obj.get("independent_test") is not False or obj.get("real_energy_measured") is not False:
        raise ValueError("Invalid unmeasured claim")
    if (obj.get("confidence"),obj.get("gt_match_iou"),obj.get("joint_nms_iou"))!=(0.25,0.5,0.7):
        raise ValueError("Fixed operating policy drift")
    entries=obj.get("rows",[])
    if len(entries)!=12:
        raise ValueError("Incomplete 2-domain x 3-seed x 2-checkpoint experiment grid")
    index={}
    for v in entries:
        key=(v.get("domain"),v.get("seed"),v.get("checkpoint"))
        if key in index or key[0] not in ("Y-PPE","Construction-PPE") or key[1] not in (17,42,2026) or key[2] not in ("last.pt","best.pt"):
            raise ValueError("Unknown or duplicate experimental cell")
        n,gt=(356,345) if key[0]=="Y-PPE" else (132,98)
        tp,fp=v.get("joint_true_positive_objects"),v.get("joint_false_detection_boxes")
        if any(type(x) is not int for x in (v.get("frames"),v.get("critical_ground_truth_objects"),tp,fp)):
            raise ValueError("Non-integer counts")
        if v["frames"]!=n or v["critical_ground_truth_objects"]!=gt or not 0<=tp<=gt or fp<0:
            raise ValueError("Invalid original sample support")
        if abs(v["recall_percent"]-100*tp/gt)>.011 or abs(v["false_detections_per_100_frames"]-100*fp/n)>.011:
            raise ValueError("Derived plotting data does not match observed integer counts")
        if key[2]=="best.pt":
            p,q=v.get("in_domain_primary_tp"),v.get("in_domain_primary_fp")
            if any(type(x) is not int for x in (p,q)) or not 0<=p<=gt or q<0:
                raise ValueError("Primary experiment comparator invalid")
        index[key]=v
    if len(index)!=12:
        raise ValueError("Missing cell")
    return index

def check_figures(f1,f2,index):
    root=ET.fromstring(f1)
    pattern=re.compile(r"^(Y-PPE|Construction-PPE) seed (17|42|2026), (last|best)\.pt: recall (\d+\.\d{2})%, (\d+\.\d{2}) FP / 100 images$")
    found={}
    for el in root.iter():
        if not el.tag.endswith("}title") or not el.text:
            continue
        m=pattern.fullmatch(el.text)
        if m:
            d,seed,c,r,fp=m.groups()
            k=(d,int(seed),c+".pt")
            if k in found: raise ValueError("Repeated figure point")
            found[k]=(float(r),float(fp))
    if set(found)!=set(index):
        raise ValueError("Plot does not contain exactly 12 source-locked experimental cells")
    for key,vals in found.items():
        source=index[key]
        if abs(vals[0]-source["recall_percent"])>.011 or abs(vals[1]-source["false_detections_per_100_frames"])>.011:
            raise ValueError("Plotted point changed from locked data")
    texts=" ".join(x.text or "" for x in ET.fromstring(f2).iter())
    bars=0
    for domain in ("Y-PPE","Construction-PPE"):
        for seed in (17,42,2026):
            v=index[(domain,seed,"best.pt")]
            dt=v["joint_true_positive_objects"]-v["in_domain_primary_tp"]
            df=v["joint_false_detection_boxes"]-v["in_domain_primary_fp"]
            if dt<=0 or f"{df/dt:.2f}  (+{dt} TP, +{df} FP)" not in texts:
                raise ValueError("Marginal cost figure does not match locked counts")
            bars+=1
    return len(found),bars

def evaluate(man,hil,agg,fig1,fig2):
    words=check_abstract(man)
    lens=check_highlights(hil)
    cells=check_data(agg)
    npoints,nbars=check_figures(fig1,fig2,cells)
    for term in ("Stage 4.5","Stage 6","best.pt","last.pt","no_boots","356","132"):
        if term not in man:
            raise ValueError("Missing essential prior exposure or support qualifier")
    if F1.name not in man or F2.name not in man:
        raise ValueError("Missing paper figure")
    return dict(
      editorial_only=True,abstract_words=words,highlights=len(lens),
      highlight_lengths=lens,locked_experiment_cells=len(cells),
      checked_figure1_points=npoints,checked_figure2_bars=nbars,
      independent_external_confirmation=False,measured_energy=False,
      journal_acceptance=False,submission_approved=False)

if __name__=="__main__":
    try:
        outcome=evaluate(MAN.read_text(encoding="utf8"),
        HIL.read_text(encoding="utf8"),
        json.loads(AGG.read_text(encoding="utf8")),
        F1.read_text(encoding="utf8"),F2.read_text(encoding="utf8"))
        print(json.dumps(outcome,sort_keys=True))
    except (ValueError,TypeError,KeyError,ET.ParseError,OSError) as ex:
        raise SystemExit("SUBMISSION_QUALITY_GATE_BLOCKED: "+type(ex).__name__)
