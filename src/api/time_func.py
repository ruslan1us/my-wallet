from datetime import datetime, date


def set_date():
    return datetime.strptime(datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")


def set_year():
    return date.today().year


def get_month():
    return date.today().month
