"""
Script to upload files to Zenodo repository.

$ python zenodome.py --help

for usage.
"""

import argparse
import json
import os
import subprocess
import shlex


parser = argparse.ArgumentParser(description='Upload to zenodo')

parser.add_argument('--id', metavar='id', type=str, nargs=1,
                    help='Zenodo depository ID; http://zenodo.org/deposit/<ID>',
                    required=True)

parser.add_argument('--token', metavar='token', type=str, nargs=1,
                    help='Zenodo API token', required=True)

parser.add_argument('--filepaths', metavar='filepaths', type=str, nargs='+',
                    help='Filepath(s) to upload. Accepts globs')

args = parser.parse_args()
filepaths = args.filepaths
depository_id = args.id[0]
token = args.token[0]

cmd = 'curl -H "Accept: application/json" -H "Authorization: Bearer {}" "https://www.zenodo.org/api/deposit/depositions/{}"'.format(token, depository_id)

p = subprocess.Popen(shlex.split(cmd), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, err = p.communicate()

json_data = json.loads(output)
bucket = json_data['links']['bucket']

for filepath in filepaths:
    filename = os.path.split(filepath)[-1]
    cmd_upload = "curl --progress-bar -o /dev/null --upload-file {} {}/{}?access_token={}" .format(filepath, bucket, filename, token)
    p = subprocess.Popen(shlex.split(cmd_upload), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = p.communicate()
