#!/usr/bin/env python3
"""Exporta únicamente los elementos y relaciones de la vista 08 del archivo ArchiMate.

Solo usa biblioteca estándar. No crea recursos GCP ni modifica el modelo de origen.
"""
from __future__ import annotations
import csv
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'architecture/source/RetailSmart_ArquitecturaSolucion.archimate'
OUT = ROOT / 'architecture/inventory'
VIEW = '08_integracion_detallada_tobe'
XSI_TYPE = '{http://www.w3.org/2001/XMLSchema-instance}type'


def write_csv(file: Path, fields: list[str], rows: list[dict]) -> None:
    file.parent.mkdir(parents=True, exist_ok=True)
    with file.open('w', newline='', encoding='utf-8') as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def export(source: Path = SOURCE, out: Path = OUT) -> tuple[int, int]:
    root = ET.parse(source).getroot()
    view = next((n for n in root.iter() if n.get('name') == VIEW and n.get(XSI_TYPE, '').endswith('ArchimateDiagramModel')), None)
    if view is None:
        raise ValueError(f'La vista {VIEW!r} no existe')
    visible_ids = {n.attrib['archimateElement'] for n in view.iter() if n.get('archimateElement')}
    relation_ids = {n.attrib['archimateRelationship'] for n in view.iter() if n.get('archimateRelationship')}
    elements: dict[str, dict] = {}
    relationships: dict[str, dict] = {}
    for n in root.iter():
        nid = n.get('id')
        typ = n.get(XSI_TYPE, '').removeprefix('archimate:')
        if nid in visible_ids and typ:
            props = {p.get('key', ''): p.get('value', '') for p in n if p.tag == 'property'}
            elements[nid] = {
                'archimate_id': nid, 'type': typ,
                'name': n.get('name', '').replace('\n', ' ').strip(),
                'gcp_technology': props.get('Tecnología GCP', ''),
                'standard': props.get('Implementación/estándar', ''),
                'documentation': (n.findtext('documentation') or '').replace('\n', ' ').strip(),
            }
        if nid in relation_ids and typ.endswith('Relationship'):
            relationships[nid] = {'archimate_relation_id': nid, 'type': typ,
                                  'source_id': n.get('source', ''), 'target_id': n.get('target', ''),
                                  'name': n.get('name', '')}
    if len(elements) != len(visible_ids) or len(relationships) != len(relation_ids):
        raise ValueError('Existen referencias no resueltas en la vista 08')
    sorted_elements = sorted(elements.values(), key=lambda r: (r['type'], r['name'], r['archimate_id']))
    enriched_relations = []
    for r in relationships.values():
        src = elements.get(r['source_id'])
        dst = elements.get(r['target_id'])
        if not src or not dst:
            raise ValueError('Relación apunta a elemento fuera de la vista 08: ' + r['archimate_relation_id'])
        enriched_relations.append({**r, 'source_name': src['name'], 'target_name': dst['name']})
    enriched_relations.sort(key=lambda r: (r['source_name'], r['target_name'], r['type']))
    write_csv(out / 'view08-elements.csv', list(sorted_elements[0]), sorted_elements)
    write_csv(out / 'view08-relations.csv', list(enriched_relations[0]), enriched_relations)
    # Only *external* producer applications: avoid misclassifying internal consumers
    # which also have Access relationships to the same objects.
    external = {e['archimate_id'] for e in elements.values() if e['name'] == 'DOMINIOS EXTERNOS'}
    changed = True
    while changed:
        old_size = len(external)
        for r in enriched_relations:
            if r['type'] == 'CompositionRelationship' and r['source_id'] in external:
                external.add(r['target_id'])
        changed = len(external) != old_size
    producers = []
    for r in enriched_relations:
        src, dst = elements[r['source_id']], elements[r['target_id']]
        if src['archimate_id'] not in external or src['type'] != 'ApplicationComponent' or dst['type'] != 'DataObject':
            continue
        if r['type'] != 'AccessRelationship':
            continue
        if dst['name'] not in ('Tópico Eventos Retail', 'Storage Landing Zone'):
            continue
        producers.append({'archimate_id': src['archimate_id'], 'producer': src['name'],
                          'mode': 'streaming' if dst['name'] == 'Tópico Eventos Retail' else 'batch',
                          'destination': dst['name']})
    producers.sort(key=lambda p: (p['mode'], p['producer']))
    write_csv(out / 'view08-producers.csv', list(producers[0]), producers)
    print(f'Vista {VIEW}: {len(elements)} elementos, {len(relationships)} relaciones')
    return len(elements), len(relationships)


if __name__ == '__main__':
    export()
