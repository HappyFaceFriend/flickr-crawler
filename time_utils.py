import datetime

format = "%Y/%m/%d"

def unixtime2str(unixtime : int):
    return datetime.datetime.fromtimestamp(unixtime).strftime(format)

def str2unixtime(formatted_date : str):
    return int(datetime.datetime.strptime(formatted_date, format).timestamp())

def today_unixtime():
    return int(datetime.datetime.today().timestamp())
