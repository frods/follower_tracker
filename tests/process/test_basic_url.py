import pytest

from process.basic_url import ProcessBasicUrl


def test_can_process():
    with pytest.raises(NotImplementedError):
        ProcessBasicUrl.can_process('')
