from typing import Literal


class IncorrectTextDecorration(Exception):
    def __init__(self, message :str='You used incorrect text decoration') -> None:
        self.message = message
        super().__init__(self.message)


def colorize(text: str, use_print: Literal[True]=True) -> str:
    END = '\033[0m'
    colors_table = {
        'blue': '\033[94m',
        'rose': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'green': '\033[92m',
        'orange': '\033[93m',
        'gray': '\033[90m',
        'red': '\033[91m'    
    }

    tags_order = []
    while (tag_top_index := text.find('<')) >= 0:
        tag_end_index = text.find('>')
        tag = text[tag_top_index+1:tag_end_index].lower()

        def replace_with(replacer: str) -> str:
            return text[:tag_top_index] + replacer + text[tag_end_index+1:]

        if tag.startswith('/'):
            tag = tag[1:]
            if not tags_order:
                raise IncorrectTextDecorration('Tag closed before being opened')
            elif tag == tags_order[-1]:
                text = replace_with(END)
                tags_order.pop()
            else:  
                raise IncorrectTextDecorration('Incorrect tag closure sequence')
        else:  
            if (color_with := colors_table.get(tag)) is None:
                raise IncorrectTextDecorration('Incorrect tag name')
            text = replace_with(color_with)
            tags_order.append(tag)

    if tags_order:
        raise IncorrectTextDecorration('Tag(s) left which were never closed')

    if use_print:
        print(text)
    return text