#!/usr/bin/env python3
"""SEER-PPE V38-B: prospective, budget-guarded two-grid XAI replication runner.

The DEFAULT and self-test paths make ZERO hosted inference calls. The paid
execution path is disabled unless an explicit separate author authorization
file exists and the exact 6000-attempt flag is provided. Image bytes are
read only from preflight-vetted local files in ephemeral storage.

Records are descriptive, development-exposed, not an independent field test.
Never read Test data, change weights, annotations, datasets, or target IDs.
"""
from __future__ import annotations
import argparse
from collections import defaultdict, Counter
from dataclasses import asdict
from hashlib import sha256
import json
import math
import os
from pathlib import Path
import random
import sys
import tempfile
from typing import Callable

import numpy as np
from PIL import Image, ImageOps

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from seer_ppe.detection_match import Detection
from seer_ppe.progressive_xai import (
    cell_bounds, gaussian_blur_baseline, progressive_curve,
    rank_grid_cells, target_score
)

MODEL="altayyar-0oflt-lafos-qqauz/2"
MANIFEST=ROOT/"V38_B_FROZEN_CANDIDATE_SAMPLE_2026-11-23.json"
SOURCE_QA=ROOT/"V38_B_CURRENT_SOURCE_EXIF_AWARE_SHA256_PREFLIGHT_2026-11-23.json"
MAX_CALLS=6000
INTENDED_MAX=5200
MIN_IOU=.50
AMBIGUITY_MARGIN=.03
CONFIDENCE=.20
OVERLAP=.50
RANDOM_SEEDS=10
INNER_STEPS=9


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save_atomic(path, obj):
    path=Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w",encoding="utf-8",
                                     dir=path.parent,delete=False) as temp:
        json.dump(obj,temp,ensure_ascii=False,indent=2,allow_nan=False)
        temp.write("\n")
        temp.flush()
        os.fsync(temp.fileno())
        name=temp.name
    os.replace(name,path)


def sha256_path(path):
    h=sha256()
    with Path(path).open("rb") as stream:
        for x in iter(lambda:stream.read(1024*1024),b""):
            h.update(x)
    return h.hexdigest()


def read_image(path, expected):
    with Image.open(path) as image:
        oriented=ImageOps.exif_transpose(image)
        rgb=np.asarray(oriented.convert("RGB"),dtype=np.uint8)
    if rgb.shape!=(int(expected["current_exif_corrected_height"]),
                   int(expected["current_exif_corrected_width"]),3):
        raise ValueError("EXIF-corrected image dimensions differ from frozen source")
    digest=sha256(rgb.tobytes()).hexdigest()
    if digest!=expected["new_current_exif_corrected_rgb_sha256"]:
        raise ValueError("EXIF-corrected image SHA-256 differs from frozen source")
    return rgb


def validate_manifest(manifest, identity):
    assert manifest["schema_version"]=="seer-ppe/v38b-prospective-candidate-freeze/v1"
    assert manifest["status"]=="FROZEN_CANDIDATES_AND_BUDGET_ONLY_NO_NEW_MODEL_CALLS"
    assert manifest["model"]=={"id":MODEL,"confidence":CONFIDENCE,
                                "overlap":OVERLAP,"weights_changed":False}
    assert identity["status"]=="PASS_24_CURRENT_SOURCE_IMAGE_BYTES_EXIF_NORMALIZED_AND_STATIC_PROTOCOL"
    assert identity["current_source_images_retrieved_readonly"]==24
    assert len(manifest["images"])==24 and len(manifest["targets"])==48
    assert len({i["source_id"] for i in manifest["images"]})==24
    assert len({t["target_id"] for t in manifest["targets"]})==48
    expected={i["source_id"] for i in manifest["images"]}
    actual={i["source_id"] for i in identity["current_source_image_sha256"]}
    assert expected==actual
    assert identity["actual_hosted_model_calls"]==0
    assert all(x["matches_v26_dimensions_after_exif"] for x in identity["current_source_image_sha256"])
    assert all(x["image_key"]=="valid:"+x["source_id"] for x in manifest["images"])
    assert {t["source_id"] for t in manifest["targets"]}==expected
    assert all(4<=n<=5 for n in Counter(t["class_name"] for t in manifest["targets"]).values())
    for x in manifest["images"]:
        assert len(x["target_ids"])==2
        assert set(x["target_ids"])=={
            t["target_id"] for t in manifest["targets"] if t["source_id"]==x["source_id"]
        }
    counts=manifest["budget"]["calls_by_phase_max"]
    assert list(counts.values())==[1920,48,2376,216,640]
    assert sum(counts.values())==INTENDED_MAX
    assert manifest["budget"]["hard_maximum_new_hosted_model_calls_including_retries"]==MAX_CALLS
    assert manifest["budget"]["actual_new_model_calls_in_this_freeze"]==0
    assert len(manifest["random_progressive_target_ids_12_different_images"])==12
    assert len(manifest["alternative_fill_image_ids_8"])==8
    by_first={im["source_id"]:next(t for t in manifest["targets"] if t["source_id"]==im["source_id"])["target_id"]
              for im in manifest["images"]}
    assert [by_first[im["source_id"]] for im in manifest["images"][:12]]==manifest["random_progressive_target_ids_12_different_images"]
    assert [im["source_id"] for im in manifest["images"][:8]]==manifest["alternative_fill_image_ids_8"]
    assert manifest["selection_guards"]["protected_test"]=="NOT_ACCESSED"
    return {r["source_id"]:r for r in identity["current_source_image_sha256"]}


