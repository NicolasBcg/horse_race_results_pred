ENV = "DEV"
PATH = "C:/Users/NicolasBocage/Documents/projet/test/"
PATH_TO_CACHE = PATH+"cache/"
PARTICIPANT_URL = PATH_TO_CACHE+"participants/"
PATH_TO_DATASETS = PATH_TO_CACHE+"datasets/"

def div_time(date,delay=0):
    nombre_de_mois_par_div=1
    year=int(date[4:8])
    div=int(int(date[2:4])/nombre_de_mois_par_div)+delay
    while div<1:
        year=year-1
        div=int(div+(12/nombre_de_mois_par_div))
    return str(year)+str(div)