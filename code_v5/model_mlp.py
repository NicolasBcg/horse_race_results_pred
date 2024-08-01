import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, log_loss, roc_curve, auc
from joblib import dump, load
from path import *
from sklearn.preprocessing import StandardScaler

# Load data
print("Extracting data")
x_train = pd.read_csv(PATH + directory_encode + '/X_train.csv')
y_train = pd.read_csv(PATH + directory_encode + '/Y_train.csv').to_numpy().astype(np.float32).reshape(-1)
print("Loaded MLP")
# Check for missing values
print("Checking for missing values in training data:")
print(pd.DataFrame(x_train).isnull().sum())



scaler = StandardScaler()
x_train = pd.DataFrame(scaler.fit_transform(x_train), columns=x_train.columns)
# Handle missing values (if any)
x_train = x_train.fillna(x_train.mean()).values
dump(scaler , PATH + directory_encode + "/encoders/scaler.joblib")
# Define the MLP model
model = MLPClassifier(hidden_layer_sizes=(128,256,64), activation='relu', solver='adam', alpha=0.0001, batch_size=32,
                      learning_rate_init=0.001, max_iter=30, verbose=True, random_state=42)

# Train the model
print("Training MLP")
start = time.time()
model.fit(x_train, y_train)
print("Training completed in", time.time() - start, "seconds")

# Save the trained model
dump(model, PATH + "mlp_model_" + directory_encode + ".joblib")

# # Load the trained model (if needed)
# model = load(PATH + "mlp_model_" + directory_encode + ".joblib")

x_train = []
y_train = []
# Extract test data
print("extracting test data ")
x_test = pd.read_csv(PATH + directory_encode + '/X_test.csv')
scaler = load(PATH + directory_encode + "/encoders/scaler.joblib")
x_test = pd.DataFrame(scaler.transform(x_test), columns=x_test.columns)
x_test = x_test.fillna(x_test.mean()).values
y_test = pd.read_csv(PATH + directory_encode + '/Y_test.csv').values.astype(np.float32).reshape(-1)
print("predicting ")

probs = model.predict_proba(x_test)[:, 1]
y_pred = model.predict(x_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Calculate log loss
print("Log Loss:")
print(log_loss(y_test, probs))

# Plot ROC Curve
fpr, tpr, _ = roc_curve(y_test, probs)
roc_auc = auc(fpr, tpr)
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
    plt.plot(x, [a / 100 for a in x], color='orange')
    plt.show()

# Function to plot probabilities
def plotProbas(pred):
    winner_proba = [res * 100 for res in pred]
    plt.hist(winner_proba, bins=[i for i in range(100)])
    plt.show()

display_prob(probs, y_test)
plotProbas(probs)