class JournaledPredictor:
    """Pre-request, fsync'd ledger; refuses any sixth call when cap=5.

    The ledger is append-only JSONL. Restarting an existing run is refused
    (including partial/failed runs). No automatic application-level retries.
    The provider is injected so offline tests consume no credits.
    """
    def __init__(self, provider, ledger_path, cap=MAX_CALLS):
        self.provider=provider
        self.ledger_path=Path(ledger_path)
        self.cap=cap
        assert 0<cap<=MAX_CALLS
        if self.ledger_path.exists():
            raise FileExistsError("A prior attempt ledger already exists; refuse duplicate billing")
        self.ledger_path.parent.mkdir(parents=True,exist_ok=True)
        self.ledger_path.touch(exist_ok=False)
        self.attempts=0
        self.successes=0
        self.context={}

    def _event(self, entry):
        with self.ledger_path.open("a",encoding="utf-8") as stream:
            stream.write(json.dumps(entry,ensure_ascii=False,allow_nan=False)+"\n")
            stream.flush()
            os.fsync(stream.fileno())

    def set_context(self, **kwargs):
        self.context=dict(kwargs)

    def __call__(self, pixels):
        if self.attempts>=self.cap:
            raise RuntimeError("V38-B HARD STOP: a further model call would exceed the maximum")
        self.attempts+=1
        index=self.attempts
        self._event({"event":"ATTEMPT_RESERVED","call_index":index,**self.context})
        try:
            response=self.provider(pixels)
            if not isinstance(response,list) or not all(isinstance(x,Detection) for x in response):
                raise TypeError("provider did not return Detection rows")
        except BaseException as err:
            self._event({"event":"ATTEMPT_FAILED","call_index":index,
                         "error_type":type(err).__name__})
            raise
        self.successes+=1
        self._event({"event":"ATTEMPT_SUCCEEDED","call_index":index,
                     "detection_count":len(response)})
        return response


