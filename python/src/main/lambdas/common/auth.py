from typing import Any, Dict, Optional


def get_caller_sub(event: Dict[str, Any]) -> Optional[str]:
    request_context = event.get("requestContext", {})
    authorizer = request_context.get("authorizer", {})

    claims = authorizer.get("claims")
    if isinstance(claims, dict) and claims.get("sub"):
        return claims["sub"]

    return None
