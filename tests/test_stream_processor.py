import json
import unittest
from pathlib import Path

from scripts.streaming.stream_processor import process_event


class StreamProcessorTest(unittest.TestCase):
    def test_valid_duplicate_and_invalid(self):
        event = json.loads(Path("tests/fixtures/streaming/channel-apps.json").read_text())
        seen = set()
        self.assertEqual(process_event(event, seen).status, "silver")
        self.assertEqual(process_event(event, seen).status, "duplicate")
        self.assertEqual(process_event({"event_id": "bad"}, seen).status, "quarantine")

    def test_quality_defect_without_origin_goes_to_dlq(self):
        event = json.loads(Path("tests/fixtures/streaming/channel-apps.json").read_text())
        event["event_id"] = "evt-defect"
        event["quality"] = {"is_projected_defect": True}
        self.assertEqual(process_event(event, set()).status, "dlq")
