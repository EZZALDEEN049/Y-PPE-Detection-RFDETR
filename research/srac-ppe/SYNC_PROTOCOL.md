# Synchronization and public-data policy

**Canonical progress file:** [PROJECT.md](PROJECT.md).  
**Append-only milestones:** [RESEARCH_LOG.md](RESEARCH_LOG.md).  
**Paper-section map:** [MANUSCRIPT_PROGRESS.md](MANUSCRIPT_PROGRESS.md).

## Update trigger
Update this folder after a **verified change in research state**, such as new audited data, executable model inference, reviewed worker labels, calibrated results, baseline experiments, methodological corrections or manuscript readiness changes.

For each update:
1. Read the current `PROJECT.md` and `RESEARCH_LOG.md` from GitHub, including their current blob SHAs.
2. Verify the new evidence directly (dataset, code/test output, model run, or source).
3. Update the current status and *append* a dated entry to the log, noting what was and was not done.
4. Create a Git commit with a meaningful message and reread the committed files.
5. Never overwrite verified previous findings with speculative plans.
6. If nothing verifiable changed, do **not** commit a cosmetic timestamp update.

## Scope and source of truth
- GitHub status is a versioned ledger, not a live mirror of ChatGPT sessions.
- New chat progress enters GitHub only through an **explicit write or a successfully configured scheduled update**. It is not pushed merely by having a conversation.
- Check for other collaborators' edits before writing, and do not rewrite unrelated repository files.
- Label states `VERIFIED`, `DRAFT`, `PLANNED`, `BLOCKED`, or `REJECTED` without ambiguity.

## Privacy, research integrity and publication
This is a **public repository**. Never commit:
- Full unpublished manuscript text without explicit publication preference/authorization;
- Private site photographs, identity-linked worker annotations, personal records, confidential correspondence;
- Roboflow/API credentials, tokens or local secrets;
- Unreleased model weights, private datasets or copyrighted third-party binaries;
- Unvalidated numeric results represented as validated findings.

Keep manuscript content and controlled datasets in authorized restricted storage. Public log contains only reproducible, non-sensitive metadata and verified research status.

## Reproducibility gates
A numerical result must state: source dataset/version, training split provenance, independent data/scene groups, detector/checkpoint version, thresholds, label ontology and PPE requirement, sample size (particularly true violations), calibration/test separation, seeds if applicable, confidence procedure, and code/commit/run identity.

**Active scheduled check:** On 2026-10-29, the researcher-requested daily ChatGPT automation `مزامنة تقدم SRAC-PPE` was created and enabled (automation ID `6ae292cd4b0c81919eaad46af1b6faa1`). It checks for *new verified project evidence* and attempts GitHub updates only when there is a substantive change. It is not instant event streaming, and a scheduled run's ability to read future project context/perform writes must still be checked from its actual run logs. No progress means no new commit.
