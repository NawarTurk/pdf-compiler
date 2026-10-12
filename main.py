"""Run the PDF combiner."""

from pathlib import Path

from pdf_combiner.config import load_config
from pdf_combiner.merger import merge_pdfs


def main() -> None:
    """Load the configuration and generate the combined PDF."""
    project_dir = Path(__file__).resolve().parent

    config = load_config(project_dir / "sequence.json")
    result = merge_pdfs(
        config,
        source_dir=project_dir / "pdf_store",
        output_dir=project_dir / "output",
    )
    print(f"Created: {result}")


if __name__ == "__main__":
    main()