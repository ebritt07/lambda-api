## lamba-api

lambda + api + dynamo db app, and aws infra deployment

### startup dynamodb local
- `cd python/src/test/runDynamoLocally`
- `mvn clean install`
- `mvn exec:java -Dexec.mainClass=.org.example.Main -Dexec.args="--port=9001"`


### startup
- `cd /python`
- `/usr/local/bin/python3.13 -m venv .venv`
- `source .venv/bin/activate`
- `export PYTHONPATH=$PYTHONPATH:.`
- test via interactive UI:
  - `uvicorn src.test.Launcher:app --reload`
  - you can test the lambdas at http://127.0.0.1:8000/docs
- or, test via unit tests
  - `pytest`