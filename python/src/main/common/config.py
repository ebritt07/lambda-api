import os

class Config:
    ENV: str = os.getenv("ENV", "LOCAL")
    REGION: str = os.getenv("REGION", "us-east-1")
    DYNAMODB_URL: str = os.getenv("DYNAMODB_URL", "http://localhost:8001")