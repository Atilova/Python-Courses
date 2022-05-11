from random import randint
from datetime import datetime
from beautifultable import BeautifulTable
from collections import deque
from inspect import cleandoc
from math import floor
from abc import (
    ABC,
    abstractmethod
)
from typing import (
    Literal,
    Tuple,
    Type,
    Dict,
    Any,
    List
)
from lessons.sixth.database.connector import Database
from lessons.sixth.static import (
    GameType,
    AnswerType,
    GameLevel,
    AUTH_MESSAGES,
    DEFAULT_GAME_MESSAGES,
    USER_COMPLEXITY_LEVELS,
    USER_GAME_MESSAGES,
    COMPUTER_GAME_MESSAGES,
    COMPUTER_COMPLEXITY_LEVELS
)


class GameHelper(ABC):            
    def __init__(
        self, 
        database, 
        user, 
        game_type,
        game_message: Dict[str, str], 
        levels: Dict[str, Tuple[int, int]]
    ) -> None:
        self.user = user
        self.database = database
        self.game_messages = game_message
        self.levels = levels
        self.complexity = self.__define_complexity()
        self.game = self.database.start_game(
            game_type,
            getattr(GameLevel, self.complexity[0]),
            self.user.id
        )
    
    def run(self) -> None:
        started_at = datetime.now()
        self._execute()        
        self.database.finish_game(
            self.game.id, 
            datetime.now() - started_at
        )

    def __call__(self, message_key: str, use_return: Literal[True , False]=False, **formatting: Dict[str, Any]) -> None | str:
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

    def _add_attempt(self, penalty, suppose, response) -> None:
        self.database.add_attempt(
            self.game.id,
            penalty,
            suppose,
            response
        )

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


class ComputerGuessGame(GameHelper):
    def __init__(self, database, user) -> None:
        self.used = set()
        super().__init__(
            database,
            user,
            GameType.COMPUTER_GUESSES,
            COMPUTER_GAME_MESSAGES,
            COMPUTER_COMPLEXITY_LEVELS
        )

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
            
    def __check_response(self, computer_supposes: int, message_key: str) -> Type[AnswerType]:
        user_sign = self.__get_user_response(message_key, computer_supposes)
        match user_sign:
            case 'bigger' | '>' | 'smaller' | '<':
                if user_sign in ('bigger', '>'):
                    if computer_supposes == self.complexity[1][1]:
                        return AnswerType.OUT_OF_RANGE
                    return AnswerType.BIGGER
                else:
                    if computer_supposes == self.complexity[1][0]:
                        return AnswerType.OUT_OF_RANGE
                    return AnswerType.SMALLER
            case 'yes' | 'y':
                return AnswerType.GUESSED
            case _:
                self('wrong_response', number=computer_supposes)
                return self.__check_response(computer_supposes, message_key)

    def _run_easy_level(self) -> None:
        def check_response(computer_supposes) -> Type[AnswerType]:
            user_sign = self.__get_user_response('easy_guess', formatting=computer_supposes)
            match user_sign:
                case 'yes' | 'y':
                    self._add_attempt(False, computer_supposes, AnswerType.GUESSED)
                    return AnswerType.GUESSED
                case 'no' | 'n':
                    total_number_count = abs(self.complexity[1][1] - self.complexity[1][0]) + 1
                    if total_number_count == len(self.used):  # Check if all of possibilities were tried
                        self._add_attempt(True, computer_supposes, AnswerType.CHEATED)
                        return AnswerType.CHEATED
                    self._add_attempt(False, computer_supposes, AnswerType.INCORRECT)    
                    return AnswerType.INCORRECT                        
                case _:
                    self('wrong_response', number=computer_supposes)
                    return check_response(computer_supposes)                        
        
        break_response = (AnswerType.GUESSED, AnswerType.CHEATED)
        while (state := check_response((suppose := self.__get_random(*self.complexity[1])))) not in break_response:
            pass
        if state == AnswerType.GUESSED:
            return self('computer_guessed', number=suppose)
        self('user_cheated')

    def _run_advanced_level(self) -> None:            
        positions = [*self.complexity[1]]
        while True:
            suppose = self.__get_random(*positions)
            match (response := self.__check_response(suppose, 'advanced_guess')):
                case AnswerType.GUESSED:
                    self._add_attempt(False, suppose, response)
                    self('computer_guessed', number=suppose)
                    break
                case AnswerType.BIGGER:                    
                    positions[0] = suppose
                case AnswerType.SMALLER:                                        
                    positions[1] = suppose
                case AnswerType.OUT_OF_RANGE:                     
                    self._add_attempt(True, suppose, response)
                    self('cheated_on_range')
                    break
            self._add_attempt(False, suppose, response)
            if positions[1] - positions[0] <= 1:
                self._add_attempt(True, suppose, AnswerType.CHEATED)
                self('user_cheated')
                break

    def _run_hard_level(self) -> None:
        positions = [*self.complexity[1]]
        suppose = positions[1]
        while True:
            self.used.add(suppose)
            match (response := self.__check_response(suppose, 'advanced_guess')):
                case AnswerType.GUESSED:
                    self._add_attempt(False, suppose, response)
                    self('computer_guessed', number=suppose)
                    break
                case AnswerType.BIGGER:
                    positions[0] = suppose
                case AnswerType.SMALLER:
                    positions[1] = suppose
                case AnswerType.OUT_OF_RANGE:
                    self._add_attempt(True, suppose, response)
                    self('cheated_on_range')
                    break                
            self._add_attempt(False, suppose, response)
            suppose = floor((positions[1]+positions[0]) / 2)   
            if positions[1] - positions[0] <= 0 or suppose in self.used:
                self._add_attempt(True, suppose, AnswerType.CHEATED)
                self('user_cheated')
                break            


