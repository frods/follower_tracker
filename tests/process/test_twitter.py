from process.twitter import ProcessTwitter

VALID_URL = 'https://twitter.com/smartzer'
ACCOUNT = 'smartzer'


def platform_getter(platform, account):
    return platform


def test_can_process_pass():
    assert ProcessTwitter.can_process(VALID_URL)


def test_can_process_fail():
    assert not ProcessTwitter.can_process('')


def test_get_followers():
    processor = ProcessTwitter(VALID_URL, False)
    followers = processor.get_followers(platform_getter)
    assert followers is not None
    assert followers.platform == ProcessTwitter.PLATFORM
    assert followers.url == VALID_URL
    assert followers.account == ACCOUNT
    assert followers.count != 0
