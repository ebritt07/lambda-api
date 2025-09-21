# lamba-api
lambda + api + dynamo db app, and aws infra deployment

### startup
- `cd /python`
- `usr/local/bin/python3.13 -m venv .venv`
- `source .venv/bin/activate`
- `export PYTHONPATH=$PYTHONPATH:.`
- `uvicorn src.test.main:app --reload`