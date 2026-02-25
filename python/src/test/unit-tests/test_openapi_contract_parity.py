import json
from pathlib import Path

from fastapi.testclient import TestClient

from src.test.main import app


def _load_terraform_openapi_contract() -> dict:
    repo_root = Path(__file__).resolve().parents[4]
    openapi_contract_path = repo_root / "terraform" / "openapi" / "openapi.json"
    return json.loads(openapi_contract_path.read_text())


def _without_security(value):
    if isinstance(value, dict):
        return {
            key: _without_security(child)
            for key, child in value.items()
            if key != "security"
        }
    if isinstance(value, list):
        return [_without_security(item) for item in value]
    return value


def _without_security_schemes(components: dict) -> dict:
    return {
        key: value
        for key, value in components.items()
        if key != "securitySchemes"
    }


def test_fastapi_openapi_paths_and_components_match_terraform_contract():
    client = TestClient(app)
    response = client.get("/openapi.json")

    assert response.status_code == 200

    generated_contract = response.json()
    terraform_contract = _load_terraform_openapi_contract()

    assert _without_security(generated_contract["paths"]) == _without_security(terraform_contract["paths"])
    assert _without_security(_without_security_schemes(generated_contract["components"])) == _without_security(
        _without_security_schemes(terraform_contract["components"])
    )
