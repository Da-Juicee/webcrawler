"""Crawl a web-site.

Fetch contnt from a URL. Extract the hyperliks and recurse (i.e. fetch
the contnt of the hyperlink URLs and extract their hyperlinks and recurse).

This code only works with Python 2.
"""

import os
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

def get_fname(url, output_dir):
    if url.endswith("/"):
        url = url[:-1]
    fname = os.path.basename(url)
    fname = os.path.join(output_dir, fname)
    if not (fname.endswith(".jpg") or fname.endswith('.png')):
        fname = fname + ".html"
    return fname

def write_page(content, fname):
    with open(fname, "w") as fhandle:
        fhandle.write(content)

def process_page(url, base_url, output_dir):
    print("Processing page:", url)
    content = fetch_content(url)
    fname = get_fname(url, output_dir)
    write_page(content, fname)

    hyperlinks = extract_hyperlinks(content)
    hyperlinks = absurl_filter(hyperlinks, base_url)
    hyperlinks = filter_hyperlinks(hyperlinks, base_url)
    print("Hyperlinks in page:", hyperlinks)
    for hlink in hyperlinks:
        if not hlink in VISITED_PAGES:
            print(hlink)
            process_page(hlink, base_url, output_dir)
        else:
            print("already processed:", hlink)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url")
    parser.add_argument("output_dir")
    args = parser.parse_args()

    if not os.path.isdir(args.output_dir):
        os.mkdir(args.output_dir)

    process_page(args.url, args.url, args.output_dir)


if __name__ == "__main__":
    main()
