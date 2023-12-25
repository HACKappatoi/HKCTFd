from CTFd.utils import get_config
import time

def load(app):
    app.jinja_env.globals['ctfHasStarted']=ctfHasStarted
    app.jinja_env.globals['ctfHasEnded']=ctfHasEnded
    app.jinja_env.globals['ctfIsRunning']=ctfIsRunning
    app.jinja_env.globals['getTimeWatch']=getTimeWatch
    app.jinja_env.globals['getTimeWatchData']=getTimeWatchData


def ctfHasStarted():
    start = get_config('start')
    now = int(time.time())
    return now >= start

def ctfHasEnded():
    end = get_config('end')
    now = int(time.time())
    return now >= end

def ctfIsRunning():
    start = get_config('start')
    end = get_config('end')
    now = int(time.time())
    return start <= now and now <= end

def getTimeWatch():
    start = get_config('start')
    end = get_config('end')
    now = int(time.time())
    
    if ctfHasEnded():
        return "Ctf has ended!"
    if ctfIsRunning():
        remaining = end - now
        remainingStr = formatSecondsToString(remaining)
        return f"{remainingStr} to end"
    if not ctfHasStarted():
        remaining = start - now
        remainingStr = formatSecondsToString(remaining)
        return f"{remainingStr} to start"
    
    return None

def getTimeWatchData():
    start = get_config('start')
    end = get_config('end')
    now = int(time.time())
    
    if ctfHasEnded():
        return "Ctf has ended!"
    
    if ctfIsRunning():
        remaining = end - now
        data = formatSecondsToDict(remaining)
        data["text"]="Time to end"
        return data
    if not ctfHasStarted():
        remaining = start - now
        data = formatSecondsToDict(remaining)
        data["text"]="Time to start"
        return data
    
    return None

def formatSecondsToString(seconds):
    days = seconds // (24 * 3600)
    seconds %= (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "%d:%d:%02d" % ( days, hour, minutes)

def formatSecondsToDict(seconds):
    days = seconds // (24 * 3600)
    seconds %= (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    data = {}
    data['days']=days
    data['hour']=hour
    data['minutes']=minutes
    data['seconds']=seconds
    return data

