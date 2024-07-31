ENV = "DEV"
PATH = "C:/Users/NicolasBocage/Documents/projet/test/"
PATH_TO_CACHE = PATH+"cache/"
PARTICIPANT_URL = PATH_TO_CACHE+"participants/"
PATH_TO_DATASETS = PATH_TO_CACHE+"datasets/"
directory_encode= "2021_2022_attele_reduced" # "short_for_dev" #"archive/tests_v3/2024_less_info" # "2023_less_info" # "v4_2023_attele" #2021_2022_attele_reduced
DATASET="short_dev"#"reduced"
DATASET_TEST= "2021_2022_reduced_20f_samefy" #"short_dev_test"#

def div_time(date,delay=0):
    nombre_de_mois_par_div=1
    year=int(date[4:8])
    div=int(int(date[2:4])/nombre_de_mois_par_div)+delay
    while div<1:
        year=year-1
        div=int(div+(12/nombre_de_mois_par_div))
    return str(year)+str(div)

# import pandas as pd
# df=pd.read_csv(PATH+directory_encode+'/X_test.csv')
# print(df.iloc[:, 133])