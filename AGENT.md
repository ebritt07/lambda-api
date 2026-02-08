# AGENT.md

## Goals
- Python Lambda API for X and Y use cases.
- Keep cold-start and request latency within targets.
- Preserve API and data compatibility for existing clients.

## Architecture Map
- Python Lambda logic (handlers + core logic): `python/src/main/lambdas/`
- API schema / DTOs: `python/src/main/api_gateway_schema/`
- Local dev/test harness (FastAPI): `python/src/test/main.py`
- Tests + local DynamoDB helpers: `python/src/test/`
- Infra (Terraform): `terraform/` (with env vars under `terraform/env/`)

## Tight Couplings (Important)
- Terraform defines DynamoDB tables and their keys/GSIs.
- Python data layer expects those exact table names and key schemas.
- Changing Terraform table names, keys, or indexes requires updating Python queries and fixtures.

## Change Hotspots
- `python/src/main/lambdas/*` for API changes
- `python/src/main/api_gateway_schema/*` for request/response schema changes
- `python/src/test/*` for local testing or fixtures
- `terraform/*` for table/index changes or infra updates
- `.github/workflows/*` for CI/CD adjustments

## DynamoDB Invariants
- Table names, PK/SK formats, and GSI names are part of the contract.
- Backfill/migration needed if key schema changes.
- Strong/Eventually consistent reads: note which paths require which.

## Terraform Notes
- Backend config: `terraform/backend.tf`
- Bootstrap backend: `terraform/backend-setup/`
- Do not edit generated files if any (state, lock, plan outputs)

## Tests
- Fast: `pytest -q tests/unit` (if/when unit tests are split)
- Integration: requires local DynamoDB (dynamodb-local) and env vars

## Local Env
- Required env vars: `ENV=LOCAL` for local DynamoDB usage
- Local DynamoDB setup: `python/src/test/runDynamoLocally` (Maven project), started by `python/src/test/test_util/dynamodb.py`

## Workflows
- Python CI: `.github/workflows/python-app.yml`
  - Runs on PRs and `main` pushes
  - Sets up Python 3.13 + JDK 21, installs deps, builds DynamoDB Local, runs flake8 + pytest
  - Uploads test artifacts, posts coverage comment on PRs
- Terraform deploy (dev): `.github/workflows/tf-deploy-dev.yml`
  - `tf-plan` on pushes to `main`, `feature-*`, `bugfix-*`
  - `tf-apply` only on `main` push
  - Uses OIDC with `vars.AWS_ROLE_ARN`

## Remaining Steps / Goals
- Align Terraform DynamoDB key schema with Python (currently Terraform uses `ID` vs code `id`).
- Add AWS Lambda, API Gateway, IAM, and logging/metrics infra (Terraform).
- Package/deploy Lambda code and wire API Gateway routes to handlers.
- Decide on and implement user profile lambdas (currently stubbed in local FastAPI only).
- Publish/validate API Gateway request schemas (if using API Gateway validation).
- Confirm CI stability for DynamoDB Local on GitHub Actions and adjust if needed.
