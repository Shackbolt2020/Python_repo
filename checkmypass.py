import requests
import hashlib
import sys

def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching {res.status_code} check API and try again')
    return res

def get_password_leaks(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0

def pwned_api_check(password):
    sha1pass = hashlib.sha1(password.encode('utf-8')).hexdigest().upper() #utf-8 is used to encode unicode characters to binary digits
    first5_char, tail = sha1pass[:5:], sha1pass[5:]
    response = request_api_data(first5_char)
    return get_password_leaks(response, tail)

def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f'{password} was found {count} times, it is suggested you change it')
        else:
            print(f'{password} was NOT found, you\'re safe!')

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
