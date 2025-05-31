from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.ai_manager.service import AIService, get_ai_service
from app.config.app_config import get_app_config, AppConfig
from app.middleware.request_middleware import (
    RequestLoggingMiddleware,
    ErrorHandlingMiddleware,
)
from contextlib import asynccontextmanager
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import Response
import logging
import aiofiles

# Настройка логирования
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Приложение запускается...")
    yield
    logger.info("Приложение завершает работу...")


app = FastAPI(title="mock-api", docs_url="/mock-api", lifespan=lifespan)

app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(ErrorHandlingMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/process")
async def process_request(
    request: Request, ai_service: AIService = Depends(get_ai_service)
):

    try:
        logger.info("Получен новый запрос")
        response = await ai_service.handle_request(request)

        if response is None:
            logger.error("Не удалось получить корректный ответ от AI")
            return {"error": "Не удалось обработать запрос"}

        logger.info("Запрос успешно обработан")
        return response

    except Exception as e:
        logger.error(f"Ошибка при обработке запроса: {str(e)}")
        return {"error": f"Внутренняя ошибка сервера: {str(e)}"}


@app.get("/set_docs")
async def set_docs(user_docs: str):
    try:
        if not user_docs:
            logger.error("Не получены user_docs в запросе")
            return {"error": "Необходимо предоставить user_docs"}

        service = await get_ai_service(user_docs=user_docs)
        logger.info("Документы успешно установлены")

        return {"status": "success", "message": "Документы успешно установлены"}

    except ValueError as e:
        logger.error(f"Ошибка при установке документов: {str(e)}")
        return {"error": f"Ошибка при установке документов: {str(e)}"}


@app.get("/docs", include_in_schema=False)
async def openapi():
    return get_swagger_ui_html(
        openapi_url="/docs/ai_docs.yaml", title="API Documentation"
    )


@app.get("/docs/ai_docs.yaml", include_in_schema=False)
async def get_openapi_yaml():
    async with aiofiles.open("./app/docs/openapi_docs.yaml", "r") as f:
        yaml_content = await f.read()
    return Response(content=yaml_content, media_type="application/x-yaml")
