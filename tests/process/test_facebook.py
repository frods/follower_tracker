from process.facebook import ProcessFacebook

VALID_URL = 'https://www.facebook.com/smartzerapp/likes'
ACCOUNT = 'smartzerapp'


def platform_getter(platform, account):
    return platform


def test_can_process_pass():
    assert ProcessFacebook.can_process(VALID_URL)


def test_can_process_fail():
    assert not ProcessFacebook.can_process('')


def test_get_followers():
    processor = ProcessFacebook(VALID_URL, False)
    followers = processor.get_followers(platform_getter)
    assert followers is not None
    assert followers.platform == ProcessFacebook.PLATFORM
    assert followers.url == VALID_URL
    assert followers.account == ACCOUNT
    assert followers.count != 0
