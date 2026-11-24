# V40-R4 — Publication declarations, Elsevier policy and release-gate audit
**Date:** 24 November 2026. **Target:** Results in Engineering. **Status:** working-source audit only; not an approval, legal opinion, ethics determination or submission authorization. No institutional contact, portal action, Zenodo deposit, rights transfer or final package was performed.

## Executive decision
Do **not** remove the internal release notes yet and do not produce a clean submission package. Several conditions that those notes identify remain genuinely unresolved. Removing the labels without completing the actions would create false assurance. The working manuscript was updated only where new evidence supports a more accurate factual record (Roboflow Research Plan support, AI-use inventory, and explicit figure-identifier/privacy warning). Pending gates remain visible in the internal working sources.

## Current Elsevier policy basis checked 24 Nov 2026
1. Generative AI: Elsevier requires a separate manuscript-preparation declaration naming the tool, purpose and extent of oversight; AI use in the research process belongs in Methods. The author remains accountable for checking accuracy, sources, privacy, rights and final content. For explanatory images, AI use is permitted subject to human oversight and disclosure in each caption, including tool, version and how it was used. AI use in data visualizations must remain directly derived from underlying data and reproducible, with tool/model/version/developer disclosed in Methods. General-purpose generative AI must not be used for graphical abstracts. Official policy: https://www.elsevier.com/about/policies-and-standards/generative-ai-policies-for-journals
2. Human research and images: Elsevier requires appropriate institutional approval for studies involving human participants and their data, or an explicit explanation of exemption/non-applicability and safeguards. Informed consent and consent for publication apply as relevant; identifiable photographs/images require written permissions/releases, and vulnerable populations (including children) require appropriate safeguards, legal-representative permissions and assent where applicable. Official policy: https://www.elsevier.com/about/policies-and-standards/research-ethics
3. Authorship, CRediT, funding and conflicts: significant contributors must be included; the corresponding author must ensure appropriate authorship and final approval. CRediT records contributions but does not determine authorship eligibility. Funding and sponsor roles must be disclosed, as must relevant financial/personal relationships. Official sources: https://www.elsevier.com/about/policies-and-standards/publishing-ethics and https://www.elsevier.com/researcher/author/policies-and-guidelines/credit-author-statement
4. Data statement: Elsevier describes data statements and asks authors to check the selected journal's Guide for Authors for the journal-specific requirements: https://www.elsevier.com/en-gb/researcher/author/tools-and-resources/research-data/data-statement
5. The live Results in Engineering Guide for Authors endpoint returned HTTP 403 in this review. The journal-specific article type, declarations fields and exact submission-file requirements therefore remain unverified; generic Elsevier guidance is not substituted for the journal's own guide.

## Source audit — internal markers found
| Working file | Current internal marker / issue | Closure evidence required before clean copy |
|:--|:--|:--|
| Main manuscript, Methods | Historical AI/code sessions do not have complete version/date logs; exact version was not consistently retained. Figure 4 caption identifies ChatGPT GPT-6.2. | Author to verify the activity inventory, review all AI-assisted text/code/visuals, and approve final declaration. Do not claim review has happened until it has. |
| Main manuscript, ethics/permissions paragraph | Institutional determination, minor safeguards, individual/legal-representative and organization/project permissions remain open. | Written determination from competent institutional authority; source-specific rights/permission evidence and scope. |
| Main manuscript, Data availability | Zenodo is intended but no deposit or DOI exists. | Rights/privacy audit, deposit only approved materials, test public access, insert actual DOI. |
| Main manuscript, Code availability | Public working repository has no explicit LICENSE file. | Author selects and approves code/data licensing; pin environment and create a sanitized immutable release. |
| Main manuscript, prior dissemination | Four related papers were screened for scientific scope; full thesis/other dissemination and exact text/figure reuse review remain open. | Compare thesis, preprints, conference papers, reports and figure/text reuse; author approves the accurate overlap statement. |
| Main manuscript, AI declaration | Author has authorized disclosure, but the author's final human review/edit and responsibility confirmation are not yet recorded. | Author must read and edit the full final manuscript, code-generated results, references and figures, then explicitly approve responsibility. |
| Cover letter | “NOT FOR SUBMISSION YET” and internal release gate remain. | Remove only after all scientific, ethical, rights, data, metadata and author-approval gates close. |
| Title page | HTML working-source comment remains. Author-supplied ORCID checksum is valid, but account ownership/linkage is unverified; email has not been compared with Editorial Manager. | Author logs in to ORCID and links/claims the correct profile; verify corresponding email in the actual portal; confirm final address and roster. |
| Supplement S1 | Working status, privacy-safe renderer and author/right sign-off notes remain. | Generate pseudonymized publication PDFs, visually inspect all ten maps, verify links and obtain release approval. |
| Supplement S2 | DOI and privacy/license clearance remain pending. | Use actual approved archive DOI; verify that all data are licensed and non-identifying. |

