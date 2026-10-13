"""Tests for PDF merging errors."""

import pytest
from pypdf import PdfWriter

from pdf_combiner.config import MergeConfig, PageSelection
from pdf_combiner.merger import merge_pdfs


def test_requested_page_exceeds_pdf_length(tmp_path):
    source_dir = tmp_path / "pdf_store"
    output_dir = tmp_path / "output"
    source_dir.mkdir()

    with PdfWriter() as writer:
        writer.add_blank_page(width=100, height=100)
        with (source_dir / "PDF1.pdf").open("wb") as source_file:
            writer.write(source_file)

    config = MergeConfig(
        output="combined.pdf",
        sequence=(PageSelection("PDF1", 1, 2),),
    )

    with pytest.raises(ValueError, match="page 2 was requested"):
        merge_pdfs(config, source_dir, output_dir)

    assert not (output_dir / "combined.pdf").exists()