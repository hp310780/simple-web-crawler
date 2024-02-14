import argparse
from typing import Set
from urllib.parse import urlparse, urljoin

import requests
from bs4 import BeautifulSoup, SoupStrainer
from requests import RequestException


class LinkSet(set):
    def add(self, item):
        length_before = len(self)
        super(LinkSet, self).add(item)
        if len(self) > length_before:
            print(f"--Child Page: {item}")


class SimpleWebCrawler:
    def __init__(self):
        self.parent = None

    def crawl(self, parent_url: str) -> Set[str]:
        if self.parent is None:
            self.parent = parent_url

        # Ensure top level domain is actually readable,
        # and throw error if not. Otherwise, an invalid top
        # level URL would mislead and return the empty set in _crawl().
        try:
            requests.get(self.parent)
        except RequestException as e:
            raise e

        return self._crawl(parent_url)

    def _crawl(self, url: str, crawled: Set[str] = None) -> Set[str]:

        if crawled is None:
            crawled = set()

        if url not in crawled:
            print(f"Page: {url}")
            crawled.add(url)
            for child_url in self._get_child_urls(url):
                self._crawl(child_url, crawled)
        return crawled

    def _get_child_urls(self, url: str) -> Set[str]:
        try:
            page_content = BeautifulSoup(
                requests.get(url, allow_redirects=False, timeout=3).content,
                "html.parser",
                parse_only=SoupStrainer("a"),
            )
        except Exception:
            return set()

        to_crawl = LinkSet()
        for link in page_content:
            if link.get("href"):
                link_url = link.get("href")
                if self._is_relative_link(link_url):
                    link_url = urljoin(self.parent, link_url)
                if not self._is_crawlable_link(link_url):
                    continue
                if self._is_same_domain_as_parent(link_url):
                    to_crawl.add(link_url)

        return to_crawl

    def _is_same_domain_as_parent(self, url: str) -> bool:
        return urlparse(url).netloc == urlparse(self.parent).netloc

    def _is_relative_link(self, url: str) -> bool:
        return url.startswith("/") or url.startswith(".")

    def _is_crawlable_link(self, url: str) -> bool:
        return urlparse(url).scheme in ("http", "https")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Crawl the given URL domain')

    parser.add_argument(dest='url',
                        type=str,
                        help='Top level URL to crawl')

    args = parser.parse_args()
    wc = SimpleWebCrawler()
    wc.crawl(args.url)
