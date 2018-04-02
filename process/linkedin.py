import logging
import asyncio
from pyppeteer import launch

from . import basic_url

LOGGER = logging.getLogger(__name__)


async def selectorVisible(page, selector):
    try:
        await page.waitForSelector(selector, visible=True, timeout=30000)
    except Exception as e:
        LOGGER.exception("Could not find %s", selector)
        return False
    return True


async def loadProperty(element, selector, prop):
    item = await element.querySelector(selector)
    if item is None:
        LOGGER.error("Could not find selector %s for element", selector)
        return None
    prop_value = await item.getProperty(prop)
    return await prop_value.jsonValue()


async def isLoggedIn(page):
    result = await page.goto("https://www.linkedin.com/feed/")

    if not result.ok:
        LOGGER.error("linkedin responded with http {}".format(result.status))
        return False

    if not await selectorVisible(page, "#extended-nav"):
        return False

    if not await selectorVisible(
            page, ".nav-item__profile-member-photo.nav-item__icon"):
        return False

    value = await loadProperty(
        page, '.nav-item__profile-member-photo.nav-item__icon', "alt")
    LOGGER.info("Logged in as %s", value)

    return True


class ProcessLinkedIn:
    PLATFORM = "linkedin"
    ACCOUNT_RE = r"linkedin\.com/company/(?P<account>[^/]*)"

    @staticmethod
    def can_process(url):
        return basic_url.get_account(
            ProcessLinkedIn.ACCOUNT_RE, url) is not None

    def __init__(self, cookie, url, store_page):
        self.cookie = cookie
        self.url = url
        self.store_page = store_page

    async def _find_followers(self, page):
        LOGGER.info("Using cookie %s", self.cookie)

        linkedin_cookie = {
            "name": "li_at",
            "value": self.cookie,
            "domain": "www.linkedin.com",
            "path": "/",
            "httpOnly": True
        }
        await page.setCookie(linkedin_cookie)

        if not await isLoggedIn(page):
            LOGGER.error("Not logged in with cookie %s", self.cookie)
            return None

        result = await page.goto(self.url)

        if not result.ok:
            LOGGER.error(
                "url: %s can't be loaded: result %s. "
                "Check if cookie is valid.",
                self.url, result.ok)
            return None

        if not await selectorVisible(
                page, ".org-top-card-module__details "):
            LOGGER.info("Not Found employees details")
            return None

        LOGGER.info("Found org-top-card-module__details")

        followers_element = ".org-top-card-module__followers-count"
        if not await selectorVisible(page, followers_element):
            return None

        value = await loadProperty(page, followers_element, "textContent")

        LOGGER.info("Found value %s", value)
        return None

    async def _get_followers(self):
        browser = await launch(devtools=True)
        page = await browser.newPage()
        followers = await self._find_followers(page)
        await browser.close()
        return followers

    def get_followers(self, platform_getter):
        result = asyncio.get_event_loop().run_until_complete(
            self._get_followers())
        return result


class ProcessLinkedInGenerator:
    @staticmethod
    def can_process(url):
        return ProcessLinkedIn.can_process(url)

    def __init__(self, cookie):
        self.cookie = cookie

    def __call__(self, url, store_page):
        return ProcessLinkedIn(self.cookie, url, store_page)
