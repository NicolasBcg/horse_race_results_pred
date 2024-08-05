import json
import os
import pandas as pd
from path import *
import datetime
import time 
import random

random.seed(42)
NB_FANTOMES=20
FILE_FANTOME="fantomes_2nd_sem_2022_reduced"
FEATURES_REUNION = [
    ["dateReunion"],
    ["nature","UNKNOWN"],
    [["pays","code"],"UNKNOWN"],
    [["meteo","nebulositeCode"],"UNKNOWN"],
    [["meteo","temperature"],15],
    [["meteo","forceVent"],4],
]

FEATURES_COURSE = [
    ["distance",None],
    ["discipline","UNKNOWN"],
    ["categorieParticularite","UNKNOWN"],
    ["typePiste","UNKNOWN"],
    #[["penetrometre","valeurMesure"],-1],
    [["penetrometre","intitule"],"UNKNOWN"],

]

NB_FEATURES_JOCKEY=6
FEATURES_JOCKEY = [
    ["nb_courses_m-1",0],
    ["nb_premier_m-1",0],
    ["nb_second_m-1",0],
    ["nb_troisieme_m-1",0],
    ["nb_non_arrive_m-1",0],
    ["nb_dernier_m-1",0],
    ["nb_courses_m-2-3",0],
    ["nb_premier_m-2-3",0],
    ["nb_second_m-2-3",0],
    ["nb_troisieme_m-2-3",0],
    ["nb_non_arrive_m-2-3",0],
    ["nb_dernier_m-2-3",0],
    ["nb_courses_m-4-6",0],
    ["nb_premier_m-4-6",0],
    ["nb_second_m-4-6",0],
    ["nb_troisieme_m-4-6",0],
    ["nb_non_arrive_m-4-6",0],
    ["nb_dernier_m-4-6",0],
    ["nb_courses_m-6-12",0],
    ["nb_premier_m-6-12",0],
    ["nb_second_m-6-12",0],
    ["nb_troisieme_m-6-12",0],
    ["nb_non_arrive_m-6-12",0],
    ["nb_dernier_m-6-12",0],
    ["nb_courses_m-13-24",0],
    ["nb_premier_m-13-24",0],
    ["nb_second_m-13-24",0],
    ["nb_troisieme_m-13-24",0],
    ["nb_non_arrive_m-13-24",0],
    ["nb_dernier_m-13-24",0],
    ["nb_courses_tot",0],
    ["nb_premier_tot",0],
    ["nb_second_tot",0],
    ["nb_troisieme_tot",0],
    ["nb_non_arrive_tot",0],
    ["nb_dernier_tot",0]
]
NB_FEATURES_ELEVEUR=6
FEATURES_ELEVEUR = [
    # ["eleveur_courses_m-1",0],
    # ["eleveur_premier_m-1",0],
    # ["eleveur_second_m-1",0],
    # ["eleveur_troisieme_m-1",0],
    # ["eleveur_non_arrive_m-1",0],
    # ["eleveur_dernier_m-1",0],
    # ["eleveur_courses_m-6-18",0],
    # ["eleveur_premier_m-6-18",0],
    # ["eleveur_second_m-6-18",0],
    # ["eleveur_troisieme_m-6-18",0],
    # ["eleveur_non_arrive_m-6-18",0],
    # ["eleveur_dernier_m-6-18",0],
    ["eleveur_courses_tot",0],
    ["eleveur_premier_tot",0],
    ["eleveur_second_tot",0],
    ["eleveur_troisieme_tot",0],
    ["eleveur_non_arrive_tot",0],
    ["eleveur_dernier_tot",0]
]
NB_FEATURES_PROPRIETAIRE=6
FEATURES_PROPRIETAIRE = [
    # ["proprietaire_courses_m-1",0],
    # ["proprietaire_premier_m-1",0],
    # ["proprietaire_second_m-1",0],
    # ["proprietaire_troisieme_m-1",0],
    # ["proprietaire_non_arrive_m-1",0],
    # ["proprietaire_dernier_m-1",0],
    # ["proprietaire_courses_m-2-3",0],
    # ["proprietaire_premier_m-2-3",0],
    # ["proprietaire_second_m-2-3",0],
    # ["proprietaire_troisieme_m-2-3",0],
    # ["proprietaire_non_arrive_m-2-3",0],
    # ["proprietaire_dernier_m-2-3",0],
    # ["proprietaire_courses_m-4-6",0],
    # ["proprietaire_premier_m-4-6",0],
    # ["proprietaire_second_m-4-6",0],
    # ["proprietaire_troisieme_m-4-6",0],
    # ["proprietaire_non_arrive_m-4-6",0],
    # ["proprietaire_dernier_m-4-6",0],
    # ["proprietaire_courses_m-6-12",0],
    # ["proprietaire_premier_m-6-12",0],
    # ["proprietaire_second_m-6-12",0],
    # ["proprietaire_troisieme_m-6-12",0],
    # ["proprietaire_non_arrive_m-6-12",0],
    # ["proprietaire_dernier_m-6-12",0],
    # ["proprietaire_courses_m-13-24",0],
    # ["proprietaire_premier_m-13-24",0],
    # ["proprietaire_second_m-13-24",0],
    # ["proprietaire_troisieme_m-13-24",0],
    # ["proprietaire_non_arrive_m-13-24",0],
    # ["proprietaire_dernier_m-13-24",0],
    ["proprietaire_courses_tot",0],
    ["proprietaire_premier_tot",0],
    ["proprietaire_second_tot",0],
    ["proprietaire_troisieme_tot",0],
    ["proprietaire_non_arrive_tot",0],
    ["proprietaire_dernier_tot",0]
]

