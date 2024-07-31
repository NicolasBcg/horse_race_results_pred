import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sklearn
from path import *
from sklearn.metrics import RocCurveDisplay
import pickle
import xgboost as xgb
import lightgbm as lgb
import os
import json

nb_chevaux_fantomes = 20
specialite = "_attele"
model_choice = "xgboost"  # Options: "xgboost", "randomForest", "lightgbm"
model_extension = ''
print("Loading Model")

CATEGORIES = ['SIMPLE_GAGNANT','E_SIMPLE_GAGNANT','SIMPLE_PLACE','E_SIMPLE_PLACE','COUPLE_GAGNANT','E_COUPLE_GAGNANT',"TRIO","E_TRIO"]

if model_choice == "xgboost":
    model = joblib.load(PATH + "xgboost_model_" + directory_encode + model_extension+".dat")
elif model_choice == "randomForest":
    model = joblib.load(PATH + "randomForest" + directory_encode + ".sav")
elif model_choice == "lightgbm":
    model = joblib.load(PATH + "lgbm_model_" + directory_encode  + model_extension+ ".dat")
else:
    raise ValueError("Invalid model choice. Please select 'xgboost', 'randomForest', or 'lightgbm'.")

print("Loading DATAS")
x_test = pd.read_csv(PATH + directory_encode + '/X_test_2.csv')
try : 
    numsPMU = x_test[["numPmu0", "numPmu01"]]
    x_test=x_test.drop(["numPmu0", "numPmu01"],axis=1)
except : 
    numsPMU = x_test[["numPmu", "numPmu.1"]]
    numsPMU = numsPMU.rename(columns={"numPmu": "numPmu0", "numPmu.1": "numPmu01"})
print("Applying model")
resultats = pd.read_csv(PATH_TO_CACHE + "datasets\\" + DATASET_TEST + specialite + "_res.csv")

def predict(races):
    if model_choice == "xgboost":
        dtest = xgb.DMatrix(races)
        return model.predict(dtest)
    elif model_choice == "lightgbm":
        #dtest = lgb.Dataset(races)
        return model.predict(races)
    else:
        return model.predict_proba(races)[:, 1]


print("calculating...")

def final_res(arrives,nb_participants,non_partants):
    res=[0 for _ in range(nb_participants)]  
    res[eval(arrives)[0]-1]=1
    res[eval(arrives)[1]-1]=2
    try:
       res[eval(arrives)[2]-1]=3
    except:
        print(nb_participants)
    for non_partant in eval(non_partants):
        res[non_partant-1]=-10
    return res


def get_place_couple_trio(id_course,nb_participants,type_paris='SIMPLE_PLACE'):
    res_simple_place=[0 for _ in range(nb_participants)] 
    res_np=[0 for _ in range(nb_participants)]
    found=False
    found_np=False
    try:
        rapport=json.loads(open(PATH_TO_CACHE+'rapports/'+id_course+'.json', "r").read())
        for type in rapport:
            if type["typePari"]==type_paris:
                for paris in type["rapports"]:
                    try :
                        if paris["libelle"][-4] == "1":
                            combinaison_int_np = []
                            for val in paris["combinaison"].split("-"):
                                if val != "NP":
                                    combinaison_int_np.append(int(val))
                            for ic in combinaison_int:
                                res_np[int(ic)-1]=paris["dividendePourUnEuro"]/100
                            found_np = True
                    except: 
                        print(id_course)
                        print("could not compute NP") 
                    try :
                        if paris["libelle"][-4] != "1":
                            combinaison=paris["combinaison"].split("-")
                            combinaison_int = [int(i) for i in combinaison]
                            for ic in combinaison_int:
                                res_simple_place[int(ic)-1]=paris["dividendePourUnEuro"]/100
                            found=True
                    except : 
                        print(id_course)
                        print("could not compute Classic") 
 
    except:
        print(id_course)
        print('file_not_found')
        res_simple_place = [-1 for _ in range(nb_participants)] 
        res_simple_place =  [-1 for _ in range(nb_participants)] 

    if not found:
        res_simple_place =  [-1 for _ in range(nb_participants)] 
    if not found_np:
        res_np =  [-1 for _ in range(nb_participants)] 
    return res_simple_place,res_np


def getraports(id_course,nb_participants):
    normaux = []
    non_partants = []
    for categorie in CATEGORIES : 
        normal,non_partant = get_place_couple_trio(id_course,nb_participants,categorie)
        normaux.append(normal)
        non_partants.append(non_partant)

    return np.array(normaux), np.array(non_partants)
    
def correct_matrice(matrice):
    res = np.copy(matrice)
    for i in range(len(matrice)):
        for j in range(len(matrice)):
            res[i][j]=(matrice[i][j]+1-matrice[j][i])/2
    for i in range(len(matrice)):
        res[i][i]=1
    return res
    
