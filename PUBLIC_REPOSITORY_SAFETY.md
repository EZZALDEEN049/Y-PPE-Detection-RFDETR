# Public repository safety and reproducibility guidance

This branch is for **source code and generic reproducibility tooling only**. It does not contain the submission manuscript, reviewer materials, research images, datasets, experiment results, model weights, or other unpublished submission files.

## Data-handling policy

- Keep final manuscript files (Word/PDF), journal cover letters, peer-review responses, and submission ZIP archives **off this public repository**.
- Keep raw and harmonized research images and annotations, trained weights, detailed test results, and any restricted data in separately controlled private storage.
- Do not place Google Drive folder IDs, private share links, access credentials, personal data, or secrets in public commits.
- The project's existing research scripts can be used locally when licensed data are available.
- Preserve a private offline snapshot of the exact code revision, file manifests, software versions, and dataset checksums for reviewer requests.
- Git ignore rules provide convenience, **not a security boundary**. Always inspect files before committing, and never use `git add -f` for confidential artifacts.
- Historical branches may already include draft materials; changing this branch does not erase them or remove their commit history.

## Before every public push

Run `git diff --cached --name-only` and verify that every staged file is safe for public release. Review `git diff --cached` for private links, credentials, unpublished text, or extracted experimental results. If in doubt, do not push.

## Release readiness

A privately stored submission package and reviewer data package are separate deliverables, and are not represented as uploaded here. This branch makes **no claim** that a complete, publicly downloadable dataset or paper is available.
