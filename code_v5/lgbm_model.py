import numpy as np
import lightgbm as lgb
from sklearn.metrics import accuracy_score, log_loss
import pandas as pd
import time
import joblib
from path import *
import sklearn.metrics as metrics

# params = {
#     'objective': 'binary',
#     'metric': 'binary_logloss',
#     'learning_rate': 0.05,
#     'max_depth': -1,
#     'num_leaves': 512, #max 256
#     'subsample': 0.7,
#     'colsample_bytree': 0.7,
#     'seed': 42
# }
# num_boost_round=3000
# prefix = '_05_512_07_3000'
def train_lgbm(directory_encode,params,num_boost_round,prefix,display_probs = False):
    print("extracting data")
    x_train = pd.read_csv(PATH+directory_encode+'/X_train.csv')
    y_train = pd.read_csv(PATH+directory_encode+'/Y_train.csv').to_numpy().astype(np.float32)
    y_train = y_train.reshape(-1)  # Reshape to a 1D array
    print("extracting data done")
    print(x_train.shape)
    print(y_train.shape)
    print("training")
    # Convert data to LightGBM Dataset format
    dtrain = lgb.Dataset(x_train, label=y_train)
    print("dataset_created")
    # Train the model
    start = time.time()
    model = lgb.train(params, dtrain, num_boost_round=num_boost_round)
    print("training end "+str(time.time()-start))

    # Save the trained model
    joblib.dump(model, PATH + "lgbm_model_" + directory_encode + prefix + ".dat")

    # Load the trained model
    # model = joblib.load(PATH + "lgbm_model_" + directory_encode + ".dat")
    x_train=[]
    y_train=[]
    if display_probs:
        # Extract test data
        print("extracting test data ")
        x_test = pd.read_csv(PATH+directory_encode+'/X_valid.csv')
        y_test = pd.read_csv(PATH+directory_encode+'/Y_valid.csv').to_numpy().astype(np.float32)
        y_test = y_test.reshape(-1)  # Reshape to a 1D array
        print("predicting ")

        # Predict probabilities
        probs = model.predict(x_test)
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




# train_lgbm(directory_encode,params,num_boost_round,prefix,display_probs)
