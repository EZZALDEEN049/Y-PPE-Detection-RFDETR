import argparse, json, pickle, numpy as np, pandas as pd
from sklearn.isotonic import IsotonicRegression
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss, log_loss
ap=argparse.ArgumentParser(); ap.add_argument("--csv",required=True,help="CSV with confidence,correct"); ap.add_argument("--method",choices=["platt","isotonic"],default="platt"); ap.add_argument("--out",required=True); a=ap.parse_args(); d=pd.read_csv(a.csv).dropna(subset=["confidence","correct"]); x=d["confidence"].to_numpy(); y=d["correct"].astype(int).to_numpy()
if len(np.unique(y))<2: raise SystemExit("Need both correct and incorrect detections")
if a.method=="platt": m=LogisticRegression(); m.fit(x.reshape(-1,1),y); p=m.predict_proba(x.reshape(-1,1))[:,1]
else: m=IsotonicRegression(out_of_bounds="clip"); m.fit(x,y); p=m.predict(x)
report={"method":a.method,"n":len(y),"brier":float(brier_score_loss(y,p)),"nll":float(log_loss(y,np.clip(p,1e-8,1-1e-8)))}
with open(a.out,"wb") as f: pickle.dump({"model":m,"report":report},f)
print(json.dumps(report,indent=2))
