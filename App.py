#!/usr/bin/env python
# coding: utf-8

# In[11]:


import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder


# In[12]:


# Load the dataset
df = pd.read_csv("merged_data.csv")


columns_to_drop=['Order ID','Order Date','Ship Date','Customer Name','Profit']

X = df.drop(columns=columns_to_drop)
y = df['Profit']

categorical_columns = ['City', 'Country', 'Region','Segment', 'Ship Mode', 'State', 'Product Name',
                       'Category', 'Sub-Category']

# Apply one-hot encoding to the categorical columns
preprocessor = ColumnTransformer(
transformers=[('encoder', OneHotEncoder(), categorical_columns)],
remainder='passthrough'
)

X_encoded = preprocessor.fit_transform(X)

from sklearn.model_selection import train_test_split

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)

# Initialize the Random Forest Regressor
from sklearn.ensemble import RandomForestRegressor

# Train the model
rf=RandomForestRegressor(n_estimators=100, max_depth=12, min_samples_split=10, random_state=1)
rf.fit(X_train,y_train)

import streamlit as st

# Create the Streamlit app
st.title('Orders Sales Prediction')

# User input for feature values
user_input = {}
for column in X.columns:
    if column in categorical_columns:
        unique_values = df[column].unique()
        user_input[column] = st.selectbox(column, unique_values)
    else:
        user_input[column] = st.number_input(column, value=0)

# Transform user input to one-hot encoding
user_input_encoded = preprocessor.transform(pd.DataFrame(user_input, index=[0]))

# Make predictions using the trained model
prediction = rf.predict(user_input_encoded)

# Display the prediction
st.subheader('Prediction')
st.write(f'The predicted Profit is: {prediction[0]}')


# In[ ]:




