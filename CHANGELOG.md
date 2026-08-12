# Changelog

All notable changes to this project will be documented in this file.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added (Unreleased)

- `justfile`: added a `version-map:` recipe to (re)generate
  `.version-map` via `grep` over tracked files.

### Fixed

- `bowtie2_build_index_workflow_all` docstring no longer recommends that
  consuming workflows bypass this aggregate rule; it previously endorsed
  depending on `bowtie2_build`'s output directly, which broke the intended
  `parent_all -> submodule_all -> rule` dependency hierarchy for consumers.

## [0.1.0] - 2026-07-30

### Added

- Initial release: `combine_fastas` + `bowtie2_build` rules, packaged as a
  reusable Snakemake `module:` (git submodule), consumed first by
  `genbank_to_replicon_workflow`.
