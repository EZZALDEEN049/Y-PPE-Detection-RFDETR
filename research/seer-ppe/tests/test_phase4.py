import csv, unittest, pathlib, json
ROOT=pathlib.Path(__file__).resolve().parents[1]

def loadcsv(path):
 with (ROOT / path).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))

class TestPhase4(unittest.TestCase):
 def test_pilot_30_unique_and_no_test(self):
  a=loadcsv('review_internal/SAMPLE_INTERNAL_RESEARCH_ONLY.csv')
  self.assertEqual(len(a),30);self.assertEqual(len({r['image_id'] for r in a}),30)
  self.assertEqual(sum(r['split']=='train' for r in a),16)
  self.assertEqual(sum(r['split']=='valid' for r in a),14)
  self.assertFalse(any(r['split']=='test' for r in a))
 def test_blind_queues_hide_prior_labels(self):
  a=loadcsv('review_internal/REVIEWER_A_BLIND_QUEUE.csv')
  b=loadcsv('review_internal/REVIEWER_B_BLIND_QUEUE.csv')
  self.assertEqual({r['image_id'] for r in a},{r['image_id'] for r in b})
  self.assertEqual(len(a),30)
  self.assertFalse('original_no_hard_hat_boxes' in a[0]);self.assertFalse('sampling_stratum' in a[0])
  self.assertTrue(all(r['review_status']=='NOT_STARTED' for r in a+b))
 def test_rights_hash_source_membership_are_unverified(self):
  a=loadcsv('review_internal/SOURCE_PROVENANCE_AND_FREEZE_GATE.csv')
  self.assertEqual(len(a),30)
  self.assertTrue(all(r['rights_review']=='UNKNOWN' and not r['sha256_file'] and not r['acquisition_group_id'] for r in a))
  self.assertTrue(all(r['clean17_archive_membership']=='UNVERIFIED' for r in a))
 def test_evidence_open_gt(self):
  a=json.loads((ROOT/'evidence/PHASE4_INDEX_AUDIT_2026-11-06.json').read_text())
  self.assertEqual(a['pilot_sample']['adjudicated_workers'],0)
  self.assertEqual(a['live_index']['unique_image_ids'],2327)
  self.assertTrue('OPEN' in a['gates']['source_group_independence'])

if __name__=='__main__':unittest.main()
