from assets import support
from time import sleep


def run_first() -> None:
    first_number, second_number = support.request_numbers()
    print('Multiplication result -> ', support.round_result(first_number*second_number))

def run_second() -> None:
    def make_devision(
        first_number: int | float, 
        second_number: int | float
    ) -> float | int | str:
        try:
          return support.round_result(first_number/second_number)
        except ZeroDivisionError:
            return 'Error'  
  
    first_number, second_number = support.request_numbers()
    to_format = f'{make_devision(first_number, second_number)}, {make_devision(second_number, first_number)}'
    result = f"""\
        Substraction -> {abs(first_number-second_number)}
        Division -> {to_format}
        Degree -> {support.round_result(first_number**second_number)}, {support.round_result(second_number**first_number)}
    """
    print(result)

def run_third() -> None:
    first_number, second_number = support.request_numbers()
    result = f'Numbers are equal, {first_number}'
    if first_number > second_number:
        result = f'First number is greater, {first_number}'
    elif first_number < second_number:
        result = f'Second number is greater, {second_number}'
    print(result)  

def run_fourth() -> None:  
    number = support.request_numbers(numbers_to_request=1)[0]
    print(f'{number} is an {"Even" if not number % 2 else "Odd"} number')
    sleep(1)

def print_range(to_print: range) -> None:
  print(*to_print, sep='\r\n')

def run_fifth() -> None:
    print_range(range(10, 21))

def run_sixth() -> None:
    print_range(range(100, 111, 2))

def run_seventh() -> None:
    print_range(reversed(range(15, 21)))
    # print_range((range(20, 14, -1)))  The same, as above 

def run_eighth() -> None:
    emoji_list = [
        '1: 😛', '2: 🤐', '3: 😎', '4: 😁', '5: 😂', '6: 😊', '7: 🤣', '8: 👌', '9: 👏', '10: 👀'
    ]
    print(
        emoji_list[0], 
        emoji_list[-1],
        emoji_list[5],
        emoji_list[:3],
        emoji_list[-4:],
        emoji_list[1::2],
        sep='\r\n'
    )

SETUP = {
    'description': 'Python basics, data types and range function',
    'solved': [
        {'callback': run_first, 'title': 'Math multiplication'},
        {'callback': run_second, 'title': 'Math operations'},
        {'callback': run_third, 'title': 'Who is greater?'},
        {'callback': run_fourth, 'title': 'Even or Odd number'},
        {'callback': run_fifth, 'title': 'Range: 10 - 20'},
        {'callback': run_sixth, 'title': 'Range: 100 - 110, step: 2'},
        {'callback': run_seventh, 'title': 'Reversed range: 20 - 15'},
        {'callback': run_eighth, 'title': 'Random list manipulation'}
    ]
}