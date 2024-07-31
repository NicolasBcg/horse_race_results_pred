import pandas as pd
import numpy as np
import pickle
from path import *
import matplotlib.pyplot as plt



# 0 : k
# 1 : ["IDS_COURSES"]
# 2 : ["NUM_PMU"] 
# 3 : ["PROBAS"]
# 4 : ["SIMPLE_GAGNANT"]
# 5 : ["E_SIMPLE_PLACE"]
# 6 : ["RES"]
def get_proba_cote(horse,bet_type):
    p=horse[3]
    r=horse[6]
    c_classic=round(horse[4],2)
    c_e=round(horse[5],2)
    c_max = max(c_classic,c_e)
    if bet_type=="max":
        c = c_max
    elif bet_type=="classic":
        c = c_classic
    elif bet_type=="e_paris":
        c = c_e
    else :
        c = -1 
    return p,c,r

def bet_on_trio(courses,seuilProba=0.13, bet_type="max"):
    paris=[0]
    paris_by_months=[[0] for _ in range(12)]
    u=0
    for course in courses:
        nbParticipants=len(course)
        month=(int(course[0][1][2:4]))-1
        p3,c3,r3=get_proba_cote(course[2],bet_type)
        r1=course[0][6]
        r2=course[1][6]
        p4=course[3][3]
        if p3-p4>seuilProba and nbParticipants > 7:# and p1-p4 < 0.04 :
            if c3!=-1 :
                paris.append(paris[-1] + c3 - 1 if 0 not in [r1,r2,r3]  else paris[-1] - 1)
                paris_by_months[month].append(paris_by_months[month][-1] + c3-1 if 0 not in [r1,r2,r3]  else paris_by_months[month][-1] - 1)
            else : 
                u+=1
    print("u="+str(u))     
    return paris,paris_by_months

def bet_on_couple(courses,seuilProba=0.13, bet_type="max"):
    paris=[0]
    paris_by_months=[[0] for _ in range(12)]
    u=0
    for course in courses:
        nbParticipants=len(course)
        month=(int(course[0][1][2:4]))-1
        p2,c2,r2=get_proba_cote(course[2],bet_type)
        r1=course[0][6]
        p3=course[3][3]
        if p2-p3>seuilProba :# and p1-p4 < 0.04 :
            if c2!=-1 :
                paris.append(paris[-1] + c2 - 1 if r1 in [1,2] and r2 in [1,2] else paris[-1] - 1)
                paris_by_months[month].append(paris_by_months[month][-1] + c2-1 if r1 in [1,2] and r2 in [1,2]  else paris_by_months[month][-1] - 1)
                # if r1 in [1,2] and r2 in [1,2]:
                #     print([r1,r2])
                #     print("course : "+course[0][1]+" gagnants : "+str(course[0][2])+"-"+str(course[1][2])+" cote : "+str(c2))
            else : 
                u+=1
    print("u="+str(u)) 
    return paris,paris_by_months
    
def bet_on_winner(courses,seuilProba=0.13, bet_type="max"):
    paris=[0]
    u=0
    total=0
    paris_by_months=[[0] for _ in range(12)]
    for course in courses:
        total+=1
        #print(course)
        #nbParticipants=len(course)
        month=(int(course[0][1][2:4]))-1
        p2=course[1][3]
        p1,c1,r1=get_proba_cote(course[0],bet_type)
        if c1==-1:
            u+=1
        elif p1-p2>seuilProba :#p1-p2>seuilProba-(nbParticipants/1000)+0.01 and p1*c1>seuilEV and nbParticipants>=12: # p1-p2>seuilProba-(nbParticipants/800)+0.0205 and p1*c1>seuilEV:
            paris.append(paris[-1] + c1 - 1 if r1 == 1  else paris[-1] - 1)
            paris_by_months[month].append(paris_by_months[month][-1] + c1 - 1 if r1 == 1 else paris_by_months[month][-1] - 1)
        # else :
        #     print(p1-p2)
    print("total ="+str(total))      
    print("u="+str(u))
    return paris,paris_by_months

