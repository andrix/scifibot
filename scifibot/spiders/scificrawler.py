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

RELEVANCY_TSHOLD = 2
SCIFI_KEYWORDS = set(['assimov', 'bradbury', 'future', 'science', 'fiction',
    'scifi', 'sci-fi', 'space', 'travel', 'alien', 'time', 'cyberpunk'
    'stephenson', 'gibson'])

is_relevant = lambda toks: len(SCIFI_KEYWORDS & set(toks)) <= RELEVANCY_TSHOLD

class ScificrawlerSpider(CrawlSpider):
    name = 'scificrawler'
    start_urls = ['http://en.wikipedia.org/wiki/Science_fiction']

    rules = (
        Rule(SgmlLinkExtractor(), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScifibotItem()
        # clean body
        orig_body = response.body_as_unicode()
        body = remove_tags_with_content(orig_body,
            which_ones=('script', 'head'))
        body = remove_tags(remove_comments(body))
        tokens = tokenize(body.lower())
        # decide if the page is interesting
        if not is_relevant(tokens):
            stats.inc_value('scifi/filtered_out') # probably not scifi page
            return

        item['keywords'] = tokens
        item['page'] = orig_body
        item['url'] = response.url
        return item
