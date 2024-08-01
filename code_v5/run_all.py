import subprocess
from path import *
from create_dataset import *
from encode import *

# generate_dataset("1/1/2020","1/1/2024",DATASET,training=True,select_specialite="attele")

# generate_dataset("1/1/2023","1/1/2024",DATASET_TEST,training=False,select_specialite="attele")

# encode_primary(directory_encode,"1/1/2020","1/1/2023",DATASET+"_attele.csv")

# encode_new_data(directory_encode,"1/1/2023","1/1/2024",DATASET+"_attele.csv",training=True)
# encode_new_data(directory_encode,"1/1/2023","1/1/2024",DATASET_TEST+"_attele.csv",training=False)



generate_dataset("1/1/2020","1/1/2024",DATASET,training=True,select_specialite="attele")

generate_dataset("1/1/2023","1/1/2024",DATASET_TEST,training=False,select_specialite="attele")

encode_primary(directory_encode,"1/1/2020","31/12/2022",DATASET+"_attele.csv")

encode_new_data(directory_encode,"1/1/2023","1/1/2024",DATASET+"_attele.csv",training=True)
encode_new_data(directory_encode,"1/1/2023","1/1/2024",DATASET_TEST+"_attele.csv",training=False)

# encode_primary(directory_encode,"1/1/2018","1/1/2022",DATASET+"_plat.csv")

# encode_new_data(directory_encode,"1/1/2022","1/1/2023",DATASET+"_plat.csv",training=True)
# encode_new_data(directory_encode,"1/1/2022","1/1/2023",DATASET_TEST+"_plat.csv",training=False)

# Liste des noms de fichiers des scripts Python à exécuter dans l'ordre
scripts = [PATH+"/code_v5/lgbm_model.py"]# PATH+"/code_v3/create_dataset.py", 
# Boucle sur chaque script dans la liste
for script in scripts:
    print(f"Exécution de {script} ...")
    # Exécute le script en utilisant subprocess et attend la fin de l'exécution
    subprocess.run(["C:/Users/NicolasBocage/AppData/Local/Programs/Python/Python312/python.exe", script], check=True)
