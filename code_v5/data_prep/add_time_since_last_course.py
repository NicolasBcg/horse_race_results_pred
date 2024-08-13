from path import *
import os
import json
from datetime import datetime


K_horse=100
K_jockey=60
K_jockey2=10
K_horse2 = 30
D=10


dates=[date.split('.')[0] for date in os.listdir(PATH_TO_CACHE+"programmes\\")]
print("FILES :")
print(len(dates))
dates_sorted = sorted(dates, key=lambda date: datetime.strptime(date, '%d%m%Y'))
# Sort the dates after converting them to datetime objects
dates_sorted = sorted(dates, key=lambda date: datetime.strptime(date, '%d%m%Y'))

last_elos_path=PATH_TO_DATASETS+"last_elo_calculated"
# Check if the file exists
if os.path.exists(last_elos_path):
    # Open and read the file if it exists
    with open(last_elos_path, 'r') as file:
        last_elos = json.load(file)
        # Convert the last_file_calculated to a datetime object
        last_date = datetime.strptime(last_elos["last_file_calculated"].split('.')[0], '%d%m%Y')
        # Exclude each file before last_file_calculated and also exclude last_file_calculated
        filtered_dates = [date for date in dates_sorted if datetime.strptime(date, '%d%m%Y') > last_date]
        files = [date+".json" for date in filtered_dates]
else:
    # Create the file with the specified structure if it does not exist
    last_elos = {
        "last_file_calculated" : "",
        "elo_jockeys": {},
        "elo_horses": {},
        "elo_jockeys_v2": {},
        "elo_horses_v2" : {},
        "last_out_jockeys" : {},
        "last_out_horses" : {}
    }

    # Convert yyyymmdd format back to ddmmyyyy format
    files = [date+".json" for date in dates_sorted]

jockeys=last_elos["last_out_jockeys"].copy() # last out
updated_jockeys=last_elos["last_out_jockeys"].copy()

elo_jockeys=last_elos["elo_jockeys"].copy()
updated_elo_jockeys=last_elos["elo_jockeys"].copy()

elo_jockeys_v2=last_elos["elo_jockeys_v2"].copy()
updated_elo_jockeys_v2=last_elos["elo_jockeys_v2"].copy()

elo_horses=last_elos["elo_horses"].copy()
elo_horses_v2=last_elos["elo_horses_v2"].copy()

horses=last_elos["last_out_horses"].copy() #last out

print("init done")


