"""V40 final-export helper (review candidate only). No inference, no submission.
After Pandoc markdown+tex_math_dollars -> DOCX conversion, apply native Word
page fields, table pagination controls and strict equation checks. The full
render still needs page-by-page visual QA; do not certify on this script alone.
"""
from pathlib import Path
import argparse
from zipfile import ZipFile
from lxml import etree
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt

def add_page_number(sec):
    p=sec.footer.paragraphs[0]
    p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    if not p._p.xpath('.//w:instrText'):
        run=p.add_run()
        field=OxmlElement("w:fldSimple")
        field.set(qn("w:instr"),"PAGE")
        run._r.addnext(field)

def verify_math(path):
    ns={"m":"http://schemas.openxmlformats.org/officeDocument/2006/math"}
    with ZipFile(path) as z:
        tree=etree.fromstring(z.read("word/document.xml"))
    pairs=[]
    for f in tree.xpath("//m:f",namespaces=ns):
        a="".join(f.xpath("m:num//m:t/text()",namespaces=ns))
        b="".join(f.xpath("m:den//m:t/text()",namespaces=ns))
        assert a.strip() and b.strip(), (a,b)
        pairs.append((a,b))
    required={("TP","TP+FP"),("TP","TP+FN"),("2PR","P+R"),("2TP","2TP+FP+FN")}
    assert required.issubset(set(pairs)), pairs
    assert len(tree.xpath("//m:oMath",namespaces=ns))>=7
    return pairs

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("docx",type=Path)
    ap.add_argument("--main",action="store_true")
    ap.add_argument("--line-numbers",action="store_true",help="Enable only if journal requires")
    args=ap.parse_args()
    doc=Document(args.docx)
    for sec in doc.sections:
        add_page_number(sec)
        if args.line_numbers:
            if not sec._sectPr.xpath("./w:lnNumType"):
                el=OxmlElement("w:lnNumType")
                el.set(qn("w:countBy"),"1")
                el.set(qn("w:restart"),"continuous")
                sec._sectPr.append(el)
    for i,t in enumerate(doc.tables,1):
        for j,row in enumerate(t.rows):
            pr=row._tr.get_or_add_trPr()
            if not pr.xpath("./w:cantSplit"):pr.append(OxmlElement("w:cantSplit"))
            if j==0 and not pr.xpath("./w:tblHeader"):pr.append(OxmlElement("w:tblHeader"))
            for cell in row.cells:
                for p in cell.paragraphs:
                    p.paragraph_format.space_after=Pt(2)
                    # Main short tables 4–6: attempt to keep all rows together.
                    # Verify actual PDF pagination; do not blindly force long S2 tables.
                    if args.main and i in (4,5,6):
                        p.paragraph_format.keep_with_next=j<len(t.rows)-1
    doc.save(args.docx)
    if args.main:
        assert len(doc.tables)==6
        assert len(doc.inline_shapes)==4
        print("NATIVE_FRACTIONS",verify_math(args.docx))
    print("PAGE_FIELD_AND_TABLE_CONTROL_OK",args.docx)
if __name__=="__main__":
    main()