FEATURES_MUSIQUE=[
    ["r1"],
    ["d1"],
    ["r2"],
    ["d2"],
    ["r3"],
    ["d3"],
    ["r4"],
    ["d4"],
    ["r5"],
    ["d5"],
    ["r6"],
    ["d6"],
    ["r7"],
    ["d7"],
    ["r8"],
    ["d8"],
    ["r9"],
    ["d9"],
    ["r10"],
    # ["d10"],
]
FEATURES_MUSIQUE = FEATURES_MUSIQUE[:19:2]
FEATURES_CHEVAL_PLAT_TROT_ATTELE=[
    ["numPmu"],
    ["age",None],
    ["sexe","UNKNOWN"],
    ["race","UNKNOWN"],
    ["oeilleres","UNKNOWN"],
    
    ["deferre","UNKNOWN"],
    ["driverChange",None],
    ["indicateurInedit","UNKNOWN"],
    ["nombreCourses",-1],
    ["nombreVictoires",-1],
    ["nombrePlaces",-1],
    ["nombrePlacesSecond",-1],
    ["nombrePlacesTroisieme",-1],
    [["gainsParticipant","gainsCarriere"],-1],
    [["gainsParticipant","gainsVictoires"],-1],
    [["gainsParticipant","gainsPlace"],-1],
    [["gainsParticipant","gainsAnneeEnCours"],-1],
    [["gainsParticipant","gainsAnneePrecedente"],-1],
    ["jumentPleine",None],
    ["engagement"],
    ["supplement",-1],
    ["handicapDistance",-1],
    ["handicapPoids",-1],
    ["poidsConditionMonteChange"],
    ["avisEntraineur","UNKNOWN"],
    ["driver_last_course",-100],
    ["driver_last_out",-100],
    ["horse_last_out",-100],
    ["horse_last_elo",1400],
    ["jockey_last_elo",1400],
    ["horse_last_elo_v2",1400],
    ["jockey_last_elo_v2",1400],
    # ["proprietaire","UNKNOWN"],
    # ["eleveur","UNKNOWN"],
    # ["driver","UNKNOWN"]
]
FEATURES_CHEVAL_TROT_ATTELE=[
    ["numPmu"],
    ["age",None],
    ["sexe","UNKNOWN"],
    ["race","UNKNOWN"],
    ["oeilleres","UNKNOWN"],
    
    ["deferre","UNKNOWN"],
    ["driverChange",None],
    ["indicateurInedit","UNKNOWN"],
    ["nombreCourses",-1],
    ["nombreVictoires",-1],
    ["nombrePlaces",-1],
    ["nombrePlacesSecond",-1],
    ["nombrePlacesTroisieme",-1],
    [["gainsParticipant","gainsCarriere"],-1],
    [["gainsParticipant","gainsVictoires"],-1],
    [["gainsParticipant","gainsPlace"],-1],
    [["gainsParticipant","gainsAnneeEnCours"],-1],
    [["gainsParticipant","gainsAnneePrecedente"],-1],
    ["jumentPleine",None],
    ["engagement"],
    # ["supplement",-1],
    ["handicapDistance",-1],
    # ["handicapPoids",-1],
    # ["poidsConditionMonteChange"],
    ["avisEntraineur","UNKNOWN"],
    ["driver_last_course",-100],
    ["driver_last_out",-100],
    ["horse_last_out",-100],
    ["horse_last_elo",1400],
    ["jockey_last_elo",1400],
    ["horse_last_elo_v2",1400],
    ["jockey_last_elo_v2",1400],
    # ["proprietaire","UNKNOWN"],
    # ["eleveur","UNKNOWN"],
    # ["driver","UNKNOWN"]
]

