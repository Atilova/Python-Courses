from enum import (
    Enum,
    auto
)


class GameType(Enum):
    COMPUTER_GUESSES = auto()
    USER_GUESSES = auto()


class AnswerType(Enum):
    SMALLER = auto()
    BIGGER = auto()
    INCORRECT = auto()
    GUESSED = auto()