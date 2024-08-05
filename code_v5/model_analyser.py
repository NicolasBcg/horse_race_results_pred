from path import *
import joblib
import matplotlib.pyplot as plt

import numpy as np
import xgboost as xgb
from sklearn.metrics import accuracy_score, log_loss
import pandas as pd
from path import *
import sklearn.metrics as metrics
recalc_prob = False
lgbm=True
xgboost=False
model_choice = "lightgbm"  # Options: "xgboost", "randomForest", "lightgbm","linregressor"
model_name = "lgbm_model_2020_2023_reduced_05_512_07_3000.dat"

if xgboost:
    # Load the XGBoost model
    model = joblib.load(PATH + model_name)

    # Get feature importance (assuming model is a Booster object)
    importance = model.get_score(importance_type='gain')#gain cover weight

    # Convert to a list of tuples and sort by importance
    importance = sorted(importance.items(), key=lambda x: x[1], reverse=True)
    print(zip(*importance))
    # Separate the feature names and their scores
    features, scores = zip(*importance[-100:-50])

    # Plot the feature importance
    plt.figure(figsize=(12, 8))
    plt.subplot(1, 2, 1)
    plt.barh(features, scores)
    plt.xlabel('gain Score')
    plt.ylabel('Feature')
    plt.title('gain Importance')
    plt.gca().invert_yaxis()



    # importance = model.get_score(importance_type='weight')#gain cover weight

    # # Convert to a list of tuples and sort by importance
    # importance = sorted(importance.items(), key=lambda x: x[1], reverse=True)
    # print(zip(*importance))
    # # Separate the feature names and their scores
    # features, scores = zip(*importance[:40])

    # plt.subplot(1, 2, 2)
    # plt.barh(features, scores)
    # plt.xlabel('weigth Score')
    # plt.ylabel('Feature')
    # plt.title('weight Importance')
    # plt.gca().invert_yaxis()
    # plt.show()


    importance = model.get_score(importance_type='cover')#gain cover weight

    # Convert to a list of tuples and sort by importance
    importance = sorted(importance.items(), key=lambda x: x[1], reverse=True)
    print(zip(*importance))
    # Separate the feature names and their scores
    features, scores = zip(*importance[-100:-50])

    plt.subplot(1, 2, 2)
    plt.barh(features, scores)
    plt.xlabel('cover Score')
    plt.ylabel('Feature')
    plt.title('cover Importance')
    plt.gca().invert_yaxis()
    plt.show()



if lgbm:

    # Load the LightGBM model
    model = joblib.load(PATH + model_name)

    # Get feature importance (gain)
    importance = model.feature_importance(importance_type='gain')

    # Get feature names
    feature_names = model.feature_name()

    # Create a list of tuples (feature, importance) and sort by importance
    importance_tuples = sorted(zip(feature_names, importance), key=lambda x: x[1], reverse=True)

    # Separate the feature names and their scores (for the middle 50 features, in this example)
    features, scores = zip(*importance_tuples[-50:])

    # Plot the feature importance for 'gain'
    plt.figure(figsize=(12, 8))
    plt.subplot(1, 2, 1)
    plt.barh(features, scores)
    plt.xlabel('gain Score')
    plt.ylabel('Feature')
    plt.title('gain Importance')
    plt.gca().invert_yaxis()

    # Get feature importance (weight/split)
    importance_weight = model.feature_importance(importance_type='split')

    # Create a list of tuples (feature, importance) and sort by importance
    importance_weight_tuples = sorted(zip(feature_names, importance_weight), key=lambda x: x[1], reverse=True)

    # Separate the feature names and their scores (top 40 features)
    features_weight, scores_weight = zip(*importance_weight_tuples[-50:])

    # Plot the feature importance for 'weight'
    plt.subplot(1, 2, 2)
    plt.barh(features_weight, scores_weight)
    plt.xlabel('weight Score')
    plt.ylabel('Feature')
    plt.title('weight Importance')
    plt.gca().invert_yaxis()

    # Show the plot
    plt.show()





# Function to display probabilities
def display_prob(probabilities, y_test):
    res = [[0, 0] for _ in range(100)]
    for i in range(len(probabilities)):
        if int(probabilities[i] * 100) in range(100):
            if y_test[i] == 1:
                res[int(probabilities[i] * 100)][0] += 1
            else:
                res[int(probabilities[i] * 100)][1] += 1

    i = 0.5
    x = []
    y = []
    for r in res:
        if r[0] + r[1] > 10:
            x.append(i)
            y.append(r[0] / (r[0] + r[1]))
        i += 1
    plt.plot(x, y)
    plt.plot(x,[a/100 for a in x],color='orange')
    plt.show()

# Function to plot probabilities
def plotProbas(pred):
    winner_proba = [res * 100 for res in pred]
    plt.hist(winner_proba, bins=[i for i in range(100)])
    plt.show()


def predict(races):
    if model_choice == "xgboost":
        dtest = xgb.DMatrix(races)
        return model.predict(dtest)
    
    elif model_choice == "lightgbm":
        #dtest = lgb.Dataset(races)
        return model.predict(races)
    
    elif model_choice == "linregressor":
        
        return model.predict_proba(races)[:, 1]
    else:
        return model.predict_proba(races)[:, 1]

if recalc_prob:
    print("extracting test data ")
    x_test = pd.read_csv(PATH+directory_encode+'/X_test.csv')
    y_test = pd.read_csv(PATH+directory_encode+'/Y_test.csv').to_numpy().astype(np.float32)
    y_test = y_test.reshape(-1)  # Reshape to a 1D array
    print("predicting ")

    # Predict probabilities
    probs = predict(x_test)

    # Predict classes
    y_pred = (probs > 0.5).astype(int)

    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy * 100:.2f}%")

    # Calculate log loss
    print("Log Loss:")
    print(log_loss(y_test, probs))

    # Plot ROC Curve
    fpr, tpr, _ = metrics.roc_curve(y_test, probs)
    roc_auc = metrics.auc(fpr, tpr)
    plt.figure()
    plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic')
    plt.legend(loc="lower right")
    plt.show()



    display_prob(probs, y_test)
    plotProbas(probs)