with open(PATH_TO_DATASETS+"jockeys.json", 'r') as f:
    resultats_jockeys = json.load(f) 
jockeys=resultats_jockeys.keys()
with open(PATH_TO_DATASETS+"eleveurs.json", 'r') as f:
    resultats_eleveurs = json.load(f) 
eleveurs=resultats_eleveurs.keys()
with open(PATH_TO_DATASETS+"proprietaires.json", 'r') as f:
    resultats_proprietaires = json.load(f) 
proprietaires=resultats_proprietaires.keys()
with open(PATH_TO_DATASETS+"FANTOMES_"+FILE_FANTOME+".json", 'r') as f:
    fantomes = json.load(f) 


def get_features_musique(musique):
    liste_resultat = []
    if musique not in ["Inédit","Inédite","couru afasec"]:
        entre_parentheses = False
        indice = 0
        for caractere in musique:
            if caractere == '(':
                entre_parentheses = True
            elif caractere == ')':
                entre_parentheses = False
            elif not entre_parentheses:
                if indice % 2 == 0:
                    if caractere in ['0','1','2','3','4','5','6','7','8','9']:
                        liste_resultat.append(int(caractere))
                    else:
                        liste_resultat.append(-1)
                    indice += 1
                else:
                    if caractere not in ['a','c','h','m','o','p','s']:
                        print(musique)
                        liste_resultat[-1]=0
                    else :
                        liste_resultat.append(caractere)
                        indice += 1

                    
    elif musique in ["couru afasec"]:
        # Compléter la liste jusqu'à 20 éléments
        while len(liste_resultat) < 20:
            if len(liste_resultat) % 2 == 0:
                liste_resultat.append(-5)
            else:
                liste_resultat.append('F')

    # Compléter la liste jusqu'à 20 éléments
    while len(liste_resultat) < 20:
        if len(liste_resultat) % 2 == 0:
            liste_resultat.append(-10)
        else:
            liste_resultat.append('U')
    lr=liste_resultat[:19:2]  # Limiter la liste à 20 éléments

    return lr

