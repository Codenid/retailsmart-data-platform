import json
import subprocess
import sys
import unittest
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parents[1]
EXPECTED = {"channel-apps", "cold-storage-cameras", "smart-shelf", "store-iot", "warehouse-sensors", "logistics-tracking"}


class StreamingFixtureTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, str(ROOT / "scripts/fixtures/generate_streaming_fixtures.py")], check=True)

    def test_six_fixtures_and_unique_ids(self):
        paths = sorted((ROOT / "tests/fixtures/streaming").glob("*.json"))
        self.assertEqual({p.stem for p in paths}, EXPECTED)
        events = [json.loads(p.read_text()) for p in paths]
        self.assertEqual(len({e["event_id"] for e in events}), 6)
        for event in events:
            self.assertEqual(event["quality"]["is_projected_defect"], False)
            datetime.fromisoformat(event["occurred_at"].replace("Z", "+00:00"))
            self.assertLessEqual(event["occurred_at"], event["emitted_at"])
            self.assertTrue(event["trace_id"])


if __name__ == "__main__":
    unittest.main()
