import json
from pathlib import Path

from fastapi.testclient import TestClient

from src.test.main import app


def _load_terraform_openapi_contract() -> dict:
    repo_root = Path(__file__).resolve().parents[4]
    openapi_contract_path = repo_root / "terraform" / "openapi" / "openapi.json"
    return json.loads(openapi_contract_path.read_text())


def test_fastapi_openapi_paths_and_components_match_terraform_contract():
    client = TestClient(app)
    response = client.get("/openapi.json")

    assert response.status_code == 200

    generated_contract = response.json()
    terraform_contract = _load_terraform_openapi_contract()

    assert generated_contract["paths"] == terraform_contract["paths"]
    assert generated_contract["components"] == terraform_contract["components"]
