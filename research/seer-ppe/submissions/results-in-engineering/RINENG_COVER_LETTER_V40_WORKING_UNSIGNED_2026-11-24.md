# Cover letter — V40 working draft (NOT FOR SUBMISSION YET)

**To:** Editor-in-Chief, *Results in Engineering* (Elsevier)  
**From:** Ezzaldeen Al-Tayar — Taiz University, Yemen  
**Subject:** Original research manuscript — Cross-Resolution Consistency of Target-Matched Perturbation Sensitivity Maps for Personal Protective Equipment Detection

Dear Editor-in-Chief,

I am pleased to present for your consideration the manuscript entitled **“Cross-Resolution Consistency of Target-Matched Perturbation Sensitivity Maps for Personal Protective Equipment Detection.”** The work examines a bounded engineering question: how consistently a fixed object detector's **target-matched perturbation sensitivity maps** rank image regions when the occlusion grid changes between 8×8 and 4×4, and how that consistency depends on the occlusion replacement operator.

Using an unchanged 17-class RF-DETR Small checkpoint, I evaluated class-exact detection outcomes on **459 original-source Validation images**, obtaining micro-F1 **0.8706** against the current single-curator annotated reference. The original exploratory spatial study contained ten target detections in eight development-exposed images. A subsequent **separately frozen diagnostic replication** evaluated **48 preselected detections in 24 Validation images**, with 4,984 hosted model requests logged through a pre-request call ledger. Of these 48 targets, **45** yielded estimable grid-pair coefficients; mean Spearman rho was **0.6490**, mean Kendall tau-b **0.5197**, and mean top-four region overlap **66.7%**. Three maps retained undefined coefficients because of ambiguous same-class target matching.

The larger experiment also compared neutral gray occlusion with Gaussian-blur fill. Across **14 valid paired operator comparisons**, the mean Spearman coefficient was **0.6943** for gray fill and **0.4811** for blur fill. A frozen subset of eleven scorable targets yielded **264 valid deletion/insertion curves**, with favorable saliency-ranking AUCs relative to ten-seed random-order averages; the ranking was computed and assessed using related detector perturbations, so no independent causal attribution-correctness or global method-superiority claim is made. The older and newer samples were **not pooled**, because of differences in selected targets and image transport encoding.

I consider these measured constraints on XAI-map resolution and operator dependence relevant to careful use of object detectors in engineering inspection and image-based diagnostic workflows. I explicitly distinguish our focus from published detector explanations such as D-MFPP (Andrés et al., 2024, *Results in Engineering*, 24, 103498). This manuscript does **not** present a new detector architecture, independently acquired field-site validation, worker-level PPE compliance measurement or verified safety outcome.

The original Y-PPE source corpus and detector are reused research resources described in earlier publications, which are cited. The present article reports different empirical endpoints. As the sole author, I confirm that the current cross-grid XAI results have not previously been published and that this manuscript has not been submitted to another journal.

Thank you for considering the manuscript.

Sincerely,

**Ezzaldeen Al-Tayar**  
Faculty of Engineering and Information Technology  
Taiz University, P.O. Box 6803, Taiz, Yemen  
Corresponding author: azzaltayyar@gmail.com

---

**Internal release gate — remove before submission:** Author-confirmed funding, competing interests, contribution roles, image/person permission attestation and AI-disclosure authorization are recorded in the manuscript. Institutional ethics determination, organization/third-party rights scope, permitted archive, full-text prior-work review, final AI-assisted content review and final author approval remain pending. No submission authorization granted.
