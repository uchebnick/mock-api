from typing import Dict, Any
from fastapi import HTTPException
import logging

logger = logging.getLogger("ai_manager.utils")

def replace_placeholders(self, template: str, context: Dict[str, Any], pattern: str = r'\{\{(\w+)\}\}') -> str:
    """Replace placeholders with actual values"""
    compiled_pattern = self._compile_pattern(pattern)
    return compiled_pattern.sub(
        lambda m: str(context.get(m.group(1), "")),
        template
    )

def read_file(path: str) -> str:
    try:
        with open(path, "r") as f:
            data = f.read()
        return data
    except FileNotFoundError:
        logger.error(f"Файл не найден: {path}")
        raise HTTPException(status_code=500, detail="Файл не найден")
    except Exception as e:
        logger.exception(f"Ошибка при чтении файла: {path}")
        raise HTTPException(status_code=500, detail="Ошибка сервера при чтении файла")
