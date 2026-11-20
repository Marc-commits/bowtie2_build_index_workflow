# Changelog

All notable changes to this project will be documented in this file.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Changed (Unreleased)

- `.pre-commit-config.yaml`: `Marc-commits/pre-commit-hooks` bumped from v0.3.3
  to v0.10.0; new `snakemake-config-validate` hook validates the config files
  against `workflow/schemas/config.schema.yaml` at commit time.
- Bumped pre-commit-hooks to v0.11.0: `snakedeploy-pin-conda-envs` is now
  manual-stage only (no pin drift on commits); run `just pin-env`.

### Added (Unreleased)

- `just config-validation` (also a dependency of `just lint`): validates
  `config/config.yaml` against `workflow/schemas/config.schema.yaml` with
  `check-jsonschema` (via `uvx`), reporting all errors at once without parsing
  the workflow.

## [0.2.0] - 2026-11-20

### Added (0.2.0)

- `workflow/schemas/config.schema.yaml` and a `validate()` call in the
  `Snakefile`: `sequences` and `index_name` are now checked at parse time,
  including when the workflow is used as a module. `tests/test_config_schema.py`
  keeps schema and `config/config.yaml` keys in sync.
- `justfile`: added `env:`/`lint:` recipes to dry-run validate
  `workflow/envs/*.yaml` conda envs and lint the Snakemake workflow.
- `justfile`: added a `version-map:` recipe to (re)generate
  `.version-map` via `grep` over tracked files.

### Changed

- `bowtie2_build`: removed the `benchmark:` directive. Snakemake does not
  allow a rule with a benchmark to be cache-eligible
  ([snakemake#2238](https://github.com/snakemake/snakemake/issues/2238)), so
  this lets consuming workflows opt in to between-workflow caching with
  `use rule bowtie2_build from ... with: cache: True`. `combine_sequences`
  keeps its benchmark.
- Rulegraph regeneration moved from `.envrc` into the justfile recipe
  `just chore`; direnv no longer rewrites `workflow/rulegraph.svg` on `cd`.

### Fixed

- `bowtie2_build_index_workflow_all` docstring no longer recommends that
  consuming workflows bypass this aggregate rule; it previously endorsed
  depending on `bowtie2_build`'s output directly, which broke the intended
  `parent_all -> submodule_all -> rule` dependency hierarchy for consumers.
- justfile rulegraph recipes no longer discard snakemake stderr and now fail
  on pipeline errors (`pipefail`), so a failed rulegraph is reported.

## [0.1.0] - 2026-07-30

### Added

- Initial release: `combine_fastas` + `bowtie2_build` rules, packaged as a
  reusable Snakemake `module:` (git submodule), consumed first by
  `genbank_to_replicon_workflow`.
