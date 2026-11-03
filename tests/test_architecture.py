"""Tests de inventario; no requieren conexión a GCP."""
import csv
import subprocess
import sys
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / 'architecture/inventory'


def read(name):
    with (INVENTORY / name).open(encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))


class View08ContractTest(unittest.TestCase):
    def test_view08_inventory_count(self):
        self.assertEqual(len(read('view08-elements.csv')), 94)
        self.assertEqual(len(read('view08-relations.csv')), 165)

    def test_relations_resolve_to_view08(self):
        ids = {e['archimate_id'] for e in read('view08-elements.csv')}
        for relation in read('view08-relations.csv'):
            self.assertIn(relation['source_id'], ids)
            self.assertIn(relation['target_id'], ids)

    def test_twelve_external_producers_six_each(self):
        producers = read('view08-producers.csv')
        self.assertEqual(len(producers), 12)
        self.assertEqual(Counter(p['mode'] for p in producers), {'batch': 6, 'streaming': 6})
        self.assertEqual(len({p['archimate_id'] for p in producers}), 12)

    def test_all_technology_services_mapped(self):
        elements = read('view08-elements.csv')
        services = {e['archimate_id'] for e in elements if e['type'] == 'TechnologyService'}
        mapping = read('view08-gcp-mapping.csv')
        self.assertEqual(len(services), 20)
        self.assertEqual({m['archimate_id'] for m in mapping}, services)
        self.assertTrue(all(m['status'] == 'PLANNED_NOT_DEPLOYED' for m in mapping))

    def test_all_view_elements_tracked(self):
        elements = {e['archimate_id'] for e in read('view08-elements.csv')}
        mapping = read('view08-traceability.csv')
        self.assertEqual({m['archimate_id'] for m in mapping}, elements)
        self.assertEqual(len(mapping), 94)

    def test_model_source_exists(self):
        self.assertTrue((ROOT / 'architecture/source/RetailSmart_ArquitecturaSolucion.archimate').exists())


if __name__ == '__main__':
    unittest.main()