def get_Features_jockey(jockey,date):
    res=[0 for _ in range(len(FEATURES_JOCKEY))]
    if jockey in jockeys:
        year_semester=div_time(date)
        last_month_div=div_time(date,-1)
        last_month_div_2_3 = [div_time(date,-2),div_time(date,-3)]
        last_month_div_4_6 = [div_time(date,-m) for m in range(4,7)]
        last_month_div_7_12 = [div_time(date,-m) for m in range(7,13)]
        last_month_div_13_24 = [div_time(date,-m) for m in range(13,24)]
        for key in resultats_jockeys[jockey].keys():
            if int(key)<int(year_semester):
                for i in range(NB_FEATURES_JOCKEY):
                    res[i+5*NB_FEATURES_JOCKEY]+=resultats_jockeys[jockey][key][i]
                if key==last_month_div:
                    for i in range(NB_FEATURES_JOCKEY):
                        res[i]+=resultats_jockeys[jockey][key][i]
                elif key in last_month_div_2_3:
                    for i in range(NB_FEATURES_JOCKEY):
                        res[i+NB_FEATURES_JOCKEY]+=resultats_jockeys[jockey][key][i]
                elif key in last_month_div_4_6:
                    for i in range(NB_FEATURES_JOCKEY):
                        res[i+2*NB_FEATURES_JOCKEY]+=resultats_jockeys[jockey][key][i]
                elif key in last_month_div_7_12:
                    for i in range(NB_FEATURES_JOCKEY):
                        res[i+3*NB_FEATURES_JOCKEY]+=resultats_jockeys[jockey][key][i]
                elif key in last_month_div_13_24:
                    for i in range(NB_FEATURES_JOCKEY):
                        res[i+4*NB_FEATURES_JOCKEY]+=resultats_jockeys[jockey][key][i]
    return res
def get_Features_eleveur(eleveur,date):
    res=[0 for _ in range(len(FEATURES_ELEVEUR))]
    if eleveur in eleveurs:
        year_semester=div_time(date)
        # last_month_div=div_time(date,-1)
        # last_month_div_1_6 = [div_time(date,-m) for m in range(1,7)]
        # last_month_div_6_18 = [div_time(date,-m) for m in range(7,18)]
        for key in resultats_eleveurs[eleveur].keys():
            if int(key)<int(year_semester):
                for i in range(NB_FEATURES_ELEVEUR):
                    res[i]+=resultats_eleveurs[eleveur][key][i]
                # if key == last_month_div:
                #     for i in range(NB_FEATURES_ELEVEUR):
                #         res[i]+=resultats_eleveurs[eleveur][key][i]
                # elif key in last_month_div_6_18:
                #     for i in range(NB_FEATURES_JOCKEY):
                #         res[i+NB_FEATURES_ELEVEUR]+=resultats_eleveurs[eleveur][key][i]
    return res

def get_FEATURES_PROPRIETAIRE(proprietaire,date):
    res=[0 for _ in range(len(FEATURES_PROPRIETAIRE))]
    if proprietaire in proprietaires:
        year_semester=div_time(date)
        # last_month_div=div_time(date,-1)
        # last_month_div_2_3 = [div_time(date,-2),div_time(date,-3)]
        # last_month_div_4_6 = [div_time(date,-m) for m in range(4,7)]
        # last_month_div_7_12 = [div_time(date,-m) for m in range(7,13)]
        # last_month_div_13_24 = [div_time(date,-m) for m in range(13,24)]
        for key in resultats_proprietaires[proprietaire].keys():
            if int(key)<int(year_semester):
                for i in range(NB_FEATURES_PROPRIETAIRE):
                    res[i]+=resultats_proprietaires[proprietaire][key][i]
                # if key == last_month_div:
                #     for i in range(NB_FEATURES_PROPRIETAIRE):
                #         res[i]+=resultats_proprietaires[proprietaire][key][i]
                # elif key in last_month_div_2_3:
                #     for i in range(NB_FEATURES_PROPRIETAIRE):
                #         res[i+NB_FEATURES_PROPRIETAIRE]+=resultats_proprietaires[proprietaire][key][i]
                # elif key in last_month_div_4_6:
                #     for i in range(NB_FEATURES_PROPRIETAIRE):
                #         res[i+2*NB_FEATURES_PROPRIETAIRE]+=resultats_proprietaires[proprietaire][key][i]
                # elif key in last_month_div_7_12:
                #     for i in range(NB_FEATURES_PROPRIETAIRE):
                #         res[i+3*NB_FEATURES_PROPRIETAIRE]+=resultats_proprietaires[proprietaire][key][i]
                # elif key in last_month_div_13_24:
                #     for i in range(NB_FEATURES_PROPRIETAIRE):
                #         res[i+4*NB_FEATURES_PROPRIETAIRE]+=resultats_proprietaires[proprietaire][key][i]
    return res

