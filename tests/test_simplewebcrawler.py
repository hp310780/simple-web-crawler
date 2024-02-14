import pytest
import requests_mock
from requests import RequestException

from simplewebcrawler import SimpleWebCrawler


def test_get_child_urls_successful(requests_mock):
    requests_mock.register_uri(
        "GET",
        "https://test.com/",
        content="<a href='https://test.com/about/'>about</a>"
                "<a href='https://test.com/careers/'>careers</a><>".encode("utf-8"),
    )
    wc = SimpleWebCrawler()
    wc.parent = "https://test.com/"
    assert wc._get_child_urls("https://test.com/") == {
        "https://test.com/careers/",
        "https://test.com/about/",
    }


def test_invalid_top_level_url_throws_exception():
    wc = SimpleWebCrawler()
    with pytest.raises(RequestException):
        wc.crawl("notavalidurl")


def test_get_child_url_invalid_url_returns_empty_set():
    wc = SimpleWebCrawler()
    assert not wc._get_child_urls("notavalidurl")


def test_is_same_domain_as_parent_successful():
    wc = SimpleWebCrawler()
    wc.parent = "https://test.com/"

    assert wc._is_same_domain_as_parent("https://test.com/about/")
    assert wc._is_same_domain_as_parent("http://test.com/about/team")
    assert not wc._is_same_domain_as_parent("https://facebook.com")
    assert not wc._is_same_domain_as_parent("https://community.test.com")


def test_is_relative_link_successful():
    wc = SimpleWebCrawler()
    wc.parent = "https://test.com/"

    assert wc._is_relative_link("/about/")
    assert wc._is_relative_link("../team/")
    assert not wc._is_relative_link("https://facebook.com")
    assert not wc._is_relative_link("https://community.test.com")


def test_is_crawlable_link_successful():
    wc = SimpleWebCrawler()
    wc.parent = "https://test.com/"

    assert wc._is_crawlable_link("https://test.com/")
    assert wc._is_crawlable_link("https://test.com/about/us")
    assert not wc._is_crawlable_link("javascript:void(0)")
    assert not wc._is_crawlable_link("?query")
    assert not wc._is_crawlable_link("#")


def test_crawl_successful(requests_mock):
    requests_mock.register_uri(
        "GET",
        "https://test.com/",
        content="<a href='https://test.com/about/'>about</a>".encode("utf-8"),
    )
    requests_mock.register_uri(
        "GET", "https://test.com/about/", content="".encode("utf-8")
    )
    wc = SimpleWebCrawler()
    assert wc.crawl("https://test.com/") == {
        "https://test.com/",
        "https://test.com/about/",
    }


def test_crawl_with_relative_links_successful(requests_mock):
    requests_mock.register_uri(
        "GET",
        "https://test.com/",
        content="<a href='/about/'>about</a>".encode("utf-8"),
    )
    requests_mock.register_uri(
        "GET", "https://test.com/about/", content="".encode("utf-8")
    )
    wc = SimpleWebCrawler()
    assert wc.crawl("https://test.com/") == {
        "https://test.com/",
        "https://test.com/about/",
    }


def test_crawl_excludes_external_links(requests_mock):
    requests_mock.register_uri(
        "GET",
        "https://test.com/",
        content="<a href='https://test.com/about/'>about</a>".encode("utf-8"),
    )

    requests_mock.register_uri(
        "GET",
        "https://test.com/about/",
        content="<a href='https://facebook.com'>Facebook</a>".encode("utf-8"),
    )
    wc = SimpleWebCrawler()
    assert wc.crawl("https://test.com/") == {
        "https://test.com/",
        "https://test.com/about/",
    }


def test_crawl_excludes_subdomains(requests_mock):
    requests_mock.register_uri(
        "GET",
        "https://test.com/",
        content="<a href='https://test.com/about/'>about</a>".encode("utf-8"),
    )
    requests_mock.register_uri(
        "GET",
        "https://test.com/about/",
        content="<a href='https://test.community.com'>Community</a>".encode("utf-8"),
    )
    wc = SimpleWebCrawler()
    assert wc.crawl("https://test.com/") == {
        "https://test.com/",
        "https://test.com/about/",
    }


def test_crawl_with_circular_links_successful(requests_mock):
    requests_mock.register_uri(
        "GET",
        "https://test.com/",
        content="<a href='https://test.com/about/'>about</a>".encode("utf-8"),
    )
    requests_mock.register_uri(
        "GET",
        "https://test.com/about/",
        content="<a href='https://test.com/'>home</a>".encode("utf-8"),
    )
    wc = SimpleWebCrawler()
    assert wc.crawl("https://test.com/") == {
        "https://test.com/",
        "https://test.com/about/",
    }


def test_crawl_with_non_crawlable_links_successful(requests_mock):
    requests_mock.register_uri(
        "GET",
        "https://test.com/",
        content="<a href='https://test.com/about/'>about</a>".encode("utf-8"),
    )
    requests_mock.register_uri(
        "GET",
        "https://test.com/about/",
        content="<a href='mailto:foo@bar.com'>email</a>".encode("utf-8"),
    )
    wc = SimpleWebCrawler()
    assert wc.crawl("https://test.com/") == {
        "https://test.com/",
        "https://test.com/about/",
    }


def test_crawl_with_inline_links_successful(requests_mock):
    requests_mock.register_uri(
        "GET",
        "https://test.com/",
        content="<a href='https://test.com/about/'>about</a><a href='#'>home</a>".encode(
            "utf-8"
        ),
    )
    requests_mock.register_uri(
        "GET",
        "https://test.com/about/",
        content="<a href='mailto:foo@bar.com'>email</a><a href='#button'>button</a>".encode(
            "utf-8"
        ),
    )
    wc = SimpleWebCrawler()
    assert wc.crawl("https://test.com/") == {
        "https://test.com/",
        "https://test.com/about/",
    }
