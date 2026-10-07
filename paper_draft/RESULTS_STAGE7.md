# Draft — Results

## Cross-domain performance degradation

The frozen held-out evaluation comprised six completed YOLO11m models, trained independently on Y-PPE-h9-v2 or Construction-PPE-h9-v2 using seeds 17, 42, and 2026, and evaluated on both domains without further training, adaptation, or checkpoint reselection. Across the three Y-PPE-trained seeds, mean in-domain mAP50:95 was 0.291 ± 0.007, whereas evaluation on Construction-PPE yielded 0.121 ± 0.003. This corresponds to an absolute generalization gap of 0.170 and a relative degradation of 58.4%. For Construction-PPE-trained models, mean in-domain mAP50:95 was 0.252 ± 0.004 and decreased to 0.082 ± 0.005 on Y-PPE, giving a comparable absolute gap of 0.170 but a larger relative degradation of 67.4%.

The direction-specific degradation was reproduced across all three seeds. Y-PPE-trained seed-level mAP50:95 gaps were 0.173, 0.178, and 0.159 for seeds 17, 42, and 2026, respectively. Construction-PPE-trained models showed corresponding gaps of 0.172, 0.166, and 0.171. Thus, the cross-domain loss was not attributable to a single anomalous initialization.

## Fixed operating-point reliability

At the frozen operating point (confidence=0.25, class-matched IoU=0.50, NMS IoU=0.70), Y-PPE-trained models decreased from mean precision/recall/F1 of 0.881/0.516/0.651 in-domain to 0.711/0.382/0.497 on Construction-PPE. Construction-PPE-trained models decreased from 0.921/0.580/0.712 in-domain to 0.766/0.209/0.328 on Y-PPE. The latter transfer direction was characterized by a particularly large recall loss, indicating that domain shift manifested primarily as missed objects rather than only an increase in false alarms.

## Safety-critical class failure

The safety-violation classes showed substantially weaker robustness than the aggregate metrics suggested. For Y-PPE-trained models, in-domain mean recall was 0.310 for no_helmet, 0.303 for no_gloves, and 0.367 for no_boots. On Construction-PPE, the corresponding recalls fell to 0.117, 0.039, and 0.000. Construction-PPE-trained models already exhibited near-floor in-domain recall for the same violation classes (0.027, 0.020, and 0.000), and cross-domain transfer to Y-PPE did not recover them.

A deterministic consensus-failure audit confirmed that these failures were highly consistent across seeds. In the Y-PPE→Construction-PPE direction, 31/37 no_helmet objects (83.8%), 47/51 no_gloves objects (92.2%), and 15/15 no_boots objects (100%) were missed by all three Y-PPE-trained models. In the Construction-PPE→Y-PPE direction, the corresponding consensus false-negative rates were 13/14 (92.9%), 85/88 (96.6%), and 30/30 (100%), respectively.

## Dataset diagnostic audit

The frozen dataset derivatives were both stored as 640×640 square images, excluding stored image resolution and aspect ratio as direct explanations for the observed domain gap. However, class support and object-scale distributions differed materially. The training-set max-to-min nonzero class-frequency ratio was 11.49 in Y-PPE and 21.76 in Construction-PPE. Safety-class support was also heterogeneous: Y-PPE contained 113/677/226 training instances of no_helmet/no_gloves/no_boots, whereas Construction-PPE contained 352/403/74.

The strongest scale mismatch occurred for no_boots. In Y-PPE training, approximately 30.5% of no_boots instances were small, 21.2% medium, and 48.2% large; Construction-PPE contained approximately 77.0% small and 23.0% medium no_boots instances, with no large instances. Nevertheless, the consensus failure audit showed that scale mismatch alone was insufficient to explain the cross-domain collapse: in Construction-PPE→Y-PPE transfer, all 30 no_boots objects were missed across small, medium, and large bins, including 14 large instances.
