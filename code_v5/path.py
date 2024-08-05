ENV = "DEV"
PATH = "C:/Users/NicolasBocage/Documents/projet/test/"
PATH_TO_CACHE = PATH+"cache/"
PARTICIPANT_URL = PATH_TO_CACHE+"participants/"
PATH_TO_DATASETS = PATH_TO_CACHE+"datasets/"
directory_encode= "2020_2023_reduced" #"2020_2023" # "short_for_dev" 
DATASET="2020_2024_reduced"#"reduced"
DATASET_TEST= "2020_2024_reduced_test"# "2024_test" #"short_dev_test"#

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
