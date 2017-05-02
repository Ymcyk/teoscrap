from trans import trans
import string
import re

def string_to_words_list(text):
    return re.findall(r"'\w+|\w+'\w+|\w+'|\w+", text)

def slugify(text):
    return trans(text).replace(' ', '').lower()

