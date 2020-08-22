#!/usr/bin/python3

#coding: utf-8

import sys
import json
import requests

args = sys.argv

if len(sys.argv) < 3:
    print("usage:"+args[0] + "input_JSON_like_file_name post_URL")
    exit(1)

path = args[1]
url = args[2]

with open(path) as fin:
    for line in fin:
        jdat = json.loads(line)
        print("line=" + line)
        print("jdat=" + json.dumps(jdat))
       res = requests.post(url, json.dumps(jdat), headers = {"Content-Type" : "application/json"})
        print("response=" + json.dumps(res.json()))

exit(0)

if __name__=='__main__':
    main()

