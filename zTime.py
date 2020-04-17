import datetime

def getTime(file_name):
    timestamp = file_name.split('_')[0]
    _date = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')

    return _date

def getDate(file_name):
    timestamp = file_name.split('_')[0]
    _date = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y%m%d')

    return _date