def bet_on_place(courses,seuilProba=0.13, bet_type="max"):
    paris=[0]
    paris_by_months=[[0] for _ in range(12)]
    u=0
    for course in courses:
        nbParticipants=len(course)
        month=(int(course[0][1][2:4]))-1
        p2,c2,r2=get_proba_cote(course[1],bet_type)
        p1,c1,r1=get_proba_cote(course[0],bet_type)
        p4=course[3][3]
        if p1-p4>seuilProba and nbParticipants > 7:# and p1-p4 < 0.04 :
            if c1!=-1 :
                paris.append(paris[-1] + c1 - 1 if r1 !=0  else paris[-1] - 1)
                paris_by_months[month].append(paris_by_months[month][-1] + c1-1 if r1 != 0 else paris_by_months[month][-1] - 1)
            else : 
                u+=1
                # c1=(c1-1)/5 + 1
                # paris.append(paris[-1] + 0.05 if y_test.iloc[course[0][2]] !=0  else paris[-1] - 1)# + c1 - 1 if y_test.iloc[course[0][2]] !=0  else paris[-1] - 1)
                # paris_by_months[month].append(paris_by_months[month][-1] + 0.05 if y_test.iloc[course[0][2]] != 0 else paris_by_months[month][-1] - 1)

        if p2-p4>seuilProba*0.95 and nbParticipants > 7 :
            if c2!=-1 :
                paris.append(paris[-1] + c2 - 1 if r2 !=0  else paris[-1] - 1)
                paris_by_months[month].append(paris_by_months[month][-1] + c2-1 if r2 != 0 else paris_by_months[month][-1] - 1)
            else : 
                u+=1
                # c2=(c2-1)/5 + 1
                # paris.append(paris[-1] + 0.05 if y_test.iloc[course[1][2]] !=0  else paris[-1] - 1)# + c1 - 1 if y_test.iloc[course[0][2]] !=0  else paris[-1] - 1)
                # paris_by_months[month].append(paris_by_months[month][-1] + 0.05 if y_test.iloc[course[1][2]] != 0 else paris_by_months[month][-1] - 1)

    print("u="+str(u))
        
    return paris,paris_by_months


def sortHorses(horses):
    return sorted(horses, key=lambda x: x[3], reverse=True)


def splitCoursesv2(probs,ids_course,numeros_PMU,classique,e_paris,results):
    splited=[]
    lastId=0
    lastCourse=ids_course[0]
    for j in range(len(ids_course)):
        course=ids_course.iloc[j]
        if course != lastCourse:
            horses=[]
            for k in range(lastId,j):
                horses.append([k,ids_course.iloc[k],numeros_PMU.iloc[k],probs.iloc[k],classique.iloc[k],e_paris.iloc[k],results.iloc[k]]) #(df["PROBAS"],df["IDS_COURSES"],df["NUM_PMU"],df["SIMPLE_GAGNANT"],df["E_SIMPLE_PLACE"])
            splited.append(sortHorses(horses))
            lastId=j
            lastCourse=ids_course.iloc[j]
    horses=[]
    for k in range(lastId,len(ids_course)):
        horses.append([k,ids_course.iloc[k],numeros_PMU.iloc[k],probs.iloc[k],classique.iloc[k],e_paris.iloc[k],results.iloc[k]])
    splited.append(sortHorses(horses))
    return splited

def calcDrawbacks(paris):
    drawbacks=[0]
    paris_gagnants=0
    for i in range(1,len(paris)):
        if paris[i]<paris[i-1]:#si la somme suivante est inferieure
             drawbacks[len(drawbacks)-1]+=1#on grandit le drawback
        else :
             drawbacks.append(0)#sinon on crée un nouveau drawback
             paris_gagnants+=1
    return drawbacks,paris_gagnants

def calcDrawbacksPlus(paris):
    drawbacks=[0]
    max=0
    currentMin=0
    for i in range(1,len(paris)):
        if paris[i]<currentMin:#si la somme suivante est inferieure au min actuel
            currentMin = paris[i]
        elif paris[i]>max:
             drawbacks.append(max-currentMin)
             currentMin=max
             max=paris[i]
    return drawbacks



