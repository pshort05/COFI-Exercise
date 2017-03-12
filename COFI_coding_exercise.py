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
import unittest

# Function to grab all the transactions from the server using a REST API like transaction
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

# Maximum number of transactions to process
MAXIMUM_TRANSACTIONS = 100000

jsonData = getAllTransactions()

# dictionaries for each transaction type to test
accountIncome = {}
accountExpenses = {}
accountExpensesDonuts = {}
currentAmount=0

# loop through the data and grab the items needed create the summary report
# I thought about importing this into SQL and using SQL statements but both methods will be just as easy to implement
# Loop through until we hit the end
for i in range (0,MAXIMUM_TRANSACTIONS):
    try:
        transactionData = jsonData["transactions"][i]
    except:
        print("Number of records", i)
        break

    amount = transactionData.get("amount")
    month = transactionData.get("transaction-time")[:7]
    merchant = transactionData.get("merchant")
    print (amount, month, merchant)

    # Summarize each of the transactions based on the amount
    if (amount > 0):
        currentAmount = accountIncome.get(month, 0)+ amount
        accountIncome.update({month : currentAmount} )
    else:
        currentAmount = accountExpenses.get(month, 0) + amount
        accountExpenses.update({month : currentAmount})

    # Grab the 'Donut' transactions - reading through the data we need to grab the "Dunkin and Krispy Kreme Donuts" vendors
    if ("DUNKIN" in merchant) or ("Donut" in merchant):
        currentAmount = accountExpensesDonuts.get(month, 0)+ amount
        accountExpensesDonuts.update({month : currentAmount} )


#temporary printing while coding
pprint.pprint( accountExpenses.items())
pprint.pprint( accountIncome.items())
pprint.pprint( accountExpensesDonuts.items())
