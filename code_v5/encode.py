import pandas as pd
import time 
import datetime
from sklearn import preprocessing
import os
import random
import copy
import joblib
from sklearn.preprocessing import LabelEncoder,OrdinalEncoder,StandardScaler
from path import *

ENCODER_TYPE = "ordinal" # or target label

# start=time.time()
# print("import end "+str(time.time()-start))
# print(data.head())

list_to_onehot=["sexe","race","oeilleres","deferre","avisEntraineur", "d1","d2","d3","d4","d5","d6","d7","d8","d9"]#,"d10"]
list_to_target=[]#["proprietaire","eleveur","driver"]
o=[feature+".1" for feature in list_to_onehot]
t=[feature+".1" for feature in list_to_target]
list_to_onehot=list_to_onehot+["nature","discipline","typePiste"]+o
list_to_target=list_to_target+["code", "categorieParticularite","intitule","nebulositeCode"] +t


def encode_primary(filename,date1,date2,DATASET,NORMALIZE = False):
    print("extracting data to encode")
    df=pd.read_csv(PATH_TO_DATASETS+DATASET)
    print("spliting data to encode")
    date1=time.mktime(datetime.datetime.strptime(date1,"%d/%m/%Y").timetuple())
    date2=time.mktime(datetime.datetime.strptime(date2,"%d/%m/%Y").timetuple())
    df = df[df.dateReunion>date1*1000]
    df = df[df.dateReunion<date2*1000]
    if df['valeurMesure'].apply(lambda x: isinstance(x, str)).any():
        df['valeurMesure']=df['valeurMesure'].str.replace(',', '.').astype(float)
    else :
        df['valeurMesure']=df['valeurMesure'].astype(float)
    df['dateReunion'] = pd.to_datetime(df['dateReunion']/1000, unit='s')
    df['day'] = df['dateReunion'].dt.day
    df['month'] = df['dateReunion'].dt.month
    df['year'] = df['dateReunion'].dt.year
    df=df.drop(["dateReunion"],axis=1)
    df_y=df[["resultats"]]
    df=df.drop(["resultats"],axis=1)
    df=df.drop(["idCourse"],axis=1)


    encoders={}

    print("Encoding")
    if ENCODER_TYPE=="target":
        for col in list_to_target:
            print("encoding "+col)
            enc = preprocessing.TargetEncoder()
            targeted = enc.fit_transform(df[[col]],df_y)
            encoders[col]=copy.copy(enc)
            df[col]= targeted
    if ENCODER_TYPE=="label":
        for col in list_to_target:
            print("encoding "+col)
            enc = LabelEncoder()
            labelled = enc.fit_transform(df[col])
            encoders[col]=copy.copy(enc)
            df[col]= labelled
    if ENCODER_TYPE=="ordinal":
        for col in list_to_target:
            print("encoding or "+col)
            enc = OrdinalEncoder(handle_unknown='use_encoded_value',unknown_value=-1)
            ordinaled = enc.fit_transform(df[[col]])
            encoders[col]=copy.copy(enc)
            df[col]= ordinaled

            
    print("One hot Encoding")
    for col in list_to_onehot:
        print("encoding oh "+col)
        encoder = preprocessing.OneHotEncoder(handle_unknown="ignore", max_categories=20, sparse_output=False)
        onehot = encoder.fit_transform(df[[col]],)
        feature_names = encoder.categories_[0]
        onehot_df = pd.DataFrame(onehot, columns=feature_names)
        encoders[col]=copy.copy(encoder)
        df.reset_index(drop=True, inplace=True)
        onehot_df.reset_index(drop=True, inplace=True)
        df= pd.concat([df, onehot_df], axis=1)
        df.drop([col], axis=1, inplace=True)
    print(df.shape)
    os.makedirs(PATH+filename)
    os.makedirs(PATH+filename+"/encoders")        
    if NORMALIZE:
    # Normalize the data
        scaler = StandardScaler()
        df = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)
        encoders['scaler'] = scaler  # Save the scaler to the encoders dictionary
        joblib.dump(scaler , PATH + filename + "/encoders/scaler.joblib")
    for key in encoders.keys():
        joblib.dump(encoders[key], PATH+filename+"/encoders/"+key+".joblib")

    print(df.shape)
    print(df_y.shape)    
    df.to_csv(PATH+filename+"/X_train.csv",index=False)
    df_y.to_csv(PATH+filename+"/Y_train.csv",index=False)

    
