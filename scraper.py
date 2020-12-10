import argparse
from bs4 import BeautifulSoup
#import logging
import os
#import random
import re
import requests
import sqlite3
#import time
#from urllib import parse
import validators
#import webbrowser

args = None
db_name = "scrapes.db"
info_log = "scraper.log"
report_log = "scraper_report.html"

def main():
    global args, info_log, report_log

    # TODO: Clean up help text
    # Input from user
    argParser = argparse.ArgumentParser(description="A basic webpage scraper which returns a string from input url(s) with content filtered by provided regular expression.")
    argParser.add_argument("urls", nargs="+", help="Input URL(s) to scrape. Accepts a string or filename (Comma Separated Values) with a .")
    argParser.add_argument("regex", help="Regular Expression to limit response from document.")
    argParser.add_argument("-u", "--user-agent", default="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36 link_checker/0.9", help="Alternative User-Agent to use with requests.get() headers")
    argParser.add_argument("-t", "--threads", type=int, default=2, help="Sets the number of concurrent threads that can be processed at one time. Be aware that increasing thread count will increase the frequency of requests to the server. Use 0 to disable multi-threading.")
    args = argParser.parse_args()

    # Valdate input
    if not is_valid_regex(args.regex):
        quit("Invalid Regular Expression provided.")

    # Check if filename or URL(s) being passed
    if os.path.exists(args.url):
        # file handler
        return

    for url in args.urls:
        if not is_valid_url(url):
            quit(url + " is invalid")

    for url in args.urls:
        page = get_page(url)
        if page.status_code == 200:
            soup = BeautifulSoup(page.text, 'html.parser')
            soup.find_all(args.regex)
        

# Check if urls are a list of urls, html string, or file

# Read and validate regex string (re.compile?)
# https://stackoverflow.com/questions/51691270/python-user-input-as-regular-expression-how-to-do-it-correctly


# Returns page response object for URL
def get_page(url: str) -> requests.Response:
    headers = {"User-Agent": args.user_agent}
    follow_redirects = True
    verify_ssl = False
    page = None
    try:
        page = requests.get(url, headers=headers, allow_redirects=follow_redirects, verify=verify_ssl)
    except requests.RequestException:
        print("Invalid page request")
    return page

# Validate regex input
def is_valid_regex(regex: str) -> bool:
    is_valid = False
    try:
        re.compile(regex)
        is_valid = True
    except re.error:
        print("Invalid regex.")
    return is_valid

# Validate URL input
def is_valid_url(url: str) -> bool:
    return validators.url(url)

# Use BeautifulSoup to filter page contents and return result


if __name__ == "__main__":
    main()