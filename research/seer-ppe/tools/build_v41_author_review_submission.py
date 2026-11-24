#!/usr/bin/env python3
"""Author-requested clean submission-format V41 candidate; no submission or release approval."""
import re, json, shutil, subprocess, sys, hashlib, zipfile, os
from pathlib import Path
import fitz,pypandoc
from docx import Document
from docx.shared import Inches,Pt,RGBColor
from docx.enum.section import WD_ORIENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
ROOT=Path(__file__).resolve().parents[1];SUB=ROOT/"submissions/results-in-engineering"
OUT=Path(sys.argv[1]);OUT.mkdir(parents=True,exist_ok=False)
PKG=OUT/"RINENG_V41_AUTHOR_REVIEW";PKG.mkdir()
R=OUT/"raster";R.mkdir()
FIG=PKG/"Figures";FIG.mkdir()
PDF=PKG/"PDF_Proofs";PDF.mkdir()
SRC=OUT/"clean_sources";SRC.mkdir()
doi="https://doi.org/10.5281/zenodo.24489644"
def get(f):return (SUB/f).read_text(encoding="utf8")
def write(p,s):p.write_text(s,encoding="utf8")
def line(t,start,new):
    assert sum(l.startswith(start) for l in t.splitlines())==1,start
    return "\n".join(new if l.startswith(start) else l for l in t.splitlines())+"\n"
def remove_markers(t):
    return re.sub(r"\s*\[(?:RELEASE GATE|FINAL CHECK REQUIRED|FINAL AUTHOR PROOF):[^\]]*\]","",t).replace("****","")
def no_postal(t):return t.replace(", P.O. Box 6803","")
def numbered(t):
    body,refs=t.split("## References\n")
    entries=refs.strip().split("\n\n");assert len(entries)==20
    d={}
    for e in entries:
        m=re.match(r"([^,]+),.*? \((\d{4}[ab]?)\)\.",e)
        assert m,e
        d[(m[1],m[2])]=e
    order=[]
    def num(a,y):
        key=(a.replace("Fong and Vedaldi","Fong"),y)
        assert key in d,key
        if key not in order:order.append(key)
        return str(order.index(key)+1)
    names="Al-Tayar|Adebayo|Andres|Barlybayev|Bouguessa|Di Renzo|Fong and Vedaldi|Hooker|Kendall|Paes|Petsiuk|Robinson|Spearman|Vaghani|Yi"
    # Handle parenthetical grouped citations, then author-name narrative citations.
    def group(m):
        chunks=m[1].split("; ")
        n=[]
        for part in chunks:
            z=re.fullmatch(r"("+names+r")(?: et al\.)?, (\d{4}[ab]?(?:, \d{4}[ab]?)*)",part)
            if not z:return m[0]
            n.extend(num(z[1],y) for y in z[2].split(", "))
        return "["+", ".join(n)+"]"
    def scan(m):
        s=m[0]
        if s.startswith("("):return group(m)
        q=re.fullmatch(r"("+names+r")((?: et al\.)?) \((\d{4}[ab]?)\)",s)
        assert q,s
        return q[1]+q[2]+" ["+num(q[1],q[3])+"]"
    # Preserve first-appearance order, including special rank-statistics clauses.
    pat=r"\(("+r"(?:"+names+r")(?: et al\.)?, \d{4}[ab]?(?:, \d{4}[ab]?)*(?:; (?:"+names+r")(?: et al\.)?, \d{4}[ab]?(?:, \d{4}[ab]?)* )*"+r")\)"
    # Use a general parenthetical scanner; exact groups are validated.
    pat=r"\(([^()\n]+)\)|(?:"+names+r")(?: et al\.)? \(\d{4}[ab]?\)"
    def convert(m):
        s=m[0]
        if s.startswith("("):
            special=re.fullmatch(r"("+names+r")(?: et al\.)?, (\d{4}[ab]?); (average ranks for ties|tie-aware|https://doi\.org/10\.5281/zenodo\.24489644)",m[1])
            if special:
                n=num(special[1],special[2])
                if special[3].startswith("http"):return "["+n+"] ("+special[3]+")"
                return "["+n+"] ("+special[3]+")"
            return group(m)
        return scan(m)
    body=re.sub(pat,convert,body)
    assert len(order)==20,(len(order),set(d)-set(order))
    assert not re.search(r"(?:et al\.,? |Vedaldi, |Al-Tayar, |Spearman, |Kendall, )\(?\d{4}[ab]?",body)
    # Literal brackets escaped to prevent Markdown interpreting them as reference links.
    refout=[]
    for i,k in enumerate(order,1):
        refout.append(f"[{i}] "+d[k])
    return body+"## References\n\n"+"\n\n".join(refout)+"\n",order
