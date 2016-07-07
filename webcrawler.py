"""Crawl a web-site.

Fetch contnt from a URL. Extract the hyperliks and recurse (i.e. fetch
the contnt of the hyperlink URLs and extract their hyperlinks and recurse).

This code only works with Python 2.
"""

import sys
import argparse
try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen
import re

VISITED_PAGES = []


def extract_hyperlinks(content):
    """Returns a list of hyperlinks."""
    #Regular expression, note that the group used to identify the hyperlink
    #uses the non-greedy version of the '*' (Repeat matching) special character.
    hyperlinks = re.findall(r'<a href="(.*?)".*>', content)
    return hyperlinks


def test_absurl():
    u = absurl("/about/", "http://site-of-interest")
    assert u == "http://site-of-interest/about/"

def absurl(rel_url, base_url):
    """Return the absolute url."""
    if rel_url == "/":
        return base_url
    return base_url + rel_url

def test_filter_hyperlinks():
    hyperlinks = ["https://www.google.co.uk/",
                  "http://site-of-interest/training/"]
    filtered = filter_hyperlinks(hyperlinks, "http://site-of-interest")
    assert filtered == ["http://site-of-interest/training/"], filtered


def absurl_filter(hyperlinks, base_url):
    """Return list where relative urls have been converted to absolute urls."""
    filtered = []
    if base_url.endswith("/"):
        base_url = base_url[:-1]
    for hlink in hyperlinks:
        if hlink.startswith("/"):
            hlink = absurl(hlink, base_url)
        filtered.append(hlink)
    return filtered

def filter_hyperlinks(hyperlinks, base_url):
    """Return list of hyperlinks belonging to base_url."""
    return [hlink for hlink in hyperlinks if hlink.startswith(base_url)]



def fetch_content(url):
    """Return the content from a URL."""
    handle = urlopen(url)
    bstring = handle.read()
    VISITED_PAGES.append(url)
    return str(bstring)


def process_page(url, base_url):
    print("Processing page:", url)
    content = fetch_content(url)
    hyperlinks = extract_hyperlinks(content)
    hyperlinks = absurl_filter(hyperlinks, base_url)
    hyperlinks = filter_hyperlinks(hyperlinks, base_url)
    print("Hyperlinks in page:", hyperlinks)
    for hlink in hyperlinks:
        if not hlink in VISITED_PAGES:
            print(hlink)
            process_page(hlink, base_url)
        else:
            print("already processed:", hlink)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url")
    args = parser.parse_args()

    process_page(args.url, args.url)


if __name__ == "__main__":
    main()
