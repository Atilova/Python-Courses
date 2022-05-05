from assets import support
from assets.colors import colorize
from time import time
from random import randint
from enum import (
    Enum,
    auto
)
from typing import (
    Any,
    List,
    Tuple,
    Type
)


def print_any_wrapper() -> None:            
    def print_any(*args: Any) -> None:
        print('', *args, sep='\r\n')
    print_any(*input('Enter some text: ').split())    

def print_date_wrapper() -> None:
    def print_date(date, month, year) -> None:
        print(f'Date -> {date}\r\nMonth -> {month}\r\nYear ->{year}')
    print_date(*support.request_numbers_inline('Date', 'Month', 'Year'))

def guess_game_wrapper() -> None:
    class WrongInputError(Exception):
        def __init__(self, message: str) -> None:
            self.message = message
            super().__init__(self.message)


    class TooLargeValueError(Exception):
        def __init__(self, message: str) -> None:
            self.message = message
            super().__init__(self.message)


    def request_numbers(request: List[str] | Tuple[str] | int) -> List[int]:
        WRONG_INPUT_MESSAGE = colorize(
            '<red>You should enter exactly a number!</red>',
            use_print=False
        )

        def get_input(message: str) -> int | float:
            user_input = input(message)
            try:
                if not (number := float(user_input)) % 1:
                    number = int(number)
                return number
            except ValueError:
                raise(WrongInputError(WRONG_INPUT_MESSAGE))

        # Error Handler
        def make_request(message: str | None=None) -> int | float:
            if message is None:
                message = 'Enter a number: '
            try:
                number = get_input(message)
            except WrongInputError as error:
                print(error)
                return make_request(message)
            return number
        if type(request) is int:
            return [make_request() for _ in range(request)]
        return [make_request(request_message) for request_message in request]

    # Game loop
    def guess_game() -> None:
        MAX_NUMBER_VALUE = 1_000_000

        def specify_range() -> List[int]:
            try:
                random_range = support.request_numbers_inline('START', 'STOP')
                start, stop = random_range
                if start >= stop:
                    raise WrongInputError('Range (START) should be smaller, then range (STOP)')
                if stop > MAX_NUMBER_VALUE:
                    raise TooLargeValueError(f'Range (STOP) should be smaller, then max - {MAX_NUMBER_VALUE}')
            except TooLargeValueError as error:
                print(error)
                return specify_range()
            except WrongInputError as error:
                print(error)
                return specify_range()
            return random_range    

        guessed_number = randint(*specify_range())
        while (user_guess := request_numbers(('Enter number to guess: ',))[0]) != guessed_number:
            print("Bigger..." if guessed_number > user_guess else "Smaller...")
        colorize(f'<blue>Hurray, you win! - {guessed_number}</blue>')        
    guess_game()

def join_input() -> None:
    print(
        ', '.join(
            map(str, support.request_numbers(
                *support.request_numbers(
                    numbers_to_request=1, 
                    user_message='Enter total count: '
                )
            ))
        )
    )

def join_data_types() -> None:
    data_list = [
        True,
        'String',
        3.14,
        lambda x: print(x),
        32,
        None
    ]
    print(' | '.join(map(str, data_list)))


def guess_number_wrapper() -> None:
    class GameState(Enum):
        SMALLER = auto()
        BIGGER = auto()
        GUESSED = auto()


    class IncorrectRange(Exception):
        def __init__(self, message: str) -> None:
            self.message = message
            super().__init__(self.message)


    GAME_MESSAGES = {
        'input_message': 'Enter number to computer guess: ',
        'incorrect_max_input': 'Your number should be smaller or equal, then max: {}',
        'incorrect_min_input': 'Your number should be bigger or equal, then min: {}',
        'computer_guessed': '<orange>Computer guessed: {number} in {attempts} attempts</orange>',
        'time_took': 'Program finished in {}'
    }

    def check_response(
        guessed_number: int,
        computer_suppose: int
    ) -> Type[GameState]:
        if computer_suppose < guessed_number:
            return GameState.BIGGER
        elif computer_suppose > guessed_number:
            return GameState.SMALLER
        else:
            return GameState.GUESSED

    def guess_number() -> None:
        MAX_NUMBER = 100_000_000_000
        MIN_NUMBER = -100_000_000_000

        def request_to_guess() -> int:
            to_guess = support.request_numbers(
                numbers_to_request=1,
                user_message=GAME_MESSAGES['input_message']
            )[0]
            try:
                if to_guess > MAX_NUMBER:
                    raise IncorrectRange(
                        GAME_MESSAGES['incorrect_max_input'].format(MAX_NUMBER)
                    )
                elif to_guess < MIN_NUMBER:
                    raise IncorrectRange(
                        GAME_MESSAGES['incorrect_min_input'].format(MIN_NUMBER)
                    )
            except IncorrectRange as error:
                print(error)
                return request_to_guess()
            return to_guess

        attempts = 0
        guessed = request_to_guess()
        position = [MIN_NUMBER, MAX_NUMBER]
        time_started = time()
        while (suppose := (position[1]+position[0]) / 2) != guessed:
            # print(suppose, position)
            match check_response(guessed, suppose):
                case GameState.BIGGER:
                    position[0] = suppose
                case GameState.SMALLER:
                    position[1] = suppose
            attempts += 1
        time_took = time() - time_started
        colorize(GAME_MESSAGES['computer_guessed'].format(
            number=suppose,
            attempts=attempts
        ))
        print(GAME_MESSAGES['time_took'].format(time_took))
    guess_number()


SETUP = {
    'description': 'Python features',
    'solved': [
        {'callback': print_any_wrapper, 'title': 'Print any data separately'},
        {'callback': print_date_wrapper, 'title': 'Print date'},
        {'callback': guess_game_wrapper, 'title': 'Try to guess the number'},
        {'callback': join_input, 'title': 'Join user input'},
        {'callback': join_data_types, 'title': 'Join list with multiple data types'},
        {'callback': guess_number_wrapper, 'title': 'Computer tries to guess user number'}
    ]
}