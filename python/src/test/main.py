
from fastapi import FastAPI, Request
import uvicorn

from src.main.common.logger import logger
from src.main.table_scanner import table_scanner

app = FastAPI()

@app.get("/ping")
def ping(request: Request):
    logger.info(f"/ping endpoint hit, method={request.method}")
    return {"status": "ok"}


@app.get("/tables")
def ping(request: Request):
    logger.info(f"/tables endpoint hit, method={request.method}")
    return table_scanner.handler({}, {})
