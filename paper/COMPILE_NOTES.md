# Compile notes

Drafted on 2026-06-30 inside the Codex desktop workspace.

The paper source is `main.tex` and the bibliography is `references.bib`. The CAISc style file was copied from `draft-format/caisc_2026.sty`.

Local TeX tooling check:

- `pdflatex`: missing
- `xelatex`: missing
- `lualatex`: missing
- `latexmk`: missing
- `tectonic`: missing
- `pandoc`: missing

Because no local LaTeX compiler is installed, `main.pdf` was generated with the bundled Python/reportlab PDF runtime as a fallback viewing PDF. This is transparent in the paper appendix. If a TeX distribution is available later, rebuild the true LaTeX PDF from this folder with:

```powershell
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

The fallback PDF is intended to preserve the paper content for review, but the `.tex` file is the canonical paper source.
