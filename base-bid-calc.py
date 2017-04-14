import pandas as pd
from pandas import DataFrame
import numpy as np
import csv

#read data file, must have "ACTR" & "PCTR as columns
df = pd.read_csv("newfile.csv")

dict1 = dict()

for x in range(1, 3): #set base bid range
    df['bid'] = df.apply(lambda row: (x) * (row['PCTR'] / row['ACTR']), axis=1)

    df2 = df[(df.bid > df.payprice)]

    base_bid = x
    ctr = df2['click'].sum().astype('float64') / df2['logtype'].sum().astype('float64')

    print "Base Bid:", x
    print "CTR:", ctr

    dict2 = {x: ctr}

    dict1.update(dict2)

print "BEST BID VALUE BELOW"
print max(dict1, key=dict1.get)

data = pd.DataFrame.from_dict(dict1, orient="index")
#SET OUTPUT CSV NAME
data.to_csv("test3.csv")
#CONFIRM OUTPUT CSV NAME
dataframe = pd.read_csv("test3.csv", index_col=0)
d = dataframe.to_dict("split")
d = dict(zip(d["index"], d["data"]))