import argparse

from ..middleware.authenticate import Authenticator
from ..middleware.log import log
from ..middleware.timestamp import timestamp


def configure_middleware(config) -> list:
    middleware = []
    if auth_token := config.get("auth_token"):
        middleware.append(Authenticator(auth_token))
    if config.get("log"):
        middleware.append(log)
    if config.get("timestamp"):
        middleware.append(timestamp)
    return middleware