def hosted_provider():
    """Strict one-POST-per-invocation transport: NO SDK/internal retries.

    Uses documented Serverless model endpoint and percent-valued confidence/
    overlap settings. Never prints URL, credentials, raw images, response or
    network exception messages. Network errors abort the run; no retry.
    """
    import base64
    from io import BytesIO
    from urllib.parse import urlencode
    from urllib.error import HTTPError, URLError
    from urllib.request import HTTPRedirectHandler, Request, build_opener

    key=os.environ.get("ROBOFLOW_API_KEY")
    if not key:
        raise RuntimeError("ROBOFLOW_API_KEY is absent; refusing hosted inference")
    class NoRedirect(HTTPRedirectHandler):
        def redirect_request(self,request,fp,code,msg,headers,newurl):
            return None
    opener=build_opener(NoRedirect())
    endpoint="https://serverless.roboflow.com/"+MODEL
    # The Hosted API REST endpoint uses percentage units (20 and 50), not SDK
    # fractional settings (0.20 and 0.50).
    private_url=endpoint+"?"+urlencode({
        "api_key":key,"confidence":20,"overlap":50
    })

    def infer_one(pixels):
        rgb=np.asarray(pixels,dtype=np.uint8)
        if rgb.ndim!=3 or rgb.shape[2]!=3:
            raise ValueError("Only a single RGB image per hosted call is allowed")
        container=BytesIO()
        # Fixed prospective V38-B amendment: quality-95 4:4:4 JPEG for EVERY
        # baseline, grid cell, deletion/insertion point and operator ablation.
        # It is lossy; acknowledge the resulting compression confound.
        Image.fromarray(rgb).save(container,format="JPEG",
                                  quality=95,subsampling=0,optimize=False)
        payload=container.getvalue()
        if not (0<len(payload)<=15*1024*1024):
            raise ValueError("JPEG95 4:4:4 payload exceeds 15MB; refusing model call")
        encoded=base64.b64encode(payload)
        req=Request(private_url,data=encoded,
                    headers={
                        "Content-Type":"application/x-www-form-urlencoded",
                        "User-Agent":"SEER-PPE-V38B-one-call-no-retry/1.0",
                        "Accept":"application/json"
                    },method="POST")
        try:
            # urllib's standard transport does not retry HTTP errors; redirects
            # are explicitly refused to prevent credential forwarding.
            with opener.open(req,timeout=120) as reply:
                if reply.status!=200 or reply.geturl().split("?")[0]!=endpoint:
                    raise RuntimeError("Unexpected hosted inference origin or status")
                body=reply.read(6*1024*1024+1)
                if len(body)>6*1024*1024:
                    raise RuntimeError("Hosted response exceeds size limit")
            result=json.loads(body)
        except HTTPError as exc:
            raise RuntimeError("Hosted inference HTTP status "+str(exc.code)+"; no retry") from None
        except URLError as exc:
            raise RuntimeError("Hosted inference transport unavailable; no retry") from None
        except Exception as exc:
            raise RuntimeError("Hosted inference transport or decode failed: "+type(exc).__name__) from None
        if not isinstance(result,dict) or not isinstance(result.get("predictions"),list):
            raise RuntimeError("Hosted response was not a predictions list")
        return [Detection(str(p.get("class") or p.get("class_name")),
                          float(p["x"]),float(p["y"]),
                          float(p["width"]),float(p["height"]),
                          float(p["confidence"]))
                for p in result["predictions"]]
    return infer_one


def reference(target, new_score):
    box=target["bbox_xywh"]
    return Detection(target["class_name"],float(box["x"]),float(box["y"]),
                     float(box["width"]),float(box["height"]),float(new_score))


def cell_list(h,w,n):
    result=[]
    for row in range(n):
        for col in range(n):
            a,b,c,d=cell_bounds(h,w,n,n,row,col)
            result.append((row,col,a,b,c,d,((b-a)*(d-c))/(h*w)))
    assert len(result)==n*n and abs(sum(t[-1] for t in result)-1)<1e-12
    return result


def response_for_all(image, blur, targets, references, predictor, grid, fill):
    h,w=image.shape[:2]
    maps={t["target_id"]:np.full((grid,grid),np.nan,dtype=float) for t in targets}
    records={t["target_id"]:[] for t in targets}
    for row,col,a,b,c,d,frac in cell_list(h,w,grid):
        altered=image.copy()
        if fill=="gray":
            altered[a:b,c:d,:]=127
        else:
            altered[a:b,c:d,:]=blur[a:b,c:d,:]
        predictor.set_context(phase="map",source_id=targets[0]["source_id"],
                              grid=grid,fill=fill,row=row,col=col)
        predicted=predictor(altered)
        for t in targets:
            tid=t["target_id"]
            ref=references[tid]
            score,status,matched=target_score(ref,predicted,
                                    minimum_iou=MIN_IOU,ambiguity_margin=AMBIGUITY_MARGIN)
            drop=None if score is None else float(ref.score-score)
            maps[tid][row,col]=np.nan if drop is None else drop
            records[tid].append({
                "row":row,"col":col,"area_fraction":frac,
                "status":status,"score_after":score,
                "score_drop":drop,"matched_iou":matched
            })
    return maps,records


def normal_ranks(data):
    """Tie-aware ordinal ranks (1=smallest) without treating cells as samples."""
    vals=list(map(float,data))
    order=sorted(range(len(vals)),key=lambda i:(vals[i],i))
    ranks=[0.]*len(vals)
    pos=0
    while pos<len(order):
        j=pos+1
        while j<len(order) and vals[order[j]]==vals[order[pos]]:
            j+=1
        mid=(pos+1+j)/2.
        for k in order[pos:j]:
            ranks[k]=mid
        pos=j
    return ranks


