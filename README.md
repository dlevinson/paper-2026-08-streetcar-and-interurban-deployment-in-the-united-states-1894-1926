<!-- Updated by Codex targeted correction on 2026-05-13 -->
# Streetcar And Interurban Deployment In The United States: 1894–1926

## Bibliographic Information

- Row ID: `paper-2026-08`
- Year: 2026
- Authors: Li, Lahoorpoor, Levinson
- Venue: Findings (2026)
- DOI/URL: 10.32866/001c.155283
- Citation: Li, Lahoorpoor, Levinson. (2026). Streetcar And Interurban Deployment In The United States: 1894–1926. Findings (2026). 10.32866/001c.155283

## Archive Status

- Workbench state: `ready_to_upload`
- Audit upload action: `derived_only_candidate`
- Rights status: `likely_clear_with_provenance`
- Controlled access status: `none`
- Human subjects status: `no`
- Asset match status: `exact_match`
- Audit timestamp: 2026-05-13 14:33:48
- Preflight state: `ready_for_draft_package`
- Preflight boundary: Derived tables/data/code plus provenance README; exclude raw third-party, publisher, restricted, or unresolved source materials.
- Decision: package the derived streetcar/interurban data files plus Haoang Li thesis-derived code/provenance and validation workbook. Do not hydrate or archive raw McGraw/HathiTrust directories or McGraw OCR/text extracts; cite those public sources instead.
- Note: the `Preflight` fields are a historical snapshot from initial staging; the current authoritative lane/status for release decisions is the `Package Hardening Status` block at the end of this README.

## Public Archive Or Source Pointers

- The coauthor Honours thesis is public at the University of Sydney repository handle: https://hdl.handle.net/2123/27119
- The published Findings article is public at https://doi.org/10.32866/001c.155283 and is licensed CC BY-SA 4.0 on the Findings page.
- HathiTrust and McGraw source directories are public/source evidence only and are not re-hosted here.
- McGraw OCR/text extracts are treated as intermediate products, not archive targets.

## Local Workbench Contents

- `candidate_files/copied_candidates/streetcar-data-summarised`: Author-derived streetcar summary dataset copied as a candidate package boundary.
- `code/legacy/candidate_files/coauthor_thesis_code`: Haoang Li thesis source excerpts, Appendix E code extracted from thesis `lstlisting` blocks, lightly cleaned compile-checked code copies, and the validation workbook comparing machine extraction with student hand-extracted values.
- `documentation/legacy_context/coauthor_thesis/Haoang_Li_Thesis_Streetcars_doc.pdf`: local thesis PDF copy used as provenance evidence; the public repository handle is listed above.
- `data/STREETCAR_PACKAGE_MANIFEST.csv`: package manifest with SHA-256 hashes for included data/code/provenance files.

## Exclusions And Non-Copied Evidence

- `/Users/dlev2617/Dropbox (Sydney Uni)/Streetcars`: Evidence/supporting context only, not a package candidate.
- `/Users/dlev2617/Dropbox (Sydney Uni)/CIVL 5703 - HWA1 Source Data`: Public source or OCR/intermediate material; cite, do not re-host.
- `Dropbox metadata /David Levinson/Streetcars/Source Documents/~McGraw electric railway manual - the red book of American street railway investment`: Source does not exist locally.

## Packaging Notes

- The thesis methods text states that Appendix D contains abbreviated annotated Python and Appendix E contains the full unannotated extraction code plus S-curve modelling code.
- The verbatim extracted Appendix E Python files are archival transcripts. A separate `cleaned_code/` directory repairs the thesis-formatting indentation issue and regex string warnings; all three cleaned files pass `python3 -m py_compile`.
- The cleaned files still require the original preprocessed OCR text files, intermediate yearly index CSVs, manual corrections described in the thesis, and historical Python dependencies. They are lightly repaired archival code, not a fully modernized standalone reproduction pipeline.
- Raw McGraw/HathiTrust scans and OCR text extracts are intentionally excluded. They are public source/intermediate materials, not the archive target.
- This package is ready for upload review as a derived-data/provenance package, with the caveat that the code is preserved as thesis-derived archival code rather than a modern turnkey pipeline.

Generated: 2026-05-13 14:33:48
## Linked Data Crosswalk Update

<!-- linked-data-crosswalk-note:start -->
- Updated: 2026-05-15 19:33:06 AEST
- Crosswalk status: `VERIFIED-CONFIRMED_PATH_REBOUND`; confidence: `high_after_source_check`.
- Confirmed or reconciled source path(s): `{DROPBOX_DATA}/Streetcars` -> `/Users/dlev2617/Sydney Uni Dropbox/David Levinson/Streetcars` (exists)
- Logical check: The paper is the US streetcar/interurban deployment paper; the Dropbox-root Streetcars folder contains McGraw/manual source documents plus derived master sheets and data_the_big_one.csv in Streetcar Data Summarised.
- Package implication: Keep READY-TO-UPLOAD/PUBLIC, but document that public McGraw/Hathi-style source PDFs/texts do not need re-archiving; the derived dataset and authored scripts/README are the archive boundary.
- Release boundary: Public derived-data/code package; external public source documents by pointer only.
- Remaining work: Confirm final derived-data variables/provenance and ensure any OCR/text extracts are treated as intermediate unless needed to reproduce the derived dataset.
<!-- linked-data-crosswalk-note:end -->



<!-- published-paper-reference:start -->
## Published Paper Reference

- Official published source: https://findingspress.org/article/155283-streetcar-and-interurban-deployment-in-the-united-states-1894-1926
- Official PDF/source link: https://findingspress.org/article/155283.pdf
- Paper-reference note: Findings records the article as published in February 2026 with DOI 10.32866/001c.155283 and public supplemental files.
<!-- published-paper-reference:end -->

<!-- package-hardening-status:start -->
## Package Hardening Status

Generated: 2026-05-22 06:51:10 AEST

- Pipeline: `READY-TO-UPLOAD/PUBLIC`
- Sidecars added/updated: `PACKAGE_STATUS.md`, `PACKAGE_MANIFEST.csv`, `LICENSE_STATUS.md`.
- Paper reference copies are for local audit convenience and are not public-upload assets without rights review.
- Final GitHub upload should use the manifest include statuses and the license-status note.
<!-- package-hardening-status:end -->