## What is now evidenced or improved
### Author and affiliation
- Working metadata records one author/corresponding author, the author-confirmed institutional affiliation, email and ORCID. These are author attestations, not independent account/portal verification.
- Official Taiz University pages use “Faculty of Engineering and Information Technology”: https://academic.taiz.edu.ye/en/DEFAULTDET.ASPX?SUB_ID=30449&pnc=235 and https://cc.taiz.edu.ye/control/uploads/EngFawziAlQahtani/CollegeGuide.pdf
- Postal-address discrepancy: the university-level directory lists one P.O. Box, while an official Faculty of Engineering document lists a different faculty-level P.O. Box: https://whed.net/detail_institution.php?Jzo2MF0tQzRWLGBgYApgCg=%3D and https://taiz.edu.ye/control/uploads/EngFawzi/ConditionsForAdmissiontoMasters.pdf. The current title page address is provisional. Do not silently choose one; author confirmation is required.
- No access to the author's Editorial Manager account or ORCID sign-in was available. Portal match and ORCID ownership are **not verified**.

### Authorship and CRediT
- The author has attested to sole authorship and selected 11 CRediT roles: Conceptualization, Formal analysis, Investigation, Methodology, Software, Validation, Visualization, Resources, Project administration, Writing – original draft, and Writing – review & editing.
- The CRediT list is not itself proof of authorship eligibility. The author must ensure that no person who significantly contributed to the conception, design, execution or interpretation of this particular article has been omitted, including prior collaborators who may have contributed to reused data/model resources. Prior authors are not automatically co-authors merely because their earlier work is reused.
- Final author approval is still pending.

### Funding and competing interests
- The author states that the research was self-funded and received no specific research grant.
- An author-supplied Roboflow screenshot documents a Research Plan with 50 monthly included credits for the 1 Nov–1 Dec 2026 cycle, 2.49 credits used, zero prepaid balance and zero estimated Flex usage. This supports describing hosted inference access as non-cash platform/computational support, not a cash grant. The screenshot does not establish the provider's role beyond hosting the inference service.
- The manuscript funding statement has been corrected from the ambiguous “free research plan or granted credits” wording to the specific Research Plan evidence. The author must confirm the sponsor-role statement. The Roboflow support must also be entered accurately in the Elsevier declaration-of-interests workflow.
- The author reports no known competing interests. The actual publisher declaration tool has not been completed.
- The author reports no acknowledgements; omission is acceptable if no one merits acknowledgement.

### Ethics, minors and image permissions
- No institutional ethics approval/exemption/determination reference is present. The draft request to Taiz University is **not sent**. No institutional determination can be supplied or inferred by the assistant.
- The frozen M0 record contains 31 annotations labelled Child across 22 images. This is not 31 unique children and does not verify ages, identities, employment or child labour. The category is sufficient to require a careful institutional assessment of the image corpus, applicable local law, legal-representative permissions, assent where applicable, privacy and public release.
- The author attests that publication permissions exist for photographs and depicted persons, but permission documents and exact scope have not been inspected. The author has separately reported taking Case C while working as a field engineer; the same image was also published by PWP. The PWP source/right chain and any organization/project restrictions remain unresolved. Do not equate a general attestation, publication on a website, or a dataset license badge with proof of all research-use, publication, derivative-map and public-redistribution rights.
- Current sampled article figures are data plots/heatmaps rather than worker photographs. This does not by itself resolve whether the underlying retrospective human-image data use requires institutional review or consent.

