from hashlib import sha1
from scrapy.exceptions import IgnoreRequest

fingerprint = lambda text: sha1(text).hexdigest()

class DuplicateDetection(object):
    """
    Simple duplicate detection middleware
    """
    def __init__(self):
        self.seenpages = set()

    def process_response(self, request, response, spider):
        fp = fingerprint(response.body)
        if fp not in self.seenpages:
            self.seenpages.add(fp)
            return response
        raise IgnoreRequest

