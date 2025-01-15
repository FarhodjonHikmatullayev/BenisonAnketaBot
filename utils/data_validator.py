from datetime import datetime
import re


async def validate_date(date_string):
    try:
        data_obj = datetime.strptime(date_string, '%d.%m.%Y')
        if data_obj > datetime.now():
            return False
        return True
    except ValueError:
        return False


async def validate_phone_number(phone_number):
    pattern = r'^\+998\d{9}$'

    if re.match(pattern, phone_number):
        return True
    else:
        return False


async def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if re.match(pattern, email):
        return True
    else:
        return False
