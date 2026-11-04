"""Núcleo determinista de validación y enrutamiento streaming."""
from dataclasses import dataclass
from typing import Any

REQUIRED = ("event_id", "producer_id", "trace_id", "occurred_at", "payload", "quality")


@dataclass(frozen=True)
class ProcessingResult:
    status: str
    event_id: str
    reason: str | None = None


def process_event(event: dict[str, Any], seen: set[str]) -> ProcessingResult:
    missing = [key for key in REQUIRED if key not in event]
    if missing:
        return ProcessingResult("quarantine", event.get("event_id", "unknown"), "missing:" + ",".join(missing))
    event_id = event["event_id"]
    if event_id in seen:
        return ProcessingResult("duplicate", event_id, "event_id_already_seen")
    if event["quality"].get("is_projected_defect") and not event["quality"].get("original_record_id"):
        return ProcessingResult("dlq", event_id, "defect_without_original_record_id")
    seen.add(event_id)
    return ProcessingResult("silver", event_id)
