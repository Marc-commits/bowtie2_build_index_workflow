# combine_sequences.py

**Purpose**: Concatenates one or more input sequence files (FASTA or
GenBank) into the single combined FASTA that `bowtie2_build` indexes. First
step of this module's `bowtie2_build_index_workflow_all` target.

**Inputs** (`snakemake.input`): `sequences` — ordered list of file paths
(e.g. a base genome FASTA plus one or more extra replicon FASTA/GenBank
files supplied by a consuming workflow). Each path is parsed as GenBank if
its extension is `.gb`/`.gbk`/`.genbank`, else as FASTA.

**Outputs**: `fasta` — a single FASTA containing every record from every
input file, in input order.

**Data transformations**:

- Reads every record from every input file with `Bio.SeqIO.parse`, using
  `"genbank"` or `"fasta"` mode per file based on its extension.
- For GenBank inputs, only the sequence and record ID are kept — gene/CDS/
  other features are discarded. Parsing GenBank features into GFF
  annotation is out of scope for this module; that's
  `genbank_to_replicon_workflow`'s job. This module only ever produces a
  bowtie2 index from raw sequence, regardless of which format that
  sequence arrived in.
- Fails fast (`ValueError`) if any two input files contain a record with
  the same ID — a silent duplicate contig would otherwise corrupt the
  resulting bowtie2 index (ambiguous alignment target) without any error.
- Record descriptions are cleared before writing, so the combined FASTA's
  headers are always bare `>id` regardless of how verbose the source
  FASTA/GenBank header was.

**Audit**:

- Duplicate-ID detection is by record ID only (accession/locus name for
  GenBank, the first whitespace-delimited token of the header for FASTA),
  not by sequence content — two different sequences accidentally sharing
  an ID are still rejected, which is the safer failure mode for a
  reference-building step.
- Format selection is purely extension-based (`.gb`/`.gbk`/`.genbank` vs.
  everything else); a mislabeled file extension will be parsed with the
  wrong `Bio.SeqIO` mode and fail with a parse error rather than silently
  producing garbage — acceptable fail-fast behavior for this scope.
- This script is fully generic: no organism-specific or plasmid-specific
  hardcoding. It doesn't know or care what the records represent.
