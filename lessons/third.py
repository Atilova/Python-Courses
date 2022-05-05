from json import dumps
from assets import support
from functools import reduce
from assets.colors import colorize
from random import randint
from typing import (
    Dict,
    List,
    Literal,
    Tuple
)


def create_even_only_list() -> None:
    a, b = support.request_numbers_inline('a', 'b')
    support.print_list([
        value 
        for value in range(a, b+1)
        if not value % 2
    ])

def create_numbers_degree_list() -> None:  
    a, b = support.request_numbers_inline('a', 'b')
    support.print_list([
        value**2 
        for value in range(a, b+1)    
    ])

def even_odd_dictionary() -> None:
    a, b = support.request_numbers_inline('a', 'b')
    result = {
        value: str(not value % 2)
        for value in range(a, b+1)
    }
    print(dumps(result, indent=2, default=str))

def create_random_numbers_list(use_print: Literal[True]=True) -> List[int]:
    total_count, start, stop = support.request_numbers_inline('N', 'start', 'stop')
    result = [
        randint(int(start), int(stop)) 
        for _ in range(total_count)
    ]
    if use_print:
        support.print_list(result)
    return result
  
def create_set_divided_by_ten() -> None:
    total_count, start, stop = support.request_numbers_inline('N', 'start', 'stop')
    support.print_list(set(
        (x := randint(start, stop), x % 10)
        for _ in range(total_count)
    ))

def sort_user_list() -> None:
    colorize('<orange>Enter Q/q to escape</orange>\r\n')
    user_list = []
    while (user_input := input('Enter number to add: ')).lower() != 'q':
        try:    
            user_list.append(support.round_result(float(user_input)))
        except ValueError:
            print('Please enter exactly a number!')
    support.print_list(sorted(user_list))


def sort_user_list_by_digits() -> None:
    random_list = create_random_numbers_list(use_print=False)
    support.print_list(sorted(random_list, key=lambda item: (len('%s' % item), -item)))

def sort_dictionary_by_values_reversed() -> None:
    some_dictionary: Dict[str, str] = {
        'name': 'Joy',
        'sex': 'mail',
        'surname': 'Doe',
        'state': 'California',
        'email': 'john@doe.com',
        'parents': 'both'
    }    
    print(dumps(
        dict(sorted(some_dictionary.items(), key=lambda pair: pair[1], reverse=True)),
        indent=2,
        default=str
    ))

def multiplicate_any_wrapper():
    def multiplicate_any(*numbers: Tuple[int]) -> int:
        return reduce(lambda total, current: total*current, numbers)

    numbers_to_multiplicate = support.request_numbers_inline()
    print(
        (' * '.join(map(str, numbers_to_multiplicate))), 
        '=', 
        multiplicate_any(*numbers_to_multiplicate)
    )

def print_square_wrapper() -> None:
    def print_square(side_length: int=8) -> None:
        colors = ('⬜', '⬛')    
        line = [colors[index & 1] for index in range(side_length)]        
        lines = (
            ' '.join(line),
            ' '.join(map(lambda item: (colors[0] if item == colors[1] else colors[1]), line))
        )
        square = [
            (lines[0] if index & 1 else lines[1])
            for index in range(side_length)
        ]
        print('', *square, sep='\r\n')
    print_square(*support.request_numbers(
        numbers_to_request=1, 
        user_message='Enter side length: '
    ))  

def create_firtree_wrapper() -> None:
    def create_firtree(rows_count: int=3, fill_with: str='*') -> None:        
        row_size = 3
        increase_row_size_by = 1
        increase_next_row_line = int(4 / len(fill_with))
        increase_next_line_with = fill_with*increase_next_row_line
        current_row_line = fill_with
        firtree = []
        for row in range(rows_count):
            next_row = []
            for _ in range(row_size):
                next_row.append(current_row_line)
                current_row_line += increase_next_line_with
            row_size += increase_row_size_by
            current_row_line = current_row_line[10:]
            firtree.extend(next_row)
        biggest_line = len(firtree[-1]) + 10
        print(*[
            colorize((
                '<green>{}</green>'.format(
                    (' ' * int((biggest_line-len(line)) / 2)) + line
                )
            ), use_print=False)
            for line in firtree
        ], sep='\r\n')

    
    create_firtree(
        *support.request_numbers(numbers_to_request=1, user_message='Enter rows count: '),
        input('Enter digit to draw with: ')
    )


SETUP = {
    'description': 'List comprehension, sort methods & function basics',
    'solved': [
        {'callback': create_even_only_list, 'title': 'Create even numbers list'},
        {'callback': create_numbers_degree_list, 'title': 'Create numbers degree list'},
        {'callback': even_odd_dictionary, 'title': 'Create dictionary full with even/odd'},
        {'callback': create_random_numbers_list, 'title': 'Create list of N random numbers'},
        {'callback': create_set_divided_by_ten, 'title': 'Create set of reminder divided by ten'},
        {'callback': sort_user_list, 'title': 'Sort user list'},
        {'callback': sort_user_list_by_digits, 'title': 'Sort user list by digits & values'},
        {'callback': sort_dictionary_by_values_reversed, 'title': 'Sort dictionary by values'},
        {'callback': multiplicate_any_wrapper, 'title': 'Multiplicate any numbers'},
        {'callback': print_square_wrapper, 'title': 'Print chess square'}, 
        {'callback': create_firtree_wrapper, 'title': 'Let\'s create a firtree'}
    ]
}