"""Pipeline Beam mínimo para publicar insights operativos en Pub/Sub."""
import json
import logging

import apache_beam as beam
from apache_beam.metrics import Metrics
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions

LOGGER = logging.getLogger(__name__)


def build_insight(event):
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
        self.received = Metrics.counter("rs010", "eventos_recibidos")
        self.insights = Metrics.counter("rs010", "insights_generados")

    def process(self, raw):
        self.received.inc()
        try:
            event = json.loads(raw.decode() if isinstance(raw, bytes) else raw)
        except (TypeError, ValueError):
            LOGGER.exception("EVENTO_DESCARTADO: motivo=json_invalido")
            return
        insight = build_insight(event)
        if insight is None:
            LOGGER.info("EVENTO_DESCARTADO: motivo=no_es_telemetria event_id=%s", event.get("event_id", "unknown"))
            return
        self.insights.inc()
        LOGGER.info("INSIGHT_GENERADO: source_event_id=%s", insight["source_event_id"])
        yield json.dumps(insight, ensure_ascii=False, sort_keys=True)


class LogReceived(beam.DoFn):
    def process(self, raw):
        LOGGER.info("EVENTO_RECIBIDO: bytes=%s", len(raw))
        yield raw


class InsightOptions(PipelineOptions):
    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_argument("--input_subscription", required=True)
        parser.add_argument("--output_topic", required=True)


def run(argv=None):
    options = InsightOptions(argv)
    options.view_as(StandardOptions).streaming = True
    pipeline = beam.Pipeline(options=options)
    (
        pipeline
        | "ReadSilverEvents" >> beam.io.ReadFromPubSub(subscription=options.input_subscription)
        | "LogEventReceived" >> beam.ParDo(LogReceived())
        | "BuildInsights" >> beam.ParDo(ProcessInsight())
        | "PublishInsights" >> beam.Map(lambda value: value.encode("utf-8"))
        | "WriteInsights" >> beam.io.WriteToPubSub(options.output_topic)
    )
    result = pipeline.run()
    if options.view_as(StandardOptions).runner == "DataflowRunner":
        print(f"Dataflow job enviado: {result.job_id()}")
        return result
    result.wait_until_finish()
    return result


if __name__ == "__main__":
    run()
