import subprocess
from typing import Tuple


class TerminalInterface:
    @classmethod
    def execute_command(cls, command: str, shell: bool = True) -> Tuple[str, str]:
        try:
            result = subprocess.run(
                command, shell=shell, capture_output=True, text=True
            )
            return result.stdout, result.stderr
        except Exception as e:
            return "", f"Terminal error: {e}"

    @classmethod
    def get_commands(cls):
        commands = {"execute_command": cls.execute_command}
        return commands
