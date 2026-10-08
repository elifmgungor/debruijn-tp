"""Check malformed FASTQ records without changing the course tests."""
import pytest
from .context import debruijn


@pytest.mark.parametrize("contents", [
    "@read\nACGT\n+\n",
    "read\nACGT\n+\nIIII\n",
    "@read\nACGT\nseparator\nIIII\n",
    "@read\nACGT\n+\nIII\n",
])
def test_invalid_fastq(tmp_path, contents):
    fastq = tmp_path / "invalid.fq"
    fastq.write_text(contents)
    with pytest.raises(ValueError):
        list(debruijn.read_fastq(fastq))


def test_final_record_without_newline(tmp_path):
    fastq = tmp_path / "valid.fq"
    fastq.write_text("@read\nACGT\n+\nIIII")
    assert list(debruijn.read_fastq(fastq)) == ["ACGT"]
