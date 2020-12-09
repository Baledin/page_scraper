import argparse
from bs4 import BeautifulSoup
#import logging
#import os
#import random
import requests
import sqlite3
#import time
#from urllib import parse
#import validators
#import webbrowser

args = None
db_name = "scrapes.db"
info_log = "scraper.log"
report_log = "scraper_report.html"

def main():
    global args, info_log, report_log

    # Clean up help text
    argParser = argparse.ArgumentParser(description="A basic webpage scraper which returns a string from input url(s).")
    argParser.add_argument("urls", nargs="+", help="Input URL(s) to scrape.")
    argParser.add_argument("regex", help="Regular Expression to limit response from document.")
    argParser.add_argument("-u", "--user-agent", default="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36 link_checker/0.9", help="Alternative User-Agent to use with requests.get() headers")
    argParser.add_argument("-t", "--threads", type=int, default=2, help="Sets the number of concurrent threads that can be processed at one time. Be aware that increasing thread count will increase the frequency of requests to the server. Use 0 to disable multi-threading.")
    args = argParser.parse_args()

    for url in args.urls:
        page = get_page(url)
        if page.status_code == 200:
            soup = BeautifulSoup(page.text, 'html.parser')
        

# Read and validate input
# Check if urls are a list or file

# Read and validate regex string (re.compile?)
# https://stackoverflow.com/questions/51691270/python-user-input-as-regular-expression-how-to-do-it-correctly

# Use Requests to fetch page contents
def get_page(url):
    headers = {"User-Agent": args.user_agent}
    follow_redirects = True
    verify_ssl = False
    page = requests.get(url, headers=headers, allow_redirects=follow_redirects, verify=verify_ssl)
    return page

# Use BeautifulSoup to filter page contents and return result


if __name__ == "__main__":
    main()