from typing import List


class TextStorageInterface:
    @classmethod
    def add_text(cls, text: str, file_path: str = "app/text_storage.txt") -> None:
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(text + "\n")
        return "success"

    @classmethod
    def get_texts(cls, file_path: str = "app/text_storage.txt") -> List[str]:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return [line.rstrip("\n") for line in f]
        except FileNotFoundError:
            return []

    @classmethod
    def clear(cls, file_path: str = "app/text_storage.txt") -> None:
        open(file_path, "w", encoding="utf-8").close()
        return "success"

    @classmethod
    def get_commands(cls):
        commands = {
            "add_text": cls.add_text,
            "get_texts": cls.get_texts,
            "clear": cls.clear,
        }
        return commands
