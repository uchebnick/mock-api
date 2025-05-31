from fastapi import Request
from fastapi.exceptions import HTTPException
from typing import Dict, Any
import logging

logger = logging.getLogger("ai_manager.utills")


async def convert_request_to_text(request: Request) -> str:

    request_info = [
        f"Method: {request.method}",
        f"URL: {request.url}",
        f"Path Parameters: {dict(request.path_params)}",
        f"Query Parameters: {dict(request.query_params)}",
        (
            f"Client: {request.client.host}:{request.client.port}"
            if request.client
            else "Client: Unknown"
        ),
        "\nHeaders:",
    ]

    headers = [f"  {name}: {value}" for name, value in request.headers.items()]

    try:
        body = await request.body()
        body_text = body.decode()
    except Exception as e:
        logger.exception("Ошибка при декодировании тела запроса")
        raise HTTPException(
            status_code=500, detail="Ошибка при декодировании тела запроса"
        )
        return

    request_text = "\n".join(request_info + headers + ["\nBody:", body_text])
    return request_text
