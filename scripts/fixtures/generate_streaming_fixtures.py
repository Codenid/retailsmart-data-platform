#!/usr/bin/env python3
"""Genera seis eventos streaming sintéticos, pequeños y reproducibles."""
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parents[2]
OUTPUT = ROOT / "tests" / "fixtures" / "streaming"
TIMESTAMP = "2026-11-03T10:00:00Z"

EVENTS = {
    "channel-apps": ("order_created", "order", "ORD-1", {"order_id": "ORD-1", "order_line_id": "ORD-1-L1", "customer_id": "CUS-1", "store_id": "STORE-1", "product_id": "PROD-1", "quantity": 1, "unit_price": 10, "currency": "USD", "channel": "web", "order_status": "created"}),
    "cold-storage-cameras": ("temperature_reading", "asset", "ASSET-1", {"asset_id": "ASSET-1", "sensor_id": "SENSOR-1", "store_id": "STORE-1", "temperature_c": 3, "humidity_pct": 70, "door_open": False, "reading_quality": "valid"}),
    "smart-shelf": ("stock_changed", "inventory", "INV-1", {"store_id": "STORE-1", "shelf_id": "SHELF-1", "product_id": "PROD-1", "quantity_visible": 4, "quantity_estimated": 5, "stock_status": "low", "replenishment_required": True}),
    "store-iot": ("store_telemetry", "sensor", "SENSOR-2", {"store_id": "STORE-1", "asset_id": "ASSET-2", "sensor_id": "SENSOR-2", "metric_name": "noise", "metric_value": 20, "metric_unit": "dB", "battery_pct": 92}),
    "warehouse-sensors": ("warehouse_telemetry", "sensor", "SENSOR-3", {"warehouse_id": "WH-1", "asset_id": "ASSET-3", "sensor_id": "SENSOR-3", "metric_name": "vibration", "metric_value": 2, "metric_unit": "mm_s", "equipment_status": "operational"}),
    "logistics-tracking": ("delivery_location", "delivery", "DEL-1", {"delivery_id": "DEL-1", "order_id": "ORD-1", "vehicle_id": "VEH-1", "latitude": -12.1, "longitude": -77.0, "status": "in_transit"}),
}


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for index, (producer_id, event) in enumerate(EVENTS.items(), start=1):
        event_type, entity_type, entity_id, payload = event
        envelope = {
            "schema_version": "1.0.0",
            "simulation_id": "sim-20261103-001",
            "scenario_id": "black-friday",
            "producer_id": producer_id,
            "event_id": f"evt-stream-{index:04d}",
            "event_type": event_type,
            "occurred_at": TIMESTAMP,
            "emitted_at": TIMESTAMP,
            "trace_id": f"trace-stream-{index:04d}",
            "entity_type": entity_type,
            "entity_id": entity_id,
            "payload": payload,
            "quality": {"is_projected_defect": False, "original_record_id": None, "defect_type": None, "defect_seed": None},
        }
        (OUTPUT / f"{producer_id}.json").write_text(json.dumps(envelope, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
