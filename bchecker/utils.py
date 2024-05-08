import sys
from json import dump
from os import get_terminal_size
from os.path import exists
from time import time


class Colors:
    GREEN = "\033[38;5;121m"
    BGREEN = "\033[38;5;82m"
    WHITE = "\033[38;5;231m"
    LBLUE = "\033[38;5;117m"
    BYELLOW = "\033[38;5;226m"
    LYELLOW = "\033[38;5;228m"
    LPURPLE = "\033[38;5;141m"
    RED = "\033[38;5;196m"
    END = "\033[0m"


class Banner:
    @staticmethod
    def __get_spaces(text: str) -> int:
        col = get_terminal_size().columns
        ntext = max(len(line.strip()) for line in text.splitlines())
        return (col - ntext) // 2

    @classmethod
    def center(cls, text: str) -> str:
        spaces = cls.__get_spaces(text=text)
        return "\n".join(f"{' ' * spaces}{line}" for line in text.splitlines())

    @staticmethod
    def faded_text(text: str) -> str:
        lines = text.splitlines()
        red_values = range(40, 256, 15)
        return "\n".join(
            f"\033[38;2;{red};0;220m{line}\033[0m"
            for line, red in zip(lines, red_values)
        )


class UserInput:
    @staticmethod
    def get_input(prompt: str) -> str:
        return input(prompt)

    @classmethod
    def get_verbose(cls, prompt: str) -> bool:
        user_choice = cls.get_input(prompt).lower()
        return user_choice == "y"


class Config:
    @staticmethod
    def load_file(filename: str) -> list:
        if not exists(filename):
            print(
                f'\nThere is no such file "{Colors.RED}{filename}{Colors.END}" Run again ..\n'
            )
            sys.exit()
        with open(filename, "r") as file:
            return [line.strip() for line in file]

    @staticmethod
    def save_results(results, config_file: str) -> None:
        with open(config_file, "a", encoding="utf8") as file:
            dump(results, file, indent=4, ensure_ascii=False)
            file.write("\n\n")
        print(
            f'\n{Colors.BYELLOW}Output saved successfully as{Colors.END} "{Colors.LPURPLE}{config_file}{Colors.END}"'
        )

    @staticmethod
    def time_taken(started_time: float) -> str:
        elapsed = round((time() - started_time), 2)
        if elapsed < 60:
            return (
                f"{elapsed} seconds!"
                if elapsed >= 1
                else f"{round(elapsed * 1000)} milliseconds!"
            )
        minutes, seconds = divmod(int(elapsed), 60)
        return f"{minutes} minutes {seconds} seconds!"
