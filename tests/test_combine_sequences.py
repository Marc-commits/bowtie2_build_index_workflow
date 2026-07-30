"""Unit tests for pure functions in workflow/scripts/combine_sequences.py."""

from pathlib import Path

import pytest
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

SCRIPT = Path(__file__).parent.parent / "workflow" / "scripts" / "combine_sequences.py"


def _load_functions():
    """Exec only the function definitions from the script (stop before snakemake calls)."""
    src = SCRIPT.read_text()
    cutoff = src.find("# snakemake object is injected")
    fn_src = src[:cutoff] if cutoff != -1 else src
    ns: dict = {}
    exec(compile(fn_src, str(SCRIPT), "exec"), ns)
    return ns


@pytest.fixture(scope="module")
def fns():
    return _load_functions()


def _write_fasta(path: Path, records: list) -> Path:
    with open(path, "w") as fh:
        for rec_id, seq in records:
            fh.write(f">{rec_id}\n{seq}\n")
    return path


def _write_genbank(path: Path, rec_id: str, seq: str) -> Path:
    record = SeqRecord(Seq(seq), id=rec_id, name=rec_id, description="test plasmid")
    record.annotations["molecule_type"] = "DNA"
    SeqIO.write([record], str(path), "genbank")
    return path


def test_format_for_detects_genbank_extensions(fns):
    f = fns["format_for"]
    assert f("plasmid.gb") == "genbank"
    assert f("plasmid.GBK") == "genbank"
    assert f("plasmid.genbank") == "genbank"
    assert f("plasmid.fasta") == "fasta"
    assert f("plasmid.fa") == "fasta"


def test_read_sequence_records_concatenates_in_order(fns, tmp_path):
    f = fns["read_sequence_records"]
    fasta_a = _write_fasta(tmp_path / "a.fasta", [("chr1", "ACGT")])
    fasta_b = _write_fasta(tmp_path / "b.fasta", [("plasmid1", "TTTT"), ("plasmid2", "GGGG")])
    records = f([str(fasta_a), str(fasta_b)])
    assert [r.id for r in records] == ["chr1", "plasmid1", "plasmid2"]
    assert str(records[0].seq) == "ACGT"


def test_read_sequence_records_rejects_duplicate_ids(fns, tmp_path):
    f = fns["read_sequence_records"]
    fasta_a = _write_fasta(tmp_path / "a.fasta", [("chr1", "ACGT")])
    fasta_b = _write_fasta(tmp_path / "b.fasta", [("chr1", "TTTT")])
    with pytest.raises(ValueError, match="Duplicate contig id 'chr1'"):
        f([str(fasta_a), str(fasta_b)])


def test_read_sequence_records_parses_genbank_sequence_only(fns, tmp_path):
    f = fns["read_sequence_records"]
    gb = _write_genbank(tmp_path / "plasmid.gb", "pSAM301", "ACGTACGTACGT")
    records = f([str(gb)])
    assert records[0].id == "pSAM301"
    assert str(records[0].seq) == "ACGTACGTACGT"
    assert records[0].description == ""


def test_read_sequence_records_mixes_fasta_and_genbank(fns, tmp_path):
    f = fns["read_sequence_records"]
    fasta_a = _write_fasta(tmp_path / "a.fasta", [("chr1", "ACGT")])
    gb = _write_genbank(tmp_path / "plasmid.gb", "pSAM301", "TTTTGGGG")
    records = f([str(fasta_a), str(gb)])
    assert [r.id for r in records] == ["chr1", "pSAM301"]


def test_write_combined_fasta_roundtrip(fns, tmp_path):
    read_f = fns["read_sequence_records"]
    write_f = fns["write_combined_fasta"]
    fasta_a = _write_fasta(tmp_path / "a.fasta", [("chr1", "ACGTACGT")])
    records = read_f([str(fasta_a)])
    out_path = tmp_path / "combined.fasta"
    write_f(records, str(out_path))
    content = out_path.read_text()
    assert ">chr1" in content
    assert "ACGTACGT" in content
