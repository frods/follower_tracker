import re
import urllib.request
import logging

from .followers import Followers

LOGGER = logging.getLogger(__name__)


def get_account(account_re, url):
    account = None
    match = re.search(account_re, url)
    if match:
        account = match.group("account")
        LOGGER.info("URL has account: %s", account)
    return account


class ProcessBasicUrl:
    PLATFORM = "basic_url define own platform"

    @staticmethod
    def can_process(url):
        raise NotImplementedError

    def __init__(self, platform, account_re, followers_res, url, store_page):
        self.platform = platform
        self.account_re = account_re
        self.followers_res = followers_res
        self.url = url
        self.store_page = store_page

    def get_followers(self, platform_getter):
        try:
            resultHandle = urllib.request.urlopen(self.url)
        except IOError as e:
            LOGGER.exception("Error accessing url: %s", self.url)
            return None

        if not resultHandle:
            LOGGER.error("Couldn't get any results for url: %s", self.url)
            return None

        followers = None
        page = resultHandle.read().decode('utf-8')

        if self.store_page:
            with open("found_page.txt", "w") as writer:
                writer.write(page)

        for follower_re in self.followers_res:
            match = re.search(follower_re, page, re.DOTALL)
            if match:
                followers = match.group("followers")
                break

        if followers is None:
            LOGGER.info("Didn't find any follower data.")
            return None

        LOGGER.info("Followers: %s", followers)
        account = get_account(self.account_re, self.url)
        platform = platform_getter(self.platform, account)

        return Followers(self.url, platform, account, followers)
