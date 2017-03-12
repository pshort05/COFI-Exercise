#!/usr/bin/python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
#
#                               COFI_coding_exercise.py     by Paul Short
#                                                           paul@jpkweb.com
#                                                           using Python v3.6
#
# ----------------------------------------------------------------------------------------------------------------------
import pycurl, json
import pprint
from io import BytesIO

def getAllTransactions():
    cofiURL = 'https://2016.api.levelmoney.com/api/v2/core/get-all-transactions'
    postData = json.dumps({"args": {"uid": 1110590645, "token": "61452E2839011A3A3D2B9B97A3FA3843", "api-token": "AppTokenForInterview", "json-strict-mode": False, "json-verbose-response": False}})
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, cofiURL)
    c.setopt(c.HTTPHEADER, ['Accept: application/json', 'Content-Type: application/json'])
    c.setopt(c.POST, 1)
    c.setopt(c.POSTFIELDS, postData)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    data = json.loads(buffer.getvalue())
    return data

#----------- begin main!!

jsonData = getAllTransactions()
pprint.pprint(jsonData)


