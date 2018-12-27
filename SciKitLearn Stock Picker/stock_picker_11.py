import pandas as pd
import numpy as np
from pathlib import Path
y=1

print("Opening data files...")
today=pd.read_csv('OTCBB_20180615.txt')
yest=pd.read_csv('OTC_BB/OTCBB_20180614.txt')
settoday=set(today['<ticker>'])

print("Gathering data...")
# Find tickers
tttticker=settoday.intersection(set(yest['<ticker>']))
for x in range(1,32):
    f=Path("OTC_BB/OTCBB_201803{:02d}.txt".format(x))
    if f.is_file():
        file0=pd.read_csv(f)
        if y==1:
            tickers=tttticker
            y=2
        tickers=tickers.intersection(file0['<ticker>'])

for x in range(1,32):
    f=Path("OTC_BB/OTCBB_201804{:02d}.txt".format(x))
    if f.is_file():
        file=pd.read_csv(f)
        tickers=tickers.intersection(file['<ticker>'])
for x in range(1,32):
    f=Path("OTC_BB/OTCBB_201805{:02d}.txt".format(x))
    if f.is_file():
        file=pd.read_csv(f)
        tickers=tickers.intersection(file['<ticker>'])
for x in range(1,32):
    f=Path("OTC_BB/OTCBB_201806{:02d}.txt".format(x))
    if f.is_file():
        file=pd.read_csv(f)
        tickers=tickers.intersection(file['<ticker>'])
# Delete backrupt companies
rem=set()
for tik in tickers:
    if tik.endswith("Q",4):
        rem.add(tik)

tickers=tickers-rem

# Gather prices/volume
c=0
rows=len(tickers)
vol=np.zeros((rows))
data1=[]

for x in range(1,32):
    f=Path("OTC_BB/OTCBB_201803{:02d}.txt".format(x))
    if f.is_file():
        file1=pd.read_csv(f)
        file1.columns=['ticker', 'per', 'date', 'open0{}'.format(x), 'high0{}'.format(x), 'low0{}'.format(x), 'close0{}'.format(x), 'vol0{}'.format(x),'und']
        file1=file1.drop(['date','per','und'],axis=1)
        file3=file1[file1['ticker'].isin(tickers)].reset_index(drop=True)
        data1.append(file3)
        vol+=np.array(file3['vol0{}'.format(x)])
        c+=1

for x in range(1,32):
    f=Path("OTC_BB/OTCBB_201804{:02d}.txt".format(x))
    if f.is_file():
        file2=pd.read_csv(f)
        file2.columns=['ticker', 'per', 'date', 'open1{}'.format(x), 'high1{}'.format(x), 'low1{}'.format(x), 'close1{}'.format(x), 'vol1{}'.format(x),'und']
        file2=file2.drop(['per','und'],axis=1)
        file3=file2[file2['ticker'].isin(tickers)].reset_index(drop=True)
        data1.append(file3)
        vol+=np.array(file3['vol1{}'.format(x)])
        c+=1
for x in range(1,32):
    f=Path("OTC_BB/OTCBB_201805{:02d}.txt".format(x))
    if f.is_file():
        file2=pd.read_csv(f)
        file2.columns=['ticker', 'per', 'date', 'open2{}'.format(x), 'high2{}'.format(x), 'low2{}'.format(x), 'close2{}'.format(x), 'vol2{}'.format(x),'und']
        file2=file2.drop(['per','und'],axis=1)
        file3=file2[file2['ticker'].isin(tickers)].reset_index(drop=True)
        data1.append(file3)
        vol+=np.array(file3['vol2{}'.format(x)])
        c+=1

for x in range(1,32):
    f=Path("OTC_BB/OTCBB_201806{:02d}.txt".format(x))
    if f.is_file():
        file2=pd.read_csv(f)
        file2.columns=['ticker', 'per', 'date', 'open3{}'.format(x), 'high3{}'.format(x), 'low3{}'.format(x), 'close3{}'.format(x), 'vol3{}'.format(x),'und']
        file2=file2.drop(['per','und'],axis=1)
        file3=file2[file2['ticker'].isin(tickers)].reset_index(drop=True)
        data1.append(file3)
        vol+=np.array(file3['vol3{}'.format(x)])
        c+=1

today5=today[today['<ticker>'].isin(tickers)].reset_index(drop=True)
yest5=yest[yest['<ticker>'].isin(tickers)].reset_index(drop=True)
tickers=set(today5['<ticker>'])

data=pd.concat(data1,axis=1)

print("Organizing data...")

test=data.iloc[:,len(data.columns)-42:]
t_conds=test['ticker'].isin(tickers)

t_conds=t_conds.iloc[:,0]

test=test[t_conds].reset_index(drop=True)
test=test.drop(['ticker','date'],axis=1)
today5=today5[t_conds].reset_index(drop=True)
yest5=yest5[t_conds].reset_index(drop=True)


ticker_frame=data['ticker']
date_frame2=data['date']
ticker_frame1=ticker_frame
data=data.drop(['ticker','date'],axis=1)
prediction_data=data.iloc[:,(c*5-35):]


