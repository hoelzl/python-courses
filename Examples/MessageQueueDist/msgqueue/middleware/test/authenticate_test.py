from ..authenticate import Authenticator


def test_authenticate_when_successful():
    msg = {'id': '1234', 'text': "text", 'auth': 'secret!'}
    keys = msg.keys()
    authenticate = Authenticator('secret!')
    result = authenticate(msg)

    assert msg is result
    assert result.keys() == keys


def check_authentication_error(msg, result):
    assert msg is not result
    assert set(result.keys()) == {'id', 'error_code', 'error_msg'}
    assert result['id'] == msg['id']
    assert result['error_code'] == 401
    assert result['error_msg'] == "Unauthorized"


def test_authenticate_when_bad_auth_token():
    msg = {'id': '1234', 'text': "text", 'auth': 'not-so-secret'}
    authenticate = Authenticator('secret!')
    result = authenticate(msg)

    check_authentication_error(msg, result)


def test_authenticate_when_no_auth_token():
    msg = {'id': '1234', 'text': "text"}
    authenticate = Authenticator('secret!')
    result = authenticate(msg)

    check_authentication_error(msg, result)
