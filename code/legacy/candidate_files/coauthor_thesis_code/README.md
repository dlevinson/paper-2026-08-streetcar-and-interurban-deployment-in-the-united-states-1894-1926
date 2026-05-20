# Coauthor Thesis Code And Provenance

This folder contains the local thesis-derived code/provenance evidence for the paper:

Li, Haoang, Bahman Lahoorpoor, and David Levinson. 2026. "Streetcar And Interurban Deployment In The United States: 1894-1926." Findings. https://doi.org/10.32866/001c.155283

The source is Haoang Li's 2021 University of Sydney Honours thesis:

Li, Haoang. 2021. "Streetcars Across America: An Analysis of the Growth and Decline of Electric Urban Railways in the United States from Directory Data." Honours thesis, University of Sydney. Public handle: https://hdl.handle.net/2123/27119

## Contents

- `../../../../documentation/legacy_context/coauthor_thesis/Haoang_Li_Thesis_Streetcars_doc.pdf`: local copy of the thesis PDF used as provenance evidence.
- `source_tex/methods.tex`: thesis methods text describing ABBYY OCR, McGraw/HathiTrust source directories, regex/string extraction, manual post-processing, validation, and S-curve modelling.
- `source_tex/appendixD.tex`: abbreviated annotated code in the thesis appendix.
- `source_tex/appendixE.tex`: full code appendix from which the extracted code files were generated.
- `source_tex/thesis.tex` and `source_tex/thesis.bib`: thesis source context and bibliography.
- `extracted_code/appendixE_01_extract_1894_1914.py`: verbatim extraction of Appendix E's 1894-1914 code block.
- `extracted_code/appendixE_02_extract_1917_1926.py`: verbatim extraction of Appendix E's 1917-1926 code block.
- `extracted_code/appendixE_03_fit_s_curve_model.py`: verbatim extraction of Appendix E's S-curve model code block.
- `cleaned_code/appendixE_01_extract_1894_1914.py`: cleaned copy of the first Appendix E code block with thesis-formatting indentation repaired.
- `cleaned_code/appendixE_02_extract_1917_1926.py`: cleaned copy of the second Appendix E code block with regex strings made warning-free.
- `cleaned_code/appendixE_03_fit_s_curve_model.py`: cleaned copy of the S-curve model code block.
- `validation_workbook/ComparisonWithStudentsWork.xlsm`: workbook comparing machine-extracted results with student hand-extracted validation values.

## Code Status

The Appendix E Python files are archival transcripts extracted verbatim from the thesis LaTeX `lstlisting` blocks. They document the authored OCR/string-extraction and modelling workflow, but they are not a modern standalone reproduction pipeline. They require the original preprocessed OCR text files, intermediate yearly index CSVs, manual corrections described in the thesis, and historical Python dependencies such as `pandas`, `numpy`, `matplotlib`, `fuzzywuzzy`, `us`, and `statsmodels`.

`python3 -m py_compile` was run on the verbatim extracted files on 2026-05-13. The first verbatim extracted file fails compilation because the thesis listing has indentation damaged by the typeset appendix. The `cleaned_code/` copies repair that indentation issue and normalize regex string literals; all three cleaned files pass `python3 -m py_compile`.

The cleaned files still require the original preprocessed OCR text files, intermediate yearly index CSVs, manual corrections described in the thesis, and Python dependencies. They should be treated as lightly repaired archival code, not a fully modernized standalone reproduction pipeline.

## Exclusions

The raw McGraw/HathiTrust directories and OCR text extracts are not included here. They are public source/intermediate materials and should be cited rather than re-hosted. The archive target is the derived streetcar/interurban dataset plus thesis-provenance code and validation materials.
