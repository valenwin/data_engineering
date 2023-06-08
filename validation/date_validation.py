from datetime import datetime


def validate_date_format(date_str, format_str):
    try:
        datetime.strptime(date_str, format_str)
        return True
    except ValueError:
        return False
