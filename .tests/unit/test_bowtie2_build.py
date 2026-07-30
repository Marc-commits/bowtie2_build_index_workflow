import shutil
import sys
import tempfile
from pathlib import Path
from subprocess import check_output

sys.path.insert(0, str(Path(__file__).parent))

RULE = "bowtie2_build"
data_path = Path(__file__).parent / RULE / "data"
SNAKEFILE = Path(__file__).parent.parent.parent / "Snakefile"

# bowtie2-build output is a binary index (not byte-stable to hand-compare
# across bowtie2 versions/platforms the way a plain-text OutputChecker
# fixture would need), so this checks existence + that bowtie2-inspect can
# read the built index back out, mirroring the pragmatic non-deterministic-
# output style used by the parent workflow's own test_bowtie2.py.
INDEX_EXTS = [".1.bt2", ".2.bt2", ".3.bt2", ".4.bt2", ".rev.1.bt2", ".rev.2.bt2"]


def test_bowtie2_build(conda_prefix):
    with tempfile.TemporaryDirectory() as tmpdir:
        workdir = Path(tmpdir)
        shutil.copytree(data_path, workdir, dirs_exist_ok=True)
        shutil.copytree(Path(__file__).parent / RULE / "config", workdir / "config")
        targets = [f"results/index/test{ext}" for ext in INDEX_EXTS]
        check_output(
            [
                "snakemake",
                *targets,
                "--snakefile",
                str(SNAKEFILE),
                "--forceall",
                "--notemp",
                "--use-conda",
                "--conda-prefix",
                str(Path.home() / ".snakemake/conda"),
                "--allowed-rules",
                RULE,
                "--cores",
                "4",
                "--configfile",
                str(workdir / "config" / "config.yaml"),
                "--directory",
                str(workdir),
            ]
            + conda_prefix
        )
        for ext in INDEX_EXTS:
            assert (workdir / "results" / "index" / f"test{ext}").exists()
        names = check_output(
            ["bowtie2-inspect", "-n", str(workdir / "results" / "index" / "test")],
            text=True,
        )
        assert "chr1" in names
        assert "plasmid1" in names
        assert "plasmid_gb" in names