def spearman(a,b):
    x=np.asarray(normal_ranks(a),dtype=float)
    y=np.asarray(normal_ranks(b),dtype=float)
    x-=x.mean();y-=y.mean()
    den=float(np.sqrt(np.dot(x,x)*np.dot(y,y)))
    return None if den<=0 else float(np.dot(x,y)/den)


def kendall_b(a,b):
    concord=discord=tie_a=tie_b=0
    for i in range(len(a)):
        for j in range(i+1,len(a)):
            da=(a[i]>a[j])-(a[i]<a[j])
            db=(b[i]>b[j])-(b[i]<b[j])
            if da==0 and db==0:continue
            if da==0:tie_a+=1
            elif db==0:tie_b+=1
            elif da==db:concord+=1
            else:discord+=1
    den=math.sqrt((concord+discord+tie_a)*(concord+discord+tie_b))
    return None if den==0 else (concord-discord)/den


def aligned_metrics(fine,coarse,shape):
    h,w=shape
    if not(np.isfinite(fine).all() and np.isfinite(coarse).all()):
        return {"status":"AMBIGUOUS_REGION","spearman_rho":None,
                "kendall_tau_b":None,"top_four_overlap_fraction":None}
    small=cell_list(h,w,8)
    big=cell_list(h,w,4)
    fine_areas=np.asarray([[t[-1] for t in small[i*8:(i+1)*8]] for i in range(8)])
    coarse_areas=np.asarray([[t[-1] for t in big[i*4:(i+1)*4]] for i in range(4)])
    aligned=[]
    for r in range(4):
        for c in range(4):
            weighted=0.
            for dr in (0,1):
                for dc in (0,1):
                    rr=2*r+dr;cc=2*c+dc
                    weighted+=float(fine[rr,cc])
            aligned.append(weighted)
    fine_aligned=np.asarray(aligned)
    direct=np.asarray(coarse,dtype=float).ravel()
    # Exactly mirror frozen V34-A: direct drop / 4x4 area versus
    # SUM of four fine-cell drops / the SAME 4x4 pixel area.
    # Do not area-normalize twice or average fine drops before summation.
    area_density_coarse=direct/coarse_areas.ravel()
    area_density_fine=fine_aligned/coarse_areas.ravel()
    # Primary comparison is area-normalized signed sensitivity density.
    rho=spearman(area_density_fine,area_density_coarse)
    tau=kendall_b(area_density_fine.tolist(),area_density_coarse.tolist())
    # Deterministic signed descending rank, row-major tie breaks.
    order1=sorted(range(16),key=lambda k:(-area_density_fine[k],k))
    order2=sorted(range(16),key=lambda k:(-area_density_coarse[k],k))
    overlap=len(set(order1[:4])&set(order2[:4]))
    return {"status":"AVAILABLE" if rho is not None and tau is not None else "CONSTANT_RANKS",
            "spearman_rho":rho,"kendall_tau_b":tau,
            "top_four_overlap_fraction":overlap/4.0,
            "top_four_overlap_regions":overlap,
            "signed_density_direct_coarse":area_density_coarse.tolist(),
            "signed_density_pooled_fine":area_density_fine.tolist(),
            "mean_absolute_density_difference":float(np.abs(area_density_coarse-area_density_fine).mean())}


