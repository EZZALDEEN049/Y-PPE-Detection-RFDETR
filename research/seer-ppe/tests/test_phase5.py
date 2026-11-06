import sys, tempfile, unittest
from pathlib import Path
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from freeze_clean17 import normalized_name,known_family,audit

class FreezeGateTests(unittest.TestCase):
    def test_roboflow_filename_normalized(self):
        self.assertEqual(normalized_name('ppe_0466.jpg'),normalized_name('ppe_0466_jpg.rf.5016b8e78cb2d5133da2ad72ee996e09.jpg'))
    def test_clone_video_family(self):
        self.assertEqual(known_family('Sapi-7_mp4-102_jpg.rf.aabbcc.jpg'),'sapi-7_mp4')
    def test_unrelated_group_is_unknown(self):
        self.assertEqual(known_family('image_349.jpg'),'')
    def test_image_file_integrity_and_cross_split_pair_flag(self):
        with tempfile.TemporaryDirectory() as d:
            r=Path(d)/'data'; out=Path(d)/'audit'
            for split in ('train','valid','test'):
                (r/split/'images').mkdir(parents=True)
                (r/split/'labels').mkdir()
                image=Image.new('RGB',(24,16),'white' if split!='valid' else 'black')
                image.save(r/split/'images'/f'{split}.png')
                (r/split/'labels'/f'{split}.txt').write_text('0 0.5 0.5 0.3 0.3\n')
            result=audit(r,out)
            issue_types=[x['type'] for x in result['issues']]
            self.assertIn('cross_split_pixels_sha256',issue_types)
            self.assertEqual(result['counts']['test']['images'],1)
            self.assertTrue((out/'clean17_file_manifest.csv').exists())
            self.assertEqual(result['status'],'FAIL_OR_REVIEW_REQUIRED')
    def test_missing_label_is_reported(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)/'dataset';out=Path(d)/'audit'
            for split in ('train','valid','test'):
                (root/split/'images').mkdir(parents=True)
                (root/split/'labels').mkdir()
            Image.new('RGB',(15,15),'white').save(root/'train/images/aaa.png')
            result=audit(root,out)
            self.assertIn('missing_label',[x['type'] for x in result['issues']])

if __name__=='__main__':unittest.main()
