#!/usr/bin/python
# filename: run.py
import re
from crawler import Crawler, CrawlerCache

if __name__ == "__main__": 
    # Using SQLite as a cache to avoid pulling twice
    crawler = Crawler(CrawlerCache('crawler.db'))
    root_re = re.compile('^/$').match
    crawler.crawl('http://foodnetwork.com/recipes/recipes-a-z', no_cache=root_re)
    crawler.crawl('http://foodnetwork.com/recipes/recipes-a-z/a', no_cache=root_re)
    crawler.crawl('http://foodnetwork.com/recipes/recipes-a-z/b', no_cache=root_re)
    crawler.crawl('http://foodnetwork.com/recipes/recipes-a-z/c', no_cache=root_re)
    crawler.crawl('http://foodnetwork.com/recipes/recipes-a-z/d', no_cache=root_re)
    crawler.crawl('http://foodnetwork.com/recipes/recipes-a-z/e', no_cache=root_re)
    crawler.crawl('http://foodnetwork.com/recipes/recipes-a-z/f', no_cache=root_re)
    crawler.crawl('http://foodnetwork.com/recipes/recipes-a-z/g', no_cache=root_re)
    crawler.crawl('http://foodnetwork.com/recipes/recipes-a-z/h', no_cache=root_re)
    crawler.crawl('http://foodnetwork.com/recipes/recipes-a-z/i', no_cache=root_re)
    crawler.crawl('http://foodnetwork.com/recipes/recipes-a-z/j', no_cache=root_re)
    crawler.crawl('http://foodnetwork.com/recipes/recipes-a-z/k', no_cache=root_re)
    crawler.crawl('http://foodnetwork.com/recipes/recipes-a-z/l', no_cache=root_re)
    crawler.crawl('http://foodnetwork.com/recipes/recipes-a-z/m', no_cache=root_re)
    crawler.crawl('http://foodnetwork.com/recipes/recipes-a-z/n', no_cache=root_re)
    crawler.crawl('http://foodnetwork.com/recipes/recipes-a-z/o', no_cache=root_re)
    crawler.crawl('http://foodnetwork.com/recipes/recipes-a-z/p', no_cache=root_re)
    crawler.crawl('http://foodnetwork.com/recipes/recipes-a-z/q', no_cache=root_re)
    crawler.crawl('http://foodnetwork.com/recipes/recipes-a-z/r', no_cache=root_re)
    crawler.crawl('http://foodnetwork.com/recipes/recipes-a-z/s', no_cache=root_re)
    crawler.crawl('http://foodnetwork.com/recipes/recipes-a-z/t', no_cache=root_re)
    crawler.crawl('http://foodnetwork.com/recipes/recipes-a-z/u', no_cache=root_re)
    crawler.crawl('http://foodnetwork.com/recipes/recipes-a-z/v', no_cache=root_re)
    crawler.crawl('http://foodnetwork.com/recipes/recipes-a-z/w', no_cache=root_re)
    crawler.crawl('http://foodnetwork.com/recipes/recipes-a-z/xyz', no_cache=root_re)
