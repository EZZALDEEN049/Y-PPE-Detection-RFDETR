# External validation data-access request — UNSENT draft

**Status (2026-10-18): prepared ONLY. No email was sent to an author, no permission received, no external data downloaded.** Sending should be decided by the research team and addressed through their institutional account. This letter does not imply a right to redistribute source workers' images.

**Source paper:** Wang, S., Kim, H., Yeo, J. & Kim, J., *YOLOv10-based multi-scale variant object detection for multi-category PPE non-compliance monitoring on construction sites*, *Scientific Reports* (2026), DOI https://doi.org/10.1038/s41598-026-53052-y. The official publication says that the data used in the study are available from the corresponding author on reasonable request, and describes a 313-image external evaluation group; the publisher provides the corresponding author's contact details.

## Proposed English email (do NOT auto-send)

**Subject:** Research request for independent PPE violation detection validation data (Scientific Reports 2026)

Dear Professor Kim,

I am preparing a scientific study on the reliability and conditional value of a second object detector for safety-critical PPE monitoring. I read your article, *YOLOv10-based multi-scale variant object detection for multi-category PPE non-compliance monitoring on construction sites* (Scientific Reports, 2026, DOI: 10.1038/s41598-026-53052-y), and noticed that the datasets are available from the corresponding author upon reasonable request.

Would it be possible to obtain an authorized research-only copy of the external evaluation cohort (reported as 313 images), its original bounding-box labels, class ID mapping and annotation definitions? Our two existing frozen detectors use the critical-class categories **no_helmet**, **no_gloves** and **no_boots**; before any evaluation, we would need to check whether your **no_shoes** definition and box geometry genuinely correspond to missing protective safety boots rather than a different absence label. We will not silently map these classes without your clarification.

For an independent external test, anonymized identifiers of the original capture sites, camera sessions and source-image families would be particularly useful, as would any duplicate/source-overlap audit and permission information for research use. The purpose is to evaluate already-trained detectors **without fitting or selecting the new detector policy on these requested images**. We would keep original images and raw image identifiers in private authorized storage, report only aggregate performance, cite your dataset and article, and not redistribute images without consent.

If direct transfer is not possible, would you be able to suggest an accessible original source or a permitted route to request the same information? We understand that you may have restrictions concerning worker photographs and site identifiers, and we are happy to use anonymized site-group information.

Thank you for considering this research request.

Sincerely,

[Researcher name and institutional affiliation]
[Institutional contact email]

## Requested response / project gate

- [ ] Author permission and restrictions received (NO response received as of preparation).
- [ ] Source image/annotation download mechanism and hashes supplied.
- [ ] Label semantics `no_shoes` versus `no_boots` approved for a shared operating protocol, or declared incompatible.
- [ ] Per-image site/source-family independent keys supplied or unavailability disclosed.
- [ ] Original image overlap with Roboflow ALTAYYAR v2 and Ultralytics Construction-PPE comprehensively screened.
- [ ] Prospective model/threshold/statistical policy and external safety standard separately approved BEFORE scoring any new images.
- [ ] Physical wall energy obtained if and only if publication claims measured sustainability.

Do not claim this request has been sent or granted. No new external performance results exist yet.
