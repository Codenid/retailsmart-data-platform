import json
import tempfile
import unittest
from pathlib import Path

from scripts.streaming.raw_event_writer import write_raw_event


class RawEventWriterTest(unittest.TestCase):
    def test_write_retry_and_conflict(self):
        event = json.loads(Path("tests/fixtures/streaming/channel-apps.json").read_text())
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            first = write_raw_event(event, root)
            second = write_raw_event(event, root)
            self.assertEqual(first.status, "written")
            self.assertEqual(second.status, "duplicate")
            self.assertTrue((root / first.object_path).exists())
            changed = dict(event)
            changed["trace_id"] = "different"
            with self.assertRaises(ValueError):
                write_raw_event(changed, root)

    def test_invalid_envelope_rejected(self):
        with self.assertRaises(ValueError):
            write_raw_event({"event_id": "x"}, Path(tempfile.mkdtemp()))