def rand_orders(target_id):
    result=[]
    for seed_index in range(RANDOM_SEEDS):
        seed=int.from_bytes(sha256(
            ("V38B-8x8-random|"+target_id+"|"+str(seed_index)).encode()
        ).digest(),"big")
        order=list(range(64))
        random.Random(seed).shuffle(order)
        result.append([(z//8,z%8) for z in order])
    assert len({tuple(x) for x in result})==RANDOM_SEEDS
    return result


def run_curve(image,blur,ref,blurred_score,predictor,tid,order,grid,direction,label):
    predictor.set_context(phase="curve",target_id=tid,grid=grid,
                          ordering=label,direction=direction)
    points,auc=progressive_curve(image,blur,ref,predictor,order,
                           direction=direction,ordering_name=label,
                           blurred_score=blurred_score,rows=grid,cols=grid,
                           step_percent=10,minimum_iou=MIN_IOU,
                           ambiguity_margin=AMBIGUITY_MARGIN)
    return {"points":[asdict(p) for p in points],
            "auc":auc,
            "status":"AVAILABLE" if auc is not None else "AUC_NULL_DUE_TO_AMBIGUITY"}


def one_image(item, targets, image, predictor, do_curve=False, do_ablation=False):
    sid=item["source_id"]
    predictor.set_context(phase="original_baseline",source_id=sid)
    original_predictions=predictor(image)
    references={}
    initial={}
    for t in targets:
        frozen=reference(t,t["baseline_confidence_from_v26"])
        score,status,matched=target_score(frozen,original_predictions)
        if status!="MATCHED" or score is None:
            raise RuntimeError("Frozen target not uniquely reproduced in current baseline")
        if abs(score-frozen.score)>.08:
            raise RuntimeError("Baseline drift greater than frozen 0.08; no threshold widening")
        references[t["target_id"]]=reference(t,score)
        initial[t["target_id"]]={"confidence":score,
                                  "matched_iou":matched,"status":status,
                                  "historical_confidence":frozen.score}
    blurred,blur_sigma=gaussian_blur_baseline(image)
    predictor.set_context(phase="blurred_endpoint",source_id=sid)
    blur_predictions=predictor(blurred)
    blurred_scores={}
    for t in targets:
        ref=references[t["target_id"]]
        score,status,matched=target_score(ref,blur_predictions)
        blurred_scores[t["target_id"]]={"score":score,"status":status,"matched_iou":matched}
    maps_by_grid={}
    records_by_grid={}
    for grid in (8,4):
        maps,records=response_for_all(image,blurred,targets,references,predictor,grid,"gray")
        maps_by_grid[grid]=maps
        records_by_grid[grid]=records
    ablation={}
    if do_ablation:
        for grid in (8,4):
            alt,record=response_for_all(image,blurred,targets,references,predictor,grid,"blur")
            ablation[grid]={"maps":alt,"trials":record}
    outcomes=[]
    for t in targets:
        tid=t["target_id"]
        fine=maps_by_grid[8][tid]
        coarse=maps_by_grid[4][tid]
        metrics=aligned_metrics(fine,coarse,image.shape[:2])
        extra={}
        if do_ablation:
            extra["blur_fill"]=aligned_metrics(ablation[8]["maps"][tid],
                                               ablation[4]["maps"][tid],image.shape[:2])
        outcomes.append({"target_id":tid,"class_name":t["class_name"],
            "baseline":initial[tid],"blurred_endpoint":blurred_scores[tid],
            "gray_map_8x8":records_by_grid[8][tid],
            "gray_map_4x4":records_by_grid[4][tid],
            "cross_resolution":metrics,"operator_ablation":extra,
            "blur_fill_map_8x8":ablation[8]["trials"][tid] if do_ablation else None,
            "blur_fill_map_4x4":ablation[4]["trials"][tid] if do_ablation else None,
            "curves":{}})
    if do_curve:
        # One frozen target per image, first of its pair. Both target IDs in the
        # map analysis remain paired on the same 80 image inferences.
        t=targets[0]
        tid=t["target_id"]
        row=next(r for r in outcomes if r["target_id"]==tid)
        b=blurred_scores[tid]
        fine=maps_by_grid[8][tid]
        coarse=maps_by_grid[4][tid]
        ref=references[tid]
        blocked=[]
        for grid,mat in ((8,fine),(4,coarse)):
            if not np.isfinite(mat).all() or float(np.maximum(mat,0.0).sum())<=0:
                blocked.append("INVALID_GRID_"+str(grid))
        if b["score"] is None:
            blocked.append("AMBIGUOUS_BLUR_ENDPOINT")
        if blocked:
            row["curves"]={"status":"NOT_RUN","reasons":blocked,"auc":None}
        else:
            sequences=[(8,"saliency",rank_grid_cells(fine))]
            sequences.extend((8,"random_seed_"+str(i),seq)
                             for i,seq in enumerate(rand_orders(tid)))
            sequences.append((4,"saliency",rank_grid_cells(coarse)))
            curves={}
            for grid,label,order in sequences:
                for direction in ("deletion","insertion"):
                    key=f"{grid}x{grid}_{label}_{direction}"
                    curves[key]=run_curve(image,blurred,ref,b["score"],predictor,
                                          tid,order,grid,direction,label)
            row["curves"]={"status":"EXECUTED","values":curves}
    return {"source_id":sid,"image_key":item["image_key"],
            "image_height":item["height"],"image_width":item["width"],
            "blur_sigma":blur_sigma,"targets":outcomes}


def run_all(manifest,identity,images_dir,predictor,output):
    targets=defaultdict(list)
    for t in manifest["targets"]:
        targets[t["source_id"]].append(t)
    by_source={x["source_id"]:x for x in identity["current_source_image_sha256"]}
    ablate=set(manifest["alternative_fill_image_ids_8"])
    curve_ids=set(manifest["random_progressive_target_ids_12_different_images"])
    result={"schema_version":"seer-ppe/v38b-two-grid-xai-execution/v1",
            "status":"IN_PROGRESS","model_id":MODEL,
            "wire_encoding":"JPEG_quality_95_chroma_444_fixed_all_requests",
            "study_cohort":"development_exposed_valid_only",
            "frozen_plan_sha256":sha256_path(MANIFEST),
            "images_total":24,"targets_total":48,"images_processed":0,
            "calls_attempted":0,"calls_succeeded":0,"no_test_accessed":True,
            "retrained":False,"per_image":[]}
    for i,item in enumerate(manifest["images"]):
        sid=item["source_id"]
        image=read_image(Path(images_dir)/(sid+".jpg"),by_source[sid])
        this=one_image(item,targets[sid],image,predictor,
                       do_curve=(targets[sid][0]["target_id"] in curve_ids),
                       do_ablation=(sid in ablate))
        result["per_image"].append(this)
        result["images_processed"]=i+1
        result["calls_attempted"]=predictor.attempts
        result["calls_succeeded"]=predictor.successes
        # A provisional numerical checkpoint is NOT an authorization to resume
        # inference automatically. Source pixels are not saved.
        save_atomic(Path(output).with_name(Path(output).name+".checkpoint.json"),result)
    result["status"]="COMPLETED"
    assert result["calls_attempted"]<=INTENDED_MAX
    assert result["calls_attempted"]==predictor.successes
    save_atomic(output,result)
    return result


def authorize_execute(args,manifest):
    # Both the file and the explicit flag are required. A valid file must be
    # created AFTER the author approves a one-time scope and cost limit.
    if args.confirm_authorized_max_attempts!=MAX_CALLS:
        raise PermissionError("No explicit 6000-call command confirmation")
    if args.authorization_file is None or not args.authorization_file.is_file():
        raise PermissionError("No separately approved one-time authorization record")
    a=load(args.authorization_file)
    for key,value in {
        "authorized":True,
        "study":"V38_B_FROZEN_24_VALID_48_TARGETS",
        "model_id":MODEL,
        "max_attempted_model_calls":MAX_CALLS,
        "intended_calls":INTENDED_MAX,
        "excluded_test":True,
        "no_training":True,
        "one_time":True,
        "wire_encoding":"JPEG_quality_95_chroma_444_fixed_all_requests",
    }.items():
        if a.get(key)!=value:
            raise PermissionError("Authorization field mismatch: "+key)
    if a.get("frozen_manifest_sha256")!=sha256_path(MANIFEST):
        raise PermissionError("Frozen manifest file hash differs from authorization")
    if a.get("approved_by_author") is not True:
        raise PermissionError("Explicit author's approval was not recorded")
    if a.get("approved_credit_cost_limit") is None:
        raise PermissionError("Credit cost ceiling was not author-approved")
    if float(a["approved_credit_cost_limit"])<1.125:
        raise PermissionError("Approved credit limit smaller than maximum estimate")
    assert manifest["budget"]["hard_maximum_new_hosted_model_calls_including_retries"]==MAX_CALLS


def self_test(output_dir):
    # All tests use a fake predictor, not a model, SDK, API key or downloaded photo.
    output_dir=Path(output_dir)
    output_dir.mkdir(parents=True,exist_ok=True)
    # A patterned image ensures blurred, gray-cell and original inputs differ.
    y,x=np.mgrid[:32,:32]
    rgb=np.stack(((17*x+13*y)%256,(x*31+y*7)%256,
                  np.where((x+y)%2==0,245,10)),axis=-1).astype(np.uint8)
    src=rgb.copy()
    box={"x":8.,"y":8.,"width":12.,"height":12.}
    t={"source_id":"mock-valid-image","image_key":"valid:mock-valid-image",
       "target_id":"mock-hard-hat","class_name":"Hard Hat",
       "bbox_xywh":box,"baseline_confidence_from_v26":.90}
    t2={"source_id":"mock-valid-image","image_key":"valid:mock-valid-image",
        "target_id":"mock-gloves","class_name":"Gloves",
        "bbox_xywh":{"x":24.,"y":24.,"width":12.,"height":12.},
        "baseline_confidence_from_v26":.80}
    def fake(pixels):
        delta=np.mean(np.abs(pixels.astype(float)-src.astype(float)))/255.
        return [Detection("Hard Hat",8.,8.,12.,12.,max(.01,.90-.4*delta)),
                Detection("Gloves",24.,24.,12.,12.,max(.01,.80-.3*delta))]
    item={"source_id":"mock-valid-image","image_key":"valid:mock-valid-image",
          "width":32,"height":32}
    ledger=output_dir/"v38b_offline_test_events.jsonl"
    ledger.unlink(missing_ok=True)
    p=JournaledPredictor(fake,ledger,cap=500)
    result=one_image(item,[t,t2],rgb,p,do_curve=True,do_ablation=True)
    # 1 original + 1 blur + 64 + 16 gray maps + 64 + 16 blur maps
    # + 11 orderings x 2 directions x 9 interiors + 1 x 2 x 9 on 4x4
    assert p.attempts==2+80+80+(11*2*9)+(1*2*9)==378
    assert p.successes==p.attempts
    assert len(result["targets"])==2
    assert all(len(t["gray_map_8x8"])==64 and len(t["gray_map_4x4"])==16
               for t in result["targets"])
    assert result["targets"][0]["cross_resolution"]["status"]=="AVAILABLE"
    assert len(result["targets"][0]["curves"]["values"])==24
    with ledger.open(encoding="utf-8") as stream:
        records=[json.loads(s) for s in stream if s.strip()]
    assert len(records)==756
    assert records[0]["event"]=="ATTEMPT_RESERVED"
    assert records[-1]["event"]=="ATTEMPT_SUCCEEDED"
    try:
        JournaledPredictor(fake,ledger,cap=500)
    except FileExistsError:
        pass
    else:
        raise AssertionError("Existing ledger must refuse duplicate execution")
    budget_ledger=output_dir/"guard_events.jsonl"
    budget_ledger.unlink(missing_ok=True)
    capped=JournaledPredictor(fake,budget_ledger,cap=3)
    for i in range(3):
        capped(rgb)
    try:
        capped(rgb)
    except RuntimeError:
        pass
    else:
        raise AssertionError("Hard cap not enforced")
    assert capped.attempts==3
    failed_ledger=output_dir/"failed_events.jsonl"
    failed_ledger.unlink(missing_ok=True)
    def broken(_):
        raise ConnectionError("synthetic transient failure")
    failing=JournaledPredictor(broken,failed_ledger,cap=3)
    try:
        failing(rgb)
    except ConnectionError:
        pass
    else:
        raise AssertionError("Failure was not propagated")
    assert failing.attempts==1 and failing.successes==0
    events=[json.loads(line) for line in failed_ledger.read_text().splitlines()]
    assert [x["event"] for x in events]==["ATTEMPT_RESERVED","ATTEMPT_FAILED"]
    # Test the *actual HTTP provider function* using a monkeypatched opener:
    # no real URL request or real credentials, and no implicit retries.
    from unittest.mock import patch
    from urllib.error import HTTPError
    class SingleRequestFailure:
        def __init__(self):
            self.calls=0
        def open(self,req,timeout):
            self.calls+=1
            raise HTTPError(req.full_url,503,"synthetic",hdrs=None,fp=None)
    fail_http=SingleRequestFailure()
    with patch.dict(os.environ,{"ROBOFLOW_API_KEY":"dummy_mock_key_no_real_auth"}):
        with patch("urllib.request.build_opener",return_value=fail_http):
            strict_hosted=hosted_provider()
            try:
                strict_hosted(rgb)
            except RuntimeError as e:
                assert "HTTP status 503" in str(e)
            else:
                raise AssertionError("Mocked HTTP 503 must abort")
    assert fail_http.calls==1, "Hosted provider must not retry HTTP failures"

    class MockResponse:
        status=200
        def __init__(self,url): self.url=url
        def geturl(self):return self.url
        def read(self,n):
            return json.dumps({"predictions":[{
                "class":"Hard Hat","x":8,"y":8,"width":12,
                "height":12,"confidence":0.90
            }]}).encode("utf8")
        def __enter__(self):return self
        def __exit__(self,*args):return False
    class SingleRequestSuccess:
        def __init__(self):self.calls=0
        def open(self,req,timeout):
            self.calls+=1
            return MockResponse(req.full_url)
    success_http=SingleRequestSuccess()
    with patch.dict(os.environ,{"ROBOFLOW_API_KEY":"dummy_mock_key_no_real_auth"}):
        with patch("urllib.request.build_opener",return_value=success_http):
            strict_hosted=hosted_provider()
            received=strict_hosted(rgb)
    assert success_http.calls==1 and len(received)==1
    assert received[0].class_name=="Hard Hat"

    constant=aligned_metrics(np.zeros((8,8)),np.zeros((4,4)),(32,32))
    assert constant["status"]=="CONSTANT_RANKS" and constant["spearman_rho"] is None
    sample={"status":"PASS_MOCK_FULL_XAI_2_TARGETS_WITHOUT_MODEL_CALLS",
            "mock_calls":p.attempts,
            "mock_curves":len(result["targets"][0]["curves"]["values"]),
            "both_grid_maps":True,"ablation":True,
            "guard_rejects_fourth_of_three":True,
            "failed_attempt_logged":True,"duplicate_ledger_rejected":True,
            "single_post_transport_one_call_failure_and_success":True,
            "actual_hosted_model_calls":0}
    save_atomic(output_dir/"v38b_mock_test_summary.json",sample)
    print(json.dumps(sample,indent=2))
    return 0


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test",action="store_true",
                        help="Full synthetic two-grid/multiple-random-orders dry run, zero Roboflow calls.")
    parser.add_argument("--preflight",action="store_true",
                        help="Verify frozen manifests; no image decode or inference.")
    parser.add_argument("--execute",action="store_true",
                        help="Live hosted mode. Requires future one-time author authorization.")
    parser.add_argument("--images-dir",type=Path)
    parser.add_argument("--output",type=Path,
                        default=ROOT/"V38_B_ACTUAL_XAI_RESULTS.json")
    parser.add_argument("--authorization-file",type=Path)
    parser.add_argument("--confirm-authorized-max-attempts",type=int)
    args=parser.parse_args()
    if sum((args.self_test,args.preflight,args.execute))!=1:
        parser.error("choose exactly one mode")
    if args.self_test:
        return self_test(args.output.parent/"v38b_offline_self_test")
    manifest=load(MANIFEST)
    identity=load(SOURCE_QA)
    valid=validate_manifest(manifest,identity)
    if args.preflight:
        checked=0
        if args.images_dir is not None:
            # Optional stronger zero-inference gate: verify all 24 downloaded
            # originals with the very same canonical EXIF-aware decoder.
            for img in manifest["images"]:
                source_id=img["source_id"]
                read_image(args.images_dir/(source_id+".jpg"),valid[source_id])
                checked+=1
        print(json.dumps({"status":"READY_READONLY_MANIFEST_QA",
                          "images":len(valid),"targets":48,
                          "images_with_canonical_rgb_sha_verified":checked,
                          "attempted_hosted_calls":0,
                          "planned_call_max":INTENDED_MAX,
                          "hard_attempted_cap":MAX_CALLS,
                          "authorization_present":False},indent=2))
        return 0
    if args.images_dir is None:
        parser.error("--images-dir is mandatory in execution mode")
    authorize_execute(args,manifest)
    # The full 24-image checksum gate is before the first hosted API call.
    for item in manifest["images"]:
        sid=item["source_id"]
        read_image(args.images_dir/(sid+".jpg"),valid[sid])
    if args.output.exists() or args.output.with_name(args.output.name+".checkpoint.json").exists():
        raise FileExistsError("Previous result/checkpoint exists: new paid execution refused")
    predictor=JournaledPredictor(hosted_provider(),
                  args.output.with_name(args.output.name+".attempts.jsonl"),MAX_CALLS)
    try:
        result=run_all(manifest,identity,args.images_dir,predictor,args.output)
    except BaseException as exc:
        save_atomic(args.output.with_name(args.output.name+".failed.json"),{
            "status":"FAILED_NO_AUTOMATIC_REPLAY",
            "error_type":type(exc).__name__,"calls_attempted":predictor.attempts,
            "calls_succeeded":predictor.successes,"no_test_accessed":True,
            "ledger_path":str(predictor.ledger_path)})
        raise
    print(json.dumps({"status":"COMPLETED",
           "calls_attempted":result["calls_attempted"],
           "images":result["images_processed"],
           "no_test_accessed":True},indent=2))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
