import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import pandas as pd
import time 
import joblib
from path import *
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import RocCurveDisplay
import sklearn


print("extracting data")


x_train = pd.read_csv(PATH+directory_encode+'/X_train.csv')#.to_numpy().astype(np.float32)
y_train = pd.read_csv(PATH+directory_encode+'/Y_train.csv').to_numpy().astype(np.float32)
y_train.shape=(1,len(y_train))
y_train=y_train[0]


print("extracting data done")
print(x_train.shape)
print(y_train.shape)
print("training")
# Création du modèle de régression logistique
start=time.time()
model = RandomForestClassifier(n_estimators=120, random_state=42)

# Entraînement du modèle
model.fit(x_train, y_train)

print("training end "+str(time.time()-start))
joblib.dump(model,PATH+ "randomForest"+directory_encode+".sav")
# print("extracting model ")
# model= joblib.load(PATH+ "randomForest_"+directory_encode+".sav")
#Prédiction sur l'ensemble de test
x_train=[]
y_train=[]
print("extracting test data ")
x_test = pd.read_csv(PATH+directory_encode+'/X_test.csv')#.to_numpy().astype(np.float32)
y_test= pd.read_csv(PATH+directory_encode+'/Y_test.csv').to_numpy().astype(np.float32)
y_test.shape=(1,len(y_test))
y_test=y_test[0]
print("predicting ")
y_pred = model.predict(x_test)
print(x_test.shape)
print(y_test.shape)
# Calcul de la probabilité d'appartenance à la classe A
probs = model.predict_proba(x_test)[:, 1]
# Affichage de l'exactitude du modèle
accuracy = accuracy_score(y_test, y_pred)
print(f"Exactitude du modèle : {accuracy * 100:.2f}%")


print(probs[:10])
print("logloss ")
print(sklearn.metrics.log_loss(y_test, probs)) 
RocCurveDisplay.from_predictions(y_test, probs)
plt.show()
    
def display_prob(probabilities,y_test):
    res=[[0,0] for _ in range(100)]
    for i in range(len(probabilities)):
        if int(probabilities[i]*100) in range(100):
            if y_test[i]==1:       
                    res[int(probabilities[i]*100)][0]+=1
            else :
                    res[int(probabilities[i]*100)][1]+=1

    i=0.5
    x=[]
    y=[]
    for r in res :      
        if r[0]+r[1]>10:
            x.append(i)
            y.append(r[0]/(r[0]+r[1]))
        i+=1
    plt.plot(x, y)
    plt.show()

def plotProbas(pred):
    winer_proba=[res*100 for res in pred]
    plt.hist(winer_proba, bins=[i for i in range(100)])
    plt.show()

display_prob(probs,y_test)  
plotProbas(probs)