### Figure privacy and public repository exposure
- Inspected the current main Figure 1 and a representative Supplementary Figure S1 directly. They do not display a worker photograph, but Figure 1 visibly includes Roboflow image IDs and S1 includes a target UUID. Figure 2 and Figure 3 are aggregate plots.
- The existing offline candidate renderer research/seer-ppe/tools/render_v40_publication_artwork_candidate.py was specifically designed to replace raw image/target IDs with pseudonymous aliases and render Figure 1 plus S1–S10 PDFs. It has not been executed; the artwork-publication directory currently contains only the Figure 4 SVG. The current manuscript points to the old V34B Figure 1 image. The publication figure links therefore remain unresolved.
- The GitHub repository is **public**. At the audited commit it contained 751 tracked files, including 31 DOCX files, two ZIP archives, 37 PNGs, one SVG and two PDFs; no LICENSE/LICENCE/COPYING file exists anywhere in the tracked tree. The working branch includes internal/unsigned drafts and source/target identifiers. Two archives and embedded DOCX media were not exhaustively inspected for embedded photographs or identifying material. Therefore the current repository is not a clean public data release and must not be cited as the sanitized archive.
- No standalone raw JPEG/PNG source photographs were found among the tracked image files; this does not prove that no photo is embedded in DOCX/ZIP files. A full embedded-media audit remains open.
- No Zenodo deposit, DOI, final public release or code/data license exists. Do not upload raw photographs, consent records, person-level information or source identifiers. Do not apply MIT/CC BY or another license without author approval and rights clearance.

## Changes made in this R4 pass
1. Main Methods AI-use record: removed unsupported bracketed requests for unknown model versions/dates and documented the known tool purposes; explicitly says historical version identifiers were not consistently retained. This does not substitute for author review.
2. Main ethics/permissions paragraph: explicitly records that the current working Figure 1 and S1 contain identifiers and are not cleared publication artwork; preserves the genuine institutional/rights gate.
3. Main Funding statement: replaced ambiguous plan-or-credits wording with the screenshot-supported Research Plan and 50 monthly included credits; described it as non-cash platform support.
4. Title-page internal comment: flags the university-versus-faculty postal-address discrepancy, unverified ORCID ownership and portal metadata.
5. No internal release gate was deleted, no cover letter or supplement was declared clean, and no final submission/Zenodo package was created.

## Required closure sequence
1. **Institutional ethics:** submit the prepared determination request to the competent Taiz University authority; obtain the written determination and conditions, especially for potential minors. No approval/exemption wording until the institution supplies it.
2. **Rights:** privately assemble source-specific permission records, legal-representative permissions/assent where applicable, and organization/project permission. Resolve the PWP-published Case C rights chain. Exclude any source that cannot be cleared or obtain appropriate rights before reuse.
3. **Privacy/artwork:** run the pseudonymous renderer; replace Figure 1 and S1–S10 aliases in the article source; inspect all figures and all embedded DOCX/ZIP media. Ensure no source IDs, target UUIDs, identifiable photos, personal records or consent documents are in the release.
4. **Archive/licensing:** choose explicit code and data licenses only for material the author owns or can license; pin dependencies; build a sanitized archive; deposit and test the DOI. The public working repo is not the archive.
5. **Author metadata and authorship:** author verifies ORCID ownership/link, portal email, correct faculty postal address, sole-author eligibility and the 11 CRediT roles; resolve whether any prior collaborator contributed substantially to this article.
6. **Declarations:** complete Elsevier Declaration of Interests form, funding/support role, ethics/consent statements and data statement; keep acknowledgements omitted if none.
7. **AI and final approval:** author reviews all AI-assisted text, code, citations, figure captions and final outputs; corrects anything necessary; confirms final responsibility and submission approval.
8. **Clean files:** only after steps 1–7, create final clean manuscript, title page, cover letter, S1/S2, Highlights and figure files; run the final Word/PDF/portal proof. Remove working comments and internal gates only when each has documentary closure.

## Current disposition
**HOLD — not ready for submission.** The scientific text is being improved, but institutional ethics, rights/permissions, privacy-safe artwork, immutable data deposit/license, author/portal verification and final human approval remain open. This report is internal and must not be uploaded as a journal file.
