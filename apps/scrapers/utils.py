import re
from datetime import datetime

def string_to_words_list(text):
    '''
    TODO: dodać wsparcie apostrphe
    http://stackoverflow.com/questions/2596893/regex-to-match-words-and-those-with-an-apostrophe
    '''
    return re.findall('\w+', text)

def string_to_date(text):
    return datetime.strptime(text, '%Y-%m-%d')

