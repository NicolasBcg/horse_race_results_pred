import numpy as np
import xgboost as xgb
from sklearn.metrics import accuracy_score, log_loss
import pandas as pd
import time 
import joblib
from path import *

# Configure XGBoost
# params = {
#     'objective': 'binary:logistic',   # Binary classification
#     'eval_metric': 'logloss',          # Use log loss as evaluation metric
#     'eta': 0.03,                        # Learning rate
#     'max_depth': 9,                    # Maximum depth of a tree
#     'subsample': 0.7,                  # Subsample ratio of the training instances
#     'colsample_bytree': 0.7,           # Subsample ratio of columns when constructing each tree
#     'seed': 42                         # Random seed for reproducibility
# }
# prefix = '_03_9_07_5000'
# num_boost_round = 5000

def train_xgb(directory_encode,params,num_boost_round,sufix,display_probs = False):
    print("extracting data")
    x_train = pd.read_csv(PATH+directory_encode+'/encoded_datas/X_train.csv')
    y_train = pd.read_csv(PATH+directory_encode+'/encoded_datas/Y_train.csv').to_numpy().astype(np.float32)
    y_train = y_train.reshape(-1)  # Reshape to a 1D array

    print("extracting data done")
    print(x_train.shape)
    print(y_train.shape)
    print("training")

    # Convert data to DMatrix format for XGBoost
    dtrain = xgb.DMatrix(x_train, label=y_train)
    print("matrix_created")
    # Train the model
    start = time.time()
    model = xgb.train(params, dtrain, num_boost_round=num_boost_round)  # Train for 100 rounds
    print("training end "+str(time.time()-start))

    # Save the trained model
    joblib.dump(model, PATH + directory_encode +"/"+directory_encode +"-xgboost-"  + sufix+".dat")

# Load the trained model
# model = joblib.load(PATH + "xgboost_model_" + directory_encode + ".dat")
    x_train=[]
    y_train=[]
    if display_probs:
        # Extract test data
        print("extracting test data ")
        x_test = pd.read_csv(PATH+directory_encode+'/encoded_datas/X_valid.csv')
        y_test = pd.read_csv(PATH+directory_encode+'/encoded_datas/Y_valid.csv').to_numpy().astype(np.float32)
        y_test = y_test.reshape(-1)  # Reshape to a 1D array
        print("predicting ")

        # Convert test data to DMatrix format
        dtest = xgb.DMatrix(x_test)

        # Predict probabilities
        probs = model.predict(dtest)

        # Predict classes
        y_pred = (probs > 0.5).astype(int)

        # Calculate accuracy
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Model Accuracy: {accuracy * 100:.2f}%")

        # Calculate log loss
        print("Log Loss:")
        print(log_loss(y_test, probs))
        plot_ROC(y_test, probs)
        display_prob(probs, y_test)
        plotProbas(probs)

