# TODOs

- Consider supporting `bowtie2-build --large-index` toggle in config if a
  consumer ever needs a >4Gbp combined reference.

## Script-audit findings (from `workflow/scripts/*_README.md`, 2026-09-04)

- `combine_sequences.py` format detection is extension-only
  (`.gb`/`.gbk`/`.genbank` vs FASTA) with no content sniff — a mislabeled file
  fails with a parse error (acceptable fail-fast, but worth noting).
  `combine_sequences_README.md:39`
