# Draft cover letter to Results in Engineering (NOT YET SUBMITTED)

**To:** Editor-in-Chief, *Results in Engineering* (Elsevier)  
**From:** Ezzaldeen Al-Tayar — Taiz University, Yemen  
**Subject:** Proposed original research paper — Cross-Resolution Consistency of Target-Matched Perturbation Sensitivity Maps for Personal Protective Equipment Detection

Dear Editor-in-Chief,

We would like to submit for consideration in *Results in Engineering* our manuscript entitled **“Cross-Resolution Consistency of Target-Matched Perturbation Sensitivity Maps for Personal Protective Equipment Detection.”** The study examines an engineering inspection problem: what evidence can be derived from black-box perturbations of equipment detections, and how reliable is the spatial ordering of the resulting sensitivity maps when the occlusion grid resolution changes?

Using an unchanged 17-class RF-DETR Small model, the study evaluated detections on 459 original-source validation images containing 3,471 currently annotated objects, yielding micro-F1=0.8706 under class-exact IoU≥0.50 matching. We subsequently analyzed ten prespecified target detections from eight development-exposed images with 8×8 and 4×4 occlusion grids and progressive deletion/insertion curves. Aligning the maps at exact pixel coordinates yielded average Spearman ρ=0.5416, Kendall τ-b=0.4239 and 65% agreement among the four most sensitive regions. One target had no common top-four regions, underscoring that sensitivity maps should not be assumed invariant to a change in spatial resolution.

We believe these findings may interest engineering researchers developing responsible image-based screening and model diagnostic workflows. The present contribution is a quantitatively auditable study of **target-matched perturbation response and cross-resolution stability**, not a new detection architecture or a claim that visual saliency proves worker-level occupational compliance. Previous publications from the research programme on PPE detection and conceptual explainable frameworks are cited and distinguished from the measurements introduced here. Our conclusions explicitly acknowledge the small, development-exposed XAI cohort, a single seeded-random ordering and the absence of tested safety or human-review outcomes.

**Author confirmation still required before this letter may be sent:** [Confirm manuscript is original in its present form, is not under consideration elsewhere, has approval of all listed authors and responsible institutions, complies with all research ethics, worker-image privacy and data rights requirements, and that funding/competing-interest/AI-use statements are accurate.]

Thank you for considering our work.

Sincerely,

**Ezzaldeen Al-Tayar**  
Faculty of Engineering and Information Technology  
Taiz University, Taiz, Yemen  
Corresponding author: azzaltayyar@gmail.com

---

**Internal editorial note — remove before submission:** This draft is not an email or an actual letter sent to Elsevier. Its novelty, rights/ethics, originality and author declarations must be approved in writing by the final author team. The title and letter should match the final scientific manuscript, and the journal's specific cover-letter requirements must be checked in its Guide for Authors.
