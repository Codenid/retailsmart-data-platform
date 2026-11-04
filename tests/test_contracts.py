import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
PRODUCERS = ROOT / "architecture" / "inventory" / "view08-producers.csv"
CONTRACTS = ROOT / "config" / "contracts"


class ContractTest(unittest.TestCase):
    def test_twelve_producer_contracts_exist(self):
        rows = PRODUCERS.read_text().splitlines()[1:]
        self.assertEqual(len(rows), 12)
        for row in rows:
            producer = row.split(",")[1]
            mode = row.split(",")[2]
            slug = {
                "Aplicación de Almacenes": "warehouse-app",
                "Benchmark Competidores": "competitor-benchmark",
                "ERP / Sistema de Inventario": "erp-inventory",
                "Eventos Locales": "local-events",
                "Redes Sociales": "social-media",
                "Sistema de Pedidos": "orders-system",
                "Aplicaciones de Canal (Web / App / POS)": "channel-apps",
                "Cámaras frigoríficas": "cold-storage-cameras",
                "Estantería Inteligente": "smart-shelf",
                "Sensores IoT de Tienda": "store-iot",
                "Sensores de almacén": "warehouse-sensors",
                "Tracking Logistico": "logistics-tracking",
            }[producer]
            self.assertTrue((CONTRACTS / mode / f"{slug}.json").exists())

    def test_schemas_have_required_fields(self):
        for path in list((CONTRACTS / "streaming").glob("*.json")) + list((CONTRACTS / "batch").glob("*.json")):
            schema = json.loads(path.read_text())
            self.assertEqual(schema["type"], "object")
            self.assertTrue(schema.get("required"))
            self.assertIn("properties", schema)

    def test_common_schemas_and_fixture(self):
        envelope = json.loads((CONTRACTS / "streaming-envelope.schema.json").read_text())
        manifest = json.loads((CONTRACTS / "batch-manifest.schema.json").read_text())
        fixture = json.loads((ROOT / "tests/fixtures/rs002-fixtures.json").read_text())
        self.assertIn("event_id", envelope["required"])
        self.assertIn("batch_id", manifest["required"])
        self.assertEqual(fixture["valid_streaming"]["payload"]["quantity_visible"], 4)
        self.assertLess(fixture["invalid_batch"]["cutoff_at"], fixture["invalid_batch"]["effective_at"])

    def test_twelve_valid_fixtures_exist(self):
        fixtures = json.loads((ROOT / "tests/fixtures/rs002-producers.json").read_text())
        self.assertEqual(len(fixtures), 12)


if __name__ == "__main__":
    unittest.main()
