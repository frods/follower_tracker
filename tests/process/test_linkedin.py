from process.linkedin import ProcessLinkedIn

VALID_URL = 'https://www.linkedin.com/company/9840573/'
ACCOUNT = '9840573'


def platform_getter(platform, account):
    return platform


def test_can_process_pass():
    assert ProcessLinkedIn.can_process(VALID_URL)


def test_can_process_fail():
    assert not ProcessLinkedIn.can_process('')


def test_get_followers():
    processor = ProcessLinkedIn(VALID_URL, False)
    followers = processor.get_followers(platform_getter)
    assert followers is not None
    assert followers.platform == ProcessLinkedIn.PLATFORM
    assert followers.url == VALID_URL
    assert followers.account == ACCOUNT
    assert followers.count != 0
