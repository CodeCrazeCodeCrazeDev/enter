from __future__ import annotations
import json
from datetime import datetime
from typing import Any, Dict


class StructuredTracer:
    """Provides OpenTelemetry style JSON tracing payloads for simulation observability."""

    def __init__(self, service_name: str) -> None:
        self.service_name = service_name

    def create_span_log(self, trace_id: str, span_id: str, message: str, metadata: Dict[str, Any]) -> str:
        """Returns standard OpenTelemetry structured log string."""
        log_payload = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "trace_id": trace_id,
            "span_id": span_id,
            "service": f"wmc.{self.service_name}",
            "level": "INFO",
            "message": message,
            "metadata": metadata
        }
        return json.dumps(log_payload)
