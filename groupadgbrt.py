import pandas as pd
from pandas import DataFrame
import numpy as np
import csv
import os.path

#read data file, must have "ACTR" & "PCTR as columns
df = pd.read_csv("GBRTPredictions.csv")

maxCTRBid = None
maxCTRValue = None

pctrmin = 0.001620

csvFileName = "AdvertiserGBRT61.csv"

advertisers = (1458, 2259, 2261, 2821, 2997, 3358, 3386, 3427, 3476)

if not os.path.isfile(csvFileName):
    thisfile = open(csvFileName, 'w')
    thisfile.write('advertiser, imps, ctr, clicks, spend, bidtotal, cpm, cpc\n')
    thisfile.close()

for advertiser in advertisers:

    x = 61

    bid = []
    for index, row in df.iterrows():
        if row['PCTR'] > pctrmin:
            bid.append((x * row['PCTR']) / row['ACTR'])
        else:
            bid.append(0)

    df['bid'] = bid

    #df['bid'] = df.apply(lambda row: (x) * (row['PCTR'] / row['ACTR']), axis=1)

    temp = df[(df.bid > df.payprice)]

    df2 = temp[df.advertiser == advertiser]

    base_bid = x
    imp = df2['logtype'].sum().astype('float64')
    ctr = df2['click'].sum().astype('float64') / df2['logtype'].sum().astype('float64')
    clicks = df2['click'].sum()
    spend = df2['payprice'].sum()/1000
    bidTotal = df2['bid'].sum()/1000
    cpm = df2['payprice'].sum() / df2['logtype'].sum().astype('float64')
    cpc = None
    if clicks == 0:
        cpc = spend
    else:
        cpc = spend.astype('float64') / clicks

    file = open(csvFileName, 'a')
    file.write('{}, {}, {}, {}, {}, {}, {}, {}\n'.format(advertiser, imp, ctr, clicks, spend, bidTotal, cpm, cpc))
    file.close()

    if ctr > maxCTRValue:
        maxCTRBid = base_bid
        maxCTRValue = ctr

    print "\nBid", x
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