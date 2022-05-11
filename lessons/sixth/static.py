from inspect import cleandoc
from typing import (
    Dict,
    List,
    Tuple,
    Any
)
from assets.colors import colorize
from enum import (
    Enum,
    auto
)


class ImprovedEnum(Enum):
    def __call__(self):
        return self.name

class GameType(ImprovedEnum):
    COMPUTER_GUESSES = auto()
    USER_GUESSES = auto()


class AnswerType(ImprovedEnum):
    SMALLER = auto()
    BIGGER = auto()
    INCORRECT = auto()
    GUESSED = auto()
    CHEATED = auto()
    OUT_OF_RANGE = auto()


class GameLevel(ImprovedEnum):        
    EASY = auto()
    ADVANCED = auto()
    HARD = auto()


AUTH_MESSAGES = {
    'select_type': colorize(cleandoc("""
        Do you have an account, or you want to register? 
            <orange>• Login / L</orange> - to sign in
            <orange>• Register / R</orange> - to sign up             
    """), use_print=False),
    'select_action': 'Select an action: ',
    'auth_user_username': 'Enter username: ',
    'auth_user_password': 'Enter password: ',
    'auth_incorrect': 'Username or password is incorrect, try again',
    'auth_cancel': 'Continue ? type Quit / Q to exit: ',        
    'auth_register': 'Let\'t register a new user',
    'register_username': 'Enter new username: ',
    'register_username_taken': 'This username is already taken',
    'register_gamename': 'Enter your gamename: ',
    'register_password': 'Enter Password: ',
    'register_password_confirm': 'Confirm password: ',
    'register_password_not_matching': 'Your passwords doesn\'t match, try again',
    'auth_logout_confirm': 'Are you sure you want to logout: Yes / Any: ',   
    'action_not_exists' : 'You selected one not actually exists',
    'auth_success': colorize('<rose>You logged in as {}</rose>', use_print=False),
    'enter_game_id': 'Enter game id: ',
    'incorrect_game_id': 'You\'ve entered incorrect game id',
    'main_action_helper': cleandoc("""
        1) Show the best games
        2) Show all games
        3) Show game attempts (Game-Id)
        4) New game
        5) Logout
    """),
    'select_game': cleandoc("""
        1) Computer guesses
        2) You guess
    """),
    'select_game_input': 'Select game: ',
    'no_games': 'You don`t have any games',
    'main_menu': 'You are back to main menu'
}

DEFAULT_GAME_MESSAGES = {
    'incorrect_level': colorize('<orange>You\'ve entered none existing level</orange>', use_print=False),
    'request_level_message': 'Level: ',
    'complexity_level': colorize(cleandoc("""            
        Select one of the followind complexity levels, please: 
        <cyan>{levels}</cyan>
    """), use_print=False),
    'selected_level': colorize('You selected: <cyan>{level}</cyan>', use_print=False),
    'integer_only': 'Your number should be exactly an integer'
}

DEFAULT_GAME_HELP = cleandoc("""
    \r\r
    Help:
        Bigger or > - means guessed number is bigger
        Smaller or < - means guessed number is smaller
        Yes or Y - computer guessed
""")

COMPUTER_GAME_MESSAGES: Dict[str, str] = {
    'easy_help': cleandoc("""
        \r\r
        Help:
            No or N - incorrect guess
            Yes or Y - computer guessed
    """),
    'advanced_help': DEFAULT_GAME_HELP,
    'hard_help': DEFAULT_GAME_HELP,
    'range_warning': colorize('<orange>Your number should be exactly in ({min_number} {max_number})</orange>', use_print=False),
    'to_guess': colorize('<green>To Guess: {number}</green>', use_print=False),
    'request_guessed': 'Enter number, so you won\'t forget it: ',
    'easy_guess': 'Is your number: {number}? ',
    'wrong_response': 'You set wrong response, try again',
    'user_cheated': colorize('<red>You cheated on a computer, no numbers left</red>', use_print=False),
    'computer_guessed': colorize('<rose>Hurray, Your number is: {number}</rose>', use_print=False),
    'cheated_on_range': colorize('<red>You cheated, your number outside the range</red>', use_print=False),
    'advanced_guess': 'Is {number} correct: '
}

COMPUTER_COMPLEXITY_LEVELS: Dict[str, Tuple[int, int]] = {
    'EASY': (-10, 10),  # Randoms only
    'ADVANCED': (-50, 50),  # Both answers & randoms
    'HARD': (-100, 100)  # Algorithm
}

USER_GAME_MESSAGES: Dict[str, str] = {
    'say_range': colorize('<orange>Computer guessed number in range ({min_number} {max_number})</orange>', use_print=False),
    'help': colorize(cleandoc("""
        \r\r
        Help:
            Computer says <rose>bigger</rose> if guessed number <rose>is bigger</rose>
            Computer says <rose>smaller</rose> if guessed number <rose>is smaller</rose>
    """), use_print=False),
    'user_guess': 'Guess a number: ',        
    'user_guessed': colorize('<rose>Hurray, you won: {number}</rose>', use_print=False),
    'bigger': 'Bigger',
    'smaller': 'Smaller',
    'fine': colorize('<red>Penalty point</red>', use_print=False),
    'user_guessed_hard_improved': colorize('<rose>Hurray, you guessed it: {number}</rose>', use_print=False),
    'user_guessed_hard': colorize(cleandoc("""
        <rose>Hurray, you guessed it: {number}</rose>
        <orange>Attempts: {attempts}</orange>
        <red>Penalty points: {points}</red>
    """), use_print=False),
    'results_help': colorize(cleandoc("""
        \r\r
        Results:
            <orange>• All</orange> - get full data
            <orange>• Bigger</orange> - get all bigger responses
            <orange>• Smaller</orange> - get all smaller responses
            <orange>• Even</orange> - get all even answers
            <orange>• Quit</orange> - to exit
    """), use_print=False),
    'select_log_level': 'Select the log level, please: ',
    'incorrect_log_level': 'You selected none existing log level, try again'
}

USER_COMPLEXITY_LEVELS: Dict[str, Tuple[int, int]] = {
    'EASY': (-100, 100),  # Game only
    'HARD': (-100, 100)  # Handle Wrong Entries
}