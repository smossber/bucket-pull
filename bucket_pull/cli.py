#!/usr/bin/env python3
from google.cloud import storage
import argparse
import re
import sys
import os
from urllib.parse import urlparse
from pathlib import Path
from threading import Thread

parser = argparse.ArgumentParser(prog="bucket-pull",
                                 description="""
                                    Utility to pull down everything in a bucket path to a local path.
                                    """,
                                 epilog="""
                                    Example: bucket-pull gs://bucket/mydir /some/path
                                    """)

parser.add_argument('bucket_url', nargs='?', metavar="gs://bucket/path/to/dir")
parser.add_argument('local_path', nargs='?',metavar="/path/to/destination")
parser.add_argument('-m',action='store_true',dest='multithread',help="multithreaded sync")

if len(sys.argv) < 2:
    parser.print_help()
    sys.exit(1)

args = parser.parse_args()

def fail(error):
    print("Error: " + error)
    sys.exit(1)

bucket_url = args.bucket_url

if not re.match(r"^gs://",bucket_url):
    fail("bucket url must start with 'gs://'")

try:
    url = urlparse(bucket_url)
except:
    fail("Could not parse bucket_url")

bucket_name = url.netloc
source_dir = url.path
source_dir = source_dir.split("/")[1]

local_path = args.local_path
if not os.path.exists(local_path):
    fail("Path %s does not exist" % local_path)


storage_client = storage.Client()

# https://github.com/googleapis/python-storage/blob/main/samples/snippets/storage_list_files.py
def list_blobs_in_dir(bucket_name,directory, storage_client):
    bucket = storage_client.get_bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=directory)
    return blobs



def download_blob(blob,destination_dir):
    path = Path(blob.name)

    destination_file_path = Path("%s/%s" % (destination_dir, str(path)))
    # Create directories if they don't exist
    destination_file_path.parent.mkdir(parents=True,exist_ok=True)

    print("Downloading to " + str(destination_file_path))


    blob.download_to_filename(str(destination_file_path))



def main():
    blob_list = list_blobs_in_dir(bucket_name,source_dir,storage_client)

    for blob in blob_list:
        # skip if blob is a directory, we create parent dirs when downloading the files
        if re.match("^(.*/)$",blob.name):
            continue
        if args.multithread:
            t = Thread(target=download_blob,args=(blob,local_path))
            t.start()
        else:
            download_blob(blob,local_path)
