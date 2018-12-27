"""
Uses a model to predict stock prices on the next day, then displays the picks
with an estimated increase above MINIMUM_EST_CHANGE, as well as the average increase.

Reads files generated from stock_data_processor_3.py:
    data that will be used to make predictions:
        prediction_stock_data.csv
    initial stock prices, before prediction day:
        stock_init.csv
    todays price changes:
        today_change.csv
    ticker symbols:
        ticker_frame.csv
Reads the model from modelX.json and weights from modelX.h5 where X is MODEL_NUMBER

"""
import numpy as np
import pandas as pd
from keras.models import model_from_json

MODEL_NUMBER = 1
MINIMUM_EST_CHANGE = 40

print("Opening data files...")
ticker_frame=np.array(pd.read_csv("ticker_frame.csv").iloc[:,1])
today_change=np.array(pd.read_csv("today_change.csv").iloc[:,1:])
prediction_data=np.array(pd.read_csv("prediction_stock_data.csv").iloc[:,1:])
init=np.array(pd.read_csv("stock_init.csv").iloc[:,1:])

json_file = open('model{}.json'.format(MODEL_NUMBER), 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
# load weights into new model
model.load_weights("model{}.h5".format(MODEL_NUMBER))

print("Making predictions...")

predictions=model.predict(prediction_data)

pre_change=(predictions+1)/(init+1)

act_change=today_change

#Pick all stocks with an estimated MINIMUM_EST_CHANGE% increase
mc=(pre_change>((MINIMUM_EST_CHANGE/100)+1)).flatten()
picks=act_change[mc]

tick=pd.DataFrame(ticker_frame[mc])

pick_list = pd.concat([tick,pd.DataFrame(picks).reset_index(drop=True),100*pd.DataFrame(pre_change[mc]).reset_index(drop=True)-100], axis=1)
pick_list.columns = ["Ticker", "Actual % Change", "Predicted % Change"]
print("\n\nPICKS")
print(pick_list)

decreased=(picks<0).sum()
total=picks<1000000
tot=total.sum()
decreased_percentage=decreased/tot

print("Percent of picks that decreased")
print("{0:.2f}%".format(decreased_percentage*100))

print("Average pick percent change")
print("{0:.2f}%".format(picks.mean()))