def calc_res(paris_version,paris_name,courses,seuilProba=0.15,bet_type="max"):
    print("---------")
    print("Seuil proba = "+str(seuilProba)+" "+paris_name+" bet_type = " +bet_type)
    paris, paris_par_mois=paris_version(courses,seuilProba=seuilProba,bet_type=bet_type)
    dr,nb_paris_gagnants=calcDrawbacks(paris)
    print("nb paris = "+str(len(paris)))
    print("Gagnants = "+str(nb_paris_gagnants))
    print("nb moyen de paris gagnants "+str(nb_paris_gagnants/len(paris)))
    print("Max drawback "+str(max(dr)))
    try:
        juste_dr = [element for element in dr if element != 0]
        print("Drawback moyen "+str(sum(juste_dr) / len(juste_dr)))
    except:
        print("Pas de drawback")

    print("Gains moyens "+str(paris[len(paris)-1]/len(paris)))
    print("Gains finaux "+str(paris[len(paris)-1]))
    print("Gains finaux par mois : "+str([int(paris_par_mois[p][len(paris_par_mois[p])-1]) for p in range(len(paris_par_mois))]))
    print("nombre paris par mois : "+str( [len(paris_par_mois[p])for p in range(len(paris_par_mois))]))
    print("nombre gagna par mois : "+str( [calcDrawbacks(paris_par_mois[p])[1] for p in range(len(paris_par_mois))]))


def test_paris(courses,resultats,types_paris=[]):
    print("Nb total de cheveaux "+str(len(resultats)))
    print("Nb total de cheveaux gagnants "+str((resultats == 1).sum()))
    p = [bet_on_winner,bet_on_place,bet_on_couple,bet_on_trio]
    pname = ["bet_on_winner","bet_on_place","bet_on_couple","bet_on_trio"]
    allParis=[]
    for seuilProb in  [0.0]:# [0.14,0.16,0.18]:#  [0.05,0.1]:#[0.15,0.16,0.18,0.2]: # [0.3,0.35,0.4,0.5]:# [0.15,0.2,0.25]: #   [0.15,0.2,0.25,0.3]: #
        for bet_type in ["max"]: #["max"]:#  ["max","classic","e_paris"]: # ["max"]:# ["max","classic","e_paris"]: #
            for pr in types_paris:
                paris = calc_res(p[pr],pname[pr],courses,seuilProba=seuilProb,bet_type=bet_type)
                allParis.append(paris)

# directory_encode="2021_2022_attele_reduced"
# with open(PATH+directory_encode+'/resultats_borda_trio_norm_20f_same_year_10_09_200.pkl', "rb") as f:

df=pd.read_csv(PATH + directory_encode + '/resultats_borda_norm.csv')
# courses= splitCoursesv2(df["PROBAS"],df["IDS_COURSES"],df["NUM_PMU"],df["SIMPLE_GAGNANT"],df["E_SIMPLE_GAGNANT"],df["RES"])
# test_paris(courses,df["RES"],[0])

# courses= splitCoursesv2(df["PROBAS"],df["IDS_COURSES"],df["NUM_PMU"],df["SIMPLE_PLACE"],df["E_SIMPLE_PLACE"],df["RES"])
# test_paris(courses,df["RES"],[1])


courses= splitCoursesv2(df["PROBAS"],df["IDS_COURSES"],df["NUM_PMU"],df["COUPLE_GAGNANT"],df["E_COUPLE_GAGNANT"],df["RES"])
test_paris(courses,df["RES"],[2])

# courses= splitCoursesv2(df["PROBAS"],df["IDS_COURSES"],df["NUM_PMU"],df["TRIO"],df["E_TRIO"],df["RES"])
# test_paris(courses,df["RES"],[3])
# 0 : ["PROBAS"]
# 1 : ["IDS_COURSES"] 
# 2 : ["NUM_PMU"]
# 3 : ["SIMPLE_GAGNANT"]
# 4 : ["E_SIMPLE_PLACE"]
# 5 : ["RES"]