columnlist=['open1','high1','low1','close1','vol1','open2','high2','low2','close2','vol2','open3','high3','low3','close3','vol3','open4','high4','low4','close4','vol4','open5','high5','low5','close5','vol5','open6','high6','low6','close6','vol6','open7','high7','low7','close7','vol7','open8','high8','low8','close8','vol8']
data4=pd.DataFrame({'open1':[],'high1':[],'low1':[],'close1':[],'vol1':[],'open2':[],'high2':[],'low2':[],'close2':[],'vol2':[],'open3':[],'high3':[],'low3':[],'close3':[],'vol3':[],'open4':[],'high4':[],'low4':[],'close4':[],'vol4':[],'open5':[],'high5':[],'low5':[],'close5':[],'vol5':[],'open6':[],'high6':[],'low6':[],'close6':[],'vol6':[],'open7':[],'high7':[],'low7':[],'close7':[],'vol7':[],'open8':[],'high8':[],'low8':[],'close8':[],'vol8':[]})
for p in range((len(data.columns)//5)-8):
    cdata=data.iloc[:,(len(data.columns)-((5*p)+40)):(len(data.columns)-(5*p))]
    ndata=cdata.columns.values
    cols={}
    for r in range(40):
        d=ndata[r]
        cols[d]=columnlist[r]
    qdata=cdata.rename(columns=cols)
    data4=pd.concat([data4,qdata],ignore_index=True)
data4 = data4[['open1','high1','low1','close1','vol1','open2','high2','low2','close2','vol2','open3','high3','low3','close3','vol3','open4','high4','low4','close4','vol4','open5','high5','low5','close5','vol5','open6','high6','low6','close6','vol6','open7','high7','low7','close7','vol7','open8','high8','low8','close8','vol8']]

print("Deleting irrelevant stocks...")
# delete stocks with price lower than 0.001 or daily volume below $1
cloprice=np.array(data4['close1'])
vol=np.array(data4['vol1'])
cloprice3=np.array(prediction_data.iloc[:,3])

vol3=np.array(prediction_data.iloc[:,4])
conds3=np.logical_and(cloprice3>0.001,(vol3*cloprice3)>1)
conds=np.logical_and(cloprice>0.001,(vol*cloprice)>1)
ticker_frame=ticker_frame[conds3].reset_index(drop=True)
prediction_data=prediction_data[conds3].reset_index(drop=True)
data4=data4[conds].reset_index(drop=True)
today5=today5[conds3].reset_index(drop=True)
yest5=yest5[conds3].reset_index(drop=True)

yest=np.array(yest5['<low>'])
today_close=np.array(today5['<low>'])
today_change=(today_close/yest)*100-100 # Today's price change

rows=conds.sum()
tail=rows//5
head=rows-tail
ini=np.array(data4.tail(tail)['close7'].values.tolist())
initial=np.array(prediction_data.iloc[:,28])

target=data4
data4=data4.drop(['open8','high8','low8','close8', 'vol8'],axis=1)

test=np.array(data4.tail(tail).values.tolist())
data=np.array(data4.head(head).values.tolist())

target_list=target['close8'].head(head).values.tolist()
target_test=np.array(target['close8'].tail(tail).values.tolist())
othtest=target['close8'].tail(tail).values.tolist()


tticker_frame=ticker_frame.tail(tail)
tticker_frame=tticker_frame.reset_index(drop=True)

print("Scaling data...")
# scale price data to start at 1
numpy_data=np.array(data)
inverse=(1/(numpy_data[:,0]+0.000000000000001))
inverse1=inverse[:,np.newaxis]
numpy_data[:,np.arange(1,(numpy_data.shape[1]+1))%5!=0]*=inverse1
numpy_data[:,np.arange(1,(numpy_data.shape[1]+1))%5!=0]-=1
numpy_data[:,np.arange(1,(numpy_data.shape[1]+1))%5==0]*=inverse1**(-1)
target_list*=inverse
target_list-=1
tinverse=(1/(np.array(prediction_data)[:,0]+0.000000000000001))
nex_inverse=(1/(test[:,0]+0.000000000000001))
tiinverse=tinverse[:,np.newaxis]
ini*=nex_inverse
initial*=tinverse
target_test*=nex_inverse

init=initial

# MACHINE LEARNING
from sklearn import linear_model
from sklearn.ensemble import RandomForestClassifier

print("Training...")
# Train price predictor
reg = linear_model.Ridge (alpha = 0.1)
reg.fit(data, target_list)

# Train accuracy detector
nex=np.array(reg.predict(test))
pre_nex_change=(nex+1)/ini
nex_data=pd.concat([pd.DataFrame(test),pd.DataFrame(pre_nex_change-1)],axis=1)
conds8=pre_nex_change>1.2
nex_data=nex_data[conds8]
act_nex=target_test/ini
act_nex=act_nex[conds8]
y=act_nex>1
clf = RandomForestClassifier(n_estimators=10)
clf.fit(nex_data, y)

print('Making predictions...')
# Make price predictions
predictions=np.array(reg.predict(np.array(prediction_data)))

pre_change=(predictions+1)/init

mc=1.2

nex_pred=pd.concat([pd.DataFrame(prediction_data[pre_change>mc].reset_index(drop=True)),pd.DataFrame(pre_change[pre_change>mc]-1).reset_index(drop=True)],axis=1)
nex_preds=clf.predict(nex_pred)

act_change0=today_change[pre_change>mc]
act_change=pd.DataFrame(act_change0[nex_preds]).reset_index(drop=True)
picks=pre_change[pre_change>mc]

# Get rid of stocks that the accuracy predictor does not predict will do well
picks=picks[nex_preds]
tickers2=ticker_frame[pre_change>mc]
tickers2=tickers2[nex_preds]

pick_list=pd.concat([tickers2.iloc[:,0].reset_index(drop=True),pd.DataFrame(picks).reset_index(drop=True)*100-100, act_change], axis=1)
pick_list.columns = ["Ticker", "Predicted % Change", "Actual % Change"]

print(pick_list)

decreased=(act_change0[nex_preds]<0).sum()
total=picks<1000000
tot=total.sum()
decreased_percentage=decreased/tot

print("Percent of picks that decreased")
print("{0:.2f}%".format(decreased_percentage*100))

print("Average pick percent change")
print("{0:.2f}%".format(picks.mean()))