m0=get("RINENG_MANUSCRIPT_V40_BATCH01_WORKING_UNSIGNED_2026-11-24.md")
m=remove_markers(no_postal(m0))
m=line(m,"**Prior dissemination and originality:**","**Prior dissemination and originality:** The four related publications from 2025 and 2026 are cited. This article reports current-reference object-detection auditing and cross-resolution perturbation measurements rather than new detector training or dataset development. The numerical reproducibility archive has been deposited in Zenodo (Al-Tayar, 2026; "+doi+"). The manuscript has not been submitted to another journal.")
m=m.replace("the deposited inventory requires confirmation.","the deposited inventory requires confirmation. No institutional approval or exemption is documented in the study record.")
m=m.replace("and must also be entered in the publisher's declaration-of-interests workflow as applicable","")
m=m.replace("Draft vector schematic prepared with OpenAI ChatGPT (GPT-6.2) assistance; final author review and approval pending.","Conceptual vector schematic prepared with OpenAI ChatGPT (GPT-6.2) assistance.")
m=m.replace("The comparison distinguishes the scientific endpoints; it does not establish reuse rights or resolve authorship questions.","The comparison distinguishes the scientific endpoints.")
m=m.replace("The complete 17-class distribution and the original per-image matching ledger are archived in the reproducibility material;","The complete 17-class distribution and per-image count records are included in the tested reproducibility candidate; the original matching ledger is retained in the research records;")
# The scientific body, equations and numerical table values must remain unchanged; only citation labels and editorial declarations are edited.
m,order=numbered(m)
oldmath=re.findall(r"^\$\$\n[\s\S]*?\n\$\$$",m0,re.M);newmath=re.findall(r"^\$\$\n[\s\S]*?\n\$\$$",m,re.M)
assert oldmath==newmath and len(oldmath)==7
oldtables=[l for l in m0.splitlines() if l.startswith("|")]
newtables=[l for l in m.splitlines() if l.startswith("|")]
assert len(oldtables)==len(newtables)
# Ignore the first cell of literature-comparison table only; all other cells remain identical.
for a,b in zip(oldtables,newtables):
    assert a==b or (re.search(r"\| (Al-Tayar|Andres) et al\.",a) and a.split("|")[2:]==b.split("|")[2:]),(a,b)
