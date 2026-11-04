import json
import unittest
from pathlib import Path

from scripts.streaming.insights_processor import build_insight, ProcessInsight


class InsightsProcessorTest(unittest.TestCase):
    def test_telemetry_produces_insight_with_source_id(self):
        event = json.loads(Path("tests/fixtures/streaming/store-iot.json").read_text())
        insight = build_insight(event)
        self.assertEqual(insight["insight_type"], "maintenance_observation")
        self.assertEqual(insight["source_event_id"], event["event_id"])
        self.assertEqual(insight["payload"], event["payload"])

    def test_non_telemetry_is_ignored(self):
        event = json.loads(Path("tests/fixtures/streaming/channel-apps.json").read_text())
        self.assertIsNone(build_insight(event))

    def test_dofn_serializes_insight(self):
        event = json.loads(Path("tests/fixtures/streaming/store-iot.json").read_text())
        output = list(ProcessInsight().process(json.dumps(event)))
        self.assertEqual(json.loads(output[0])["source_event_id"], event["event_id"])
