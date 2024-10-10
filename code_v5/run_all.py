import subprocess
from path import *
from C_Create_dataset import *
from D_encode import *
from model_lgbm import *
from E_treat_classifier_results import *
from model_xgboost import *
from F_add_cotes import *
# generate_dataset("1/1/2022","1/1/2023",DATASET,training=True,select_specialite="all")
# print("first dataset created")
# generate_dataset("1/8/2022","1/1/2023",DATASET_TEST,training=False,select_specialite="all")
# print("Second dataset created")

# encode_primary(directory_encode,"1/1/2019","1/8/2022",DATASET+"_PLAT.csv")

# encode_new_data(directory_encode,"1/8/2022","1/1/2023",DATASET+"_PLAT",training=True)
# encode_new_data(directory_encode,"1/8/2022","1/1/2023",DATASET_TEST+"_PLAT",training=False)


params = {
    'objective': 'binary',
    'metric': 'binary_logloss',
    'learning_rate': 0.05,
    'max_depth': -1,
    'num_leaves': 512, #max 256
    'subsample': 0.8,
    'colsample_bytree': 0.8,
    'seed': 42
}
sufix="_05_512_08_3000"
# sufix="_03_1024_08_2000"

train_lgbm(directory_encode,params,num_boost_round=200,sufix=sufix,display_probs = True)
file_created = process_classifier("lgbm",directory_encode,sufix,display=False) #model_choice = "lightgbm"  # Options: "xgboost", "randomForest", "lightgbm","linregressor"
add_odds_ZETurf(file_created,intermediate_directory=directory_encode)
# params = {
#     'objective': 'binary',
#     'metric': 'binary_logloss',
#     'learning_rate': 0.03,
#     'max_depth': -1,
#     'num_leaves': 1024, #max 256
#     'subsample': 0.8,
#     'colsample_bytree': 0.8,
#     'seed': 42
# }
# sufix="_03_1024_08_2000"
# # train_lgbm(directory_encode,params,num_boost_round=2000,sufix=sufix,display_probs = False)
# process_classifier("lgbm",directory_encode,sufix,display=False) #model_choice = "lightgbm"  # Options: "xgboost", "randomForest", "lightgbm","linregressor"


# params = {
#     'objective': 'binary',
#     'metric': 'binary_logloss',
#     'learning_rate': 0.08,
#     'max_depth': -1,
#     'num_leaves': 256, #max 256
#     'subsample': 1,
#     'colsample_bytree': 1,
#     'seed': 42
# }
# sufix="08_256_1_4000"
# # train_lgbm(directory_encode,params,num_boost_round=4000,sufix=sufix,display_probs = True)
# process_classifier("lgbm",directory_encode,sufix,display=False) #model_choice = "lightgbm"  # Options: "xgboost", "randomForest", "lightgbm","linregressor"



# # Configure XGBoost
# params = {
#     'objective': 'binary:logistic',   # Binary classification
#     'eval_metric': 'logloss',          # Use log loss as evaluation metric
#     'eta': 0.03,                        # Learning rate
#     'max_depth': 10,                    # Maximum depth of a tree
#     'subsample': 0.8,                  # Subsample ratio of the training instances
#     'colsample_bytree': 0.8,           # Subsample ratio of columns when constructing each tree
#     'seed': 42                         # Random seed for reproducibility
# }
# sufix = '_03_10_08_2000'
# # train_xgb(directory_encode,params,num_boost_round=2000,sufix=sufix,display_probs=False)
# process_classifier("xgboost",directory_encode,sufix,display=False) #model_choice = "lightgbm"  # Options: "xgboost", "randomForest", "lightgbm","linregressor"

# # Configure XGBoost
# params = {
#     'objective': 'binary:logistic',   # Binary classification
#     'eval_metric': 'logloss',          # Use log loss as evaluation metric
#     'eta': 0.05,                       # Learning rate
#     'max_depth': 8,                    # Maximum depth of a tree
#     'subsample': 1,                  # Subsample ratio of the training instances
#     'colsample_bytree': 1,           # Subsample ratio of columns when constructing each tree
#     'seed': 42                         # Random seed for reproducibility
# }
# sufix = '_05_8_1_4000'
# # train_xgb(directory_encode,params,num_boost_round=4000,sufix=sufix,display_probs=False)
# process_classifier("xgboost",directory_encode,sufix,display=False) #model_choice = "lightgbm"  # Options: "xgboost", "randomForest", "lightgbm","linregressor"

# # Configure XGBoost
# params = {
#     'objective': 'binary:logistic',   # Binary classification
#     'eval_metric': 'logloss',          # Use log loss as evaluation metric
#     'eta': 0.05,                       # Learning rate
#     'max_depth': 9,                    # Maximum depth of a tree
#     'subsample': 0.8,                  # Subsample ratio of the training instances
#     'colsample_bytree': 0.8,           # Subsample ratio of columns when constructing each tree
#     'seed': 42                         # Random seed for reproducibility
# }
# sufix = '_05_9_08_4000'
# # train_xgb(directory_encode,params,num_boost_round=4000,sufix=sufix,display_probs=False)
# process_classifier("xgboost",directory_encode,sufix,display=False) #model_choice = "lightgbm"  # Options: "xgboost", "randomForest", "lightgbm","linregressor"

# #LGBM BIG
# params = {
#     'objective': 'binary',
#     'metric': 'binary_logloss',
#     'learning_rate': 0.03,
#     'max_depth': -1,
#     'num_leaves': 2048, #max 256
#     'subsample': 0.8,
#     'colsample_bytree': 0.8,
#     'seed': 42
# }
# sufix="_03_2048_08_3000"
# # train_lgbm(directory_encode,params,num_boost_round=3000,sufix=sufix,display_probs = False)
# process_classifier("lgbm",directory_encode,sufix,display=False) #model_choice = "lightgbm"  # Options: "xgboost", "randomForest", "lightgbm","linregressor"

# # Configure XGBoost BIG
# params = {
#     'objective': 'binary:logistic',   # Binary classification
#     'eval_metric': 'logloss',          # Use log loss as evaluation metric
#     'eta': 0.03,                       # Learning rate
#     'max_depth': 11,                    # Maximum depth of a tree
#     'subsample': 0.7,                  # Subsample ratio of the training instances
#     'colsample_bytree': 0.7,           # Subsample ratio of columns when constructing each tree
#     'seed': 42                         # Random seed for reproducibility
# }
# sufix = '_03_11_07_4000'
# # train_xgb(directory_encode,params,num_boost_round=4000,sufix=sufix,display_probs=False)
# process_classifier("xgboost",directory_encode,sufix,display=False) #model_choice = "lightgbm"  # Options: "xgboost", "randomForest", "lightgbm","linregressor"

# # Configure XGBoost BIG
# params = {
#     'objective': 'binary:logistic',   # Binary classification
#     'eval_metric': 'logloss',          # Use log loss as evaluation metric
#     'eta': 0.02,                       # Learning rate
#     'max_depth': 12,                    # Maximum depth of a tree
#     'subsample': 0.6,                  # Subsample ratio of the training instances
#     'colsample_bytree': 0.6,           # Subsample ratio of columns when constructing each tree
#     'seed': 42                         # Random seed for reproducibility
# }
# sufix = '_02_12_06_4000'
# # train_xgb(directory_encode,params,num_boost_round=4000,sufix=sufix,display_probs=False)
# process_classifier("xgboost",directory_encode,sufix,display=False) #model_choice = "lightgbm"  # Options: "xgboost", "randomForest", "lightgbm","linregressor"