title=no_postal(re.sub(r"<!--[\s\S]*?-->","",get("RINENG_TITLE_PAGE_V40_WORKING_UNSIGNED_2026-11-24.md")))
cover=no_postal(get("RINENG_COVER_LETTER_V40_WORKING_UNSIGNED_2026-11-24.md")).split("\n---\n")[0]
cover=cover.replace("# Cover letter — V40 working draft (NOT FOR SUBMISSION YET)","# Cover letter")
cover=cover.replace("As the sole author, I confirm that the current cross-grid XAI results have not previously been published and that this manuscript has not been submitted to another journal.","As the sole author, I confirm that this manuscript has not been submitted to another journal. The numerical reproducibility archive has been deposited in Zenodo (v1, "+doi+"). The tested archive candidate supports offline recomputation and figure regeneration; complete hosted inference reproducibility is not claimed. Correspondence between the tested candidate and deposited files remains to be verified.")
s1=get("RINENG_SUPPLEMENT_V40_S1_WORKING_UNSIGNED_2026-11-24.md")
s1=re.sub(r"^\*\*Status:\*\*.*\n","",s1,flags=re.M)
s1=line(s1,"**Publication artwork note (working source):**","The vector artwork was regenerated from the frozen numerical arrays with pseudonymous target and image labels. Original archived figures remain unchanged.")
s1=line(s1,"**Author approval pending:**","The author reports Zenodo v1 deposition at "+doi+". The tested review candidate includes the historical spatial-agreement and native-cell numerical records; deposited-file correspondence and license scope require verification.")
s2=get("RINENG_SUPPLEMENT_V40_S2_WORKING_UNSIGNED_2026-11-24.md").replace("These remain separate author/editorial release requirements.","")
hi=get("RINENG_Highlights_V40_WORKING_2026-11-24.md")
bullets=[l[2:] for l in hi.splitlines() if l.startswith("- ")];assert 3<=len(bullets)<=5 and max(map(len,bullets))<=85
jobs=[("Manuscript",m,False,6,4),("Supplement_S1",s1,True,2,10),("Supplement_S2",s2,True,7,0),("Title_Page",title,False,0,0),("Cover_Letter",cover,False,0,0),("Highlights",hi,False,0,0)]
for n in [f"Figure_{i}" for i in range(1,5)]+[f"Figure_S{i}" for i in range(1,11)]:
    p=SUB/"artwork-publication/r5"/(n+".pdf")
    with fitz.open(p) as d:
        assert len(d)==1 and not d[0].get_images(full=True)
        d[0].get_pixmap(dpi=500,alpha=False).save(R/(n+".png"))
    shutil.copyfile(p,FIG/p.name)
ref=ROOT/"exports/RINENG_V38C_Manuscript_v0.3_2026-11-23.docx"
for name,md,landscape,nt,ni in jobs:
    assert not re.search(r"\[(?:RELEASE GATE|FINAL CHECK REQUIRED|FINAL AUTHOR PROOF):",md)
    write(SRC/(name+".md"),md)
    text,count=re.subn(r"!\[([^\]]*)\]\(artwork-publication/r5/(Figure_(?:[1-4]|S(?:10|[1-9])))\.pdf\)",lambda x:f"![{x[1]}]({R}/{x[2]}.png)",md)
    assert count==ni,(name,count)
    path=PKG/(name+".docx")
    pypandoc.convert_text(text,"docx",format="markdown+tex_math_dollars",outputfile=str(path),extra_args=["--standalone","--reference-doc="+str(ref)])
    doc=Document(path)
    doc.core_properties.author="Ezzaldeen Al-Tayar";doc.core_properties.title=name
    for sec in doc.sections:
        sec.page_width=Inches(11.69 if landscape else 8.27);sec.page_height=Inches(8.27 if landscape else 11.69)
        sec.orientation=WD_ORIENT.LANDSCAPE if landscape else WD_ORIENT.PORTRAIT
        sec.left_margin=sec.right_margin=Inches(.7 if landscape else .85);sec.top_margin=sec.bottom_margin=Inches(.75)
    # Preserve editable tables with simple horizontal rules, without shaded/vertical rules.
    for t in doc.tables:
        pr=t._tbl.tblPr
        borders=pr.find(qn("w:tblBorders"))
        if borders is not None:pr.remove(borders)
        borders=OxmlElement("w:tblBorders")
        for side in ("top","bottom","insideH","left","right","insideV"):
            el=OxmlElement("w:"+side);el.set(qn("w:val"),"single" if side in ("top","bottom","insideH") else "nil");el.set(qn("w:sz"),"4");el.set(qn("w:color"),"888888");borders.append(el)
        pr.append(borders)
        for row in t.rows:
            for cell in row.cells:
                tcpr=cell._tc.get_or_add_tcPr()
                for shd in list(tcpr.findall(qn("w:shd"))):tcpr.remove(shd)
                for p in cell.paragraphs:
                    for r in p.runs:r.font.size=Pt(9)
    assert len(doc.tables)==nt and len(doc.inline_shapes)==ni,(name,len(doc.tables),len(doc.inline_shapes))
    doc.save(path)
    subprocess.run([sys.executable,str(ROOT/"tools/v40_word_export_qa.py"),str(path)]+(["--main"] if name=="Manuscript" else []),check=True)
    print("DOCX",name,nt,ni)
