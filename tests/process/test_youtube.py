from process.youtube import ProcessYoutube

VALID_URL = 'https://m.youtube.com/user/Mytheresacom'
ACCOUNT = 'Mytheresacom'


def platform_getter(platform, account):
    return platform


def test_can_process_pass():
    assert ProcessYoutube.can_process(VALID_URL)


def test_can_process_fail():
    assert not ProcessYoutube.can_process('')


def test_get_followers():
    processor = ProcessYoutube(VALID_URL, False)
    followers = processor.get_followers(platform_getter)
    assert followers is not None
    assert followers.platform == ProcessYoutube.PLATFORM
    assert followers.url == VALID_URL
    assert followers.account == ACCOUNT
    assert followers.count != 0