class UserGuessGame(GameHelper):    
    def __init__(self, database, user) -> None:
        self.guesses = []
        super().__init__(
            database,
            user,
            GameType.USER_GUESSES,
            USER_GAME_MESSAGES,
            USER_COMPLEXITY_LEVELS
        )

    def _execute(self) -> None:
        start, stop = self.complexity[1]
        self.positions = [start, stop]
        self.guessed = randint(start, stop)
        self('say_range', min_number=start, max_number=stop)
        self('help')
        self._start_level(self.complexity[0].lower())

    def __analyze_user_response(self, user_supposes) -> Type[AnswerType]:
        response, fine = AnswerType.GUESSED, False
        if user_supposes <= self.positions[0] or user_supposes >= self.positions[1]:
            self('fine')
            fine = True
        if user_supposes < self.guessed:
            response = AnswerType.BIGGER                
            self.positions[0] = user_supposes if not fine else self.positions[0]
        elif user_supposes > self.guessed:
            response =AnswerType.SMALLER
            self.positions[1] = user_supposes if not fine else self.positions[1]
        self._add_attempt(fine, user_supposes, response)
        return response

    def _run_easy_level(self) -> None:
        while (suppose := self._get_exactly_int(self('user_guess', use_return=True))) != self.guessed:
            if suppose < self.guessed:
                self._add_attempt(False, suppose, AnswerType.BIGGER)
                self('bigger')  
            else: 
                self._add_attempt(False, suppose, AnswerType.SMALLER)
                self('smaller')
        self._add_attempt(False, suppose, AnswerType.GUESSED)
        self('user_guessed', number=suppose)

    def _run_hard_level(self) -> None:
        while (
            response := self.__analyze_user_response(
                self._get_exactly_int(self('user_guess', use_return=True))
            )
        ) != AnswerType.GUESSED:
            self('bigger') if response == AnswerType.BIGGER else self('smaller')
        self('user_guessed_hard_improved', number=self.guessed)