def update_jockeys(participants,updated_jockeys,updated_elo_jockeys,updated_elo_jockeys_v2,time_course,ordreArrivee):
        jockey_racers=[]
        jockey_racers2=[]
        jockey_names=[]
        horse_racers=[]
        horse_racers2=[]
        horse_names=[]
        num_racers=[]
        for index, participant in enumerate(participants["participants"]):
            num_racers.append(participant["numPmu"])
            if "driver" in participant.keys():
                jockey=participant["driver"]
                if jockey in jockeys.keys():
                    participants["participants"][index]["driver_last_out"]=time_course-jockeys[jockey]
                if jockey in updated_jockeys.keys():
                    participants["participants"][index]["driver_last_course"]=time_course-updated_jockeys[jockey]
                updated_jockeys[jockey]=time_course

                if jockey in elo_jockeys.keys():
                    jockey_racers.append(elo_jockeys[jockey])
                    jockey_racers2.append(elo_jockeys_v2[jockey])
                    participants["participants"][index]["jockey_last_elo"]=elo_jockeys[jockey]
                    participants["participants"][index]["jockey_last_elo_v2"]=elo_jockeys_v2[jockey]
                else:
                    jockey_racers.append(1400)
                    jockey_racers2.append(1400)
                    participants["participants"][index]["jockey_last_elo"]= 1400
                    participants["participants"][index]["jockey_last_elo_v2"]=1400
                jockey_names.append(jockey)
            else:
                jockey_racers.append(1400)
                jockey_racers2.append(1400)
                jockey_names.append("none")

                
            if "nom" in participant.keys():
                horse=participant["nom"]
                if horse in horses.keys():
                    participants["participants"][index]["horse_last_out"]=time_course-horses[horse]    
                horses[horse]=time_course

                if horse in elo_horses.keys():
                    horse_racers.append(elo_horses[horse])
                    horse_racers2.append(elo_horses[horse])
                    participants["participants"][index]["horse_last_elo"]=elo_horses[horse]
                    participants["participants"][index]["horse_last_elo_v2"]=elo_horses_v2[horse]
                else:
                    horse_racers.append(1400)
                    horse_racers2.append(1400)
                    participants["participants"][index]["horse_last_elo"]= 1400
                    participants["participants"][index]["horse_last_elo_v2"]= 1400
                horse_names.append(horse)
            else:
                horse_racers.append(1400)
                horse_racers2.append(1400)
                horse_names.append("none")

        new_elos_horses=[]
        N=len(horse_racers)
        for index,elo_horse in enumerate(horse_racers):
            if num_racers[index] in ordreArrivee:
                for indice_arrive, num in enumerate(ordreArrivee):
                    if num_racers[index]==num:
                        p = indice_arrive+1
            else :
                p= len(ordreArrivee)+1
            Ex=0
            for index_i,elo_horse_i in enumerate(horse_racers):
                if index_i!=index:
                    Ex+=1/(1+pow(10,(elo_horse_i-elo_horse)/D))
            Ex=Ex*2/(N*(N-1))
            Sx=2*(N-p)/(N*(N-1))
            new_elos_horses.append(elo_horse + K_horse*(Sx-Ex))
        for name,new_elo in zip(horse_names,new_elos_horses):
            elo_horses[name]=new_elo

        new_elos_jockeys=[]
        N=len(jockey_racers)
        for index,elo_jockey in enumerate(jockey_racers):
            if num_racers[index] in ordreArrivee:
                for indice_arrive, num in enumerate(ordreArrivee):
                    if num_racers[index]==num:
                        p = indice_arrive+1
            else :
                p= len(ordreArrivee)+1
            Ex=0
            for index_i,elo_jockey_i in enumerate(jockey_racers):
                if index_i!=index:
                    Ex+=1/(1+pow(10,(elo_jockey_i-elo_jockey)/2))
            Ex=Ex*2/(N*(N-1))
            Sx=2*(N-p)/(N*(N-1))
            new_elos_jockeys.append(K_jockey*(Sx-Ex))
        for name,new_elo in zip(jockey_names,new_elos_jockeys):
            if name in updated_elo_jockeys.keys():
                updated_elo_jockeys[name]= updated_elo_jockeys[name]+new_elo
            else:
                updated_elo_jockeys[name]= 1400+new_elo

        new_elos_v2_horses=[0 for _ in horse_racers2]
        for index1,elo_horse1 in enumerate(horse_racers2):
            if num_racers[index1] in ordreArrivee:
                for indice_arrive, num in enumerate(ordreArrivee):
                    if num_racers[index1]==num:
                        p1 = indice_arrive+1
            else :
                p1= len(ordreArrivee)+1
            for index2,elo_horse2 in enumerate(horse_racers2):
                if num_racers[index1] != num_racers[index2]:
                    if num_racers[index2] in ordreArrivee:
                        for indice_arrive, num in enumerate(ordreArrivee):
                            if num_racers[index2]==num:
                                p2 = indice_arrive+1
                    else :
                        p2= len(ordreArrivee)+1

                    if p1 > p2 :
                        s1=1
                    elif p1 == p2 :
                        s1=0.5
                    else :
                        s1=0
                    e1= 1/(1+pow(10,elo_horse2-elo_horse1))
                    new_elos_v2_horses[index1] += K_horse2*(s1-e1)
        for name,new_elo in zip(horse_names,new_elos_v2_horses):
            if name in elo_horses_v2.keys():
                elo_horses_v2[name]= elo_horses_v2[name]+new_elo  
            else:
                elo_horses_v2[name]= 1400+new_elo

        new_elos_v2_jockeys=[0 for _ in jockey_racers2]
        for index1,elo_jockey1 in enumerate(jockey_racers2):
            if num_racers[index1] in ordreArrivee:
                for indice_arrive, num in enumerate(ordreArrivee):
                    if num_racers[index1]==num:
                        p1 = indice_arrive+1
            else :
                p1= len(ordreArrivee)+1
            for index2,elo_jockey2 in enumerate(jockey_racers2):
                if num_racers[index1] != num_racers[index2]:
                    if num_racers[index2] in ordreArrivee:
                        for indice_arrive, num in enumerate(ordreArrivee):
                            if num_racers[index2]==num:
                                p2 = indice_arrive+1
                    else :
                        p2= len(ordreArrivee)+1

                    if p1 > p2 :
                        s1=1
                    elif p1 == p2 :
                        s1=0.5
                    else :
                        s1=0
                    e1= 1/(1+pow(10,(elo_jockey2-elo_jockey1)/D))
                    new_elos_v2_jockeys[index1] += K_jockey2*(s1-e1)    
        for name,new_elo in zip(jockey_names,new_elos_v2_jockeys):
            if name in updated_elo_jockeys_v2.keys():
                updated_elo_jockeys_v2[name]= updated_elo_jockeys_v2[name]+new_elo   
            else:
                updated_elo_jockeys_v2[name]= 1400+new_elo

        return updated_jockeys,participants,updated_elo_jockeys,updated_elo_jockeys_v2
                

