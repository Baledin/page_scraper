import argparse
from bs4 import BeautifulSoup
import csv
import logging
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
    argParser = argparse.ArgumentParser(description="A basic webpage scraper which returns regular expression matching content from input url(s).")
    argParser.add_argument("urls", nargs="+", help="Input URL(s) to scrape. Accepts a string or filename (Comma Separated Values) with a .")
    argParser.add_argument("regex", help="Regular Expression to limit response from document.")
    argParser.add_argument("-c", "--column", type=int, default=0, help="If providing a CSV file, set the Column which contains the URL data (starting from 0), defaults to the first column.")
    argParser.add_argument("-i", "--ignore-header", default=False, action="store_true", help="Indicates that provided CSV file's first line is a header and can be ignored.")
    argParser.add_argument("--encoding", default="utf8", help="Override the default UTF8 file encoding when providing a filename as input.")
    argParser.add_argument("-u", "--user-agent", default="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36 link_checker/0.9", help="Alternative User-Agent to use with requests.get() headers")
    argParser.add_argument("-l", "--log-level", default="INFO", choices=["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"], help="Log level to report in %s." % info_log)
    argParser.add_argument("-t", "--threads", type=int, default=2, help="Sets the number of concurrent threads that can be processed at one time. Be aware that increasing thread count will increase the frequency of requests to the server. Use 0 to disable multi-threading.")
    args = argParser.parse_args()

    # Set up logging
    logging.basicConfig(
        level=args.log_level,
        filename=info_log,
        filemode="w+",
        format="%(asctime)s\t%(levelname)s\t%(message)s")

    # Valdate input
    if not is_valid_regex(args.regex):
        quit("Invalid Regular Expression provided.")

    # Check if filename or URL(s) being passed, supports multiple files
    urls = []
    for user_input in args.urls:
        if os.path.exists(user_input):
            urls = urls + get_urls_from_file(user_input, args.encoding, args.column, args.ignore_header)
        else:
            urls.append(user_input)

    for url in urls:
        # Check for valid URL
        if is_valid_url(url):
            page = get_page(url)
            if page.status_code == 200:
                soup = BeautifulSoup(page.text, 'html.parser')
                x = soup.find_all(args.regex)
        else:
            logging.warning(url + " is invalid")

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

def get_urls_from_file(filename: str, encoding: str, col: int, header: bool) -> list[str]:
    try:
        urls = []
        with open(filename, mode='r', encoding=encoding) as csv_file:
            first_line = True
            reader = csv.reader(csv_file, delimiter=',')
            for row in reader:
                if first_line and header:
                    first_line = False
                else:
                    urls.append(row[col])
        return urls
    except UnicodeDecodeError:
        quit("Wrong encoding provided for file. Selected encoding option is " + encoding + ".")
    except:
        quit("Error reading input file.")

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