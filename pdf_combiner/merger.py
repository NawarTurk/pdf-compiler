"""Combine configured page selections into one PDF."""

from pathlib import Path

from pypdf import PdfReader, PdfWriter

from pdf_combiner.config import MergeConfig


def merge_pdfs(
    config: MergeConfig,
    source_dir: Path,
    output_dir: Path,
) -> Path:
    """Merge selected pages in order and return the output path."""
    output_path = output_dir / config.output

    with PdfWriter() as writer:
        for selection in config.sequence:
            source_path = source_dir / f"{selection.source}.pdf"
            reader = PdfReader(source_path)

            if selection.end_page > len(reader.pages):
                raise ValueError(
                    f"{source_path.name} has {len(reader.pages)} pages; "
                    f"page {selection.end_page} was requested."
                )

            # Convert inclusive, 1-based ranges to 0-based indices.
            for index in range(
                selection.start_page - 1, selection.end_page
            ):
                writer.add_page(reader.pages[index])

        output_dir.mkdir(parents=True, exist_ok=True)

        # Exclusive creation prevents overwriting an existing file.
        with output_path.open("xb") as output_file:
            writer.write(output_file)

    return output_path