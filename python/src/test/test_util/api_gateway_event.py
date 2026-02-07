from dataclasses import dataclass, field


@dataclass
class APIGatewayTestEvent:
    method:str
    raw_path:str = ""
    query_params : dict = field(default_factory=dict)
    body_dict:dict = field(default_factory=dict)

    def export_event(self) -> dict:
        return    {
            'version': '2.0',
            'headers': {
                'accept': 'application/json',
                'content-length': '100',
                'content-type': 'application/json',
                'x-forwarded-proto': 'https'
            },
            'queryStringParameters': self.query_params,
            "requestContext": {
                "http": {
                    "method": self.method,
                },
                "time": "07/Feb/2026:07:01:11 +0000",
                "timeEpoch": 1770447671652
            },
            "body": self.body_dict,
            "isBase64Encoded": False
        }


"""
good to inspect this from 

"""