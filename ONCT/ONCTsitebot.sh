#!/bin/bash
dirname="$HOME/twibot/"
filename="${dirname}ONCTSitelog/`date +'%d-%H%M'`.html"

curl -s -o $filename -H "User-Agent: CrawlBot; taC.handstandingcat@gmail.com" https://www.oyama-ct.ac.jp/
date >> "${dirname}diff.log"
diff -u  "${dirname}ONCTSitelog/latest.html" $filename | grep -E "^\+" | sed -e 1d | cut -c 2- | \
    tee -a "${dirname}diff.log" | tee "${dirname}diff.txt"|  python3 "${dirname}parser0.1.0.py" &>> "${dirname}parser.log"

cp -f $filename "${dirname}ONCTSitelog/latest.html"

cat "${dirname}diff.txt" | python3 "${dirname}parser1.0.0.py" >> "${dirname}test.log"