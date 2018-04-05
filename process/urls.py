import time
import logging

from .pinterest import ProcessPinterest
from .twitter import ProcessTwitter
from .youtube import ProcessYoutube
from .google_plus import ProcessGooglePlus
from .instagram import ProcessInstagram
from .linkedin import ProcessLinkedInGenerator

LOGGER = logging.getLogger(__name__)

BASIC_PROCESSORS = [
    ProcessPinterest,
    ProcessTwitter,
    ProcessYoutube,
    ProcessGooglePlus,
    ProcessInstagram,
]


class ProcessUrls:
    def __init__(
        self, urls, stores, store_page, named_platforms, linkedin_cookie
    ):
        self.urls = urls
        self.stores = stores
        self.store_page = store_page
        self.named_platforms = named_platforms
        self.processors = BASIC_PROCESSORS[:]
        if linkedin_cookie is not None:
            self.processors.append(ProcessLinkedInGenerator(linkedin_cookie))
        self.processed_platforms = []

    def _plaform_getter(self, raw_platform, account):
        LOGGER.debug("Current platforms %s", self.processed_platforms)
        platform = raw_platform
        if self.named_platforms or platform in self.processed_platforms:
            platform = "%s_%s" % (raw_platform, account)
            if not self.named_platforms:
                LOGGER.info("Platform clash, using %s", platform)

        orig_platform = platform
        count = 2
        while platform in self.processed_platforms:
            platform = orig_platform + str(count)
            count += 1
            LOGGER.info("Platform clash, using %s", platform)

        self.processed_platforms.append(platform)
        return platform

    def _process_url(self, url):
        LOGGER.info("Processing url: %s", url)

        processor = None
        for p in self.processors:
            if p.can_process(url):
                processor = p(url, self.store_page)

        if not processor:
            LOGGER.error(
                "Error could not identify the platform of the url: \"%s\"",
                url)
            return

        print(type(processor))
        followers = processor.get_followers(self._plaform_getter)

        if followers is not None:
            for store in self.stores:
                store.store_followers(self.scan_time, followers)

    def process(self):
        self.scan_time = time.strftime("%a %b %d %H:%M %Y")
        LOGGER.info("Getting followers from urls:\n%s", self.urls)
        for url in self.urls:
            self._process_url(url)
        LOGGER.info("Finished processing urls")
