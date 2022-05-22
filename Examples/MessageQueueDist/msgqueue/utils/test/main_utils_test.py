from argparse import Namespace

from ..main_utils import configure_middleware
from ...middleware.authenticate import Authenticator
from ...middleware.log import log
from ...middleware.timestamp import timestamp


def create_namespace(log=False, auth=False, timestamp=False):
    n = Namespace()
    n.log = log
    n.auth = auth
    n.timestamp = timestamp
    return n


def test_configure_middleware_without_args():
    n = create_namespace()
    middleware = configure_middleware(n)
    assert middleware == []


def test_configure_middleware_with_log_and_timestamp():
    n = create_namespace(log=True, timestamp=True)
    middleware = configure_middleware(n)
    assert middleware == [log, timestamp]