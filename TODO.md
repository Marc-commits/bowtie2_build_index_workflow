# TODOs

- Consider supporting `bowtie2-build --large-index` toggle in config if a
  consumer ever needs a >4Gbp combined reference.

## Script-audit findings (from `workflow/scripts/*_README.md`, 2026-09-04)

- `combine_sequences.py` format detection is extension-only
  (`.gb`/`.gbk`/`.genbank` vs FASTA) with no content sniff — a mislabeled file
  fails with a parse error (acceptable fail-fast, but worth noting).
  `combine_sequences_README.md:39`

## Workflow audit findings (2026-09-19, see `2026-09-19_AUDIT.md`)

- [ ] Run `snakefmt` on `Snakefile` and `workflow/rules/build_index.smk`
  (2 files flagged by `--check`)
- [ ] Add `sys.stderr` redirection to `snakemake.log[0]` in
  `combine_sequences.py` (log: declared but unused)
- [ ] Regenerate `workflow/rulegraph.svg` (currently 0 bytes) and embed it
  in README
- [ ] Add README prerequisites section and pipeline-overview table
- [ ] Add `config/README.md` and an inline-commented
  `config/example.config.yaml`
- [ ] Decide: migrate `bowtie2_build` rule to the `bio/bowtie2/build`
  snakemake-wrapper (flag-and-ask, needs approval)
