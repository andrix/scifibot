from hashlib import sha1
from scrapy.exceptions import IgnoreRequest

fingerprint = lambda text: sha1(text).hexdigest()

class DuplicateDetection(object):

    seenpages = set()

    def process_response(self, request, response, spider):
        fp = fingerprint(response.body)
        if fp in self.seenpages:
            raise IgnoreRequest
        return response

