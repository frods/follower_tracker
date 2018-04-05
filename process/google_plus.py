from . import basic_url


class ProcessGooglePlus(basic_url.ProcessBasicUrl):
    PLATFORM = "google plus"
    ACCOUNT_RE = r"plus\.google\.com.*?/(?P<account>[^/]*)"
    FOLLOWERS_RES = [
        r'<div class="WH0GUe"><span>(?P<followers>[\d,]+)</span> followers',
        r'">(?P<followers>[\d,]+)</span> followers',
        r'<br>(?P<followers>[\d,]+) followers</div>']

    @staticmethod
    def can_process(url):
        return basic_url.get_account(
            ProcessGooglePlus.ACCOUNT_RE, url) is not None

    def __init__(self, url, store_page):
        super(ProcessGooglePlus, self).__init__(
            ProcessGooglePlus.PLATFORM,
            ProcessGooglePlus.ACCOUNT_RE,
            ProcessGooglePlus.FOLLOWERS_RES,
            url,
            store_page)
