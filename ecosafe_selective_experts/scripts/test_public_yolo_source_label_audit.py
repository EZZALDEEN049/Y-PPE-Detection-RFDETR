"""Synthetic bytes/YOLO labels ONLY, never images of people or a detector."""
from __future__ import annotations
import tempfile,unittest
from pathlib import Path
from importlib.util import module_from_spec,spec_from_file_location
sp=spec_from_file_location("source",Path(__file__).with_name("17_public_yolo_source_label_audit.py"))
audit=module_from_spec(sp)
sp.loader.exec_module(audit)


class SourceAuditTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        (self.root/"data.yaml").write_text(
          "nc: 4\nnames: ['nohelmet', 'noglove', 'noboots', 'person']\n",encoding="utf8")
        im=self.root/"train"/"images"
        lab=self.root/"train"/"labels"
        im.mkdir(parents=True)
        lab.mkdir()
        for i,c in enumerate((0,1,2)):
            (im/f"fake{i}.jpg").write_bytes(("synthetic bytes "+str(i)).encode())
            (lab/f"fake{i}.txt").write_text(f"{c} 0.5 0.5 0.2 0.2\n",encoding="utf8")
        self.schema={"reviewed_class_map":{"0":"no_helmet","1":"no_gloves","2":"no_boots"},
                     "research_use_acknowledged":True}

    def test_valid_synthetic_record_is_not_external_confirmation(self):
        result=audit.inspect(self.root,self.schema)
        self.assertEqual(result["critical_gt_counts"],
          {"no_boots":1,"no_gloves":1,"no_helmet":1})
        self.assertEqual(result["image_counts_per_split"],{"train":3})
        self.assertFalse(result["test_authorized"])
        self.assertFalse(result["human_worksite_groups_verified"])
        self.assertNotIn("image_names",result)

    def test_missing_label_fails(self):
        (self.root/"train"/"labels"/"fake1.txt").unlink()
        with self.assertRaises(ValueError):audit.inspect(self.root,self.schema)

    def test_wrong_box_fails(self):
        (self.root/"train"/"labels"/"fake1.txt").write_text("1 0.9 0.5 0.5 0.3\n")
        with self.assertRaises(ValueError):audit.inspect(self.root,self.schema)

    def test_missing_class_fails(self):
        (self.root/"train"/"labels"/"fake2.txt").write_text("")
        with self.assertRaises(ValueError):audit.inspect(self.root,self.schema)

    def test_reject_no_shoes_not_safety_boots(self):
        (self.root/"data.yaml").write_text(
          "nc: 4\nnames: ['nohelmet', 'noglove', 'no_shoes', 'person']\n")
        with self.assertRaises(ValueError):audit.inspect(self.root,self.schema)

    def test_missing_rights_attestation_fails(self):
        self.schema["research_use_acknowledged"]=False
        with self.assertRaises(ValueError):audit.inspect(self.root,self.schema)

    def test_wrong_native_mapping_fails(self):
        self.schema["reviewed_class_map"]["2"]="no_helmet"
        with self.assertRaises(ValueError):audit.inspect(self.root,self.schema)

    def test_unknown_original_class_order_fails(self):
        self.schema["reviewed_class_map"]["17"]="no_boots"
        del self.schema["reviewed_class_map"]["2"]
        with self.assertRaises(ValueError):audit.inspect(self.root,self.schema)

    def test_duplicate_source_bytes_across_splits_flagged_not_independence_certified(self):
        p=self.root/"val"/"images";l=self.root/"val"/"labels"
        p.mkdir(parents=True);l.mkdir()
        (p/"shadow.jpg").write_bytes((self.root/"train"/"images"/"fake0.jpg").read_bytes())
        (l/"shadow.txt").write_text("0 0.5 0.5 0.2 0.2\n")
        r=audit.inspect(self.root,self.schema)
        self.assertEqual(r["exact_cross_split_duplicate_sha_groups"],1)
        self.assertFalse(r["human_worksite_groups_verified"])

    def test_polygon_labels_are_blocked(self):
        (self.root/"train"/"labels"/"fake0.txt").write_text("0 0.1 0.1 0.2 0.2 0.2 0.3 0.1 0.3\n")
        with self.assertRaises(ValueError):audit.inspect(self.root,self.schema)

    def test_yaml_block_class_order_supported(self):
        (self.root/"data.yaml").write_text(
         "nc: 4\nnames:\n  0: nohelmet\n  1: noglove\n  2: noboots\n  3: person\n")
        self.assertEqual(audit.read_class_names((self.root/"data.yaml").read_text()),
                         ["nohelmet","noglove","noboots","person"])
        self.assertEqual(audit.inspect(self.root,self.schema)["native_class_count"],4)

if __name__=="__main__":
    unittest.main()
