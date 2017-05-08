from trans import trans
import string
import re

def string_to_words_list(text):
    return re.sub(r"[.!,;?]", ' ', text).lower().split()

def slugify(text):
    return trans(text).replace(' ', '').lower()

