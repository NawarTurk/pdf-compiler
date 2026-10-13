"""Tests for configuration validation."""

import pytest

from pdf_combiner.config import (
    MergeConfig,
    PageSelection,
    validate_config,
)


def test_valid_config():
    data = {
        "output": "combined.pdf",
        "sequence": [
            {"source": "PDF1", "pages": [1, 3]},
            {"source": "PDF2", "pages": [1, 2]},
        ],
    }

    result = validate_config(data)

    assert result == MergeConfig(
        output="combined.pdf",
        sequence=(
            PageSelection("PDF1", 1, 3),
            PageSelection("PDF2", 1, 2),
        ),
    )


@pytest.mark.parametrize("pages", [[0, 3], [5, 2]])
def test_invalid_page_range(pages):
    data = {
        "output": "combined.pdf",
        "sequence": [{"source": "PDF1", "pages": pages}],
    }

    with pytest.raises(ValueError, match="1 <= first_page <= last_page"):
        validate_config(data)