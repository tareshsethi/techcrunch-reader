import argparse
from secrets import token_hex

import app.auth.jwt_auth

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--string_id', help='ID of the token', required=True)
    args = parser.parse_args()

    token = token_hex(16)
    print(f'Token: {token}')
    encoded_token = app.auth.jwt_auth.encode_auth_token(args.string_id, token)
    print(f'Encoded Token: {encoded_token}')