k=0
for f in files:
    k+=1
    if k%100==0:
        print(k)
    with open(PATH_TO_CACHE+"programmes\\"+f, 'r') as file:
        programme = json.loads(file.read())
    date=f.split('.')[0]
    year_semester=div_time(date)
    with open(PATH_TO_CACHE+"programmes\\"+f, 'r') as file:
        programme = json.loads(file.read())
    for reunion in programme["reunions"]:
        num_reunion = reunion['numOfficiel']
        for course in reunion['courses']:
            time_course=course["heureDepart"]/(1000)
            if "ordreArrivee" in course.keys(): 
                ordreArrivee = [i[0] for i in course["ordreArrivee"]]
                file_opened=True
                try:
                    with open(PATH_TO_CACHE+"participants\\"+date+'-'+str(num_reunion)+'-'+str(course["numOrdre"])+'.json', 'r') as file:
                        participants = json.loads(file.read())
                except:
                    file_opened=False
                    print(PATH_TO_CACHE+"participants\\"+date+'-'+str(num_reunion)+'-'+str(course["numOrdre"])+'.json')
                #print(PATH_TO_CACHE+"participants\\"+date+'-'+str(num_reunion)+'-'+str(course["numOrdre"])+'.json')
                if file_opened:
                    updated_jockeys,updated_participants,updated_elo_jockeys,updated_elo_jockeys_v2=update_jockeys(participants,updated_jockeys,updated_elo_jockeys,updated_elo_jockeys_v2,time_course,ordreArrivee)
                    with open(PATH_TO_CACHE+"participants\\"+date+'-'+str(num_reunion)+'-'+str(course["numOrdre"])+'.json', 'w') as file:
                        json.dump(updated_participants, file)
        jockeys = updated_jockeys.copy()
        elo_jockeys = updated_elo_jockeys.copy()
        elo_jockeys_v2=updated_elo_jockeys_v2.copy()

last_elos["last_out_jockeys"] = jockeys # last out
last_elos["elo_jockeys"] = elo_jockeys
last_elos["elo_jockeys_v2"] = elo_jockeys_v2
last_elos["elo_horses"] = elo_horses
last_elos["elo_horses_v2"] = elo_horses_v2
last_elos["last_out_horses"] = horses #last out

last_elos["last_file_calculated"] = f
json.dump(last_elos, last_elos_path)