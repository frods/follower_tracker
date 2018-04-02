from process.pinterest import ProcessPinterest

VALID_URL = 'https://www.pinterest.com/mytheresacom/'
ACCOUNT = 'mytheresacom'


def platform_getter(platform, account):
    return platform


def test_can_process_pass():
    assert ProcessPinterest.can_process(VALID_URL)


def test_can_process_fail():
    assert not ProcessPinterest.can_process('')


def test_get_followers():
    processor = ProcessPinterest(VALID_URL, False)
    followers = processor.get_followers(platform_getter)
    assert followers is not None
    assert followers.platform == ProcessPinterest.PLATFORM
    assert followers.url == VALID_URL
    assert followers.account == ACCOUNT
    assert followers.count != 0
