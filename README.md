# bowtie2_build_index_workflow

A small, generic Snakemake module: concatenate one or more FASTA files and
build a bowtie2 index from the result. No organism/plasmid-specific logic —
this module only knows about FASTA files and bowtie2.

## What it does

1. `combine_fastas` — concatenates `config["fastas"]` (an ordered list of
   FASTA paths) into one FASTA, failing fast on duplicate contig IDs.
2. `bowtie2_build` — runs `bowtie2-build` on the combined FASTA, producing
   the standard 6-file bowtie2 index at `config["index_name"]`.

## Usage as a standalone workflow

```bash
snakemake --use-conda --conda-frontend mamba --conda-prefix ~/.snakemake \
  --latency-wait 30 bowtie2_build_index_workflow_all
```

Edit `config/config.yaml` (`fastas`, `index_name`) first, or override on the
command line with `--config fastas='[a.fasta,b.fasta]' index_name=...`.

## Usage as a Snakemake module (git submodule)

```python
_bowtie2_module_config = {
    "fastas": ["resources/reference/base_genome.fasta", replicon_fasta],
    "index_name": "resources/bowtie2_index/combined",
}

module bowtie2:
    snakefile:
        "../../submodules/bowtie2_build_index_workflow/Snakefile"
    config:
        _bowtie2_module_config

use rule * from bowtie2 as bowtie2_*
```

Config passed to the module must be a flat dict matching the keys above —
the consuming workflow does any nesting/renaming at its own `module:`
config line, not this module.

## Tests

- `tests/` — pytest unit tests for the pure functions in
  `workflow/scripts/combine_fastas.py`.
- `.tests/unit/` — Snakemake rule-level integration tests
  (`pytest .tests/unit`), generated/maintained following
  `snakemake --generate-unit-tests` conventions.
