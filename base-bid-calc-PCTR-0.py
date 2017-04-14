import pandas as pd
from pandas import DataFrame
import numpy as np
import csv

#read data file, must have "ACTR" & "PCTR as columns
df = pd.read_csv("newfile.csv")
dict1 = dict()

pctrmin = 0.00196419

print "PCTR Minimum:", pctrmin

for x in range(1, 11):
    bid = []
    for index, row in df.iterrows():
        if row['PCTR'] > pctrmin:
            bid.append((x * row['PCTR']) / row['ACTR'])
        else:
            bid.append(0)

    df['bid'] = bid

    df2 = df[(df.bid > df.payprice)]

    base_bid = x
    ctr = df2['click'].sum().astype('float64') / df2['logtype'].sum().astype('float64')
    clicks = df2['click'].sum()
    spend = df2['bid'].sum()
    bidTotal = df['bid'].sum()
    cpm = spend.astype('float64') / df2['logtype'].sum().astype('float64')
    cpc = None
    if clicks == 0:
        cpc = spend
    else:
        cpc = spend.astype('float64') / clicks

    print "\nBase Bid:", x
    print "Click-Through Rate:", ctr
    print "Clicks", clicks
    print "Spend", spend
    print "Total Bidprice:", bidTotal
    print "Average CPM:", cpm
    print "Average CPC:", cpc

    dict2 = {x: ctr}

    dict1.update(dict2)

print "BEST BID VALUE BELOW"
print max(dict1, key=dict1.get)

data = pd.DataFrame.from_dict(dict1, orient="index")
#SET OUTPUT CSV NAME
data.to_csv("PRINTED.csv")
#CONFIRM OUTPUT CSV NAME
dataframe = pd.read_csv("PRINTED.csv", index_col=0)
d = dataframe.to_dict("split")
d = dict(zip(d["index"], d["data"]))