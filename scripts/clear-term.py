import requests
import time
import argparse

BASE_URI = 'http://15.165.226.60:8080'

def request(method, path, headers=None, body=None):
    global BASE_URI

    res = requests.request(method=method, url=BASE_URI + path, json=body, headers=headers)
    res.raise_for_status()

def main():
    parser = argparse.ArgumentParser(description='Clear term')
    parser.add_argument('--term')
    args = parser.parse_args()

    while True: 
        try:
            requests.request(method='GET', url=BASE_URI + '/')
            break
        except requests.exceptions.ConnectionError:
            time.sleep(1)

    request('POST', f"/admin/clear-term/{args.term}")

if __name__ == '__main__':
    main()
