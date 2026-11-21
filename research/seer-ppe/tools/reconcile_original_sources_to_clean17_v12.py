#!/usr/bin/env python3
"""SEER-PPE V12: join already-saved Source and Clean17 *metadata*, not images.
Never reads Test image bytes, calls Roboflow, changes split or publishes binary data.
Candidate filename/dHash joins do NOT prove image identity or Clean17 membership.
"""
from __future__ import annotations
import argparse,csv,hashlib,json,re,sys
from collections import Counter,defaultdict
from pathlib import Path

EXPECTED_SOURCE={"train":1625,"valid":468}
EXPECTED_CLEAN={"train":1595,"valid":459}
CLEAN_CSV_SHA="4b7c458d6895706e7bc0886619be9ea12964ff5a9ba51a41f8af297e88a48345"
EXPECTED_SOURCE_PROJECT="softyyemen/altayyar-0oflt-lafos-qqauz"
STATUSES=("VERIFIED_RAW_BYTES_MATCH","NAME_AND_NEAR_DHASH_CANDIDATE",
          "NAME_ONLY_CANDIDATE","AMBIGUOUS_NAME","MULTIPLE_SOURCES_TO_CLEAN",
          "NOT_IN_CLEAN_NAME_INDEX","SOURCE_INTEGRITY_UNVERIFIED")

def norm(s):
    s=Path(s).name.lower()
    s=re.sub(r"_([a-z0-9]+)\.rf\.[a-f0-9]{32}\.[a-z0-9]+$",r".\1",s)
    return re.sub(r"[^a-z0-9]+","",s).replace("jpeg","jpg")

def fail(msg):
    raise ValueError("V12_RECONCILIATION_BLOCKED:"+msg)

def good_sha(s):
    return isinstance(s,str) and re.fullmatch("[0-9a-f]{64}",s) is not None

def sha(x):
    return hashlib.sha256(x).hexdigest()

def distance(a,b):
    if not (isinstance(a,str) and isinstance(b,str) and re.fullmatch("[0-9a-f]{16}",a) and re.fullmatch("[0-9a-f]{16}",b)):
        return None
    return (int(a,16)^int(b,16)).bit_count()

def resolve(source,clean,exclusions=None):
    """Input metadata only. Never accepts Test rows into comparison universe."""
    exclusion_keys={(x["split"],norm(x["file"])) for x in (exclusions or [])
        if x.get("split") in EXPECTED_SOURCE and x.get("action")=="exclude"}
    clean_by_name=defaultdict(list)
    clean_by_raw=defaultdict(list)
    for c in clean:
        if c["split"] not in EXPECTED_CLEAN: fail("CLEAN_TEST_RECORD_IN_MATCH_UNIVERSE")
        if not good_sha(c.get("source_file_sha256")):fail("BAD_CLEAN_SHA")
        clean_by_name[(c["split"],norm(c["file"]))].append(c)
        clean_by_raw[(c["split"],c["source_file_sha256"])].append(c)
    rows=[]
    for s in source:
        if s["split"] not in EXPECTED_SOURCE:fail("SOURCE_TEST_RECORD_IN_MATCH_UNIVERSE")
        if not good_sha(s.get("bytes_sha256")):fail("BAD_SOURCE_SHA")
        key=(s["split"],norm(s["filename"]))
        named=clean_by_name.get(key,[])
        exact=clean_by_raw.get((s["split"],s["bytes_sha256"]),[])
        status,chosen="NOT_IN_CLEAN_NAME_INDEX",None
        if len(exact)==1:
            chosen=exact[0];status="VERIFIED_RAW_BYTES_MATCH"
        elif len(exact)>1: status="AMBIGUOUS_NAME"
        elif len(named)==1:
            chosen=named[0]
            d=distance(s.get("dhash64"),chosen.get("dhash64"))
            status="NAME_AND_NEAR_DHASH_CANDIDATE" if d is not None and d<=4 else "NAME_ONLY_CANDIDATE"
        elif len(named)>1:status="AMBIGUOUS_NAME"
        rows.append({"source_id":s["source_id"],"split":s["split"],"source_filename":s["filename"],
          "source_width":s["width"],"source_height":s["height"],
          "clean_export_file_candidate":chosen["file"] if chosen else None,
          "clean_export_sha256_candidate":chosen["source_file_sha256"] if chosen else None,
          "status":status,
          "raw_byte_identity_verified":status=="VERIFIED_RAW_BYTES_MATCH",
          "clean17_membership_verified":status=="VERIFIED_RAW_BYTES_MATCH",
          "source_name_matches":len(named),"source_exact_raw_matches":len(exact),
          "dimension_equal_to_candidate":(s["width"]==int(chosen["width"]) and s["height"]==int(chosen["height"])) if chosen else None,
          "candidate_dhash_hamming":distance(s.get("dhash64"),chosen.get("dhash64")) if chosen else None,
          "listed_in_historical_exclusion_manifest_by_split_and_normalized_name":key in exclusion_keys,
          "source_group_independence_certified":False,
          "valid_scoring_eligible":False})
    # A shared clean-export candidate may not be given several unique Source IDs.
    by_clean=defaultdict(list)
    for r in rows:
        if r["clean_export_file_candidate"]:
            by_clean[(r["split"],r["clean_export_file_candidate"])].append(r)
    for group in by_clean.values():
        if len(group)>1:
            # Genuine byte equivalence could be from duplicate original Sources; still ambiguous ID ownership.
            for row in group:
                row["status"]="MULTIPLE_SOURCES_TO_CLEAN"
                row["raw_byte_identity_verified"]=False
                row["clean17_membership_verified"]=False
    return rows

