# SEER-PPE: cumulative research (v0.6, 10 Nov 2026)

**This is a developing research manuscript, not a completed or published efficacy study.**

Canonical mutable draft: [MANUSCRIPT_MASTER.md](MANUSCRIPT_MASTER.md)  
Progress: [PROGRESS.md](PROGRESS.md)  
Phase-6 integrity and feasibility report: [PHASE6_REPORT.md](PHASE6_REPORT.md)  
Experimental plan: [PROTOCOL_MASTER.md](PROTOCOL_MASTER.md)  
Source changes: [CHANGELOG.md](CHANGELOG.md).

## Verifiable accomplishments

- Corrected 17-class Y-PPE: **2,288 images, 16,300 annotations**, independently SHA/ZIP checked after reconstruction from the frozen clone and 39 exclusions.
- The full **127,166,577-byte archive** was saved as 3 wrapped parts in the **owner's restricted Drive** (not in public GitHub), then reconstructed and verified locally. SHA-256: `d47d9676b785a847ef1bcb8a871574815b0b67b967f9107680fb0b85b1a52d61`.
- Seven dHash<=4 cross-split candidates were visually reviewed by a **single analyst** as different photos/objects, still pending independent source-family verification.
- Thirty pilot development images screened for context: **14 plausible fieldwork, 14 product/non-work controls, 2 uncertain**. This is **not** expert PPE compliance ground truth.
- Research Python prototype includes target-preserving XAI occlusion, routing, confidence and hardware checks. All **56/56 local synthetic unit tests** passed; **52 public-safe tests** exclude four tests dependent on private review-queue files.

## Run public-safe engineering tests

```bash
cd research/seer-ppe
pip install -r requirements-min.txt pillow
for test in test_prototype.py test_phase3.py test_phase5.py test_phase6.py; do
  PYTHONPATH=. python -m unittest discover -s tests -p "$test" -v
done
```

## Strict claims boundary

No independently verified worker-level PPE mandate, completed human A/B review, **exact trained 17-class local XAI**, real energy-metered joule measurements, independent site-group final test, or safety-energy SEER benefit exists yet. Historical trained 9-class checkpoints are **not** substitutes for ALTAYYAR's 17-class detector.

Archive images, reviewer case mapping, and image-contact sheets are **not published to GitHub**. Even within the owner's internal Drive research vault, individual image rights require separate clearance before onward sharing.

Every subsequent phase updates this same manuscript, progress log and changelog; no unexecuted metrics are treated as research findings.
