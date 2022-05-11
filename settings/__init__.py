import os
from pathlib import Path


BASE_DIRECTORY = Path(__file__).resolve().parent.parent

LESSONS_FOLDER = 'lessons'

LESSONS_LIST = [
    'first',
    'second',
    'third',
    'fourth',
    'fifth',
    'fifth_improved'
]

def initialize() -> None:
    os.system('')  # Allows colorized text