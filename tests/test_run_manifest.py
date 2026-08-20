from usembridge.run_manifest import build_manifest


def test_manifest_has_prompt_hash(tmp_path):
    manifest = build_manifest(
        project_root=tmp_path,
        run_id="smoke-001",
        dataset={"name": "synthetic"},
        model={"name": "none"},
        prompt_text="frozen prompt",
        decoding={"temperature": 0.0},
        solver={"name": "z3"},
        seed=42,
    )
    assert manifest["run_id"] == "smoke-001"
    assert len(manifest["prompt_sha256"]) == 64
    assert manifest["seed"] == 42
