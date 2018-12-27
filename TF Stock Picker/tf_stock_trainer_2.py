"""
Creates a TF ML model to predict stock prices on the next day from 30 days of data,
then uses the model to make predictions that are displayed if the estimated percent
change is higher than MINIMUM_EST_CHANGE.

Reads files created with stock_data_processor_3.py
"""
import tensorflow as tf
import pandas as pd
import numpy as np

MODEL_NUMBER = 1 # save to model{MODEL_NUMBER}.json
BATCH_SIZE = 500
EPOCHS = 25
MINIMUM_EST_CHANGE = 40 # Minimum estimated percent change for the pick to be displayed

# Custom loss function, with exponential loss for guessing too high and linear loss for guessing too low
def loss(y_true, y_pred):
    err=(y_true-y_pred)*10
    x=err+0.5439
    abs_x=tf.abs(x)
    exp_x=(-1)*x
    r=(x**2/(abs_x+1))+tf.exp(exp_x)-0.7721
    return r

print("Gathering Data...")
training_data = np.array(pd.read_csv("training_stock_data.csv").iloc[:,1:])
target_data=np.array(pd.read_csv("target_stock_data.csv").iloc[:,1:])
ticker_frame=np.array(pd.read_csv("ticker_frame.csv").iloc[:,1])
init=np.array(pd.read_csv("stock_init.csv").iloc[:,1:])
prediction_data=np.array(pd.read_csv("prediction_stock_data.csv").iloc[:,1:])
today_change=np.array(pd.read_csv("today_change.csv").iloc[:,1:])

print("Creating Neural Network...")
model = tf.keras.Sequential()
model.add(tf.keras.layers.Dense(1024, activation=tf.nn.tanh, input_shape=(145,)))
model.add(tf.keras.layers.Dense(512, activation=tf.nn.tanh))
model.add(tf.keras.layers.Dense(256, activation=tf.nn.tanh))
model.add(tf.keras.layers.Dense(128, activation=tf.nn.tanh))
model.add(tf.keras.layers.Dense(64, activation=tf.nn.tanh))
model.add(tf.keras.layers.Dense(32, activation=tf.nn.tanh))
model.add(tf.keras.layers.Dense(32, activation=tf.nn.tanh))
model.add(tf.keras.layers.Dense(16, activation=tf.nn.tanh))
model.add(tf.keras.layers.Dense(8, activation=tf.nn.tanh))
model.add(tf.keras.layers.Dense(4, activation=tf.nn.tanh))
model.add(tf.keras.layers.Dense(1, activation='linear'))

model.compile(loss=loss, optimizer='adam', metrics=['accuracy'])

model.summary()

print("Training Network...")
model.fit(training_data, target_data, epochs=EPOCHS, batch_size=BATCH_SIZE)

predictions=model.predict(prediction_data)

pre_change=(predictions+1)/(init+1)

act_change=today_change

# Pick all stocks with an estimated 20% increase
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

print("Saving model to model{MODEL_NUMBER}.json and model{MODEL_NUMBER}.h5".format(MODEL_NUMBER=MODEL_NUMBER))
model_json = model.to_json()
with open("model{}.json".format(MODEL_NUMBER), "w") as json_file:
    json_file.write(model_json)

model.save_weights("model{}.h5".format(MODEL_NUMBER))





