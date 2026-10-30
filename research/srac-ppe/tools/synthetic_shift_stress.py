#!/usr/bin/env python3
"""Synthetic-only risk control stress test. Never describe as RF-DETR performance.

Independent, identically distributed violation examples are sampled at one
calibration site. The second population deliberately violates exchangeability.
"""
import json
import numpy as np
from scipy.stats import beta

GRID=np.array([.02,.05,.10,.15,.20,.30,.40,.50,.60])

def simulate(n=350,trials=5000,seed=20261030,miss=.02,policy_error=.01,
             target_miss=.07,target_policy_error=.02,target_score_power=.5):
    rng=np.random.default_rng(seed)
    cats=rng.random((trials,n))
    bad=cats<miss+policy_error
    normal=~bad
    scores=rng.random((trials,n))
    kfc=np.stack([np.sum(normal&(scores<=t),axis=1) for t in GRID],axis=1)
    kuc=kfc+bad.sum(axis=1)[:,None]
    tail=.05/(2*len(GRID))
    ks=np.arange(n+1)
    lookup=np.where(ks==n,1.,beta.ppf(1-tail,ks+1,n-ks))
    lookup[-1]=1.
    feasible=(lookup[kfc]<=.05)&(lookup[kuc]<=.15)
    ix=np.where(feasible,np.arange(len(GRID)), -1).max(axis=1)
    selected=ix>=0
    tau=GRID[np.maximum(ix,0)]
    cal_fc=(1-miss-policy_error)*tau
    cal_uc=miss+policy_error+cal_fc
    shift_fc=(1-target_miss-target_policy_error)*tau**target_score_power
    shift_uc=target_miss+target_policy_error+shift_fc
    cal_violations=selected&((cal_fc>.05)|(cal_uc>.15))
    shift_violations=selected&((shift_fc>.05)|(shift_uc>.15))
    return {"warning":"SYNTHETIC SIMULATION ONLY; NOT A MODEL OR FIELD EXPERIMENT",
            "n_independent_simulated_violations":n,"simulations":trials,"seed":seed,
            "selection_rate":float(selected.mean()),
            "calibration_population_bound_exceed_count":int(cal_violations.sum()),
            "shifted_population_bound_exceed_count":int(shift_violations.sum()),
            "selected_threshold_counts":{str(t):int(np.sum(selected&(tau==t))) for t in GRID},
            "calibration_population":{"miss_probability":miss,"policy_error_probability":policy_error,
                                      "violation_score_cdf":"uniform"},
            "shifted_population":{"miss_probability":target_miss,
                                  "policy_error_probability":target_policy_error,
                                  "violation_score_cdf":f"F(t)=t**{target_score_power}"}}

if __name__=="__main__":
    print(json.dumps(simulate(),indent=2))
