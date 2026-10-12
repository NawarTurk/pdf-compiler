"""Load and validate PDF merge configurations."""

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PageSelection:
    """A source PDF and an inclusive, 1-based page range."""

    source: str
    start_page: int
    end_page: int


@dataclass(frozen=True)
class MergeConfig:
    """The output filename and ordered page selections."""

    output: str
    sequence: tuple[PageSelection, ...]


def validate_config(data: object) -> MergeConfig:
    """Validate configuration data.

    Raises:
        ValueError: If the configuration has invalid fields.
    """
    if not isinstance(data, dict):
        raise ValueError("Configuration must be a JSON object.")

    output = data.get("output")
    if not isinstance(output, str) or not output.strip():
        raise ValueError("'output' must be a nonempty filename.")

    if "/" in output or "\\" in output:
        raise ValueError("'output' must be a filename without folders.")

    if not output.lower().endswith(".pdf"):
        raise ValueError("'output' must end with '.pdf'.")

    sequence = data.get("sequence")
    if not isinstance(sequence, list) or not sequence:
        raise ValueError("'sequence' must be a nonempty list.")

    selections = []

    for position, entry in enumerate(sequence, start=1):
        label = f"Sequence entry {position}"

        if not isinstance(entry, dict):
            raise ValueError(f"{label} must be an object.")

        source = entry.get("source")
        if not isinstance(source, str) or not source.strip():
            raise ValueError(f"{label}: 'source' must be nonempty text.")

        if "/" in source or "\\" in source or source in {".", ".."}:
            raise ValueError(f"{label}: 'source' must not contain a path.")

        if source.lower().endswith(".pdf"):
            raise ValueError(
                f"{label}: use the source name without '.pdf'."
            )

        pages = entry.get("pages")
        if not isinstance(pages, list) or len(pages) != 2:
            raise ValueError(
                f"{label}: 'pages' must contain [first_page, last_page]."
            )

        # Booleans are subclasses of int, but are not valid page numbers.
        if any(type(page) is not int for page in pages):
            raise ValueError(f"{label}: page numbers must be integers.")

        start_page, end_page = pages

        if start_page < 1 or end_page < start_page:
            raise ValueError(
                f"{label}: pages must satisfy 1 <= first_page <= last_page."
            )

        selections.append(
            PageSelection(
                source=source,
                start_page=start_page,
                end_page=end_page,
            )
        )

    return MergeConfig(output=output, sequence=tuple(selections))


def load_config(config_path: Path) -> MergeConfig:
    """Read a JSON configuration and return validated selections.

    Raises:
        OSError: If the configuration file cannot be read.
        ValueError: If the JSON or configuration is invalid.
    """
    try:
        data = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid JSON in {config_path}: {error.msg} "
            f"(line {error.lineno}, column {error.colno})."
        ) from error

    return validate_config(data)