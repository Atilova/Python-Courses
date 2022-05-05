from random import randint
from assets import support
from time import sleep
from assets.colors import colorize


def run_ninth() -> None:  
    random_number = randint(1, support.request_numbers(
        numbers_to_request=1, 
        user_message='Enter number to define random range: '
    )[0])
    while random_number != (requested := support.request_numbers(numbers_to_request=1, user_message='Try to guess: ')[0]):
        print('Bigger...' if random_number > requested else 'Smaller...')
    colorize('<rose>You win, hurray!!</rose>')  

def run_tenth() -> None:
    my_list = [1, 2, 3, 4, 5, 9, 4, 2, 8, 9, 2, 7, 5]
    print(my_list, list(dict.fromkeys(my_list)), sep='\r\n')

def run_eleventh() -> None:
    requested = support.request_numbers(numbers_to_request=1, user_message='Enter number to handle in loop: ')[0]
    for number in range(10, requested+1):
        if not number % 10:
            print(number, ' | -> ', number**number)

def run_twelfth() -> None:
    string = input('Type something to count every symbol: ').lower()
    total_result = [
        f'{symbol.upper() if symbol != " " else "Spaces"}: {string.count(symbol)}'
        for symbol in set(string)
    ]
    print(*total_result, sep='\r\n')

def run_thirteenth() -> None:
    default_line = '|$_^_$_*_ || _$_*_*__|'  
    lines = [default_line, default_line[::-1]]
    event = support.wait_key()
    print('Press q to stop')
    while not event.is_set():    
        print(lines[0])
        lines[0], lines[1] = lines[1], lines[0]
        sleep(0.4);


SETUP = {
    'description': 'Python list, random numbers & user input',
        'solved': [
        {'callback': run_ninth, 'title': 'Computer game, try to guess the number'},
        {'callback': run_tenth, 'title': 'Clear duplicated values in list'},
        {'callback': run_eleventh, 'title': 'Handle inside loop'},
        {'callback': run_twelfth, 'title': 'Count symbols in string'},
        {'callback': run_thirteenth, 'title': 'Reversed string printing'}
    ]
}