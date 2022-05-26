# Python Projects

There are two of my own python projects, which pick stocks on the OTC BB, in addition to 4 school assignments.

## TensorFlow Stock Picker

This stock picker consists of three python programs:

### stock_data_processor_3.py
This program takes .txt files for the OTC BB which are available at eoddata.com and converts them into the files necessary for tf_stock_trainer_2.py This file must be run to operate the stock trainer, because the files are not on GitHub due to their size. However the stock picker can be run with the files already on GitHub.

### tf_stock_trainer_2.py
This program trains a neural network to predict the next day's stock price based on the previous 30 days. It saves the model which can be run by tf_stock_picker_3.py

### tf_stock_picker_3.py
This program picks stocks based on the given model and shows their predicted and actual price changes.

## SciKitLearn Stock Picker
This stock picker has one program (stock_picker_11.py) which does all processing, training, and stock picking. It takes data in a similar way to the TF Stock Picker. It makes predictions for the next day's price based on the previous 8 days.
