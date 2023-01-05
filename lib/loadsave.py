from datetime import date, datetime


def get_date():
    today = date.today()
    return (str(today.year).zfill(4) +
            str(today.month).zfill(2) +
            str(today.day).zfill(2))


def get_time():
    now = datetime.now()
    return now.strftime("%H%M%S")
