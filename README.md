## lamba-api

lambda + api + dynamo db app, and aws infra deployment

### setup dynamodb local
set up the local dynamo db runner so it can be booted up by the pythontest app
- `cd python/src/test/runDynamoLocally`
- `mvn clean install`

### integration tests via Docker
Run the same steps as the CI deployment stage inside a container (Python 3.13 + JDK 21 + DynamoDB Local).
- `docker build -f Dockerfile.integration -t lambda-api-integration .`
- `docker run --rm lambda-api-integration pytest -s -o log_cli=true -o log_cli_level=INFO`


### startup
- `cd /python`
- `/usr/local/bin/python3.13 -m venv .venv`
- `source .venv/bin/activate`
- `export PYTHONPATH=$PYTHONPATH:.`
- test via interactive UI:
- `python src/test/app.py`
  - you can test the lambdas at http://127.0.0.1:8000/docs
- or, test via unit tests with logging
  - `pytest -s -o log_cli=true -o log_cli_level=INFO`
