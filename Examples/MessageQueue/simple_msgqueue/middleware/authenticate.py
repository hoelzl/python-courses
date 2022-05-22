def authenticate(msg: dict) -> dict:
    print(f"-> Authenticating message {msg.get('id', '<no id>')}")
    if msg.get('auth') == 'secret!':
        return msg
    else:
        return {
            'id': msg.get('id', "No ID!"),
            'error_code': 401,
            'error_msg': "Unauthorized"
        }


class Authenticator:
    def __init__(self, secret: str):
        self.secret = secret

    def __call__(self, msg: dict):
        print(f"-> Authenticating message {msg.get('id', '<no id>')} against {self.secret}")
        if msg.get('auth') == self.secret:
            return msg
        else:
            return {
                'id': msg.get('id', "No ID!"),
                'error_code': 401,
                'error_msg': "Unauthorized"
            }
