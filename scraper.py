import argparse
import csv
import logging
import os
import regex
import requests
from typing import List
import validators

args = None
info_log = "scraper.log"
report_file = "scraper_report.csv"

def main():
    global args

    # TODO: Clean up help text
    # Process user input
    argParser = argparse.ArgumentParser(description="A basic webpage scraper which returns regular expression matching content from input url(s). Note that the string to return must be enclosed in a capture group.")
    argParser.add_argument("urls", nargs="+", help="Input URL(s) to scrape. Accepts a string or filename (Comma Separated Values) with a .")
    argParser.add_argument("regex", help="Regular Expression to limit response from document.")
    argParser.add_argument("-c", "--column", type=int, default=0, help="If providing a CSV file, set the Column which contains the URL data (starting from 0), defaults to the first column.")
    argParser.add_argument("-i", "--ignore-header", default=False, action="store_true", help="Indicates that provided CSV file's first line is a header and can be ignored.")
    argParser.add_argument("--encoding", default="utf8", help="Override the default UTF8 file encoding when providing a filename as input.")
    argParser.add_argument("-u", "--user-agent", default="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36 link_checker/0.9", help="Alternative User-Agent to use with requests.get() headers")
    argParser.add_argument("-l", "--log-level", default="INFO", choices=["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"], help="Log level to report in %s." % info_log)
    # Testing flag, will limit results to first 10 instead of processing everything
    argParser.add_argument("-test", default=False, action="store_true", help=argparse.SUPPRESS)
    args = argParser.parse_args()

    # Configure logging
    logging.basicConfig(
        level=args.log_level,
        filename=info_log,
        filemode="w+",
        format="%(asctime)s\t%(levelname)s\t%(message)s")

    # Valdate input - regex validated before heavier loads
    if not is_valid_regex(args.regex):
        quit("Invalid Regular Expression provided.")

    # Check if filename or URL(s) being passed, supports multiple files and urls
    urls = []
    for user_input in args.urls:
        if os.path.exists(user_input):
            urls = urls + get_urls_from_file(user_input, args.encoding, args.column, args.ignore_header)
        else:
            urls.append(user_input)

    # Sets testing limiter if flag is set
    max_entries = len(urls) if not args.test else min(len(urls), 10)

    # Convert URLs to dictionary keys, removes duplicates
    dict_urls = dict.fromkeys(urls[:max_entries], 1)

    # Process urls
    results = process_pages(dict_urls, args.regex)
    
    # Output results
    output_results(results)

# Returns page response object for URL
def get_page(url: str) -> requests.Response:
    # Ignores SSL warnings if using verify_ssl = False
    # requests.urllib3.disable_warnings(requests.urllib3.exceptions.InsecureRequestWarning)

    logging.info("Retrieving page: " + url)
    headers = {"User-Agent": args.user_agent}
    follow_redirects = True
    verify_ssl = True
    page = None
    try:
        page = requests.get(url, headers=headers, allow_redirects=follow_redirects, verify=verify_ssl)
    except requests.RequestException:
        logging.warning("Invalid page request: " + url)
    return page

# Returns list of URLs from filename
def get_urls_from_file(filename: str, encoding: str, col: int, header: bool) -> List[str]:
    logging.info("Building list of URLs from " + filename)
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
        logging.error("Wrong encoding provided for " + filename)
    except:
        quit("Error reading input file.")

# Validate regex input
def is_valid_regex(expression: str) -> bool:
    is_valid = False
    try:
        regex.compile(expression)
        is_valid = True
    except:
        error_msg = "Invalid regular expression."
        logging.error(error_msg)
    return is_valid

# Validate URL input
def is_valid_url(url: str) -> bool:
    return validators.url(url)

# Converts dictionary to output CSV
def output_results(results: dict[str, str]) -> None:
    with open(report_file, "w", newline='') as out:
        writer = csv.writer(out)
        for key, items in results.items():
            if isinstance(items, list):
                for item in items:
                    writer.writerow([key, item])
            else:
                writer.writerow([key, items])

# Process page, retrieving page data and comparing to Regex string
def process_page_regex(page: requests.Response, expr: str) -> str:
    result = ""
    
    # Check for valid URL
    if is_valid_url(page):
        page = get_page(page)
        if page.status_code == 200:
            match = regex.search(expr, page.text)
            if not match == None:
                result = match[0]
    else:
        logging.warning(result + " is invalid.")
    
    return result

# Process URLs, retrieving page data and comparing to Regex string
def process_pages(pages: List[requests.Response], expr: str) -> dict[str, str]:
    for page in pages:
        pages[page] = process_page_regex(page, expr)
    
    return pages

if __name__ == "__main__":
    main()