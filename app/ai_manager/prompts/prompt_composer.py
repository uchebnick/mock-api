from ..utils import prompt_utils
from typing import List, Dict, Any, Pattern
import logging
from functools import lru_cache
import re

logger = logging.getLogger("ai_manager.docs.composer")

class PromptComposer:
    def __init__(self, component_paths: List[str], context: Dict):
        self.component_paths = component_paths
        self.context = context
        self.templates = self._load_templates()

    @lru_cache
    def _load_templates(self) -> List[str]:
        templates = []
        for path in self.component_paths:
            try:
                template = prompt_utils.read_file(path)
                templates.append(template)
                logger.info(f"Загружен шаблон: {path}")
            except Exception as e:
                logger.warning(f"Не удалось загрузить шаблон {path}: {e}")
        return templates

    @lru_cache
    def _compile_pattern(self, pattern: str) -> Pattern:

        try:
            return re.compile(pattern)
        except re.error as e:
            logger.error(f"Ошибка компиляции регулярного выражения: {e}")
            return re.compile(r'\{\{(\w+)\}\}')

    def replace_placeholders(self, template: str, context: Dict[str, Any], pattern: str = r'\{\{(\w+)\}\}') -> str:
        """Replace placeholders with actual values"""
        compiled_pattern = self._compile_pattern(pattern)
        return compiled_pattern.sub(
            lambda m: str(context.get(m.group(1), "")),
            template
        )

    def build_prompt(self) -> str:
        full_template = "\n\n".join(self.templates)
        return self.replace_placeholders(template=full_template, context=self.context)
