from path import *
import json
import pandas as pd

def get_odds_ZETurf(id_course,num_pmu):
    try:
        if id_course.split('-')[0]=='15012024' and id_course.split('-')[1] == '5':
            id_course='15012024-5-'+str(int(id_course.split('-')[2])+2)
        rapport=json.loads(open(PATH_TO_CACHE+'ZETURF_rapports_prealable/'+id_course+'.json', "r").read())
    except :
        return -1,-1,-1
    odds = rapport[str(num_pmu)]["odds"]
    if isinstance(odds["SG"], bool): 
        return -1,-1,-1 
    return odds["SG"],odds["SPMin"],odds["SPMax"]

def extract_cotes_normal_online(idCourse, num_pmu, e_simple = False):
    if e_simple :
        e_simp = 'E_simple_'
    else : 
        e_simp = ''
    try:
        with open(PATH_TO_CACHE+e_simp+'rapports_prealable/'+idCourse+'.json', 'r') as f:
            raport = json.load(f)
    except : 
        return -1
    for participant in raport["rapportsParticipant"]:
        if participant["numPmu"] == num_pmu :
            return participant["rapportDirect"]
    return -1

def add_odds_ZETurf(file , intermediate_directory=''):
    df= pd.read_csv(PATH + intermediate_directory  +'/resultats/'+file+'.csv')
    df[['ZETURF_SG', 'ZETURF_SPMin', 'ZETURF_SPMax']] = df.apply(
        lambda row: get_odds_ZETurf(row["IDS_COURSES"], row["NUM_PMU"]), axis=1, result_type='expand'
    )
    df['COTES_PROBABLES'] = df.apply(
        lambda row: extract_cotes_normal_online(row["IDS_COURSES"], row["NUM_PMU"]), axis=1, result_type='expand'
    )
    df['E_COTES_PROBABLES'] = df.apply(
        lambda row: extract_cotes_normal_online(row["IDS_COURSES"], row["NUM_PMU"], e_simple= True ), axis=1, result_type='expand'
    )
    print(df.head())
    df.to_csv(PATH + intermediate_directory  +'/resultats/'+file+'.csv',index=False)

    