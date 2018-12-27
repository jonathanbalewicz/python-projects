"""
Purpose: Preprocess OTC BB stock data for machine learning. ML should make a model
to predict the next day's price. Test data is saved as a percent increase rather
than prices. Slices data into 30 day slices, ML will make predictions based on
the previous 30 days. Saves in the format Open, High, Low, Close, Volume where
volume is normalized and prices are scaled to start at 1. Stock data is taken from
csv files from eoddata.com. Reads "todays" (June 15 2018) data from this folder.
Reads in the folder /OTC_BB from January 1 to June 14 2018. 

Saves:
    training data:
        training_stock_data.csv
    target data:
        target_stock_data.csv
    data that will be used by the ml to make predictions:
        prediction_stock_data.csv
    initial stock prices, before predictions:
        stock_init.csv
    todays price changes:
        today_change.csv
    ticker symbols:
        ticker_frame.csv

"""

import pandas as pd
import numpy as np
from pathlib import Path

y=1

first_month=1
first_year=2018
last_month=6
last_year=2018

todays_date = 20180615
yest_date =20180614

days=30 # Days per slice

# GATHER DATA

print("Gathering data [1/4] ...")
print("Gathering tickers...")

today=pd.read_csv('OTCBB_{}.txt'.format(todays_date))
yest=pd.read_csv('OTC_BB/OTCBB_{}.txt'.format(yest_date))
settoday=set(today['<ticker>'])

tttticker=settoday.intersection(set(yest['<ticker>']))

# Read files for tickers into var tickers
for x in range(1,32):
    f=Path("OTC_BB/OTCBB_{year}{first_month:02d}{day:02d}.txt".format(day=x, first_month=first_month, year=first_year))
    if f.is_file():
        file0=pd.read_csv(f)
        if y==1:
            tickers=tttticker
            y=2
        tickers=tickers.intersection(file0['<ticker>'])
for year in range(first_year-last_year+1):
    year+=first_year
    for month in range(last_month-first_month):
        month+=first_month+1
        for x in range(1,32):
            f=Path("OTC_BB/OTCBB_{year}{month:02d}{day:02d}.txt".format(day=x,month=month, year=year))
            if f.is_file():
                file=pd.read_csv(f)
                tickers=tickers.intersection(file['<ticker>'])

# Get rid of bankrupt companies
rem=set()
for tik in tickers:
    if tik.endswith("Q",4):
        rem.add(tik)

tickers=tickers-rem

c=0
rows=len(tickers)
vol=np.zeros((rows))
data1=[]

print("Gathering prices and volume...")
#read prices into var data1
for year in range(last_year-first_year+1):
    year+=first_year
    for month in range(last_month-first_month+1):
        month+=first_month
        for x in range(1,32):
            f=Path("OTC_BB/OTCBB_{year}{month:02d}{day:02d}.txt".format(day=x, month=month, year=year))
            if f.is_file():
                file1=pd.read_csv(f)
                # prevent holidays and weekends from being included
                vol_sum=0
                for z in range(10):
                    vol_sum+=int(file1.iloc[z,7])
                if vol_sum!=0:
                    file1.columns=['ticker', 'per', 'date', 'open{year}{month}{day}'.format(day=x, month=month, year=year), 'high{year}{month}{day}'.format(day=x, month=month, year=year), 'low{year}{month}{day}'.format(day=x, month=month, year=year), 'close{year}{month}{day}'.format(day=x, month=month, year=year), 'vol{year}{month}{day}'.format(day=x, month=month, year=year),'und']
                    file1=file1.drop(['date','per','und'],axis=1)
                    file3=file1[file1['ticker'].isin(tickers)].reset_index(drop=True) # Get rid of bankrupt companies
                    data1.append(file3)
                    vol+=np.array(file3['vol{year}{month}{day}'.format(day=x, month=month, year=year)])
                    c+=1

print("Organizing data [2/4]...")
today5=today[today['<ticker>'].isin(tickers)].reset_index(drop=True)
yest5=yest[yest['<ticker>'].isin(tickers)].reset_index(drop=True)
tickers=set(today5['<ticker>'])

data=pd.concat(data1,axis=1)

# SLICE DATA
print("Slicing {} day slices...".format(days))
test=data.iloc[:,len(data.columns)-(5*days+2):]

# t_conds is true if the ticker data is available for all time in the time frame
t_conds=test['ticker'].isin(tickers)

t_conds=t_conds.iloc[:,0]

test=test[t_conds].reset_index(drop=True)
test=test.drop(['ticker'],axis=1)
today5=today5[t_conds].reset_index(drop=True)
yest5=yest5[t_conds].reset_index(drop=True)

