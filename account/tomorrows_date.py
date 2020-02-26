import datetime

def tomorrows_date():
    today = datetime.datetime.today()
    tomorrow = today + datetime.timedelta(days=1)
    return tomorrow