import argparse
#from bs4 import BeautifulSoup
#import logging
#import os
#import random
#import requests
import sqlite3
#import time
#from urllib import parse
#import validators
#import webbrowser

def main():
    argParser = argparse.ArgumentParser(description="A basic webpage scraper which returns a string from input url(s).")
    argParser.add_argument("urls", nargs="+", help="Input URL(s) to scrape.")
    argParser.add_argument("-u", "--user-agent", default="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36 link_checker/0.9", help="Alternative User-Agent to use with requests.get() headers")
    argParser.add_argument("-t", "--threads", type=int, default=2, help="Sets the number of concurrent threads that can be processed at one time. Be aware that increasing thread count will increase the frequency of requests to the server. Use 0 to disable multi-threading.")


if __name__ == "__main__":
    main()