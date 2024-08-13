import subprocess
from path import *
from create_dataset import *
from encode import *
from lgbm_model import *
from treat_classifier_results import *
from model_xgboost import *
# generate_dataset("1/1/2021","1/1/2024",DATASET,training=True,select_specialite="attele")

# generate_dataset("1/3/2023","1/1/2024",DATASET_TEST,training=False,select_specialite="attele")

# encode_primary(directory_encode,"1/1/2021","28/2/2023",DATASET+"_attele.csv")

# encode_new_data(directory_encode,"1/4/2023","1/1/2024",DATASET+"_attele",training=True)
# encode_new_data(directory_encode,"1/4/2023","1/1/2024",DATASET_TEST+"_attele",training=False)


params = {
    'objective': 'binary',
    'metric': 'binary_logloss',
    'learning_rate': 0.07,
    'max_depth': -1,
    'num_leaves': 350, #max 256
    'subsample': 0.7,
    'colsample_bytree': 0.7,
    'seed': 42
}
prefix="_07_350_07_2000"
train_lgbm(directory_encode,params,num_boost_round=2000,prefix=prefix,display_probs = False)

process_classifier("lightgbm",directory_encode,prefix,display=True) #model_choice = "lightgbm"  # Options: "xgboost", "randomForest", "lightgbm","linregressor"