ticker_frame=data['ticker']

ticker_frame1=ticker_frame
data=data.drop(['ticker'],axis=1)
prediction_data=data.iloc[:,(c*5-(5*(days-1))):]

# make a list of columns and a dict of empty lists for each list
columnlist2=[]
data_dict={}
for g in range(days):
    columnlist=[]
    columnlist.append("open{}".format(g))
    columnlist.append("high{}".format(g))
    columnlist.append("low{}".format(g))
    columnlist.append("close{}".format(g))
    columnlist.append("vol{}".format(g))
    columnlist2.extend(columnlist)
    for w in columnlist:
        data_dict[w]=[]

# Slice 30 day slices, var data4 conatains these slices
data4=pd.DataFrame(data_dict)
for p in range((len(data.columns)//5)-days):
    cdata=data.iloc[:,(len(data.columns)-((5*p)+(5*days))):(len(data.columns)-(5*p))]
    ndata=cdata.columns.values
    cols={}
    for r in range(5*days):
        d=ndata[r]
        cols[d]=columnlist2[r]
    qdata=cdata.rename(columns=cols)
    data4=pd.concat([data4,qdata],ignore_index=True)

data4 = data4[columnlist2]

# CLEAN DATA
print("Deleting irrelevent stocks...")
cloprice=np.array(data4['close1'])
vol=np.array(data4['vol1'])
cloprice3=np.array(prediction_data.iloc[:,3])

# Delete stocks with prices < $0.001 or dollar volume < $1
vol3=np.array(prediction_data.iloc[:,4])
conds3=np.logical_and(cloprice3>0.001,(vol3*cloprice3)>1)
conds=np.logical_and(cloprice>0.001,(vol*cloprice)>1)
ticker_frame=ticker_frame[conds3].reset_index(drop=True)
prediction_data=prediction_data[conds3].reset_index(drop=True)
data4=data4[conds].reset_index(drop=True)
today5=today5[conds3].reset_index(drop=True)
yest5=yest5[conds3].reset_index(drop=True)

print("Calculating percent changes...")
yest=np.array(yest5['<low>'])
today_close=np.array(today5['<low>'])
today_change=(today_close/yest)*100-100

print("Separating target, test, and training data...")
target=data4
data4=data4.drop(['open{}'.format(days-1),'high{}'.format(days-1),'low{}'.format(days-1),'close{}'.format(days-1), 'vol{}'.format(days-1)],axis=1)

data=np.array(data4.values.tolist())#add head


target_list=target['close{}'.format(days-1)].values.tolist()#add head

othtest=target['close{}'.format(days-1)].values.tolist()#add tail

print("Creating ticker list...")
tticker_frame=ticker_frame#add tail
tticker_frame=tticker_frame.reset_index(drop=True)

print("Pre-processing data [3/4] ...")

#Scale data
numpy_data=np.array(data)
inverse=(1/(numpy_data[:,0]+0.000000000000001))
inverse1=inverse[:,np.newaxis]
numpy_data[:,np.arange(1,(numpy_data.shape[1]+1))%5!=0]*=inverse1
numpy_data[:,np.arange(1,(numpy_data.shape[1]+1))%5!=0]-=1
target_list*=inverse
target_list-=1

tinverse=(1/(np.array(prediction_data)[:,0]+0.000000000000001))

ttinverse=tinverse[:,np.newaxis]

numpy_prediction_data = np.array(prediction_data)
numpy_prediction_data*=ttinverse

initial=np.array(numpy_prediction_data[:,(days*5-12)])
initial-=1
prediction_data-=1

init=initial

# Scale volume
from sklearn import preprocessing
numpy_data[:,np.arange(1,(numpy_data.shape[1]+1))%5==0]=preprocessing.scale(numpy_data[:,np.arange(1,(numpy_data.shape[1]+1))%5==0])

print("Saving data [4/4] 0%...")
print("Saving training data...")
pd.DataFrame(numpy_data).to_csv("training_stock_data.csv")

print("Saving data 16%...")
print("Saving target data...")
pd.DataFrame(target_list).to_csv("target_stock_data.csv")

print("Saving data 33%...")
print("Saving test data...")
pd.DataFrame(numpy_prediction_data).to_csv("prediction_stock_data.csv")

print("Saving data 50%...")
print("Saving initial stock prices...")
pd.DataFrame(init).to_csv("stock_init.csv")

print("Saving data 67%...")
print("Saving price % changes...")
pd.DataFrame(today_change).to_csv("today_change.csv")

print("Saving data 83%...")
print("Saving ticker symbols...")
pd.DataFrame(ticker_frame).to_csv("ticker_frame.csv")
print("Saving data 100%...")

print('Done')
