import urllib.request
import re
import time
import logging

LOGGER = logging.getLogger(__name__)

PLATFORM_RES = {
    "pinterest": [
        r"pinterest\.com/(?P<account>[^/]*)",
        [r'name="pinterestapp:followers" content="(?P<followers>\d+)"']],
    "twitter": [
        r"twitter\.com/(?P<account>[^/]*)",
        [r'followers">.*<div class="statnum">(?P<followers>.*?)</div>.*?'
            '<div class="statlabel"> Followers </div>',
         r'title="(?P<followers>[\d,]+) Followers" data-nav="followers"']],
    "facebook": [
        r"facebook\.com/(?P<account>[^/]*)",
        [r'<meta name="description" content=".*?(?P<followers>[\d,]+) likes',
         r'<span id="PagesLikesCountDOMID">.*?>(?P<followers>[\d,]+) <',
         r'content=".* (?P<followers>[\d,]+) likes']],
    "youtube": [
        r"youtube\.com/user/(?P<account>[^/]*)",
        [r'aria-label="(?P<followers>[\d,]+) subscribers']],
    "google plus": [
        r"plus\.google\.com.*?/(?P<account>[^/]*)",
        [r'<div class="WH0GUe"><span>(?P<followers>[\d,]+)</span> followers',
         r'">(?P<followers>[\d,]+)</span> followers',
         r'<br>(?P<followers>[\d,]+) followers</div>']],
    "instagram": [
        r"instagram\.com/(?P<account>[^/]*)",
        [r'\"followed_by\":(?P<followers>[\d]+)',
         r'\"followed_by\":\s*{\"count\":\s*(?P<followers>[\d]+)}']]}


class ProcessUrls:
    def __init__(self, urls, stores, store_page, platforms):
        self.urls = urls
        self.stores = stores
        self.store_page = store_page
        self.platforms = platforms

        self.processed_platforms = []

    def _process_url(self, url):
        LOGGER.info("Processing url: %s", url)
        followers_platform = None
        followers_res = []
        for platform, values in PLATFORM_RES.items():
            match = re.search(values[0], url)
            if match:
                followers_platform = platform
                account = match.group("account")
                LOGGER.info("URL has account: %s", account)
                followers_res = values[1]

        if not followers_res:
            LOGGER.error(
                "Error could not identify the platform of the url: \"%s\"",
                url)
            return

        try:
            resultHandle = urllib.request.urlopen(url)
        except IOError as e:
            LOGGER.exception("Error accessing url: %s", url)
            return

        if not resultHandle:
            LOGGER.error("Couldn't get any results for url: %s", url)

        followers = None
        page = resultHandle.read().decode('utf-8')

        if self.store_page:
            with open("found_page.txt", "w") as writer:
                writer.write(page)

        for follower_re in followers_res:
            match = re.search(follower_re, page, re.DOTALL)
            if match:
                followers = match.group("followers")
                break

        if followers:
            LOGGER.info("Followers: %s", followers)
            LOGGER.debug("Current platforms %s", self.processed_platforms)
            platform = followers_platform
            if self.platforms or platform in self.processed_platforms:
                platform = "%s_%s" % (followers_platform, account)
                if not self.platforms:
                    LOGGER.info("Platform clash, using %s", platform)

            orig_platform = platform
            count = 2
            while platform in self.processed_platforms:
                platform = orig_platform + str(count)
                count += 1
                LOGGER.info("Platform clash, using %s", platform)

            self.processed_platforms.append(platform)

            for store in self.stores:
                store.store_followers(platform, followers, self.scan_time, url)
        else:
            LOGGER.info("Didn't find any follower data.")

    def process(self):
        self.scan_time = time.strftime("%a %b %d %H:%M %Y")
        LOGGER.info("Getting followers from urls:\n%s", self.urls)
        for url in self.urls:
            self._process_url(url)
        LOGGER.info("Finished processing urls")
