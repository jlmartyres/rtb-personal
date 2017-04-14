import pandas as pd
from pandas import DataFrame
import numpy as np
import csv
import os.path

#read data file, must have "ACTR" & "PCTR as columns
df = pd.read_csv("GBRTPredictions.csv")

pctrmin = 0.00081

print "PCTR Minimum:", pctrmin

maxCTRBid = None
maxCTRValue = None

csvFileName = "GBRTOutputPCTR0dot00081.csv"

if not os.path.isfile(csvFileName):
    thisfile = open(csvFileName, 'w')
    thisfile.write('basebid, imps, ctr, clicks, spend, bidtotal, cpm, cpc\n')
    thisfile.close()

for x in range(9, 301):
    bid = []
    for index, row in df.iterrows():
        if row['PCTR'] > pctrmin:
            bid.append((x * row['PCTR']) / row['ACTR'])
        else:
            bid.append(0)

    df['bid'] = bid

    #df['bid'] = df.apply(lambda row: (x) * (row['PCTR'] / row['ACTR']), axis=1)

    df2 = df[(df.bid > df.payprice)]

    base_bid = x
    imp = df2['logtype'].sum().astype('float64')
    ctr = df2['click'].sum().astype('float64') / df2['logtype'].sum().astype('float64')
    clicks = df2['click'].sum()
    spend = df2['payprice'].sum()/1000
    bidTotal = df['bid'].sum()/1000
    cpm = df2['payprice'].sum() / df2['logtype'].sum().astype('float64')
    cpc = None
    if clicks == 0:
        cpc = spend
    else:
        cpc = spend.astype('float64') / clicks

    file = open(csvFileName, 'a')
    file.write('{}, {}, {}, {}, {}, {}, {}, {}\n'.format(base_bid, imp, ctr, clicks, spend, bidTotal, cpm, cpc))
    file.close()

    if ctr > maxCTRValue:
        maxCTRBid = base_bid
        maxCTRValue = ctr

    print "\nBase Bid", x
    print "Click-Through Rate:", ctr
    print "Clicks", clicks
    print "Spend", spend
    print "Total Bidprice:", bidTotal
    print "Average CPM:", cpm
    print "Average CPC:", cpc

    if spend > 6250:
        print "\nBid Total Exceeded, Terminating"
        break

print "\nFinished"
print "\nBase Bid", maxCTRBid, "has largest CTR", maxCTRValue