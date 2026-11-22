#!/usr/bin/env python3
"""Fetch ONLY the 24 frozen V38-B Valid originals to ephemeral disk.

Read-only public Roboflow source fetch; no API key and no hosted inference.
Checks raw SHA-256, EXIF-corrected RGB SHA-256 and dimensions against the
read-only source identity preflight. Never upload or commit image bytes.
"""
from __future__ import annotations
import argparse
from hashlib import sha256
import json
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import Request,urlopen
from io import BytesIO
from PIL import Image,ImageOps

ROOT=Path(__file__).resolve().parents[1]
MAX_BYTES=40*1024*1024

def get_json(path):
    return json.loads(Path(path).read_text(encoding="utf8"))

def namespace():
    old=get_json(ROOT/"V30_BASELINE_PREFLIGHT_ACTUAL_2026-11-22.json")
    assert old["status"]=="PASSED"
    names=set()
    for entry in old["source_images"]:
        p=urlsplit(entry["source_url"])
        assert p.scheme=="https" and p.hostname=="source.roboflow.com"
        assert not (p.username or p.password or p.query or p.fragment)
        parts=p.path.strip("/").split("/")
        assert len(parts)==3 and parts[1]==entry["asset_id"] and parts[2]=="original.jpg"
        names.add(parts[0])
    assert len(names)==1
    return names.pop()

def fetch_raw(namespace,source_id):
    assert 10<=len(source_id)<=40 and source_id.isalnum()
    url=f"https://source.roboflow.com/{namespace}/{source_id}/original.jpg"
    with urlopen(Request(url,headers={"User-Agent":"SEER-PPE-V38B-ReadOnly-Source-2026"}),timeout=60) as response:
        final=urlsplit(response.geturl())
        if response.status!=200 or final.scheme!="https" or final.hostname!="source.roboflow.com":
            raise RuntimeError("Unexpected redirect or response; source retrieval blocked")
        length=response.headers.get("Content-Length")
        if length is not None and int(length)>MAX_BYTES:
            raise RuntimeError("Original media too large")
        data=response.read(MAX_BYTES+1)
    if len(data)<128 or len(data)>MAX_BYTES:
        raise RuntimeError("Missing or oversized original source bytes")
    return data

def inspect_original(data,expected):
    raw=sha256(data).hexdigest()
    if raw!=expected["new_current_source_raw_sha256"]:
        raise ValueError("Source RAW SHA-256 has changed")
    with Image.open(BytesIO(data)) as probe:
        probe.verify()
    with Image.open(BytesIO(data)) as image:
        oriented=ImageOps.exif_transpose(image).convert("RGB")
        width,height=oriented.size
        rgb=sha256(oriented.tobytes()).hexdigest()
    if (width,height)!=(expected["current_exif_corrected_width"],
                        expected["current_exif_corrected_height"]):
        raise ValueError("EXIF-normalized image dimensions have changed")
    if rgb!=expected["new_current_exif_corrected_rgb_sha256"]:
        raise ValueError("EXIF-normalized RGB SHA-256 has changed")
    return {"raw_sha256":raw,"oriented_rgb_sha256":rgb,
            "width":width,"height":height,"byte_size":len(data)}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--destination",type=Path,required=True)
    p.add_argument("--check-only",action="store_true",
                  help="Confirm the frozen manifest and identity records without network use.")
    p.add_argument("--report",type=Path)
    args=p.parse_args()
    manifest=get_json(ROOT/"V38_B_FROZEN_CANDIDATE_SAMPLE_2026-11-23.json")
    qa=get_json(ROOT/"V38_B_CURRENT_SOURCE_EXIF_AWARE_SHA256_PREFLIGHT_2026-11-23.json")
    assert qa["status"]=="PASS_24_CURRENT_SOURCE_IMAGE_BYTES_EXIF_NORMALIZED_AND_STATIC_PROTOCOL"
    records={e["source_id"]:e for e in qa["current_source_image_sha256"]}
    assert len(manifest["images"])==len(records)==24
    assert all(r["source_id"] in records for r in manifest["images"])
    if args.check_only:
        print(json.dumps({"status":"V38B_SOURCE_FETCH_MANIFEST_READY_ZERO_NETWORK",
                          "images":24,"model_calls":0}))
        return
    args.destination.mkdir(parents=True,exist_ok=True)
    if any(args.destination.iterdir()):
        raise RuntimeError("Refusing to mix with a nonempty image directory")
    prefix=namespace()
    summaries=[]
    for row in manifest["images"]:
        sid=row["source_id"]
        # Never print the source URL or source bytes.
        raw=fetch_raw(prefix,sid)
        data=inspect_original(raw,records[sid])
        if (data["width"],data["height"])!=(row["width"],row["height"]):
            raise RuntimeError("Current input diverges from frozen V26 geometry")
        output=args.destination/(sid+".jpg")
        with output.open("xb") as fh:
            fh.write(raw)
        summaries.append({"source_id":sid,**data})
    assert len(summaries)==24
    if args.report:
        args.report.parent.mkdir(parents=True,exist_ok=True)
        args.report.write_text(json.dumps({
            "status":"V38B_24_EPHEMERAL_SOURCE_HASHES_VERIFIED",
            "model_calls":0,"no_test_accessed":True,
            "never_upload_image_bytes":True,"sources":summaries
        },indent=2)+"\n",encoding="utf8")
    print(json.dumps({"status":"V38B_24_EPHEMERAL_SOURCE_HASHES_VERIFIED",
                      "images":24,"model_calls":0}))
if __name__=="__main__":
    main()
