import json
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.streaming.dataflow_pipeline import SilverEventWriter, ValidateAndNormalize


class DataflowPipelineTest(unittest.TestCase):
    def test_validates_contract_minimum(self):
        event = json.loads(Path("tests/fixtures/streaming/channel-apps.json").read_text())
        processor = ValidateAndNormalize("demo-local")
        self.assertEqual(list(processor.process(json.dumps(event))), [event])
        self.assertEqual(list(processor.process(json.dumps({"event_id": "x"}))), [])

    def test_writer_uses_stable_object_path(self):
        class Blob:
            def upload_from_string(self, content, content_type):
                self.content = content
                self.content_type = content_type

        class Bucket:
            def blob(self, name):
                self.name = name
                self.result = Blob()
                return self.result

        class Client:
            def bucket(self, name):
                self.result = Bucket()
                return self.result

        event = json.loads(Path("tests/fixtures/streaming/channel-apps.json").read_text())
        with patch("scripts.streaming.dataflow_pipeline.storage.Client", return_value=Client()):
            writer = SilverEventWriter("silver-bucket", "demo-local")
            writer.setup()
            self.assertEqual(list(writer.process(event)), [f"gs://silver-bucket/eventos/demo/demo-local/{event['event_id']}.json"])
            self.assertEqual(writer.bucket.name, f"eventos/demo/demo-local/{event['event_id']}.json")

