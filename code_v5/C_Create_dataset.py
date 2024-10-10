import json
import os
import pandas as pd
from path import *
import datetime
import time 
import random

random.seed(42)
NB_FANTOMES=25
FILE_FANTOME="new"

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
# with open(PATH_TO_DATASETS+"horse_parents.json", 'r') as f:
#     parents = json.load(f) 
# peres=parents["fathers"]
# meres=parents["mothers"]
with open(PATH_TO_DATASETS+"genealogy_parents.json", 'r') as f:
    genealogy = json.load(f) 
gen_tree = genealogy["Horses"]
gen_parents = ["parents"]
genealogy = {}

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
    ["eleveur_courses_m-6",0],
    ["eleveur_premier_m-6",0],
    ["eleveur_second_m-6",0],
    ["eleveur_troisieme_m-6",0],
    ["eleveur_non_arrive_m-6",0],
    ["eleveur_dernier_m-6",0],
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
    ["proprietaire_courses_m-6",0],
    ["proprietaire_premier_m-6",0],
    ["proprietaire_second_m-6",0],
    ["proprietaire_troisieme_m-6",0],
    ["proprietaire_non_arrive_m-6",0],
    ["proprietaire_dernier_m-6",0],
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
FEATURES_CHEVAL_PLAT=[
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


FEATURES_PARENTS = [
    ["Place1_pere"],
    ["Place2_pere"],
    ["Place3_pere"],
    ["Total_course_pere"],
    ["Gains_moyens_pere"],
    ["Gain_Max_pere"],
    ["Place1_mere"],
    ["Place2_mere"],
    ["Place3_mere"],
    ["Total_course_mere"],
    ["Gains_moyens_mere"],
    ["Gain_Max_mere"],
    ["Place1_Grand_pere"],
    ["Place2_Grand_pere"],
    ["Place3_Grand_pere"],
    ["Total_course_Grand_pere"],
    ["Gains_moyens_Grand_pere"],
    ["Gain_Max_Grand_pere"],
]

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
        last_month_div_6 = [div_time(date,-m) for m in range(6)]
        # last_month_div_6_18 = [div_time(date,-m) for m in range(7,18)]
        for key in resultats_eleveurs[eleveur].keys():
            if int(key)<int(year_semester):
                for i in range(NB_FEATURES_ELEVEUR):
                    res[i+NB_FEATURES_ELEVEUR]+=resultats_eleveurs[eleveur][key][i]
                if key in last_month_div_6:
                    for i in range(NB_FEATURES_ELEVEUR):
                        res[i]+=resultats_eleveurs[eleveur][key][i]
                # elif key in last_month_div_6_18:
                #     for i in range(NB_FEATURES_JOCKEY):
                #         res[i+NB_FEATURES_ELEVEUR]+=resultats_eleveurs[eleveur][key][i]
    return res
def get_FEATURES_PROPRIETAIRE(proprietaire,date):
    res=[0 for _ in range(len(FEATURES_PROPRIETAIRE))]
    if proprietaire in proprietaires:
        year_semester=div_time(date)
        last_month_div_6 = [div_time(date,-m) for m in range(6)]

        for key in resultats_proprietaires[proprietaire].keys():
            if int(key)<int(year_semester):
                for i in range(NB_FEATURES_PROPRIETAIRE):
                    res[i+NB_FEATURES_PROPRIETAIRE]+=resultats_proprietaires[proprietaire][key][i]
                if key in last_month_div_6:
                    for i in range(NB_FEATURES_PROPRIETAIRE):
                        res[i]+=resultats_proprietaires[proprietaire][key][i]

    return res
def get_features_parents(internal_id):
    if internal_id in gen_tree.keys():
        res_parents=[]
        horse_parents = gen_tree[internal_id][1]
        for parent in horse_parents:#[:2]:
            if parent in gen_parents.keys():
                res_parents=res_parents+gen_parents[parent]
            else :
                res_parents=res_parents+[-1 for _ in range(12)]
        return res_parents
    else :
        return [-1 for _ in range(18)]
        
def extract_cotes(raport):
    cotes=[0 for _ in range(raport["nbParticipants"])]
    for participant in raport["rapportsParticipant"]:
        cotes[participant["numPmu"]-1]=participant["rapportDirect"]
    return cotes


def create_feature_list(specialite,training=True):
    features=[]
    if specialite == "TROT_ATTELE":
        FEATURES_CHEVAL = FEATURES_CHEVAL_TROT_ATTELE
        FEATURES_CHEVAL_ALL = FEATURES_CHEVAL+FEATURES_JOCKEY+FEATURES_ELEVEUR+FEATURES_PROPRIETAIRE+FEATURES_MUSIQUE
    else : 
        FEATURES_CHEVAL = FEATURES_CHEVAL_PLAT
        FEATURES_CHEVAL_ALL = FEATURES_CHEVAL+FEATURES_JOCKEY+FEATURES_ELEVEUR+FEATURES_PROPRIETAIRE+FEATURES_MUSIQUE + FEATURES_PARENTS
    features_lists=[FEATURES_CHEVAL_ALL,FEATURES_REUNION,FEATURES_COURSE,FEATURES_CHEVAL_ALL]

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
        date_reu=reunion["dateReunion"]
        infos_reunion = extract_features(reunion,FEATURES_REUNION)
        for course in reunion['courses']:
            specialite=course["specialite"]
            
            if specialite == "TROT_ATTELE" :
                FEATURES_CHEVAL = FEATURES_CHEVAL_TROT_ATTELE
            else :
                FEATURES_CHEVAL = FEATURES_CHEVAL_PLAT
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
                        if "nom" in participant.keys():
                            horse_name = participant["nom"]
                        else: 
                            horse_name = "unknown"
                        if specialite == "TROT_ATTELE" :
                            chevaux.append(extract_features(participant,FEATURES_CHEVAL)+get_Features_jockey(jockey,date)+get_Features_eleveur(eleveur,date)+get_FEATURES_PROPRIETAIRE(proprietaire,date)+get_features_musique(musique))
                        else : 
                            chevaux.append(extract_features(participant,FEATURES_CHEVAL)+get_Features_jockey(jockey,date)+get_Features_eleveur(eleveur,date)+get_FEATURES_PROPRIETAIRE(proprietaire,date)+get_features_musique(musique)+get_features_parents(horse_name))

                    data_by_race.append(infos_reunion+info_course+[chevaux]+[ordreArrivee]+[idCourse]+[time_start]+[non_partants]+[specialite]+[date_reu])
    return data_by_race

def generate_rows_from_race(race,training=True,select_specialite="all"):
    date_reunion=race.pop()
    specialite=race.pop()
    non_partants = race.pop()
    time_course= race.pop()
    rows=[]
    if select_specialite=="all" or specialite == select_specialite:
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
                        cotes = extract_cotes(json.load(f))
                    with open(PATH_TO_CACHE+'E_simple_rapports_prealable/'+idCourse+'.json', 'r') as f:
                        e_cotes = extract_cotes(json.load(f))
                    course = [resultats]+[idCourse]+[nb_participants]+[cotes]+[time_course]+[non_partants]+[e_cotes]+[date_reunion]

                      
                except:
                    course = [resultats]+[idCourse]+[nb_participants]+[[-1 for _ in range(nb_participants)]]+[time_course]+[non_partants]+[[-1 for _ in range(nb_participants)]]+[date_reunion]
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
                    # print("here")
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
    dataset_spec={}
    course_spec={}
    #create dataset
    file_treated=0
    for f in files:  
        dfile = time.mktime(datetime.datetime.strptime(f.split('.')[0],"%d%m%Y").timetuple())
        if dfile>=date1 and dfile<date2:
            if ENV == "DEV":
                print(f)
            file_treated+=1
            races = recup_infos(f,training) #recup races info for each file
            for race in races: 
                specialite=race[-2]
                if specialite == select_specialite or select_specialite=="all" :
                    rows,specialite,course=generate_rows_from_race(race,training=training,select_specialite=select_specialite)
                    if specialite in dataset_spec.keys():
                        dataset_spec[specialite]=dataset_spec[specialite]+rows
                    else :
                        dataset_spec[specialite]=rows
                        course_spec[specialite]=[]
                    if not training:
                        course_spec[specialite].append(course)

  
  
    #Save every 20 and at the end
            if file_treated>30:
                print(file_treated)
                file_treated=0
                for spec in dataset_spec.keys():
                    tamporary_path = PATH_TO_CACHE+"datasets\\"+dname+"_"+spec+".csv"
                    if not os.path.exists(tamporary_path):
                        df = pd.DataFrame([], columns =create_feature_list(spec,training=training))
                        df.to_csv(tamporary_path, mode='w', index=False, header=True)

                    df = pd.DataFrame(dataset_spec[spec], columns =create_feature_list(spec,training=training))
                    df.to_csv(tamporary_path, mode='a', index=False, header=False)
                dataset_spec={}

    for spec in dataset_spec.keys():
        df = pd.DataFrame(dataset_spec[spec], columns =create_feature_list(spec,training=training))
        df.to_csv(PATH_TO_CACHE+"datasets\\"+dname+"_"+spec+".csv", mode='a', index=False, header=False)
    if not training:
        for spec in course_spec.keys():
            pd.DataFrame(course_spec[spec], columns =["resultats","idCourse","nbParticipants","cotes","heure_depart","non_partants","e_cotes","dateReunion"]).to_csv(PATH_TO_CACHE+"datasets\\"+dname+"_"+spec+"_res.csv", mode='w', index=False, header=True)


def generate_fantomes(date1,date2,dname):
    #init files and df
    date1=time.mktime(datetime.datetime.strptime(date1,"%d/%m/%Y").timetuple())
    date2=time.mktime(datetime.datetime.strptime(date2,"%d/%m/%Y").timetuple())
    files=os.listdir(PATH_TO_CACHE+"programmes\\")
    dataset_spec={}

    #create dataset
    file_treated=0
    for f in files:  
        dfile = time.mktime(datetime.datetime.strptime(f.split('.')[0],"%d%m%Y").timetuple())
        if dfile>=date1 and dfile<date2:
            file_treated+=1
            print(f)
            races = recup_infos(f) #recup races info for each file
            for race in races: 

                arrive =race[-7]
                resultats= race[-6]

                specialite=race[-2]
                chevaux = []
                for cheval in arrive :
                    try : 
                        if len(arrive)>8:
                            if cheval[0] in resultats[5:-3] :
                                chevaux.append(cheval)
                    except :
                        pass
                if specialite in dataset_spec.keys():
                        dataset_spec[specialite]=dataset_spec[specialite]+chevaux
                else :
                        dataset_spec[specialite]=chevaux
    for specialite in dataset_spec.keys():
        fantomes[specialite] = dataset_spec[specialite]
    
    with open(PATH_TO_DATASETS+"FANTOMES_"+dname+".json", "w") as json_file:
        json.dump(fantomes, json_file)
# generate_fantomes("1/7/2022","1/12/2022","new")

    
