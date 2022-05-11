from random import randint
from beautifultable import BeautifulTable
from inspect import cleandoc
from math import floor
from enum import (
    Enum,
    auto
)
from abc import (
    ABC,
    abstractmethod
)
from typing import (
    Tuple,
    Type,
    Dict,
    Any
)

from lessons.sixth.static import (
    DEFAULT_GAME_MESSAGES,
    USER_COMPLEXITY_LEVELS,
    USER_GAME_MESSAGES,
    COMPUTER_GAME_MESSAGES,
    COMPUTER_COMPLEXITY_LEVELS
)

class GameHelper(ABC):
    def __init__(self, game_message: Dict[str, str], levels: Dict[str, Tuple[int, int]]) -> None:
        self.game_messages = game_message
        self.levels = levels
        self.complexity = self.__define_complexity()
    
    def run(self) -> None:
        self._execute()

    def __call__(self, message_key: str, use_return=False, **formatting: Dict[str, Any]) -> None | str:
        if (notification := DEFAULT_GAME_MESSAGES.get(message_key)) is None:
            notification = self.game_messages[message_key]
        if formatting is not None:
            notification = notification.format(**formatting)
        if use_return:
            return notification    
        print(notification)

    def __define_complexity(self) -> Tuple[str, int]:
        possible_levels = self.levels.keys()
        self(
            'complexity_level',
            levels=cleandoc('- ' + '\r\n - '.join(possible_levels))
        )
        while (
            complexity_level := input(self('request_level_message', use_return=True)).strip().upper()
        ) not in possible_levels:
            self('incorrect_level')

        self('selected_level', level=complexity_level)
        return (complexity_level, self.levels[complexity_level])

    def _get_exactly_int(self, request_message: str) -> int:
        def check_response(to_check: str) -> True | False:
            if to_check.startswith('-'):
                to_check = to_check[1:]
            return True if to_check.isdigit() else False


        while not check_response(number := input(request_message)):
            self('integer_only')
        return int(number) 

    def _start_level(self, complexity: str) -> None:
        getattr(self, f'_run_{complexity}_level')()

    @abstractmethod
    def _execute(self) -> None:
        ...


def guess_user_number() -> None:
    class GameState(Enum):
        GUESSED = auto()
        BIGGER = auto()
        SMALLER = ()
        INCORRECT = auto()
        CHEATED = auto()
        OUT_OF_RANGE = auto()


    class Game(GameHelper):
        def __init__(self) -> None:            
            self.used = set()
            super().__init__(COMPUTER_GAME_MESSAGES, COMPUTER_COMPLEXITY_LEVELS)
    
        def __mark_guessed_input(self) -> None:
            self('to_guess', number=self._get_exactly_int(self('request_guessed', use_return=True)))            
        
        def _execute(self) -> None:
            start, stop = self.complexity[1]
            self(
                'range_warning', 
                min_number=start,
                max_number=stop
            )
            complexity_lowered = self.complexity[0].lower()
            self.__mark_guessed_input()
            self(f'{complexity_lowered}_help')
            self._start_level(complexity_lowered)

        def __get_random(self, start: int, stop: int) -> int:
            while (number := randint(start, stop)) in self.used:
                ...
            self.used.add(number)
            return number

        def __get_user_response(self, message_key: str, formatting: int) -> str:
            return input(
                self(message_key, number=formatting, use_return=True)
            ).strip().lower()
               
        def __check_response(self, computer_supposes: int, message_key: str) -> Type[GameState]:
            user_sign = self.__get_user_response(message_key, computer_supposes)
            match user_sign:
                case 'bigger' | '>' | 'smaller' | '<':
                    if user_sign in ('bigger', '>'):
                        if computer_supposes == self.complexity[1][1]:
                            return GameState.OUT_OF_RANGE
                        return GameState.BIGGER
                    else:
                        if computer_supposes == self.complexity[1][0]:
                            return GameState.OUT_OF_RANGE
                        return GameState.SMALLER
                case 'yes' | 'y':
                    return GameState.GUESSED
                case _:
                    self('wrong_response', number=computer_supposes)
                    return self.__check_response(computer_supposes, message_key)

        def _run_easy_level(self) -> None:
            def check_response(computer_supposes) -> Type[GameState]:
                user_sign = self.__get_user_response('easy_guess', formatting=computer_supposes)
                match user_sign:
                    case 'yes' | 'y':
                        return GameState.GUESSED
                    case 'no' | 'n':
                        total_number_count = abs(self.complexity[1][1] - self.complexity[1][0]) + 1
                        if total_number_count == len(self.used):  # Check if all of possibilities were tried
                            return GameState.CHEATED
                        return GameState.INCORRECT                        
                    case _:
                        self('wrong_response', number=computer_supposes)
                        return check_response(computer_supposes)                        
            
            break_response = (GameState.GUESSED, GameState.CHEATED)
            while (state := check_response((suppose := self.__get_random(*self.complexity[1])))) not in break_response:
                pass
            if state == GameState.GUESSED:
                return self('computer_guessed', number=suppose)
            self('user_cheated')

        def _run_advanced_level(self) -> None:            
            positions = [*self.complexity[1]]
            while True:
                suppose = self.__get_random(*positions)
                match self.__check_response(suppose, 'advanced_guess'):
                    case GameState.GUESSED:
                        self('computer_guessed', number=suppose)
                        break
                    case GameState.BIGGER:
                        positions[0] = suppose
                    case GameState.SMALLER:
                        positions[1] = suppose
                    case GameState.OUT_OF_RANGE:
                        self('cheated_on_range')
                        break
                if positions[1] - positions[0] <= 1:
                    self('user_cheated')
                    break

        def _run_hard_level(self) -> None:
            positions = [*self.complexity[1]]
            suppose = positions[1]
            while True:
                self.used.add(suppose)
                match self.__check_response(suppose, 'advanced_guess'):
                    case GameState.GUESSED:
                        self('computer_guessed', number=suppose)
                        break
                    case GameState.BIGGER:
                        positions[0] = suppose
                    case GameState.SMALLER:
                        positions[1] = suppose
                    case GameState.OUT_OF_RANGE:
                        self('cheated_on_range')
                        break
                suppose = floor((positions[1]+positions[0]) / 2)   
                if positions[1] - positions[0] <= 0 or suppose in self.used:
                    self('user_cheated')
                    break            


    Game().run()    

