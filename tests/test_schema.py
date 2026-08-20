from pathlib import Path

from usembridge.schema import load_and_validate


def test_example_cir_validates():
    root = Path(__file__).resolve().parents[1]
    obj = load_and_validate(root / "examples" / "legal_deletion_request.cir.json")
    assert obj["instance_id"] == "legal-demo-001"