def extract_cotes(raport):
    cotes=[0 for _ in range(raport["nbParticipants"])]
    for participant in raport["rapportsParticipant"]:
        cotes[participant["numPmu"]-1]=participant["rapportDirect"]
    return cotes


def create_feature_list(training=True):
    features=[]
    features_lists=[FEATURES_CHEVAL_TROT_ATTELE,FEATURES_JOCKEY,FEATURES_ELEVEUR,FEATURES_PROPRIETAIRE,FEATURES_MUSIQUE,FEATURES_REUNION,FEATURES_COURSE,FEATURES_CHEVAL_TROT_ATTELE,FEATURES_JOCKEY,FEATURES_ELEVEUR,FEATURES_PROPRIETAIRE,FEATURES_MUSIQUE]
    for features_list in features_lists:
        for feature in features_list:
            if type(feature[0])==str:
                features.append(feature[0])
            else:
                features.append(feature[0][1])
    if training : 
        features.append("resultats")
    features.append("idCourse")
    return features

def extract_features(source,features_list):
    features=[]
    for feature in features_list:
        if type(feature[0])==str:
            if feature[0] in source.keys():
                features.append(source[feature[0]])
            else : 
                #print(feature[0])
                features.append(feature[1])
        else:
            if feature[0][0] in source.keys():
                if feature[0][1] in source[feature[0][0]].keys():
                    features.append(source[feature[0][0]][feature[0][1]])
                else :
                    features.append(feature[1])
            else :
                #print(feature[0])
                features.append(feature[1])
    return features

def possible_bets(paris):
    for bet in paris:
        try:
            if (bet["typePari"] == "SIMPLE_GAGNANT" and bet["audience"]!="LOCAL"):# or bet["typePari"] == "E_SIMPLE_GAGNANT":
                return True
        except:
            pass
    return False

def get_incidents(course): 
    if "incidents" in course.keys():
        for incident in course["incidents"]:
            if incident["type"] == "NON_PARTANT":
                # print(incident["numeroParticipants"])
                return incident["numeroParticipants"]
    return []

def recup_infos(file_name,training=True):
    data_by_race = []
    date=file_name.split('.')[0]
    with open(PATH_TO_CACHE+"programmes\\"+file_name, 'r') as file:
        programme = json.loads(file.read())
    for reunion in programme["reunions"]:
        num_reunion = reunion['numOfficiel']
        infos_reunion = extract_features(reunion,FEATURES_REUNION)
        for course in reunion['courses']:
            specialite=course["specialite"]
            if possible_bets(course["paris"]):
                time_start= datetime.datetime.utcfromtimestamp((course["heureDepart"]/1000)+7200).strftime('%H:%M')
                
                if ("ordreArrivee" in course.keys() and ENV=="DEV") or ENV=="PROD" :
                    if ENV=="DEV":
                        ordreArrivee = [i[0] for i in course["ordreArrivee"]]
                    else:
                        ordreArrivee=[]
                    info_course = extract_features(course,FEATURES_COURSE)
                    with open(PATH_TO_CACHE+"participants\\"+date+'-'+str(num_reunion)+'-'+str(course["numOrdre"])+'.json', 'r') as file:
                        participants = json.loads(file.read())
                    idCourse=date+'-'+str(num_reunion)+'-'+str(course["numOrdre"])
                    chevaux=[]

                    if training == False : 
                        non_partants = get_incidents(course)
                    else : 
                        non_partants = []
                        
                    for participant in participants["participants"]:  

                        if "driver" in participant.keys():
                            jockey=participant["driver"]
                        else:
                            jockey="unknown"         
                        if "eleveur" in participant.keys():
                            eleveur=participant["eleveur"]
                        else:
                            eleveur="unknown"           
                        if "proprietaire" in participant.keys():
                            proprietaire=participant["proprietaire"]
                        else:
                            proprietaire="unknown"   
                        if "musique" in participant.keys():
                            musique=participant["musique"]
                        else:
                            musique=""   
                        chevaux.append(extract_features(participant,FEATURES_CHEVAL_TROT_ATTELE)+get_Features_jockey(jockey,date)+get_Features_eleveur(eleveur,date)+get_FEATURES_PROPRIETAIRE(proprietaire,date)+get_features_musique(musique))
                    data_by_race.append(infos_reunion+info_course+[chevaux]+[ordreArrivee]+[idCourse]+[time_start]+[non_partants]+[specialite])
    return data_by_race

