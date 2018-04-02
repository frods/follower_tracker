from process.instagram import ProcessInstagram

VALID_URL = 'https://instagram.com/mytheresaprgirl/'
ACCOUNT = 'mytheresaprgirl'


def platform_getter(platform, account):
    return platform


def test_can_process_pass():
    assert ProcessInstagram.can_process(VALID_URL)


def test_can_process_fail():
    assert not ProcessInstagram.can_process('')


def test_get_followers():
    processor = ProcessInstagram(VALID_URL, False)
    followers = processor.get_followers(platform_getter)
    assert followers is not None
    assert followers.platform == ProcessInstagram.PLATFORM
    assert followers.url == VALID_URL
    assert followers.account == ACCOUNT
    assert followers.count != 0
