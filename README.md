## lamba-api

lambda + api gateway + cognito + dynamo db app, deployed using terraform in GH actions.
- it's my first e2e project using AI assistants.
- it's serverless so it doesn't run up any bills
- lambda functions have no external dependencies, so it's fast even in cold start.

webite available on https://ebritt07.click.

### setup dynamodb local
set up the local dynamo db runner so it can be booted up by the pythontest app
- `cd python/src/test/runDynamoLocally`
- `mvn clean install`

### integration tests via Docker
Run the same steps as the CI deployment stage inside a container (Python 3.13 + JDK 21 + DynamoDB Local).
  - `docker build -f Dockerfile.testsuite -t lambda-api-testsuite .`
  - `docker run --rm lambda-api-testsuite`


### startup
- `cd /python`
- `/usr/local/bin/python3.13 -m venv .venv`
- `source .venv/bin/activate`
- `export PYTHONPATH=$PYTHONPATH:.`
- test via interactive UI:
- `python src/test/main.py`
  - you can test the lambdas at http://127.0.0.1:8000/docs
- or, test via unit tests with logging
  - `pytest -s -o log_cli=true -o log_cli_level=INFO`
