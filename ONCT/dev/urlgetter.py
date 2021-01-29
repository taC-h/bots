from bs4 import BeautifulSoup


def html2url(text,*, parser="html.parser"):
    soup = BeautifulSoup(text, parser)
    anc = soup.find_all("a")
    urls = set()
    for i in anc:
        url = i["href"]#a要素のhrefを抽出
        if not "https" in url:#相対pathを絶対pathに
            url = "https://www.oyama-ct.ac.jp{}".format(url)
        urls.add(url)
    return urls