# -*- coding: utf-8 -*-
"""capstone_project_GE.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18qRnq4z-8pF7jtOeRgHYQzmnAXbA5F9S
"""

from google.colab import drive
drive.mount('/content/gdrive', force_remount = True)

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

data = pd.read_csv('gdrive/My Drive/Colab_Notebooks/capstoneproject/capstonedata.csv')

data.head(2)

visit_date = data['visit_date']
print(visit_date.dtype)

visit_date1=visit_date.astype("string")
print(visit_date1.dtype)

new = visit_date1.str.split(" ", n=1, expand=True)
visit_date2= new[0]
print(visit_date2)

visit_date3= pd.to_datetime(visit_date2)
print(visit_date3)

data2= data.drop(['visit_date'],axis=1)
data2 #drop object Visit Date

data2.insert(3,"visit_date",visit_date3,True) #insert datetime date

doctor_id = data2['doctor_id']

m1 = doctor_id.ne(doctor_id.shift())
m2 = visit_date.ne(visit_date.shift())
data2['visit_count'] = data2.groupby((m1 | m2).cumsum()).cumcount().add(1).values

data2.head(10)

data3 =data2.groupby(data2['visit_date'],as_index=False).sum('count') #,as_index=False
Visdate = data3.visit_date
data3.head(10)

data3=data3.set_index('visit_date')
data3.head(10)

!pip install pandas-datareader

import pandas_datareader.data as web
import datetime

import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

import matplotlib.pyplot as plt
import seaborn as sns

sns.set()

split_point = 100
data_upper = data3.iloc[:split_point]
print(data_upper['visit_count'].dtype)

split_point = 100
data_lower = data3.iloc[:split_point]
print(data_lower.columns)

plt.ylabel('Amount of patients')
plt.xlabel('date')
plt.xticks(rotation=45)

Vdate = data3.index
VCount= data3.visit_count
plt.plot(Vdate, VCount, )

train = data3[Vdate < pd.to_datetime("2022-11-01", format='%Y-%m-%d')]
test = data3[Vdate > pd.to_datetime("2022-11-01", format='%Y-%m-%d')]

#x = train['visit_date']

plt.plot(train, color='black')
plt.plot(test, color='red')
plt.ylabel('Number of Patients')
plt.xlabel('date')
plt.xticks(rotation=45)
plt.title("Train/Test split for Patient Data")
plt.show()

plt.legend()

print(test.index)
print(data3.columns)

import streamlit as st

def main():
  st.title('Clinic Peak Hour Prediction System')
  input_text = st.date_input("Enter Date to find busyness")

  results = getprediction(input_text)
  st.markdown(results)

if __name__ == "__main__":
    main()

def getprediction(input_date):
  y = train['visit_count']

  ARMAmodel = SARIMAX(y, order = (1, 0, 1))
  ARMAmodel = ARMAmodel.fit()

  y_pred = ARMAmodel.get_forecast(len(test.index))
  y_pred_df = y_pred.conf_int(alpha = 0.05)
  y_pred_df["Predictions"] = ARMAmodel.predict(start = y_pred_df.index[0], end = y_pred_df.index[-1])
  y_pred_df.index = test.index
  y_pred_out = y_pred_df["Predictions"]

  return y_pred_out

"""#1. ARMA"""

!pip install statsmodels

from statsmodels.tsa.statespace.sarimax import SARIMAX

print(train.columns)

y = train['visit_count']

ARMAmodel = SARIMAX(y, order = (1, 0, 1))
ARMAmodel = ARMAmodel.fit()

y_pred = ARMAmodel.get_forecast(len(test.index))
y_pred_df = y_pred.conf_int(alpha = 0.05)
y_pred_df["Predictions"] = ARMAmodel.predict(start = y_pred_df.index[0], end = y_pred_df.index[-1])
y_pred_df.index = test.index
y_pred_out = y_pred_df["Predictions"]

