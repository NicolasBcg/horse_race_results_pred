from path import *
import os
import json

FEATURES_ELEVEUR = [
    ["nb_courses",0],
    ["nb_premier",0],
    ["nb_second",0],
    ["nb_troisieme",0],
    ["nb_non_arrive",0],
    ["nb_dernier",0]
]

eleveurs={} #eleveur->year_semester-> nb courses, pl 1er, pl 2eme, pl 3eme, non_arrive,dernier
files=os.listdir(PATH_TO_CACHE+"programmes\\")
print("FILES :")
print(len(files))
def update_eleveurs(participants,ordreArrivee):
                for participant in participants["participants"]:
                    if "eleveur" in participant.keys():
                        eleveur=participant["eleveur"]
                        num_PMU=participant["numPmu"]
                        if eleveur in eleveurs.keys():
                            if year_semester not in eleveurs[eleveur].keys():
                                eleveurs[eleveur][year_semester]=[0,0,0,0,0,0]
                        else : 
                            eleveurs[eleveur]= {}
                            eleveurs[eleveur][year_semester]=[0,0,0,0,0,0]
                        eleveurs[eleveur][year_semester][0]+=1
                        if num_PMU not in ordreArrivee:
                            eleveurs[eleveur][year_semester][4]+=1
                        elif num_PMU == ordreArrivee[0]:
                            eleveurs[eleveur][year_semester][1]+=1
                        elif num_PMU == ordreArrivee[1]:
                            eleveurs[eleveur][year_semester][2]+=1
                        elif num_PMU == ordreArrivee[2]:
                            eleveurs[eleveur][year_semester][3]+=1
                        elif num_PMU == ordreArrivee[-1]:
                            eleveurs[eleveur][year_semester][5]+=1



k=0
for f in files:
    k+=1
    if k%100==0:
        print(k)
    date=f.split('.')[0]
    year_semester=div_time(date)
    with open(PATH_TO_CACHE+"programmes\\"+f, 'r') as file:
        programme = json.loads(file.read())
    for reunion in programme["reunions"]:
        num_reunion = reunion['numOfficiel']
        for course in reunion['courses']:
            if "ordreArrivee" in course.keys():
                ordreArrivee = [i[0] for i in course["ordreArrivee"]]
                try:
                    with open(PATH_TO_CACHE+"participants\\"+date+'-'+str(num_reunion)+'-'+str(course["numOrdre"])+'.json', 'r') as file:
                        participants = json.loads(file.read())
                    #print(PATH_TO_CACHE+"participants\\"+date+'-'+str(num_reunion)+'-'+str(course["numOrdre"])+'.json')
                    update_eleveurs(participants,ordreArrivee)
                except :
                    print(PATH_TO_CACHE+"participants\\"+date+'-'+str(num_reunion)+'-'+str(course["numOrdre"])+'.json')

with open(PATH_TO_DATASETS+"eleveurs.json", "w") as json_file:
    json.dump(eleveurs, json_file)
