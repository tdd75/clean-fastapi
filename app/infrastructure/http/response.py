from typing import Any
import msgspec

from fastapi.responses import JSONResponse


class MsgSpecJSONResponse(JSONResponse):
    """
    JSON response using the high-performance msgspec library to serialize data to JSON.
    """

    def render(self, content: Any) -> bytes:
        return bytes(msgspec.json.encode(content))