plt.plot(y_pred_out, test['visit_count'], color='green', label = 'Predictions')

!pip install streamlit





"""# 1.ANN"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

data = pd.read_csv('gdrive/My Drive/Colab_Notebooks/capstoneproject/capstonedata.csv', parse_dates=['visit_date'], index_col='visit_date')
doctor_id = data['doctor_id']
data['date'] = data.index.date

doctor_id = data['doctor_id']
visit_date = data.index.to_series()
m1 = doctor_id.ne(doctor_id.shift())
m2 = visit_date.dt.date.ne(visit_date.dt.date.shift())
data['count'] = data.groupby((m1 | m2).cumsum()).cumcount().add(1).values

out = data.groupby(['date', 'doctor_id'])['count'].max().reset_index()

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense, SpatialDropout1D
from keras.utils import to_categorical

#seperating the date and count
date = out['date']
count = out['count']

labels = pd.get_dummies(date)

X_train, X_test, y_train, y_test = train_test_split(count, labels, test_size=0.2, random_state=42)

embedding_dim = 100
model = Sequential()
model.add(Embedding(1000, embedding_dim, input_length=100))
model.add(SpatialDropout1D(0.2))
model.add(LSTM(100, dropout=0.2, recurrent_dropout=0.2))
model.add(Dense(len(labels.columns), activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the LSTM model
epochs = 50
batch_size = 64
history = model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(X_test, y_test), verbose=2)

loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
print("LSTM Test Accuracy:", accuracy)

import matplotlib.pyplot as plt

train_loss = history.history['loss']
val_loss = history.history['val_loss']

# Get training and validation accuracy
train_acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

# Plot loss
plt.figure(figsize=(10, 5))
plt.plot(train_loss, label='Training Loss', color='blue')
plt.plot(val_loss, label='Validation Loss', color='red')
plt.title('Training and Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

# Plot accuracy
plt.figure(figsize=(10, 5))
plt.plot(train_acc, label='Training Accuracy', color='blue')
plt.plot(val_acc, label='Validation Accuracy', color='red')
plt.title('Training and Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.show()

data = pd.read_csv('gdrive/My Drive/Colab_Notebooks/capstoneproject/capstonedata.csv', parse_dates=['visit_date'], index_col='visit_date')
doctor_id = data['doctor_id']
data['date'] = data.index.date

doctor_id = data['doctor_id']
visit_date = data.index.to_series()
m1 = doctor_id.ne(doctor_id.shift())
m2 = visit_date.dt.date.ne(visit_date.dt.date.shift())
data['count'] = data.groupby((m1 | m2).cumsum()).cumcount().add(1).values

out = data.groupby(['date'])['count'].max().reset_index()

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

plt.ylabel('Amount of patients')
plt.xlabel('date')
plt.xticks(rotation=45)

plt.plot(out['date'], out['count'], )

train = out['count'][out['date'] < pd.to_datetime("2022-11-01", format='%Y-%m-%d')]
test = out['count'][out['date'] > pd.to_datetime("2022-11-01", format='%Y-%m-%d')]

plt.plot(train, color='black')
plt.plot(test, color='red')
plt.ylabel('Number of Patients')
plt.xlabel('date')
plt.xticks(rotation=45)
plt.title("Train/Test split for Patient Data")
plt.show()

date = out['date']
count = out['count']

labels = pd.get_dummies(date)

X_train, X_test, y_train, y_test = train_test_split(count, labels, test_size=0.2, random_state=42)

embedding_dim = 100
model = Sequential()
model.add(Embedding(1000, embedding_dim, input_length=100))
model.add(SpatialDropout1D(0.2))
model.add(LSTM(100, dropout=0.2, recurrent_dropout=0.2))
model.add(Dense(len(labels.columns), activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the LSTM model
epochs = 50
batch_size = 64
history = model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(X_test, y_test), verbose=2)

loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
print("LSTM Test Accuracy:", accuracy)