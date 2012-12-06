import re

from scrapy.stats import stats
from scrapy.exceptions import CloseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from scifibot import settings
from scifibot.items import ScifibotItem

from w3lib.html import remove_tags_with_content, remove_tags, remove_comments

words = re.compile('[\w_-]+')
tokenize = lambda text: words.findall(text)

SCIFI_KEYWORDS = ['assimov', 'bradbury', 'future', 'science', 'fiction', 
    'scifi', 'sci-fi', 'space', 'travel', 'alien', 'time', 'cyberpunk'
    'stephenson', 'gibson']

class ScificrawlerSpider(CrawlSpider):
    name = 'scificrawler'
    start_urls = ['http://en.wikipedia.org/wiki/Science_fiction']

    rules = (
        Rule(SgmlLinkExtractor(), callback='parse_item', follow=True),
    )
    page_count = 0

    def parse_item(self, response):
        self.page_count += 1
        if self.page_count > settings.MAX_PAGES:
            raise CloseSpider('max num of pages reached')
        item = ScifibotItem()
        # clean body
        orig_body = response.body_as_unicode()
        body = remove_tags_with_content(orig_body,
            which_ones=('script', 'head'))
        body = remove_comments(body)
        body = remove_tags(body).lower()
        tokens = tokenize(body)

        # decide if the page is interesting
        if len(set(SCIFI_KEYWORDS) & set(tokens)) <= 2:
            stats.inc_value('scifi/filtered_out')
            # probably not a sci fi page
            return

        item['keywords'] = tokens
        item['page'] = orig_body
        item['url'] = response.url
        return item
