# SimpleWebCrawler

## Requirements
* Python 3.9+
* Poetry

## Installation
1. Run `poetry install` from the project root.
2. Run `poetry run python simplewebcrawler.py <YOUR URL TO CRAWL>` from the project root.
3. Alternatively, the following code will create the web crawler and crawl https://www.bbc.co.uk:
```
from simplewebcrawler import SimpleWebCrawler

wc = SimpleWebCrawler()
wc.crawl("https://www.bbc.co.uk")
```

Example Output:
```
Page: https://www.bbc.co.uk
--Child Page: https://www.bbc.co.uk
--Child Page: https://www.bbc.co.uk/accessibility/
--Child Page: https://www.bbc.co.uk/live
--Child Page: https://www.bbc.co.uk/notifications
--Child Page: https://www.bbc.co.uk/news
--Child Page: https://www.bbc.co.uk/sport
--Child Page: https://www.bbc.co.uk/weather
...
```

## Running Tests
Run `poetry run pytest` from the project root. 
The test files are found in the `tests/` directory.

Run `poetry run pytest --cov=simplewebcrawler tests/` to get test coverage.

### Performance Test
A simple performance test is included which returns the time taken in seconds to crawl https://crawler-test.com/ in `tests/performance_tests.py` (~249s).

Run `poetry run python tests/performance_tests.py`. 

## Linting
To format, run `poetry run black simplewebcrawler.py`.

## Future Improvements
* I present this workable `SimpleWebCrawler` (and acknowledge its limitations), and would like to investigate the following:
  * Any potential performance gains in multithreading.
  * More nuanced handling of relative and non-crawlable links.
  * Integration tests with the expected output (an approximation of a large test site with the expected output of a crawler).
  * Any alternative graph traversal algorithms that would be suited to this task.
  * Better printing output to visualise the website link graph.
  * Look into [scrapy](https://scrapy.org/).
  * Introduce logging/monitoring of non-requestable URLs to understand any patterns in links that should be crawled but are currently throwing errors.

## Assumptions
* Relative links are defined as links starting with `/` or `.` (as in `../about.html`). Could this be improved with a regex?
* Non-crawlable absolute links are defined as any not using the http or https protocol.
* Links in a page's source are defined by `a` and `href` tags. Could this be improved with a regex?
* 3 seconds timeout on requests was reasonable for current functionality.