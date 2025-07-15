import sys
import requests
import xml.etree.ElementTree as ET
from pathlib import Path
import argparse
from tqdm.auto import tqdm
from time import sleep


def my_progress_bar(current_value, max_value, file_name):
    if max_value == 0:
        progress = 0
    else:
        progress = current_value / max_value
    bar_length = 50
    filled_length = int(bar_length * progress)
    bar = '=' * filled_length + '-' * (bar_length - filled_length)
    tqdm.write(f"\r[{bar}] {progress:.0%} : {file_name}", end="")


def parse_args(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', action='store_true',
                        help="Download files instead of dry run")
    parser.add_argument('-u', type=str, required=True,
                        help="URL of the S3 bucket to process (required)")
    return parser.parse_args(argv)


def download_file(url: str) -> str:
    """Download a binary file creating parent directories as needed."""
    local_filename = "/".join(url.split('/')[2:])
    local_directory = "/".join(url.split('/')[2:-1])
    Path(local_directory).mkdir(parents=True, exist_ok=True)
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename


def main(argv=None):
    args = parse_args(argv)
    download = args.d
    url = args.u
    if not url.endswith('/'):
        url += '/'
    if not url.startswith('http'):
        sys.exit('Not a url')

    response = requests.get(url)
    root = ET.fromstring(response.text)
    keys = root.findall('.//{*}Contents/{*}Key')

    total = sum(1 for k in keys if not k.text.endswith('/'))
    print('number of files to be downloaded: ' + str(total))

    index = 0
    try:
        for key in keys:
            if key.text.endswith('/'):
                continue
            index += 1
            if download:
                download_file(url + key.text)
                sleep(1)
                my_progress_bar(index, total, key.text.split('/')[-1])
            else:
                print(key.text)
    except KeyboardInterrupt:
        print('\nGoodbye :)')

    if not download:
        print('\n=========================\n\nNumber of items: ' + str(index) +
              '\n\nThis is a dry run. to download the files run the script with -d')


if __name__ == '__main__':
    main()
