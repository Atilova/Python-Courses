import sys
import settings
from assets.colors import colorize
from time import (
  sleep
)
from itertools import zip_longest
from typing import (
    List, 
    Dict,
    Any, 
    Callable
)
from assets.static import USER_MESSAGES


class Controller():
    class IncorrectRange(Exception):
        def __init__(self, message: str='Incorrect range definition') -> None:
            self.message = message
            super().__init__(self.message)


    def __init__(self) -> None:
        self.lessons = {}    
        for module in settings.LESSONS_LIST:
            try:
                setup = __import__(
                    f'{settings.LESSONS_FOLDER}.{module}', 
                    fromlist=['object']
                ).SETUP
                self.lessons[module] = setup
            except ImportError as error:
                colorize(USER_MESSAGES['import_error'].format(module))
                print(error)
                return quit()
            except AttributeError:
                colorize(USER_MESSAGES['wrong_setup'].format(module))
                return quit()

        total_errors: Dict[str, List[str]] = {}
        self.script_arguments = sys.argv[1:]
        self.solved_description_list: List[str] = []
        is_list_command = '-l' in self.script_arguments
        for lesson_name, lesson_setup in self.lessons.items():
            lesson_errors = []
            if (description := lesson_setup.get('description')) is None:
                lesson_errors.append(USER_MESSAGES['incorrect_description_setup'])
            if (solved := lesson_setup.get('solved')) is None:
                lesson_errors.append(USER_MESSAGES['incorrect_solved_setup'])
            else:
                lesson_solved_list = []
                for index, problem in enumerate(solved):
                    to_user_index = index+1
                    if (title := problem.get('title')) is None or problem.get('callback') is None:
                        lesson_errors.append(USER_MESSAGES['wrong_problem_setup'].format(to_user_index))
                    elif is_list_command and not total_errors:
                        lesson_solved_list.append(f'  {colorize(f"<blue>{to_user_index})</blue> ", use_print=False)}{title}')
            if lesson_errors:
                total_errors[lesson_name] = lesson_errors
            elif is_list_command and not total_errors:
                lessons_solved_formatted = '\r\n'.join(lesson_solved_list)
                if not lesson_solved_list:
                    lessons_solved_formatted = colorize(USER_MESSAGES['lesson_empty'], use_print=False)
                self.solved_description_list.append(
                    f'\r{colorize(f"<rose>{description}: ({lesson_name})</rose>", use_print=False)}\r\n{lessons_solved_formatted}\r\n'
                )
        if total_errors:
            colorize(USER_MESSAGES['import_failed'])
            for lesson_name, lesson_error in total_errors.items():
                colorize(USER_MESSAGES['lesson_error'].format(lesson_name))
                colorize('\r\n'.join([
                    f'  №{index+1}: {error}'
                    for index, error in enumerate(lesson_error)
                ]))        
        else:
            try:
                self.__execute()
            except KeyboardInterrupt:
                print('\r\n', colorize(USER_MESSAGES['quit'], use_print=False), sep='\r')
                return quit(0)

    def __execute(self) -> None:                
        def get_item(items_list: List[Any], item_index: int=0) -> Any:
            return (items_list[item_index:item_index+1] or (None,))[0]

        def get_list_pairs(to_pair: List[Any], pair_size: int=2) -> Dict[str, str]:
            return {key:value for key, value in zip_longest(*[iter(to_pair)] * pair_size)}
        
        def start(lessons: List[Dict[str, str | List[Dict[str, Callable]]]]) -> None:
            for lesson in lessons:
                colorize(f'<rose>{lesson["description"]}:</rose>')
                if not lesson['solved']:
                    colorize(USER_MESSAGES['lesson_empty'])
                else:        
                    for solved_problem in lesson['solved']:
                        colorize(f'<blue>№ {solved_problem["title"]}:</blue>')
                        solved_problem.get('callback')()
                        print()          
                        sleep(1)
                print()
            colorize(USER_MESSAGES['bye'])  

        def throw_error(error: str) -> None:
            colorize(error)
            return quit()
    
        match get_item(self.script_arguments):
            case None:                
                colorize(USER_MESSAGES['import_success'])    
            case '-h' :
                colorize(USER_MESSAGES['help_command'])  
            case '-l':        
                self.solved_description_list[-1] = self.solved_description_list[-1][:-2]
                print(*self.solved_description_list)
            case '--all':
                start(self.lessons.values())
            case '-r' | '--part':                                
                range_arguments = get_list_pairs(self.script_arguments)        
                if not '--part' in range_arguments:
                    throw_error(USER_MESSAGES['part_not_set'])
                if (part_name := range_arguments.get('--part')) is None:
                    throw_error(USER_MESSAGES['part_value_not_set'])
                if (lesson_part := self.lessons.get(part_name)) is None:
                    throw_error(USER_MESSAGES['incorrect_part_name'])
                total_problems_count = len(lesson_part['solved'])
                if not total_problems_count:
                    throw_error(USER_MESSAGES['lesson_empty'])

                def check_limit(number: int) -> bool:
                    return True if number >= 1 and number <= total_problems_count else False

                def define_range(pair: List[int]) -> List[int]:    
                    if len(pair) > 2:
                        raise self.IncorrectRange()

                    if get_item(pair, 1) is None:
                        pair.append(pair[0])
                    return pair

                if '-r' in range_arguments:
                    if (range_limit := range_arguments.get('-r')) is None:
                        throw_error(USER_MESSAGES['range_not_set'])          
                    limit_pairs = range_limit.split(',')
                    closed_pairs = [
                        (f'{pair}{total_problems_count}' if pair.endswith('-') else pair)
                        for pair in limit_pairs
                    ]
                    try:
                        range_pairs = [
                            define_range(pair) 
                            for pair in [list(map(int, range_pair.split('-'))) for range_pair in closed_pairs]          
                        ] 
                    except ValueError:
                        return colorize(USER_MESSAGES['wrong_range_values'])
                    except self.IncorrectRange:
                        return colorize(USER_MESSAGES['wrong_range_definition'])
                    if not all(pair[0] <= pair[1] for pair in range_pairs):
                        return colorize(USER_MESSAGES['wrong_range_order'])
                    if not all(check_limit(pair[0]) and check_limit(pair[1]) for pair in range_pairs) :
                        return colorize(USER_MESSAGES['wrong_range_bound'])
                    start([{
                      **lesson_part,
                      'solved': [
                        problem
                        for range_start, range_end in range_pairs
                        for problem in lesson_part['solved'][range_start-1:range_end]
                      ]
                    }])
                else:
                    start([lesson_part])
            case _:
                colorize(USER_MESSAGES['incorrect_argument'])


if __name__ == '__main__':
    settings.initialize()
    app_controller = Controller()  