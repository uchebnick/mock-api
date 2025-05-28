import subprocess
from typing import Tuple

class TerminalInterface:
    def execute_command(self, command: str, shell: bool = True) -> Tuple[str, str]:
        """
        Выполняет команду в терминале и возвращает (stdout, stderr).
        """
        try:
            result = subprocess.run(command, shell=shell, capture_output=True, text=True)
            return result.stdout, result.stderr
        except Exception as e:
            return "", f"Terminal error: {e}"

    def get_commands(self):
        commands = {
            "execute_command": self.execute_command
        }
        return commands