def encode_new_data(filename,date1,date2,DATASET,training=True,NORMALIZE = False):
    print("extracting data to encode")
    df=pd.read_csv(PATH_TO_DATASETS+DATASET)
    print("spliting data to encode")
    date1=time.mktime(datetime.datetime.strptime(date1,"%d/%m/%Y").timetuple())
    date2=time.mktime(datetime.datetime.strptime(date2,"%d/%m/%Y").timetuple())
    df = df[df.dateReunion>=date1*1000]
    df = df[df.dateReunion<date2*1000]
    if df['valeurMesure'].apply(lambda x: isinstance(x, str)).any(): 
        df['valeurMesure']=df['valeurMesure'].str.replace(',', '.').astype(float)
    else :
        df['valeurMesure']=df['valeurMesure'].astype(float)
    df['dateReunion'] = pd.to_datetime(df['dateReunion']/1000, unit='s')
    df['day'] = df['dateReunion'].dt.day
    df['month'] = df['dateReunion'].dt.month
    df['year'] = df['dateReunion'].dt.year
    df=df.drop(["dateReunion"],axis=1)
    if training:
        df_y=df[["resultats"]]
        df=df.drop(["resultats"],axis=1)
    df=df.drop(["idCourse"],axis=1)
    numsPMU = df[["numPmu", "numPmu.1"]]

    print(df.shape)
    if training:
        print(df_y.shape) 

    encoders=list_to_target
    if ENCODER_TYPE=="target":
        for encoder in encoders:
            print("encoding "+encoder)
            enc = joblib.load( PATH+filename+"/encoders/"+encoder+".joblib")
            targeted = enc.transform(df[[encoder]])
            df[encoder]= targeted
    if ENCODER_TYPE=="label":
        for encoder in encoders:
            print("encoding "+encoder)
            enc = joblib.load( PATH+filename+"/encoders/"+encoder+".joblib")
            labelled = enc.transform(df[encoder])
            df[encoder]= labelled   
    if ENCODER_TYPE=="ordinal":
        for encoder in encoders:
            print("encoding or "+encoder)
            enc = joblib.load( PATH+filename+"/encoders/"+encoder+".joblib")
            labelled = enc.transform(df[[encoder]])
            df[encoder]= labelled 
            

    encoders=list_to_onehot
    print(df.shape)
    for encoder in encoders:
        print("encoding oh "+encoder)
        enc = joblib.load( PATH+filename+"/encoders/"+encoder+".joblib")
        onehot = enc.transform(df[[encoder]],)
        feature_names = enc.categories_[0]
        onehot_df = pd.DataFrame(onehot, columns=feature_names)
        df.reset_index(drop=True, inplace=True)
        onehot_df.reset_index(drop=True, inplace=True)
        df= pd.concat([df, onehot_df], axis=1)
        df.drop([encoder], axis=1, inplace=True)
    if NORMALIZE:
        scaler = joblib.load(PATH + filename + "/encoders/scaler.joblib")
        df = pd.DataFrame(scaler.transform(df), columns=df.columns)

    print(df.shape)
    if training:
        print(df_y.shape)
        df.to_csv(PATH+filename+"/X_test.csv",index=False)
        df_y.to_csv(PATH+filename+"/Y_test.csv",index=False)
    else : 
        df = pd.concat([df, numsPMU["numPmu"].rename("numPmu0"),numsPMU["numPmu.1"].rename("numPmu01")], axis=1)
        print("concatenated")
        df.to_csv(PATH+filename+"/X_test_2.csv",index=False)

# encode_new_data(directory_encode,"1/1/2023","1/1/2024",DATASET_TEST+"_attele.csv",training=False)
# filename=directory_encode
# df=pd.read_csv(PATH+filename+"/X_test_2.csv")
# print(df.shape)
# df['valeurMesure']=df['valeurMesure'].str.replace(',', '.').astype(float)
# df.to_csv(PATH+filename+"/X_test_2.csv",index=False)

# df=pd.read_csv(PATH+filename+"/X_test.csv")
# df['valeurMesure']=df['valeurMesure'].str.replace(',', '.').astype(float)
# df.to_csv(PATH+filename+"/X_test.csv",index=False)

# df=pd.read_csv(PATH+filename+"/X_train.csv")
# df['valeurMesure']=df['valeurMesure'].str.replace(',', '.').astype(float)
# df.to_csv(PATH+filename+"/X_train.csv",index=False)

#encode_primary(directory_encode,"1/1/2018","1/1/2022",DATASET+"_attele.csv")
#encode_new_data(directory_encode,"1/1/2022","1/1/2023",DATASET+"_attele.csv",training=True)


#encode_new_data(directory_encode,"1/1/2022","1/1/2023",DATASET_TEST+"_attele.csv",training=False)




