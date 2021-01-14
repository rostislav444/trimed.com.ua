import urllib.request
import urllib.parse
from project import settings

def SendMessage(msg):
    msg = urllib.parse.quote(msg)
    url = settings.TELEGRAM_GET_LINK + msg
    contents = urllib.request.urlopen(url).read()
    return contents