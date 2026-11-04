#!/usr/bin/env python3
"""Persistencia local idempotente del evento original en Bronze raw."""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

REQUIRED = ("schema_version", "simulation_id", "scenario_id", "producer_id", "event_id", "event_type", "occurred_at", "emitted_at", "trace_id", "entity_type", "entity_id", "payload", "quality")


@dataclass(frozen=True)
class RawWriteResult:
    status: str
    event_id: str
    object_path: str
    content_sha256: str


def write_raw_event(event: dict[str, Any], bronze_root: Path) -> RawWriteResult:
    missing = [field for field in REQUIRED if field not in event]
    if missing:
        raise ValueError(f"envelope incompleto: {','.join(missing)}")
    occurred = datetime.fromisoformat(event["occurred_at"].replace("Z", "+00:00"))
    producer = event["producer_id"]
    event_id = event["event_id"]
    relative = Path("streaming/raw") / f"producer_id={producer}" / f"dt={occurred.date().isoformat()}" / f"event_id={event_id}.json"
    target = bronze_root / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    encoded = (json.dumps(event, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()
    digest = hashlib.sha256(encoded).hexdigest()
    if target.exists():
        existing = target.read_bytes()
        if existing != encoded:
            raise ValueError(f"conflicto de event_id: {event_id}")
        return RawWriteResult("duplicate", event_id, str(relative), digest)
    temporary = target.with_suffix(".tmp")
    temporary.write_bytes(encoded)
    temporary.replace(target)
    return RawWriteResult("written", event_id, str(relative), digest)
