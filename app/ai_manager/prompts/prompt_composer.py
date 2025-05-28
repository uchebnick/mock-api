from ..utils import prompt_utils
from typing import List, Dict
import logging

logger = logging.getLogger("ai_manager.prompts.composer")

class PromptComposer:
    def __init__(self, component_paths: List[str], context: Dict):
        self.component_paths = component_paths
        self.context = context
        self.templates = self._load_templates()

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

    def build_prompt(self) -> str:
        full_template = "\n\n".join(self.templates)
        return prompt_utils.replace_placeholders(template=full_template, context=self.context)
