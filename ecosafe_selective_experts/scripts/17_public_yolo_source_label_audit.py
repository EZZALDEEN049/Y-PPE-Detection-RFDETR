#!/usr/bin/env python3
"""Offline PRIVATE Roboflow/YOLO external candidate annotation preflight.

NO detector inference, no test threshold selection, no capture-site independence
certification. Reads source image BYTES only to find exact duplicated files; it
does not render workers or upload original frame names, boxes or image hashes.
"""
from __future__ import annotations
import argparse,ast,hashlib,json,re
from collections import Counter,defaultdict
from pathlib import Path

ALIASES={
    "no_helmet":{"nohelmet","nosafetyhelmet","nohardhat"},
    "no_gloves":{"noglove","nogloves","nosafetygloves"},
    "no_boots":{"noboot","noboots","nosafetyboots"},
}
IMAGE_SUFFIXES={".jpg",".jpeg",".png",".webp"}
SPLITS={"train":"train","valid":"val","val":"val","test":"test"}


def read_class_names(text):
    match=re.search(r"(?m)^names\s*:\s*(.*)$",text)
    if not match:
        raise ValueError("Missing data.yaml names")
    raw=match.group(1).strip()
    if raw.startswith("["):
        try:
            names=ast.literal_eval(raw)
        except (ValueError,SyntaxError):
            names=[x.strip().strip(" '\"") for x in raw.strip("[]").split(",")]
        if not isinstance(names,list) or not all(isinstance(x,str) and x for x in names):
            raise ValueError("Unrecognized names list")
        return names
    block=[]
    lines=text[match.end():].splitlines()
    for line in lines:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if not line.startswith((" ","\t")):
            break
        part=line.strip()
        m=re.match(r"^(?:-\s*|\d+\s*:\s*)(.+)$",part)
        if not m:
            raise ValueError("Unrecognized YAML names block")
        block.append(m.group(1).strip().strip("'\""))
    if not block:
        raise ValueError("No class names recognized")
    return block


def sha256(file):
    digest=hashlib.sha256()
    with file.open("rb") as h:
        for b in iter(lambda:h.read(1024*1024),b""):
            digest.update(b)
    return digest.hexdigest()


def inspect(root,source_schema):
    names=read_class_names((root/"data.yaml").read_text(encoding="utf-8"))
    nc_match=re.search(r"(?m)^nc\s*:\s*(\d+)\s*$",(root/"data.yaml").read_text(encoding="utf-8"))
    if nc_match and int(nc_match.group(1))!=len(names):
        raise ValueError("Native class count and class name order disagree")
    m=source_schema.get("reviewed_class_map")
    if not isinstance(m,dict) or len(m)!=3 or set(m.values())!=set(ALIASES):
        raise ValueError("Three mapped absence classes must be explicitly reviewed")
    mapped={}
    for native_id,canonical in m.items():
        if not isinstance(native_id,str) or not native_id.isdecimal() or int(native_id)>=len(names):
            raise ValueError("Native class ID outside source YAML")
        name_normalized=re.sub(r"[^a-z0-9]","",names[int(native_id)].lower())
        if name_normalized not in ALIASES[canonical]:
            raise ValueError("Ontology alias not accepted: manual source-label adjudication required")
        mapped[int(native_id)]=canonical
    if source_schema.get("research_use_acknowledged") is not True:
        raise ValueError("Rights/source review not acknowledged")
    images=defaultdict(list)
    for split,canon in SPLITS.items():
        folder_candidates=[(root/split/"images",root/split/"labels"),
                           (root/"images"/split,root/"labels"/split)]
        image_dir,label_dir=next(((a,b) for a,b in folder_candidates if a.is_dir() and b.is_dir()),(None,None))
        if image_dir is None:
            continue
        for img in sorted(image_dir.iterdir()):
            if not img.is_file() or img.suffix.lower() not in IMAGE_SUFFIXES:
                continue
            label=label_dir/(img.stem+".txt")
            if not label.is_file():
                raise ValueError("Missing paired annotation file")
            if img.stat().st_size==0:
                raise ValueError("Empty image bytes")
            images[canon].append((img,label))
    if not images or sum(len(v) for v in images.values())<3:
        raise ValueError("Too few candidate images")
    counts=Counter()
    frames=Counter()
    content_sha_splits=defaultdict(set)
    for split,items in images.items():
        stems=set()
        for img,label in items:
            if img.stem in stems:
                raise ValueError("Duplicate image stem inside split")
            stems.add(img.stem)
            digest=sha256(img)
            content_sha_splits[digest].add(split)
            frames[split]+=1
            for line in label.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                fields=line.strip().split()
                if len(fields)!=5:
                    raise ValueError("Non-bounding-box annotation or malformed row")
                try:
                    cl=int(fields[0]);box=list(map(float,fields[1:]))
                except (ValueError,TypeError) as e:
                    raise ValueError("Non-numeric YOLO class/box") from e
                if not 0<=cl<len(names) or any(not 0<=v<=1 for v in box):
                    raise ValueError("Invalid normalized class or bbox")
                x,y,w,h=box
                if w<=0 or h<=0 or x-w/2 < -1e-7 or y-h/2 < -1e-7 or x+w/2>1+1e-7 or y+h/2>1+1e-7:
                    raise ValueError("Invalid bounding box geometry")
                if cl in mapped:
                    counts[mapped[cl]]+=1
        if frames[split]!=len(items):
            raise ValueError("Image count mismatch")
    if any(counts[c]<1 for c in ALIASES):
        raise ValueError("Missing a required safety-negative ground truth class")
    cross_sha=sum(len(s)>1 for s in content_sha_splits.values())
    return {
      "status":"private_source_annotation_preflight_not_independent_confirmation",
      "no_detector_predictions_used":True,
      "source_yaml_sha256":sha256(root/"data.yaml"),
      "native_class_count":len(names),
      "source_splits_present":sorted(images),
      "image_counts_per_split":dict(sorted(frames.items())),
      "critical_gt_counts":dict(sorted(counts.items())),
      "exact_cross_split_duplicate_sha_groups":cross_sha,
      "potential_source_family_leakage_unchecked":True,
      "human_worksite_groups_verified":False,
      "semantic_completeness_independently_verified":False,
      "test_authorized":False,
      "independent_experiment_completed":False,
      "energy_measured":False,
    }


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--private-export-root",type=Path,required=True)
    ap.add_argument("--private-reviewed-map",type=Path,required=True)
    ap.add_argument("--aggregate-out",type=Path,required=True)
    args=ap.parse_args()
    try:
        if args.aggregate_out.exists():
            raise ValueError("Do not overwrite existing review evidence")
        manifest=json.loads(args.private_reviewed_map.read_text(encoding="utf-8"))
        summary=inspect(args.private_export_root,manifest)
        args.aggregate_out.parent.mkdir(parents=True,exist_ok=True)
        args.aggregate_out.write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
        print(json.dumps({"status":summary["status"],"critical_classes":summary["critical_gt_counts"],"model_test_run":False}))
    except (OSError,ValueError,KeyError,TypeError) as ex:
        # Fail without exposing user-private filenames, worker IDs or annotation rows.
        raise SystemExit("PUBLIC_YOLO_SOURCE_GATE_BLOCKED: "+type(ex).__name__)

if __name__=="__main__":
    main()