def generate_matrices(probas,results,numsPMU):
    matrices=[]
    k=0
    res=[]
    cotes_normales=np.array([[] for _ in CATEGORIES])
    cotes_non_partants=np.array([[] for _ in CATEGORIES])
    ids_course=[]
    numeros_PMU=[]
    for c in range(len(results)):
        nb_participants=results["nbParticipants"].iloc[c]
        arrives=results["resultats"].iloc[c]
        non_partants=results["non_partants"].iloc[c]
        ids=[results["idCourse"].iloc[c] for _ in range(nb_participants)] 
        matrice=np.ones((nb_chevaux_fantomes, nb_chevaux_fantomes), dtype=float)
        #print("nb participants : "+str(nb_participants))
        for i in range(nb_participants):
            for j in range (nb_chevaux_fantomes):
                if i<nb_participants:
                    ch1=numsPMU["numPmu0"].iloc[k]-1
                else : 
                    ch1=i
                if j < nb_participants:
                    ch2=numsPMU["numPmu01"].iloc[k]-1
                else: 
                    ch2=j
                # print(str(ch1)+" and "+str(ch2))
                proba=probas[k]
                k+=1
                matrice[ch1][ch2]=proba
        final_result=final_res(arrives,nb_participants,non_partants)
        res=res+final_result
        numeros_PMU=numeros_PMU+[i+1 for i in range(nb_participants)]
        normaux,c_non_partants= getraports(ids[0],nb_participants)
        cotes_normales=np.hstack((cotes_normales, normaux))
        cotes_non_partants=np.hstack((cotes_non_partants, c_non_partants))
        ids_course=ids_course+ids
        matrices.append([matrice,nb_participants])
    return matrices,res,ids_course,numeros_PMU,cotes_normales,cotes_non_partants

def nicolas_count(matrice,nb_courreurs):
    res = []
    for ligne in matrice[:nb_courreurs]:
        proba=1
        for element in ligne:
            proba=proba*element      
        res.append(proba)
    return res

def borda_count(matrice,nb_courreurs):
    res = []
    # nb_courreurs=int( )
    for ligne in matrice[:nb_courreurs]:
        proba=1
        for element in ligne:
            proba=proba+element      
        res.append(proba/len(ligne))
    return res

def normalize_probas(probas):
    total=0
    for p in probas :
        total+=p
    return (probas/total)

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
    plt.plot(x,[a/100 for a in x],color='orange')
    plt.show()

def plotProbas(pred):
    winer_proba=[res*100 for res in pred]
    plt.hist(winer_proba, bins=[i for i in range(100)])
    plt.show()


lines = [0]
lines_res = [0]
for i in range(len(resultats)):
    lines[-1]+= resultats["nbParticipants"].iloc[i]*nb_chevaux_fantomes
    lines_res[-1]+=1
    if lines_res[-1] > 200 :
        lines.append(0)
        lines_res.append(0)

probs = []
res,ids_courses,numeros_PMU,cotes,cotes_non_partants,probs = [],[],[],np.array([[] for _ in CATEGORIES]),np.array([[] for _ in CATEGORIES]),[]
for n,r in zip(lines,lines_res) :
    partition = x_test.iloc[:n]
    x_test = x_test.iloc[n:]
    num_partition = numsPMU.iloc[:n]
    numsPMU = numsPMU.iloc[n:]
    partition_resultats = resultats.iloc[:r]
    resultats = resultats.iloc[r:]
    
    probas = predict(partition)
    matrices_2,part_res,part_ids_courses,part_numeros_PMU,part_cotes,part_cotes_non_partants=generate_matrices(probas,partition_resultats,num_partition)
    res = res + part_res
    ids_courses = ids_courses + part_ids_courses
    numeros_PMU = numeros_PMU + part_numeros_PMU
    cotes = np.hstack((cotes, part_cotes))
    cotes_non_partants = np.hstack((cotes_non_partants, part_cotes_non_partants))
    print("calculating final probas")
    for mat in matrices_2:
        for prob in normalize_probas(borda_count(correct_matrice(mat[0]),mat[1])): #  borda_count(correct_matrice(mat[0]),mat[1]): #  normalize_probas(borda_count(correct_matrice(mat[0]),mat[1])): # 
            probs.append(prob)


# cotes=[]
# for index, row in resultats.iterrows():
#     cote=eval(row.iloc[3])
#     cotes=cotes+cote
# probs = [1 / value if value > 0 else 1/10000 for value in cotes]

final = pd.DataFrame(np.hstack((cotes.T,cotes_non_partants.T)), columns=CATEGORIES+[categorie+'_NP' for categorie in CATEGORIES])
final["PROBAS"] = probs
final["IDS_COURSES"] = ids_courses
final["RES"] = res
final["NUM_PMU"] = numeros_PMU


final.to_csv(PATH + directory_encode + '/resultats_'+model_choice+'_borda_norm.csv',index=False)
        
display_prob(probs,res)  
plotProbas(probs)

# print("logloss ")
# print(sklearn.metrics.log_loss(resultats, probs)) 
# RocCurveDisplay.from_predictions(resultats, probs)
# plt.show()
