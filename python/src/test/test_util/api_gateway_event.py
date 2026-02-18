from dataclasses import dataclass, field
from typing import Optional


@dataclass
class APIGatewayTestEvent:
    method: str
    raw_path: str = ""
    query_params: dict = field(default_factory=dict)
    body_json_str: Optional[str] = None

    def export_event(self) -> dict:
        event = {
            "version": "2.0",
            "headers": {
                "accept": "application/json",
                "content-length": "100",
                "content-type": "application/json",
                "x-forwarded-proto": "https"
            },
            "queryStringParameters": self.query_params,
            "requestContext": {
                "http": {
                    "method": self.method,
                },
                "time": "07/Feb/2026:07:01:11 +0000",
                "timeEpoch": 1770447671652
            },
            "isBase64Encoded": False
        }
        if self.body_json_str:
            event["body"] = self.body_json_str
        return event