def generate_rows_from_race(race,training=True,select_specialite="all"):
    specialite=race.pop()
    non_partants = race.pop()
    time_course= race.pop()
    rows=[]
    if (select_specialite=="all" and (specialite == "TROT_ATTELE" or specialite == "PLAT")) or (specialite == "TROT_ATTELE" and select_specialite=="attele") or (specialite == "PLAT" and select_specialite=="plat") :
        ordre = {}
        idCourse = race.pop()
        resultats = race.pop()
        for i in range(len(resultats)):
            ordre[str(resultats[i])]=i
        chevaux=race.pop()
        if training :
            finishers=[]
            for participant in chevaux:
                if participant[0] in resultats:
                    finishers.append(participant)
            finishers_bis=finishers
        else : 
            finishers=chevaux
            finishers_bis = chevaux.copy()
            nb_participants=len(chevaux)
            while len(finishers_bis)<NB_FANTOMES:
                finishers_bis.append(random.choice(fantomes[specialite]))

            if not training :
                try:
                    with open(PATH_TO_CACHE+'rapports_prealable/'+idCourse+'.json', 'r') as f:
                        raport = json.load(f)
                        course = [resultats]+[idCourse]+[nb_participants]+[extract_cotes(raport)]+[time_course]+[non_partants]
                except:
                    course = [resultats]+[idCourse]+[nb_participants]+[[-1 for _ in range(nb_participants)]]+[time_course]+[non_partants]
            else : 
                course = []

        for cheval1 in finishers:
            for cheval2 in finishers_bis:
                if training and ordre[str(cheval1[0])] != ordre[str(cheval2[0])]:
                    if ordre[str(cheval1[0])] < ordre[str(cheval2[0])] : # =1 si le cheval 1 gagne face au cheval 2
                        res=1
                    elif  ordre[str(cheval1[0])] > ordre[str(cheval2[0])]:
                        res=0
                    rows.append(cheval1+race+cheval2+[res]+[idCourse])
                elif not training: 
                    rows.append(cheval1+race+cheval2+[idCourse])
        if training:
            return rows,specialite,[]
        else :
            return rows,specialite,course
    else :
        return rows,specialite,[]

