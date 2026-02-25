# AGENT.md


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
- API schema / DTOs: `python/src/main/api_gateway_schema/`. These will be plugged into API Gateway V2.
- Local dev/test harness (FastAPI): `python/src/test/main.py`
- Tests + local DynamoDB helpers: `python/src/test/`
- Infra (Terraform): `terraform/` (with env vars under `terraform/env/`)
- UI (Vite + React): `typescript/`
  - Header build label reads `VITE_BUILD_BRANCH` + `VITE_PIPELINE_NUMBER` (fallback `development`)
  - Header sticker links to pipeline run when `VITE_GITHUB_REPOSITORY` + `VITE_PIPELINE_RUN_ID` are set (`VITE_GITHUB_BASE_URL` defaults to `https://github.com`)
  - Sign-in uses `react-oidc-context` config in `typescript/src/auth/cognitoConfig.ts` (Cognito code flow)
  - Redirect/logout URI: `http://localhost:5173/` for `development` builds, otherwise `https://ebritt07.click`

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

## Tests Instructions
- Before either test suite:
  - Activate the Python 3.13 venv: `source .venv/bin/activate`
  - Install test deps: `python -m pip install -r requirements-test.txt`
- Unit tests:
  - Run from `python/`
  - `pytest`
-  Integration tests (needs docker):
  - Run from project root
  - `docker build -f Dockerfile.testsuite -t lambda-api-testsuite .`
  - `docker run --rm lambda-api-testsuite`
  - During Docker test runs, avoid posting intermediate command output/status commentary until the run completes (pass/fail summary after completion only)
- Default for small changes: run unit tests only (no Docker testsuite)
- Do not run Docker testsuite on every change; reserve it for pre-PR verification
- Before submitting a PR: run Docker integration test suite
  
## PR Description Format
- Include two labeled lines:
  - Summary: description of the change
  - Testing: describe what you ran, not the exact command
    - Example: "Docker integration test" or "Local pytest"

## Workflows
- Python CI: `.github/workflows/python-app.yml`
  - Sets up Python 3.13 + JDK 21, installs deps, builds DynamoDB Local, runs flake8 + pytest
  - Actually runs all tests including DynamoDB integration
  - Uploads test artifacts, posts coverage comment on PRs
- Terraform deploy (dev): `.github/workflows/tf-deploy-dev.yml`
  - `tf-plan` on pushes to `main`, `feature-*`, `bugfix-*`
  - `tf-apply` only on `main` push
  - Uses OIDC with `vars.AWS_ROLE_ARN`
