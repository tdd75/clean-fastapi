import json
import logging
from typing import Callable, Awaitable, Any

from starlette.requests import Request
from starlette.responses import Response

from app.infrastructure.helper.log_helper import mask_sensitive_values

logger = logging.getLogger(__name__)


async def log_request_response_middleware(request: Request, call_next: Callable[[Request], Awaitable[Any]]) -> Response:
    try:
        req_body = await request.body()
        if req_body:
            try:
                parsed = json.loads(req_body)
                sanitized = mask_sensitive_values(parsed, ['password'])
                print(
                    f'{request.client.host}:{request.client.port} - "{request.method} {request.url}"\n'
                    f'{json.dumps(sanitized, ensure_ascii=False)}'
                )
            except Exception:
                print(
                    f'{request.client.host}:{request.client.port} - "{request.method} {request.url}"\n'
                    f'{req_body.decode(errors="ignore")}'
                )
    except Exception as e:
        logger.error(f'Error reading request body: {e}')

    response = await call_next(request)
    chunks = []
    async for chunk in response.body_iterator:
        chunks.append(chunk)
    res_body = b''.join(chunks)

    return Response(
        content=res_body,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.media_type,
    )
