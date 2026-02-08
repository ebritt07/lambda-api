# AGENT.md

## Instructions
- Before raising PR's, do review 

## Goals
- Python Lambda API for read and writing to dynamo DB.
- Lambdas accessed by API Gateway, which validate and authenticate requests
- Keep cold-start and request latency very low

## Remaining Steps
- Add AWS Lambda, API Gateway, IAM, infra (Terraform).
- Package/deploy Lambda code and wire API Gateway routes to handlers.
- Add Auth layer to API Gateway
- Decide on and implement user profile lambdas (currently stubbed in local FastAPI only).
- Publish/validate API Gateway request schemas

## Architecture Map
- Python Lambda logic (handlers + core logic): `python/src/main/lambdas/`
- API schema / DTOs: `python/src/main/api_gateway_schema/`
 - These will be plugged into API Gateway V2
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


## Terraform Notes
- Do not edit backend config:
  - `terraform/backend.tf`
  - `terraform/backend-setup/`

## Tests
- Command: `pytest` 
- Integration tests are marked skipped in local codex env due to unable to start dynamodb

## Workflows
- Python CI: `.github/workflows/python-app.yml`
  - Sets up Python 3.13 + JDK 21, installs deps, builds DynamoDB Local, runs flake8 + pytest
  - Actually runs all tests including DynamoDB integration
  - Uploads test artifacts, posts coverage comment on PRs
- Terraform deploy (dev): `.github/workflows/tf-deploy-dev.yml`
  - `tf-plan` on pushes to `main`, `feature-*`, `bugfix-*`
  - `tf-apply` only on `main` push
  - Uses OIDC with `vars.AWS_ROLE_ARN`


