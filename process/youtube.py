from . import basic_url


class ProcessYoutube(basic_url.ProcessBasicUrl):
    PLATFORM = "youtube"
    ACCOUNT_RE = r"youtube\.com/user/(?P<account>[^/]*)"
    FOLLOWERS_RES = [
        r'aria-label="(?P<followers>[\d,]+) subscribers']

    @staticmethod
    def can_process(url):
        return basic_url.get_account(
            ProcessYoutube.ACCOUNT_RE, url) is not None

    def __init__(self, url, store_page):
        super(ProcessYoutube, self).__init__(
            ProcessYoutube.PLATFORM,
            ProcessYoutube.ACCOUNT_RE,
            ProcessYoutube.FOLLOWERS_RES,
            url,
            store_page)
