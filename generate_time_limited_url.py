#!/usr/bin/python
from __future__ import print_function
import boto
import argparse

parser = argparse.ArgumentParser(description="Generates a time limited url for\
                                            a key you control on Amazon S3.")

parser.add_argument("s3key",
        help="Target s3key full path e.g. s3://my.bucket/bla/bli.csv")

parser.add_argument("--expires-in", default='300', type=int,
        help="Url validity time in seconds, default 5 minutes.")

parser.add_argument("--access-key-id",
        help="Amazon API access key (best if you put in default boto location\
                ~/.aws/credentials).")
parser.add_argument("--secret-key",
        help="Amazon API secret key (best if you put in default boto location\
                ~/.aws/credentials).")

args = parser.parse_args()

s3key = args.s3key
expires_in = args.expires_in

def parse_s3key(s3key):
    tokens = s3key.split('/')
    if len(tokens) < 4 or tokens[0] != 's3:' or tokens[1] != '':
        raise(ValueError("invalid s3 key supplied",s3key))
    file_name = tokens[-1]
    bucket = tokens [2]
    prefix = '/'.join(tokens[3:-1]) if len(tokens) > 4 else ''
    return bucket, prefix, file_name

bucket, prefix, file_name = parse_s3key(s3key)

s3_conn = boto.connect_s3(args.access_key_id, args.secret_key)
bucket = s3_conn.get_bucket(bucket)
key = bucket.get_key(prefix+'/'+file_name)
if key:
    print(key.generate_url(expires_in))
    print("Expires in", expires_in, "seconds.")
else:
    print("Unable to find key on S3.")