class App():    
    def __init__(self) -> None:
        self.database  = Database()                
        self.make_call = self.__select_auth_action
        self.cancel_words = ('quit', 'q')
    
    def __call__(self, message_key: str, *formatting: Tuple[Any], use_print=True) -> None:
        message = AUTH_MESSAGES.get(message_key)
        if formatting is not None:
            message = message.format(*formatting)
        if not use_print:
            return message
        print(message)

    def get_input(self, message_key: str, use_lower=False) -> str:
        result = input(self(message_key, use_print=False)).strip()
        return result.lower() if use_lower else result

    def __call_next(self) -> Any:
        while self.make_call is not None:
            yield self.make_call()

    def run(self) -> None:
        self.database.migrate()
        deque(self.__call_next())            

    def __select_auth_action(self) -> None:
        self('select_type')
        while (action := self.get_input('select_action', use_lower=True)) not in ('register', 'r',  'login', 'l'):
            pass
        self.make_call = self.__make_authentication if action in ('login', 'l') else  self.__register_new_user

    def __cancel_auth_action(self) -> None:
        if input(self('auth_cancel', use_print=False)).strip().lower() in self.cancel_words:
            self.make_call = self.__select_auth_action
            return True
        return False

    def __make_authentication(self) -> None:        
        if self.__cancel_auth_action():
            return
        username, password = self.get_input('auth_user_username'), \
                             self.get_input('auth_user_password')   
        user = self.database.authenticate_user(username, password)
        if user != -1:
            self.user = user
            self.make_call = self.__select_game_action
        else:
            self('auth_incorrect')    
        
    def __register_new_user(self) -> None:
        if self.__cancel_auth_action():
            return
        gamename = self.get_input('register_gamename')        
        while self.database.check_for_user((username := self.get_input('register_username'))) is not None:
            self('register_username_taken')
        while (password := self.get_input('register_password')) != self.get_input('register_password_confirm'):
            self('register_password_not_matching')
            if self.__cancel_auth_action():
                return                
        self.user = self.database.create_new_user(gamename, username, password)
        self.make_call = self.__select_game_action

    def __build_games_table(self, games: List, table_type: str, extra_message: str | None=None) -> None:
        def make_formatting(data, handler):
            if handler is not None:
                return handler[0](data)
            return data    
        
        if not games:
            return self('no_games')

        table = BeautifulTable(detect_numerics=False)
        title = extra_message or '' 
        match table_type:
            case 'USER':
                title += 'USER GUESSES'                
                fields_object = {
                    'id': ('Id',),
                    'points': ('Points',),
                    'bits_mask': ('Bits',),
                    'total_fine': ('Fine',),
                    'level': ('Level', lambda data: data()),
                    'guessed_in': ('Guessed In (s)', lambda data: f'{data.total_seconds():.0f}s')
                }            
            case  'COMPUTER':            
                title += 'COMPUTER GUESSES'
                fields_object = {
                    'id': ('Id',),
                    'points': ('Points',),
                    'level': ('Level', lambda data: data()),
                    'guessed_in': ('Guessed In (s)', lambda data: f'{data.total_seconds():.0f}s')
                }
            case 'ATTEMPTS':
                title += 'GAME ATTEMPTS'
                fields_object = {
                    'suppose': ('Suppose',),
                    'penalty': ('Penalty', lambda data: '🟥' if data else '🟩'),
                    'response': ('Response', lambda data: data())                    
                }
            case _:
                return -1        
        print('\r\n', title)
        table.columns.header = [value[0] for value in fields_object.values()]        
        for game in games:
            table.rows.append([
                make_formatting(getattr(game, key), (value[1:] or None))                                
                for key, value in fields_object.items()
            ])            
        print(table, '\r\n')        

    def __select_game_action(self) -> None:        
        def get_games() -> List:
            if not (games := self.database.get_all_games(self.user.username)):
                self('no_games')
                return False
            return games    

        def get_user_games(games: List) -> List:
            games = filter(
                lambda game: game.game_type is GameType.USER_GUESSES, 
                games
            )
            return games
        
        self('auth_success', self.user.gamename)
        while True:            
            self('main_action_helper')        
            action = self.get_input('select_action')
            match action[:1] if action.endswith(')') else action:
                case '1':
                    if not (games := get_games()):
                        continue
                    games = get_user_games(games)    
                    self.__build_games_table(
                        sorted(games, key=lambda game: (-game.points, game.id))[:3],
                        'USER'
                    )
                case '2':                    
                    if not (games := get_games()):
                        continue
                    user_guesses = list(get_user_games(games))
                    computer_guesses = set(games) - set(user_guesses)
                    self.__build_games_table(
                        sorted(computer_guesses, key=lambda user_game: user_game.id),
                        'COMPUTER'
                    )
                    self.__build_games_table(
                        user_guesses,
                        'USER'
                    )
                case '3':
                    game_id = self.get_input('enter_game_id')
                    if (game := self.database.get_game(game_id)) is None or game.user_id != self.user.id:
                        self('incorrect_game_id')
                        continue
                    
                    self.__build_games_table(
                        self.database.get_game_attempts(game.id),
                        'ATTEMPTS',
                        extra_message=f'{game.game_type()}({game.id}): '
                    )
                case '4':
                    self('select_game')
                    match self.get_input('select_game_input'):
                        case '1':
                            game = ComputerGuessGame(self.database, self.user)
                        case '2':
                            game = UserGuessGame(self.database, self.user)
                        case _:
                            self('select_game_input')
                            continue
                    game.run()
                    print()
                    self('main_menu')
                case '5':
                    if self.get_input('auth_logout_confirm') in ('yes', 'y'):
                        break
                case _:
                    self('action_not_exists')
        self.make_call = None              


SETUP = {
    'description': 'Python more Class features',
    'solved': [
        {'callback': App().run, 'title': 'Games app'}
    ]
}