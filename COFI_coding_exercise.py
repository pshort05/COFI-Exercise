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
import sys
import unittest

# TODO: move these functions into a class - this is a short exercise but the class would be more useful if this gets expanded

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
    return json.loads(buffer.getvalue())

# I just duplicated the code to get the future transacations
# TODO: create a generic transaction with variable URL, POST and HEADER
def getFutureTransactions():
    cofi_url = 'https://2016.api.levelmoney.com/api/v2/core/projected-transactions-for-month'
    postData = json.dumps({"args": {"uid": 1110590645, "token": "61452E2839011A3A3D2B9B97A3FA3843", "api-token": "AppTokenForInterview", "json-strict-mode": False, "json-verbose-response": False}, "year": 2017, "month": 3})
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, cofi_url)
    c.setopt(c.HTTPHEADER, ['Accept: application/json', 'Content-Type: application/json'])
    c.setopt(c.POST, 1)
    c.setopt(c.POSTFIELDS, postData)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    return json.loads(buffer.getvalue())


# ----------- begin main!! -----------

# Maximum number of transactions to process
MAXIMUM_TRANSACTIONS = 100000

# get all the transaction data
jsonData = getAllTransactions()
futureData = getFutureTransactions()

# dictionaries for each transaction type to test
accountIncome = {}
accountExpenses = {}
accountExpensesDonuts = {}
accountCCPayments = {}
accountCCExpenses = {}
accountFutureExpenses = {}
currentAmount=0

# used to save the first and last month in the series - for now it will assume that the transactions are in order by date
# additional code should be put in place to handle out of order transactions
monthBegin = ''
monthEnd = ''
month = ''

# items to calculate the average expenses and income - since we are walking through all transactions we will use this to
# to calculate the data rather then running through the data a second time
# calcuation used to determine the "average" income and expenses :  simple average calculation with the max and min removed


# loop through the data and grab the items needed create the summary report
# I thought about importing this into SQL and using SQL statements but both methods will be just as easy to implement
# Loop through until we hit the end
for i in range (0,MAXIMUM_TRANSACTIONS):
    try:
        transactionData = jsonData["transactions"][i]
    except:
        #save the last month of the transactions
        monthEnd = month
        #print("Number of records:", i, "First Month:", monthBegin, "Last Month:", monthEnd)
        break

    amount = transactionData.get("amount")/10000
    month = transactionData.get("transaction-time")[:7]
    merchant = transactionData.get("merchant")
    #save the first month in the transactions
    if( i == 0 ) :
        monthBegin = month
    #print (round(amount, 2), month, merchant)

    # Summarize each of the transactions based on the amount
    if (amount > 0):
        currentAmount = accountIncome.get(month, 0)+ amount
        accountIncome.update({month : round(currentAmount, 2)} )
    else:
        currentAmount = accountExpenses.get(month, 0) + amount
        accountExpenses.update({month : round(currentAmount, 2)})

    # Grab the 'Donut' and Credit Card transactions - reading through the data we need to grab the "Dunkin and Krispy Kreme Donuts" vendors
    # this code is a bit redundant and can be simplified by passing the account directionary and the amount to a function
    if ("DUNKIN" in merchant) or ("Donut" in merchant):
        currentAmount = accountExpensesDonuts.get(month, 0)+ amount
        accountExpensesDonuts.update({month : round(currentAmount, 2)} )
    elif ( "Credit Card Payment" in merchant ):
        currentAmount = accountCCExpenses.get(month, 0)+ amount
        accountCCExpenses.update({month : round(currentAmount, 2)} )
    elif ( "CC Payment" in merchant ):
        currentAmount = accountCCPayments.get(month, 0)+ amount
        accountCCPayments.update({month : round(currentAmount, 2)} )

# Process the expected transactions
for i in range (0, MAXIMUM_TRANSACTIONS):
    pass

# Print all the data out now that it's collected
# Print out the transactions in a ledger like format
# Convert the dates in to numbers that can be used in for statements
startYear = int(monthBegin[:4])
endYear = int(monthEnd[:4])
expenseSum = 0
incomeSum = 0
numMonths = 0
#print (startYear, endYear)


print( "Month   Expenses  Income   Donuts  CreditCard")
print( "-----   --------  ------   ------  ----------")
# walk through all the possible months from the start to end - note there are extra in the first and last year using this method
for yr in range (startYear, endYear+1):
    for mn in range ( 1, 13):
        tmpYear = str(yr).zfill(4) + "-" + str(mn).zfill(2)
        tmpExpense = accountExpenses.get(tmpYear, 0)
        tmpIncome = accountIncome.get(tmpYear, 0)
        if( (tmpExpense != 0) and (tmpIncome!=0) ):
            # TODO : this won't work if there is a month with no income or expenses, but the data did not have that so it will work for the demo
            expenseSum += tmpExpense
            incomeSum += tmpIncome
            numMonths += 1
            print( tmpYear, "$%.2f" % accountExpenses.get(tmpYear,0), "$%.2f" % accountIncome.get(tmpYear,0), "$%06.2f" % accountExpensesDonuts.get(tmpYear,0), "$%07.2f" % accountCCPayments.get(tmpYear,0) )
print ( "Average", "$%.2f" % (expenseSum/numMonths), "$%.2f" % (incomeSum/numMonths) )



