import argparse, json, random
from pathlib import Path
ap=argparse.ArgumentParser(); ap.add_argument("--variant",choices=["nano","small","medium","large"],required=True); ap.add_argument("--dataset",required=True); ap.add_argument("--output",required=True); ap.add_argument("--epochs",type=int,default=20); ap.add_argument("--batch-size",default="auto"); ap.add_argument("--grad-accum-steps",type=int,default=1); ap.add_argument("--lr",type=float,default=1e-4); ap.add_argument("--seed",type=int,default=20260927); a=ap.parse_args()
import torch
from rfdetr import RFDETRNano, RFDETRSmall, RFDETRMedium, RFDETRLarge
cls={"nano":RFDETRNano,"small":RFDETRSmall,"medium":RFDETRMedium,"large":RFDETRLarge}[a.variant]; batch=a.batch_size if a.batch_size=="auto" else int(a.batch_size); random.seed(a.seed); torch.manual_seed(a.seed)
if torch.cuda.is_available(): torch.cuda.manual_seed_all(a.seed)
Path(a.output).mkdir(parents=True,exist_ok=True); (Path(a.output)/"run_config.json").write_text(json.dumps(vars(a),indent=2),encoding="utf-8")
m=cls(); m.train(dataset_dir=a.dataset,epochs=a.epochs,batch_size=batch,grad_accum_steps=a.grad_accum_steps,lr=a.lr,output_dir=a.output,early_stopping=True,run_test=False,tensorboard=True)
