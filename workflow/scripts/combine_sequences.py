"""
Concatenate one or more sequence files (FASTA or GenBank) into a single
combined FASTA, failing fast on duplicate contig/record IDs.

GenBank inputs contribute sequence only — any gene/CDS features they carry
are ignored here. Parsing GenBank features into GFF annotation is out of
scope for this module (that's genbank_to_replicon_workflow's job); this
module only ever produces a bowtie2 index from raw sequence, regardless of
which format that sequence arrived in.

Called via Snakemake script: directive. Receives paths through the snakemake
object injected at runtime.

Input (snakemake.input):
  sequences — list of file paths to concatenate, in order. Each is parsed
              as GenBank if its extension is .gb/.gbk/.genbank, else as
              FASTA.

Output (snakemake.output):
  fasta — combined FASTA (records from all inputs, in input order)
"""

from pathlib import Path

from Bio import SeqIO

GENBANK_EXTENSIONS = {".gb", ".gbk", ".genbank"}


def format_for(path: str) -> str:
    return "genbank" if Path(path).suffix.lower() in GENBANK_EXTENSIONS else "fasta"


def read_sequence_records(paths: list) -> list:
    records = []
    seen_ids = set()
    for path in paths:
        for record in SeqIO.parse(path, format_for(path)):
            if record.id in seen_ids:
                raise ValueError(
                    f"Duplicate contig id '{record.id}' found while combining "
                    f"sequence files: {paths}"
                )
            seen_ids.add(record.id)
            record.description = ""
            records.append(record)
    return records


def write_combined_fasta(records: list, output_path: str) -> None:
    SeqIO.write(records, output_path, "fasta")


# snakemake object is injected by the script: directive at runtime
records = read_sequence_records(list(snakemake.input.sequences))  # noqa: F821
write_combined_fasta(records, str(snakemake.output.fasta))  # noqa: F821
