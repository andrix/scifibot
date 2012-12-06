# Scrapy settings for scifibot project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'scifibot'

SPIDER_MODULES = ['scifibot.spiders']
NEWSPIDER_MODULE = 'scifibot.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'scifibot (university assignment)'

MAX_PAGES = 10

SCHEDULER = 'scifibot.randomscheduler.RandomScheduler'

SPIDER_MIDDLEWARES = {
    'scrapy.contrib.spidermiddleware.offsite.OffsiteMiddleware': None,
}

DOWNLOADER_MIDDLEWARES = {
    'scifibot.middleware.DuplicateDetection': 600,
}
