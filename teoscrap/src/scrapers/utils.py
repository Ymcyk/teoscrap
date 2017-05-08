from datetime import datetime

def string_to_date(text):
    return datetime.strptime(text, '%Y-%m-%d').date()
