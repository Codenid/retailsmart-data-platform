"""Happy path Beam: Pub/Sub -> validación -> objeto JSON individual en Silver."""
import json
import logging
import re

import apache_beam as beam
from apache_beam.metrics import Metrics
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
from google.cloud import storage

REQUIRED = ("event_id", "producer_id", "trace_id", "occurred_at", "payload", "quality")
SAFE_ID = re.compile(r"^[A-Za-z0-9._-]+$")
LOGGER = logging.getLogger(__name__)


class StreamingOptions(PipelineOptions):
    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_argument("--input_subscription")
        parser.add_argument("--input_file")
        parser.add_argument("--silver_bucket")
        parser.add_argument("--demo_run_id")


def parse(raw):
    return json.loads(raw.decode() if isinstance(raw, bytes) else raw)


class ValidateAndNormalize(beam.DoFn):
    def __init__(self, demo_run_id):
        self.demo_run_id = demo_run_id
        self.received = Metrics.counter("rs009", "eventos_recibidos")
        self.valid = Metrics.counter("rs009", "eventos_validos")

    def process(self, raw):
        self.received.inc()
        event = parse(raw)
        missing = [key for key in REQUIRED if key not in event]
        if missing or not isinstance(event.get("quality"), dict):
            LOGGER.warning("Evento descartado: event_id=%s demo_run_id=%s", event.get("event_id", "unknown"), self.demo_run_id)
            return
        event_id = event["event_id"]
        if not isinstance(event_id, str) or not SAFE_ID.fullmatch(event_id):
            raise ValueError(f"event_id no seguro: {event_id!r}")
        self.valid.inc()
        LOGGER.info("Evento válido: event_id=%s demo_run_id=%s", event_id, self.demo_run_id)
        yield event


class SilverEventWriter(beam.DoFn):
    """Escribe un objeto estable por evento; los reintentos reutilizan la ruta."""

    def __init__(self, bucket_name, demo_run_id):
        self.bucket_name = bucket_name
        self.demo_run_id = demo_run_id
        self.client = None
        self.uploads = Metrics.counter("rs009", "subidas_silver_exitosas")

    def setup(self):
        self.client = storage.Client()
        self.bucket = self.client.bucket(self.bucket_name)

    def process(self, event):
        event_id = event["event_id"]
        object_name = f"eventos/demo/{self.demo_run_id}/{event_id}.json"
        content = json.dumps(event, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        self.bucket.blob(object_name).upload_from_string(content, content_type="application/json")
        uri = f"gs://{self.bucket_name}/{object_name}"
        self.uploads.inc()
        LOGGER.info("Subida Silver exitosa: event_id=%s demo_run_id=%s uri=%s", event_id, self.demo_run_id, uri)
        yield uri


def run(argv=None):
    options = StreamingOptions(argv)
    if not (options.input_subscription or options.input_file):
        raise ValueError("requiere input_subscription o input_file")
    if not options.silver_bucket or not options.demo_run_id or not SAFE_ID.fullmatch(options.demo_run_id):
        raise ValueError("requiere demo_run_id seguro y silver_bucket")
    source = beam.io.ReadFromPubSub(subscription=options.input_subscription) if options.input_subscription else beam.io.ReadFromText(options.input_file)
    options.view_as(StandardOptions).streaming = bool(options.input_subscription)
    pipeline = beam.Pipeline(options=options)
    pipeline | "ReadEvents" >> source | "ValidateAndNormalize" >> beam.ParDo(ValidateAndNormalize(options.demo_run_id)) | "SilverEventWriter" >> beam.ParDo(SilverEventWriter(options.silver_bucket, options.demo_run_id))
    result = pipeline.run()
    if options.view_as(StandardOptions).runner == "DataflowRunner":
        print(f"Dataflow job enviado: {result.job_id()}")
        return result
    result.wait_until_finish()
    return result


if __name__ == "__main__":
    run()
