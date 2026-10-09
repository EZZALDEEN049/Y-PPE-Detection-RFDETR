# Stage 11B — Safety-Class Interpretation Revision

## Reviewer concern addressed
The prior manuscript risked conflating:
1. in-domain class learnability failure; and
2. additional cross-domain degradation.

This is most important for Construction-PPE-trained violation classes, which were already near floor in-domain.

## Revised interpretation

### Y-PPE → Construction-PPE
This direction supports a genuine additional transfer-degradation claim at the frozen operating point:
- no_helmet: 0.310 → 0.117 (loss 0.193)
- no_gloves: 0.303 → 0.039 (loss 0.264)
- no_boots: 0.367 → 0.000 (loss 0.367)

### Construction-PPE → Y-PPE
This direction does **not** support attributing the safety-class failure primarily to domain shift:
- no_helmet: 0.027 → 0.024 (additional loss 0.003)
- no_gloves: 0.020 → 0.015 (additional loss 0.005)
- no_boots: 0.000 → 0.000 (additional loss 0.000)

The correct interpretation is that the Construction-PPE-trained models show a severe in-domain learnability limitation for the explicit violation classes under the frozen training protocol.

## Consensus-FN interpretation
Three-seed consensus is now described as persistence under training stochasticity, not independent replication.

## Stage 11A robustness result integrated
The aggregate domain-gap result remains substantial after:
- strict confirmed near-duplicate exclusion; and
- conservative direct train-scene exclusion.

Therefore, the manuscript now separates three evidence layers:
1. aggregate bidirectional domain degradation;
2. Y→C safety-class transfer degradation;
3. Construction-PPE safety-class learnability failure.

This revision narrows the claim while making it scientifically stronger.
