import requests
import urllib3
import os
import sys 

import numpy as np 
import pandas as pd
import dfply
import seaborn as sns
import matplotlib.pyplot as plt

# Importing necessary libraries
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV, cross_val_score, train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.compose import ColumnTransformer


sys.path.append("../")
from Scripts.Data_Pull import *
from Scripts.Location_Filter import *

import streamlit as st
from joblib import dump, load




#Drop Bad Requests which have no name value
df=df.dropna(axis=0, subset=['name'])

#Split the data into training and testing for predictors and target
X = df.drop('athlete', axis=1)
y = df['athlete']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Step 1: Create Preprocessing Steps
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler())])

text_transformer = Pipeline(steps=[
    ('tfidf', TfidfVectorizer(max_features=500))])

categorical_transformer = Pipeline(steps=[
    ('onehot', OneHotEncoder(handle_unknown='ignore'))])

# Apply transformations to the appropriate columns
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, ['distance', 'elapsed_time', 'total_elevation_gain', 'kudos_count', 'average_heartrate', 'elev_high']),
        ('text', text_transformer, 'name'),
        ('cat', categorical_transformer, ['sport_type', 'private'])])

# Step 2: Create Pipelines

pipelines= [Pipeline([('preprocess', preprocessor),
                    ('classifier', RandomForestClassifier())]), 
            Pipeline([('preprocess', preprocessor),
                    ('classifier', GradientBoostingClassifier())]),
            Pipeline([('preprocess', preprocessor),
                    ('classifier', LogisticRegression())])]

# Step 3: Hyperparameter Tuning
param_grids = [{'classifier__n_estimators': [50, 100, 200]},
               {'classifier__n_estimators': [50, 100, 200]},
               {'classifier__C': [0.1, 1, 10]}]


def train_and_select_model(X, y):
    best_score = 0.0
    best_pipeline = None
    
    for i, pipeline in enumerate(pipelines):
        param_grid = param_grids[i]
        grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring='accuracy')
        grid_search.fit(X, y)
        
        if grid_search.best_score_ > best_score:
            best_score = grid_search.best_score_
            best_pipeline = grid_search.best_estimator_
    
    return best_pipeline


best_pipeline = train_and_select_model(X_train, y_train)

# Evaluate the model on the test set
y_pred = best_pipeline.predict(X_test)
test_accuracy = accuracy_score(y_test, y_pred)

# Decision point
if test_accuracy > 0.75:
    # Refit model to the entire dataset
    best_pipeline.fit(X,y)
    # Save the refitted model
    dump(best_pipeline, 'best_model.joblib')
    
else:
    # Take other actions, like revisiting feature engineering, etc.
    print("The new model is not performing at an accuracy of 75{%} or greater, so the model was not refit!")



