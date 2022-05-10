from os.path import join
from settings import BASE_DIRECTORY


DATABASE = {
    'ENGINE': 'sqlite',
    'NAME': join(BASE_DIRECTORY, 'sixth.db')
}