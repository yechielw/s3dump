#!/bin/python
import sys
import requests
import xml.etree.ElementTree as ET
from pathlib import Path
import requests
import argparse
from tqdm.auto import tqdm
from time import sleep
def my_progress_bar(current_value, max_value,file_name):
    progress = current_value / max_value
    bar_length = 50
    filled_length = int(bar_length * progress)
    bar = '=' * filled_length + '-' * (bar_length - filled_length)
    tqdm.write(f"\r[{bar}] {progress:.0%} : {file_name}", end="")

parser = argparse.ArgumentParser()
parser.add_argument('-d', action='store_true')
parser.add_argument('-u', type=str)
args = parser.parse_args()

download = args.d

url = args.u

if not url.endswith("/"):
    url += "/"
if not url.startswith("http"):
    sys.exit("Not a url")


# a function that downloads a binery file and cerats its parent directory if doesnt exits
def download_file(url):
    local_filename =  ("/".join(url.split('/')[2:]))
    local_directory =  ("/".join(url.split('/')[2:-1]))
    Path(local_directory).mkdir(parents=True, exist_ok=True)
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk:
                f.write(chunk)
    return local_filename


response = requests.get(url)
root = ET.fromstring(response.text)

keys = root.findall(".//{*}Contents/{*}Key")

total = 0 
for ind in keys:
    if not ind.text.endswith("/"):
        total += 1
print("number of files to be downloaded: "+ str(total))

index = 0
try:
    for key in keys:
        if not key.text.endswith("/"):


            #for ind in keys:
                    
            index += 1
            if download == True:
                download_file(url+key.text)
                sleep(1)
                my_progress_bar(index,total,key.text.split("/")[-1])
            else:
                print(key.text)
except KeyboardInterrupt:
    print("\nGoodbye :)")

if download == False:
    print("\n=========================\n\nNumber of items: "+str(index)+"\n\nThis is a dry run. to download the files run the script with -d")
