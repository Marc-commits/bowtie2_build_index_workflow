"""config.schema.yaml accepts config/config.yaml and rejects malformed configs."""

from pathlib import Path

import pytest
import yaml
from jsonschema import ValidationError, validate

ROOT = Path(__file__).parent.parent
SCHEMA = yaml.safe_load((ROOT / "workflow" / "schemas" / "config.schema.yaml").read_text())
CONFIG = yaml.safe_load((ROOT / "config" / "config.yaml").read_text())


def test_default_config_valid():
    validate(CONFIG, SCHEMA)


def test_schema_keys_match_default_config():
    assert set(SCHEMA["properties"]) == set(CONFIG)


@pytest.mark.parametrize(
    "bad",
    [
        {"index_name": "x"},
        {"sequences": ["a.fa"]},
        {"sequences": [], "index_name": "x"},
        {"sequences": ["a.fa"], "index_name": "x", "unknown": 1},
    ],
)
def test_invalid_config_rejected(bad):
    with pytest.raises(ValidationError):
        validate(bad, SCHEMA)