def generate_dataset(date1,date2,dname,training=True,select_specialite="all"):
    #init files and df
    date1=time.mktime(datetime.datetime.strptime(date1,"%d/%m/%Y").timetuple())
    date2=time.mktime(datetime.datetime.strptime(date2,"%d/%m/%Y").timetuple())
    files=os.listdir(PATH_TO_CACHE+"programmes\\")
    dataset_attele=[]
    dataset_plat=[]
    courses_trot=[]
    courses_plat=[]
    ftrs=create_feature_list(training=training)
    df = pd.DataFrame(dataset_attele, columns =ftrs)
    if select_specialite=="all" or select_specialite=="attele":
        df.to_csv(PATH_TO_CACHE+"datasets\\"+dname+"_attele.csv", mode='w', index=False, header=True)
    dfplat = pd.DataFrame(dataset_plat, columns =ftrs)
    if select_specialite=="all" or select_specialite=="plat":
        dfplat.to_csv(PATH_TO_CACHE+"datasets\\"+dname+"_plat.csv", mode='w', index=False, header=True)

    #create dataset
    file_treated=0
    for f in files:  
        dfile = time.mktime(datetime.datetime.strptime(f.split('.')[0],"%d%m%Y").timetuple())
        if dfile>=date1 and dfile<date2:
            file_treated+=1
            print(f)
            races = recup_infos(f,training) #recup races info for each file
            for race in races: 
                rows,specialite,course=generate_rows_from_race(race,training=training,select_specialite=select_specialite)
                if specialite == "TROT_ATTELE" and (select_specialite=="all" or select_specialite=="attele"):
                    dataset_attele=dataset_attele+rows
                    if not training:
                        courses_trot.append(course)
                if specialite == "PLAT" and (select_specialite=="all" or select_specialite=="plat"):
                    dataset_plat=dataset_plat+rows
                    if not training:
                        courses_plat.append(course)
  
  
    #Save every 20 and at the end
            if file_treated>20:
                file_treated=0
                if select_specialite=="all" or select_specialite=="attele":
                    df = pd.DataFrame(dataset_attele, columns =ftrs)
                    df.to_csv(PATH_TO_CACHE+"datasets\\"+dname+"_attele.csv", mode='a', index=False, header=False)
                if select_specialite=="all" or select_specialite=="plat":
                    dfplat = pd.DataFrame(dataset_plat, columns =ftrs)
                    dfplat.to_csv(PATH_TO_CACHE+"datasets\\"+dname+"_plat.csv", mode='a', index=False, header=False)
                dataset_attele=[]
                dataset_plat=[]
    if select_specialite=="all" or select_specialite=="attele":
        df = pd.DataFrame(dataset_attele, columns =ftrs)
        df.to_csv(PATH_TO_CACHE+"datasets\\"+dname+"_attele.csv", mode='a', index=False, header=False)
    if select_specialite=="all" or select_specialite=="plat":
        dfplat = pd.DataFrame(dataset_plat, columns =ftrs)
        dfplat.to_csv(PATH_TO_CACHE+"datasets\\"+dname+"_plat.csv", mode='a', index=False, header=False)
    if not training:
        if select_specialite=="all" or select_specialite=="attele":
            pd.DataFrame(courses_trot, columns =["resultats","idCourse","nbParticipants","cotes","heure_depart","non_partants"]).to_csv(PATH_TO_CACHE+"datasets\\"+dname+"_attele_res.csv", mode='w', index=False, header=True)
        if select_specialite=="all" or select_specialite=="plat":
            pd.DataFrame(courses_plat, columns =["resultats","idCourse","nbParticipants","cotes","heure_depart","non_partants"]).to_csv(PATH_TO_CACHE+"datasets\\"+dname+"_plat_res.csv", mode='w', index=False, header=True)

def generate_fantomes(date1,date2,dname,select_specialite="all"):
    #init files and df
    date1=time.mktime(datetime.datetime.strptime(date1,"%d/%m/%Y").timetuple())
    date2=time.mktime(datetime.datetime.strptime(date2,"%d/%m/%Y").timetuple())
    files=os.listdir(PATH_TO_CACHE+"programmes\\")
    dataset_attele=[]
    dataset_plat=[]

    #create dataset
    file_treated=0
    for f in files:  
        dfile = time.mktime(datetime.datetime.strptime(f.split('.')[0],"%d%m%Y").timetuple())
        if dfile>=date1 and dfile<date2:
            file_treated+=1
            print(f)
            races = recup_infos(f) #recup races info for each file
            for race in races: 
                arrive =race[-6]
                resultats= race[-5]
                specialite=race.pop()
                chevaux = []
                for cheval in arrive :
                    try : 
                        if cheval in arrive[6:10] :
                            chevaux.append(cheval)
                    except :
                        pass
                if specialite == "TROT_ATTELE" and (select_specialite=="all" or select_specialite=="attele"):
                    dataset_attele=dataset_attele+chevaux
                if specialite == "PLAT" and (select_specialite=="all" or select_specialite=="plat"):
                    dataset_plat=dataset_plat+chevaux
    fantomes={"PLAT" : dataset_plat,"TROT_ATTELE" : dataset_attele}
    with open(PATH_TO_DATASETS+"FANTOMES_"+dname+".json", "w") as json_file:
        json.dump(fantomes, json_file)
# generate_fantomes("1/7/2022","1/1/2023","fantomes_2nd_sem_2022_reduced",select_specialite="all")

    
