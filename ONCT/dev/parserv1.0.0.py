from logging import INFO, getLogger, FileHandler, basicConfig, DEBUG
import sys
import datetime

from urlgetter import html2url
from tweeter import TweetManager, MocTw

basicConfig(level=INFO)
logger = getLogger(__name__)
logger.setLevel(INFO)
fh =  FileHandler(__name__ + ".log")
fh.setLevel(INFO)

def main():
    data = sys.stdin.readlines()
    now = datetime.datetime.today()
    
    if not data:
        logger.info(f"{now}: null")
        return
    
    urls = html2url("".join(data))
    tw = MocTw()
    TweetManager(
        tw,
        *urls
    )()
    logger.info(f"{now}: done")

if __name__ == "__main__":
    main()