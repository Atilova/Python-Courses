import msvcrt
from typing import (
    List,
    Tuple,
    Any
)
from threading import (
    Thread,
    Event
)


def print_list(list_to_print: List[Any]) -> None:
    print(*list_to_print, sep='\r\n')

def round_result(number: int | float) -> int | float:    
    rounded_number = round(number, 3)
    if rounded_number % 1 == 0:
        rounded_number = int(number)
    return rounded_number    

def request_numbers_inline(*values_to_request: str | None) -> List[int | float]:
    is_count_set = values_to_request or False
    if is_count_set:
        prompt = 'Enter: ' + ', '.join(values_to_request) + ' = '
    else:
        prompt = 'Enter so numbers, as you want: ' 
    if len(number_list := input(prompt).split()) != len(values_to_request) and is_count_set:
        print('Please enter requested numbers count')
        return request_numbers_inline(*values_to_request)
    try:
        result = [
            round_result(float(number.replace(',', '.'))) 
            for number in number_list
        ]
    except ValueError:
        print('You should enter numbers only')
        return request_numbers_inline(*values_to_request)
    return result

def request_numbers(numbers_to_request: int=2, user_message: str | None=None) -> Tuple[int | float]:
    def get_user_input() -> int | float:
        prompt = 'Enter a number: ' if user_message is None or user_message == '' else user_message
        try:
            number = float(input(prompt).replace(',', '.'))
            if number % 1 == 0:
                number = int(number)
            return number
        except ValueError:
            print('You should enter a number')
            return get_user_input()
    return tuple(get_user_input() for _ in range(numbers_to_request))
    
def wait_key(key: str='q', message: str | None='Quiting...') -> Event:
    event = Event()
    def key_waiter():
        while not event.is_set():
            if msvcrt.kbhit() and msvcrt.getch().decode() == key:                
                event.set()
                if message is not None:
                    print(message)
    Thread(target=key_waiter, daemon=True).start()
    return event