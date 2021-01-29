import sys
import urllib.parse as urp
from bs4 import BeautifulSoup
import twitter 
import datetime

DIRNAME ="/home/ebi/公開/twibot/"

PARSER_NAME = "html.parser"
DST_PATH = DIRNAME + "dst.log"
TWEET_PATH = DIRNAME + "tweet.log"


auth = twitter.OAuth(
    consumer_key="",
    consumer_secret="",
    token="",
    token_secret=""
)

t = twitter.Twitter(auth=auth)

def main():
    time = datetime.datetime.today()
    print(time, end="")#logへ

    data = sys.stdin.readlines()

    if not data:
        print(" null")#logへ
        return#終了

    tmp = BeautifulSoup("".join(data),PARSER_NAME)
    anchor = tmp.find_all('a')#a要素を全探索
    href = []
    for i in anchor:
        j = i["href"]#a要素のhrefを抽出
        if not "https" in j:#相対pathを絶対pathに
            j = "https://www.oyama-ct.ac.jp{}".format(j)
        #j = urp.unquote(j)
        href.append(j)
    
    dst = tmp.getText().replace(" ","").replace("　","").split("\n")#余計な空白文字の削除
    while True:#分割した際に発生空文字列の削除
        try:
            dst.remove("")
        except ValueError:
            break 

    dst = list(dict.fromkeys(dst))#順序付き重複削除
    href = list(dict.fromkeys(href))
    hlen = len(href)#リンクの文字数は常に11.5/140
    status = ""
    
    with open(DST_PATH, mode="a",encoding="utf-8") as f:
        f.write("{}\n{}\n{}\n".format(time,dst,href))
    dst = "\n".join(dst)
    
    if (len(dst) + hlen*12) < 128:#文字数制限の回避
        href = "\n".join(href)
        status = "更新がありました\n{}\nLink\n{}".format(dst,href)
    elif hlen*12 < 132:
        href = "\n".join(href)
        status = "更新がありました\n{}".format(href)
    else:
        href = "\n".join(href[:9])
        status = "表示しきれないほど更新がありました\n{}\n他".format(href)
    
    print(" tweet")#logへ
    t.statuses.update(status=status)#tweet

    with open(TWEET_PATH,mode="a",encoding="utf-8") as f:
        f.write("{}\n{}\n".format(time,status))


if __name__ == "__main__":
    main()