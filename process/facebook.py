from . import basic_url


class ProcessFacebook(basic_url.ProcessBasicUrl):
    PLATFORM = "facebook"
    ACCOUNT_RE = r"facebook\.com/(?P<account>[^/]*)"
    FOLLOWERS_RES = [
        r'<meta name="description" content=".*?(?P<followers>[\d,]+) likes',
        r'<span id="PagesLikesCountDOMID">.*?>(?P<followers>[\d,]+) <',
        r'content=".* (?P<followers>[\d,]+) likes']

    @staticmethod
    def can_process(url):
        return basic_url.get_account(
            ProcessFacebook.ACCOUNT_RE, url) is not None

    def __init__(self, url, store_page):
        super(ProcessFacebook, self).__init__(
            ProcessFacebook.PLATFORM,
            ProcessFacebook.ACCOUNT_RE,
            ProcessFacebook.FOLLOWERS_RES,
            url,
            store_page)
