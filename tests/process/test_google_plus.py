import pytest

from process.google_plus import ProcessGooglePlus

VALID_URL = 'https://plus.google.com/app/basic/+mytheresa'
ACCOUNT = '+mytheresa'


def platform_getter(platform, account):
    return platform


def test_can_process_pass():
    assert ProcessGooglePlus.can_process(VALID_URL)


def test_can_process_fail():
    assert not ProcessGooglePlus.can_process('')


@pytest.mark.skip(reason="followers no long shown on page")
def test_get_followers():
    processor = ProcessGooglePlus(VALID_URL, False)
    followers = processor.get_followers(platform_getter)
    assert followers is not None
    assert followers.platform == ProcessGooglePlus.PLATFORM
    assert followers.url == VALID_URL
    assert followers.account == ACCOUNT
    assert followers.count != 0
