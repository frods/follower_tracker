from . import basic_url


class ProcessInstagram(basic_url.ProcessBasicUrl):
    PLATFORM = "instagram"
    ACCOUNT_RE = r"instagram\.com/(?P<account>[^/]*)"
    FOLLOWERS_RES = [
        r'\"followed_by\":(?P<followers>[\d]+)',
        r'\"followed_by\":\s*{\"count\":\s*(?P<followers>[\d]+)}',
        r'\"edge_followed_by":\s*{\"count\":\s*(?P<followers>[\d]+)}'
    ]

    @staticmethod
    def can_process(url):
        return basic_url.get_account(
            ProcessInstagram.ACCOUNT_RE, url) is not None

    def __init__(self, url, store_page):
        super(ProcessInstagram, self).__init__(
            ProcessInstagram.PLATFORM,
            ProcessInstagram.ACCOUNT_RE,
            ProcessInstagram.FOLLOWERS_RES,
            url,
            store_page)
