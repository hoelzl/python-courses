from ..main_utils import configure_middleware
from ...middleware.log import log
from ...middleware.timestamp import timestamp


def make_dict(log=False, auth=False, timestamp=False):
    return dict(log=log, auth=auth, timestamp=timestamp)


def test_configure_middleware_without_args():
    middleware = configure_middleware(**make_dict())
    assert middleware == []


def test_configure_middleware_with_log_and_timestamp():
    d = make_dict(log=True, timestamp=True)
    middleware = configure_middleware(**d)
    assert middleware == [log, timestamp]