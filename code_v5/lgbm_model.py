import numpy as np
import lightgbm as lgb
from sklearn.metrics import accuracy_score, log_loss
import matplotlib.pyplot as plt
import pandas as pd
import time
import joblib
from path import *
import sklearn.metrics as metrics

print("extracting data")
x_train = pd.read_csv(PATH+directory_encode+'/X_train.csv')
y_train = pd.read_csv(PATH+directory_encode+'/Y_train.csv').to_numpy().astype(np.float32)
y_train = y_train.reshape(-1)  # Reshape to a 1D array

print("extracting data done")
print(x_train.shape)
print(y_train.shape)
print("training")
# Configure LightGBM
params = {
    'objective': 'binary',
    'metric': 'binary_logloss',
    'learning_rate': 0.03,
    'max_depth': -1,
    'num_leaves': 512, #max 256
    'subsample': 0.6,
    'colsample_bytree': 0.6,
    'seed': 42
}

# Convert data to LightGBM Dataset format
dtrain = lgb.Dataset(x_train, label=y_train)
print("dataset_created")
# Train the model
start = time.time()
model = lgb.train(params, dtrain, num_boost_round=6000)
print("training end "+str(time.time()-start))

# Save the trained model
joblib.dump(model, PATH + "lgbm_model_" + directory_encode + ".dat")

# Load the trained model
# model = joblib.load(PATH + "lgbm_model_" + directory_encode + ".dat")

x_train=[]
y_train=[]
# Extract test data
print("extracting test data ")
x_test = pd.read_csv(PATH+directory_encode+'/X_test.csv')
y_test = pd.read_csv(PATH+directory_encode+'/Y_test.csv').to_numpy().astype(np.float32)
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

display_prob(probs, y_test)
plotProbas(probs)
