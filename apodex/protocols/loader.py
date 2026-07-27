from __future__ import annotations
import json
import yaml
from typing import Dict, Any, Union
from apodex.harness.schemas.protocol_spec import ProtocolSpec


class ProtocolLoader:
    """Loads and validates declarative YAML/JSON protocol definitions using Pydantic."""

    @staticmethod
    def load_from_dict(data: Dict[str, Any]) -> ProtocolSpec:
        return ProtocolSpec.model_validate(data)

    @staticmethod
    def load_from_json(json_str: str) -> ProtocolSpec:
        return ProtocolSpec.model_validate_json(json_str)

    @staticmethod
    def load_from_yaml(yaml_str: str) -> ProtocolSpec:
        # Utilizing pyyaml or standard fallback if needed
        parsed = yaml.safe_load(yaml_str)
        return ProtocolSpec.model_validate(parsed)
