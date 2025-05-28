from typing import List

class TextStorageInterface:
    def __init__(self, file_path: str = 'app/text_storage.txt'):
        self.file_path = file_path

    def add_text(self, text: str) -> None:
        with open(self.file_path, 'a', encoding='utf-8') as f:
            f.write(text + '\n')

    def get_texts(self) -> List[str]:
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return [line.rstrip('\n') for line in f]
        except FileNotFoundError:
            return []

    def clear(self) -> None:
        """Очищает файл хранения текста."""
        open(self.file_path, 'w', encoding='utf-8').close()
