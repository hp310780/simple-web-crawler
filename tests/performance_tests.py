import time

from simplewebcrawler import SimpleWebCrawler


def simplewebcrawler_performance():
    wc = SimpleWebCrawler()
    start = time.perf_counter()
    wc.crawl("https://crawler-test.com/")
    end = time.perf_counter()

    print(f"Simple web crawl of https://crawler-test.com/ {end - start:0.4f} seconds")


simplewebcrawler_performance()