def count_splits(rows):
    return dict(Counter(x["split"] for x in rows))
def load_clean_manifest(path):
    # Only materialized *metadata*, no image binaries. Skip historical Test records.
    with path.open(encoding="utf8",newline="") as f:
        clean=[r for r in csv.DictReader(f) if r.get("split") in EXPECTED_CLEAN]
    if count_splits(clean)!=EXPECTED_CLEAN:fail("CLEAN_TRAIN_VALID_COUNTS")
    if len({(x["split"],x["file"]) for x in clean})!=len(clean):fail("DUPLICATE_CLEAN_EXPORT_FILE")
    return clean

def main(args):
    m=json.loads(args.source_report.read_text(encoding="utf8"))
    manifest=json.loads(args.source_index.read_text(encoding="utf8"))
    if manifest.get("project")!=EXPECTED_SOURCE_PROJECT or manifest.get("image_count")!=2093:fail("WRONG_FROZEN_SOURCE_INDEX")
    index={x["image_id"]:x for x in manifest["images"] if x["split"] in EXPECTED_SOURCE}
    if len(index)!=2093:fail("SOURCE_INDEX_DUPLICATES_OR_COUNT")
    source=m.get("source_fingerprints",[])
    if len(source)!=2093 or count_splits(source)!=EXPECTED_SOURCE:fail("SOURCE_FINGERPRINT_COVERAGE")
    if len({x["source_id"] for x in source})!=2093:fail("DUPLICATE_SOURCE_FINGERPRINT")
    if m.get("test_sources_queried")!=0 or m.get("image_bytes_uploaded") is not False:fail("TEST_OR_RAW_IMAGE_ACCESS_FLAG")
    for x in source:
        v=index.get(x["source_id"])
        if not v or x["split"]!=v["split"] or x["filename"]!=v["filename"]:
            fail("ORIGINAL_SOURCE_INDEX_MISMATCH")
        if (x["width"],x["height"])!=(v["width"],v["height"]):fail("ORIGINAL_DIMENSIONS_MISMATCH")
    # V5 manifest digest may be recorded in the older audit summary, but implementations
    # may differ in generation; fail if expected digest does not match.
    digest=sha(args.clean_manifest.read_bytes())
    if digest!=CLEAN_CSV_SHA:fail("CLEAN_FROZEN_MANIFEST_DIGEST_MISMATCH")
    clean=load_clean_manifest(args.clean_manifest)
    with args.corrections.open(encoding="utf8",newline="") as f:
        correction=[x for x in csv.DictReader(f) if x.get("split") in EXPECTED_SOURCE]
    rows=resolve(source,clean,correction)
    if count_splits(rows)!=EXPECTED_SOURCE:fail("RESULT_SOURCE_SPLIT_COUNTS")
    counts=Counter(r["status"] for r in rows)
    verify=sum(r["clean17_membership_verified"] for r in rows)
    candidates=sum(r["clean_export_file_candidate"] is not None and not r["clean17_membership_verified"] for r in rows)
    corrections=Counter(x["split"] for x in correction if x["action"]=="exclude")
    if corrections != Counter({"train":30,"valid":9}):fail("EXPECTED_30_9_CORRECTION_COUNTS")
    # No model eligibility is automatically asserted from either exact file identity
    # or a source-to-export candidate: source-family and PPE truth are separate.
    result={
      "schema_version":"seer-ppe/source-to-clean17-metadata-reconciliation/v0.12",
      "date":"2026-11-21",
      "method":"READ_ONLY_EXISTING_GITHUB_ACTIONS_METADATA_ONLY",
      "source_project":EXPECTED_SOURCE_PROJECT,
      "source_manifest":"SOURCE_ID_MANIFEST_TRAIN_VALID_2026-11-19_V01.json",
      "clean17_manifest_expected_sha256":CLEAN_CSV_SHA,
      "source_original_count":len(source),"clean17_train_valid_count":len(clean),
      "source_split_counts":EXPECTED_SOURCE,"clean17_split_counts":EXPECTED_CLEAN,
      "historical_exclusions_train_valid":{"train":30,"valid":9},
      "identity_proven_raw_bytes_count":verify,
      "not_proven_candidate_links":candidates,
      "status_counts":dict(sorted(counts.items())),
      "valid_identity_proven_raw_bytes":sum(r["clean17_membership_verified"] for r in rows if r["split"]=="valid"),
      "valid_candidates_not_cryptographically_proven":sum(r["clean_export_file_candidate"] is not None and not r["clean17_membership_verified"] for r in rows if r["split"]=="valid"),
      "not_read_test_image_bytes":True,
      "test_image_metadata_not_used_for_matching":True,
      "original_data_modified":False,
      "original_model_modified":False,
      "source_lineage_independence_signed":False,
      "automatically_scoring_eligible_valid_images":0,
      "scientific_scoring_ready":False,
      "rows":sorted(rows,key=lambda r:(r["split"],r["source_id"]))
    }
    args.report.parent.mkdir(parents=True,exist_ok=True)
    args.report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    with args.candidate_csv.open("w",encoding="utf8",newline="") as f:
        fields=["source_id","split","source_filename","clean_export_file_candidate","status",
                "raw_byte_identity_verified","clean17_membership_verified",
                "source_name_matches","dimension_equal_to_candidate","candidate_dhash_hamming",
                "listed_in_historical_exclusion_manifest_by_split_and_normalized_name"]
        writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader()
        for row in result["rows"]:writer.writerow({k:row[k] for k in fields})
    summary={k:v for k,v in result.items() if k!="rows"}
    print(json.dumps(summary,ensure_ascii=False,indent=2))
    print("SEER_V12_SOURCE_TO_CLEAN17_METADATA_RECONCILIATION_FAIL_CLOSED_PASS")

