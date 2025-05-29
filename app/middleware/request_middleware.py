from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import time
import logging
import json

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        request_id = request.headers.get("X-Request-ID", "unknown")
        method = request.method
        url = str(request.url)
        
        logger.info(f"Request started: {request_id} - {method} {url}")
        
        try:
            body = await request.body()
            if body:
                try:
                    body_json = json.loads(body)
                    logger.debug(f"Request body: {json.dumps(body_json, ensure_ascii=False)}")
                except json.JSONDecodeError:
                    logger.debug(f"Request body: {body.decode()}")
            
            response = await call_next(request)
            
            process_time = time.time() - start_time
            
            logger.info(
                f"Request completed: {request_id} - {method} {url} - "
                f"Status: {response.status_code} - Time: {process_time:.2f}s"
            )
            
            return response
            
        except Exception as e:
            logger.error(
                f"Request failed: {request_id} - {method} {url} - Error: {str(e)}",
                exc_info=True
            )
            
            return JSONResponse(
                status_code=500,
                content={
                    "error": "Internal Server Error",
                    "request_id": request_id,
                    "message": str(e)
                }
            )

class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as e:
            logger.error(f"Unhandled error: {str(e)}", exc_info=True)
            return JSONResponse(
                status_code=500,
                content={
                    "error": "Internal Server Error",
                    "message": str(e)
                }
            ) 