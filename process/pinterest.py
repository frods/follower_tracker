from . import basic_url


class ProcessPinterest(basic_url.ProcessBasicUrl):
    PLATFORM = "pinterest"
    ACCOUNT_RE = r"pinterest\.com/(?P<account>[^/]*)"
    FOLLOWERS_RES = [
        r'name="pinterestapp:followers" content="(?P<followers>\d+)"']

    @staticmethod
    def can_process(url):
        return basic_url.get_account(
            ProcessPinterest.ACCOUNT_RE, url) is not None

    def __init__(self, url, store_page):
        super(ProcessPinterest, self).__init__(
            ProcessPinterest.PLATFORM,
            ProcessPinterest.ACCOUNT_RE,
            ProcessPinterest.FOLLOWERS_RES,
            url,
            store_page)