def selftest():
    h=lambda n:f"{n:064x}"
    c=lambda name,n,split="valid":dict(split=split,file=name,source_file_sha256=h(n),dhash64="0000000000000000",width="100",height="100")
    s=lambda id,name,n,split="valid":dict(source_id=id,filename=name,bytes_sha256=h(n),dhash64="0000000000000000",width=100,height=100,split=split)
    aa=resolve([s("a","image_12.jpg",1),s("b","image_13.jpg",9)],
       [c("image_12_jpg.rf."+"a"*32+".jpg",1),c("image_13_jpg.rf."+"b"*32+".jpg",10)])
    assert aa[0]["status"]=="VERIFIED_RAW_BYTES_MATCH" and aa[0]["clean17_membership_verified"]
    assert aa[1]["status"]=="NAME_AND_NEAR_DHASH_CANDIDATE" and not aa[1]["clean17_membership_verified"]
    assert resolve([s("c","none.jpg",8)],[c("image_12.jpg",1)])[0]["status"]=="NOT_IN_CLEAN_NAME_INDEX"
    dd=resolve([s("a","a.jpg",10),s("b","a.jpg",11)],[c("a.jpg",12)])
    assert all(x["status"]=="MULTIPLE_SOURCES_TO_CLEAN" for x in dd)
    assert norm("image_12_jpg.rf."+"0"*32+".jpg")==norm("image_12.jpg")
    try:
        resolve([s("t","bad.jpg",1,"test")],[c("a.jpg",1)])
        raise AssertionError("test case was accepted")
    except ValueError as e:
        assert "SOURCE_TEST" in str(e)
    print("SEER_V12_SYNTHETIC_RECONCILIATION_AND_TEST_SEAL_PASS")

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--self-test",action="store_true")
    p.add_argument("--source-report",type=Path)
    p.add_argument("--source-index",type=Path)
    p.add_argument("--clean-manifest",type=Path)
    p.add_argument("--corrections",type=Path)
    p.add_argument("--report",type=Path)
    p.add_argument("--candidate-csv",type=Path)
    a=p.parse_args()
    try:
        if a.self_test:selftest()
        else:
            if any(getattr(a,k) is None for k in ("source_report","source_index","clean_manifest","corrections","report","candidate_csv")):
                fail("MISSING_INPUT_FILE_ARGUMENT")
            main(a)
    except Exception as e:
        print(str(e),file=sys.stderr)
        sys.exit(2)
