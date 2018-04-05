from . import basic_url


class ProcessTwitter(basic_url.ProcessBasicUrl):
    PLATFORM = "twitter"
    ACCOUNT_RE = r"twitter\.com/(?P<account>[^/]*)"
    FOLLOWERS_RES = [
        r'followers">.*<div class="statnum">(?P<followers>.*?)</div>.*?'
        '<div class="statlabel"> Followers </div>',
        r'title="(?P<followers>[\d,]+) Followers" data-nav="followers"']

    @staticmethod
    def can_process(url):
        return basic_url.get_account(
            ProcessTwitter.ACCOUNT_RE, url) is not None

    def __init__(self, url, store_page):
        super(ProcessTwitter, self).__init__(
            ProcessTwitter.PLATFORM,
            ProcessTwitter.ACCOUNT_RE,
            ProcessTwitter.FOLLOWERS_RES,
            url,
            store_page)
