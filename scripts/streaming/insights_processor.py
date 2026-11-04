"""Transformación académica mínima de telemetría Silver a insight operativo."""
import json
import logging

import apache_beam as beam
from apache_beam.metrics import Metrics

LOGGER = logging.getLogger(__name__)


def build_insight(event):
    """Construye un insight observable sin aplicar reglas de negocio inventadas."""
    payload = event.get("payload", {})
    if event.get("event_type", "").endswith("telemetry") or "sensor_id" in payload:
        return {
            "insight_type": "maintenance_observation",
            "source_event_id": event["event_id"],
            "producer_id": event["producer_id"],
            "trace_id": event["trace_id"],
            "occurred_at": event["occurred_at"],
            "status": "observed",
            "entity_id": event.get("entity_id"),
            "payload": payload,
        }
    return None


class ProcessInsight(beam.DoFn):
    def __init__(self):
        self.received = Metrics.counter("rs010", "eventos_silver_recibidos")
        self.insights = Metrics.counter("rs010", "insights_generados")

    def process(self, raw):
        self.received.inc()
        event = json.loads(raw.decode() if isinstance(raw, bytes) else raw)
        insight = build_insight(event)
        if insight is not None:
            self.insights.inc()
            LOGGER.info("Insight generado: source_event_id=%s", insight["source_event_id"])
            yield json.dumps(insight, ensure_ascii=False, sort_keys=True)
