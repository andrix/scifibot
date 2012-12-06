import random
from scrapy import log
from scrapy.utils.misc import load_object

from scrapy.core.scheduler import Scheduler

class RandomScheduler(Scheduler):

    def __init__(self, dupefilter, stats=None):
        self.df = dupefilter
        self.stats = stats
        self.requests = []

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        dupefilter_cls = load_object(settings['DUPEFILTER_CLASS'])
        dupefilter = dupefilter_cls.from_settings(settings)
        return cls(dupefilter, stats=crawler.stats)

    def has_pending_requests(self):
        return len(self) > 0

    def open(self, spider):
        self.spider = spider
        if self.requests:
            del self.requests
        self.requests = []

    def close(self, reason):
        del self.requests
        return self.df.close(reason)

    def enqueue_request(self, request):
        if not request.dont_filter and self.df.request_seen(request):
            return
        self.requests.append(request)
        self.stats.inc_value('scheduler/enqueued', spider=self.spider)

    def next_request(self):
        if not self.requests:
            return
        ri = random.randint(0, len(self.requests) - 1)
        request = self.requests.pop(ri)
        log.msg("Next request to process at random: %d" % ri)
        if request:
            self.stats.inc_value('scheduler/dequeued', spider=self.spider)
        return request

    def __len__(self):
        return len(self.requests)