subprocess.run(["libreoffice","-env:UserInstallation=file:///tmp/v41_review_lo","--headless","--convert-to","pdf","--outdir",str(PDF),*[str(p) for p in PKG.glob("*.docx")]],check=True)
stats={}
for p in PDF.glob("*.pdf"):
    with fitz.open(p) as d:
        text="\n".join(pg.get_text() for pg in d)
        assert len(d)>0 and len(text)>80
        if p.stem=="Manuscript":
            for token in ("0.8706","0.6490","0.5459","0.6709","10.5281/zenodo.24489644"):assert token in text,token
        # Render every page and audit text bounding boxes, not a substitute for human visual inspection.
        outliers=0
        for pg in d:
            pix=pg.get_pixmap(matrix=fitz.Matrix(1.0,1.0),alpha=False)
            assert pix.width>100 and pix.height>100
            for b in pg.get_text("dict")["blocks"]:
                for l in b.get("lines",[]):
                    for sp in l["spans"]:
                        if sp["text"].strip() and not (fitz.Rect(sp["bbox"]) in pg.rect+(-2,-2,2,2)):outliers+=1
        stats[p.stem]={"pages":len(d),"word_tokens":len(text.split()),"out_of_page_text_spans":outliers}
assert len(stats)==6
# Do not claim that unverified Zenodo contents or ethical gates have been cleared.
note="""# V41 — Author review before submission
This is the requested clean submission-format candidate, not an authorized submission and not a certification of journal readiness.

Main manuscript, separate title page, cover letter, Highlights, both editable supplements, 14 separate vector figures and matching PDF proofs are provided. The working-source editorial bracket markers were moved to this checklist; substantive disclosure limitations remain in the text. References are numbered by first appearance. The archived scientific data and model were not changed; no inference was run.

Before uploading:
- Obtain/document the applicable institutional ethics determination and any required safeguards, particularly for potentially depicted minors; capture consent is not research-specific consent. No approval/exemption is documented.
- Verify the actual Zenodo v1 DOI, files, access and license scopes against the tested archive, including checksums. The author reports the publication; independent content verification remains outstanding. Check for privacy/rights exposure; restrict access or correct by a new version if required.
- Complete the author's independent review and approve the AI-assisted content and conceptual Figure 4, the text/figure reuse rights, title-page postal address and final declarations. Do not claim complete author review until performed.
- Verify the current Results in Engineering guide, portal article type, file slots, citation style and any mandatory publisher declarations. The live guide returned HTTP 403. A graphical abstract is not included. Do not represent the internal proof as accepted or publication-ready.
- Inspect every rendered page at full size for typography, table pagination and figure placement. Automated render and structural checks do not replace that inspection.
- After clearance, submit only manuscript, title page, cover letter, highlights, supplements and required figures (not this checklist, QA report or PDF proofs unless requested by the portal).

No journal submission has occurred.
"""
write(PKG/"READ_BEFORE_SUBMISSION.md",note)
write(PKG/"QA_REPORT.json",json.dumps({"status":"CANDIDATE_ONLY_PENDING_AUTHOR_AND_RELEASE_GATES","source_revision":subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip(),"documents":stats,"references":len(order),"doi_identifiers":16,"equations":7,"figure_pdfs":14,"tables":15,"new_model_calls":0},indent=2)+"\n")
write(PKG/"SHA256SUMS.txt","".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(PKG).as_posix()}\n" for p in sorted(PKG.rglob("*")) if p.is_file()))
z=OUT/"RINENG_V41_Submission_Format_AUTHOR_REVIEW.zip"
with zipfile.ZipFile(z,"w",zipfile.ZIP_DEFLATED) as zz:
    for p in sorted(PKG.rglob("*")):
        if p.is_file():zz.write(p,p.relative_to(PKG))
with zipfile.ZipFile(z) as zz:assert zz.testzip() is None;print("ZIP_FILES",len(zz.namelist()))
print("V41_QA",json.dumps(stats),"ZIP_BYTES",z.stat().st_size,"ZIP_SHA256",hashlib.sha256(z.read_bytes()).hexdigest())