def guess_computer_number():
    class ComputerResponse(Enum):
        BIGGER = auto()
        SMALLER = auto()
        GUESSED = auto()

        def __call__(self):
            return self.name.capitalize()


    class Game(GameHelper):    
        def __init__(self) -> None:
            self.guesses = []
            super().__init__(USER_GAME_MESSAGES, USER_COMPLEXITY_LEVELS)            

        def _execute(self) -> None:
            start, stop = self.complexity[1]
            self.positions = [start, stop]
            self.guessed = randint(start, stop)
            self('say_range', min_number=start, max_number=stop)
            self('help')
            self._start_level(self.complexity[0].lower())

        def __analyze_user_response(self, user_supposes):
            def add_entry(number: int, result: Type[ComputerResponse], fine: True | False) -> None:
                self.guesses.append({
                    'number': number, 
                    'result': result,
                    'fine': fine
                })

            response, fine = ComputerResponse.GUESSED, False
            if user_supposes <= self.positions[0] or user_supposes >= self.positions[1]:
                self('fine')
                fine = True
            if user_supposes < self.guessed:
                response = ComputerResponse.BIGGER                
                self.positions[0] = user_supposes if not fine else self.positions[0]
            elif user_supposes > self.guessed:
                response =ComputerResponse.SMALLER
                self.positions[1] = user_supposes if not fine else self.positions[1]
            add_entry(user_supposes, response, fine)
            return response

        def _run_easy_level(self):
            while (suppose := self._get_exactly_int(self('user_guess', use_return=True))) != self.guessed:
                self('bigger') if suppose < self.guessed else self('smaller')
            self('user_guessed', number=suppose)

        def _run_hard_level(self):
            while (
                response := self.__analyze_user_response(
                    self._get_exactly_int(self('user_guess', use_return=True))
                )
            ) != ComputerResponse.GUESSED:
                self('bigger') if response == ComputerResponse.BIGGER else self('smaller')

            self(
                'user_guessed_hard', 
                number=self.guessed, 
                attempts=len(self.guesses), 
                points=len(list(filter(lambda score: score['fine'], self.guesses)))
            )
            self('results_help')
            while (log_level := input(self('select_log_level', use_return=True)).strip().lower()) not in 'quit':
                match log_level:
                    case 'all':
                        to_display = self.guesses
                    case 'bigger':
                        to_display = filter(lambda score: score['result'] == ComputerResponse.BIGGER, self.guesses)
                    case 'smaller':
                        to_display = filter(lambda score: score ['result'] == ComputerResponse.SMALLER, self.guesses)
                    case 'even':
                        to_display = filter(lambda score: not score['number'] & 1, self.guesses)
                    case _:
                        self('incorrect_log_level')
                        continue

                table = BeautifulTable()
                table.columns.header = ["№", 'Guess', 'Response', 'Fine']
                for index, score in enumerate(to_display):
                    table.rows.append([
                        index+1,
                        score['number'],
                        score['result'](),
                        '❌' if score['fine'] else '✔'
                    ])
                print(table)
            
            guess_numbers = tuple(score['number'] for score in self.guesses)
            pairs = list(zip(guess_numbers, guess_numbers[1:]))
            diff_more_five = list(
                map(lambda pair: str(pair[1]), 
                    filter(
                        lambda pair: abs(pair[1] - pair[0]) >= 5, pairs
                    )
                )
            )
            print('\r\nFilter by 5 diff: ', ' -> '.join(diff_more_five))
            table = BeautifulTable()
            table.columns.header = ['Last Value', 'Next Value', 'Diff']
            for row in map(lambda pair: (*pair, abs(pair[1] - pair[0])), pairs):
                table.rows.append(row)
            print('', 'Pairs Diff Table:', table, sep='\r\n')
            table.clear(reset_columns=True)
            table.columns.header = ['Guess', 'Degree']
            for row in map(lambda number: (number, number**2), guess_numbers):
                table.rows.append(row)
            print('', 'Guesses Degree Table:', table, sep='\r\n')   


    Game().run()         


SETUP = {
    'description': 'Python Classes, map & filter',
    'solved': [
        {'callback': guess_user_number, 'title': 'Computer tries to guess an user number'},
        {'callback': guess_computer_number, 'title': 'User tries too guess a computer number'}
    ]
}