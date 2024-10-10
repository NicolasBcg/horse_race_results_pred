
from itertools import repeat
import os
import json
import requests
import numpy as np
from path import *
from datetime import date, timedelta
from multiprocessing import Process
import time 
from bs4 import BeautifulSoup

def get_programme(date, use_cache=True):
    URL = "https://tablette.turfinfo.api.pmu.fr/rest/client/1/programme/{}".format(date)
    FILE = "{}cache/programmes/{}.json".format(PATH, date)
    if use_cache:
        if os.path.exists(FILE):
            print("Programme {} found in cache".format(date))
            return json.loads(open(FILE, "r").read())
    # print("Downloading programme {}".format(date))
    try:
        result = requests.get(URL)
        time.sleep(0.02)
    except Exception as e:
        print("Cannot download programme {}, retrying...".format(date))
        print(e)
        time.sleep(0.5)
        return get_programme(date)
    try:
        result_json = json.loads(result.text.replace("\r\n", ""))
        if not "programme" in result_json:
            print("Cannot download programme {}".format(date))
            return -1
        with open(FILE, "w+") as file:
            file.write(json.dumps(result_json["programme"]))
        return result_json["programme"]
    except Exception as e:
        # print("Cannot download programme {}".format(date))
        print(e)
        return -1

def get_participants(date, reunion, course, use_cache=True):
    URL = "https://tablette.turfinfo.api.pmu.fr/rest/client/1/programme/{}/R{}/C{}/participants".format(
        date, reunion, course
    )
    FILE = "{}cache/participants/{}.json".format(
        PATH, "{}-{}-{}".format(date, reunion, course)
    )
    if use_cache:
        if os.path.exists(FILE):
            return json.loads(open(FILE, "r").read())
    # print("Downloading race {} R{} C{}".format(date, reunion, course))
    try:
        result = requests.get(URL)
        time.sleep(0.1)
    except:
        print("Cannot download participants {} R{}C{}, retyring...".format(date, reunion, course))
        time.sleep(0.1)
        return get_participants(date, reunion, course)
    try:
        result_json = json.loads(result.text)
        if not "participants" in result_json:
            print( "Wrong format: Cannot download {} R{}C{}".format(date, reunion, course))
            return -1
        with open(FILE, "w+") as file:
            file.write(json.dumps(result_json))
        return result_json
    except Exception as e:
        #print("Cannot download {} R{}C{}".format(date, reunion, course))
        print(e)
        return -1

def get_course(date, reunion, course, use_cache=True):
    FILE = "{}cache/courses/{}.json".format(
        PATH, "{}-{}-{}".format(date, reunion, course)
    )
    if use_cache:
        if os.path.exists(FILE):
            return json.loads(open(FILE, "r").read())
    programme = get_programme(date, use_cache)
    if programme == -1:
        return -1
    participants = get_participants(date, reunion, course, use_cache)
    if participants == -1:
        return -1
    try:
        participants = participants["participants"]
        course_obj = programme["reunions"][reunion - 1]["courses"][course - 1]
        finish = course_obj["arriveeDefinitive"]
        result = {"finish": finish, "horses": participants}
        if finish:
            finishOrder = list(
                np.array(course_obj["ordreArrivee"], dtype=np.int32).flatten()
            )
            result["result"] = course_obj["ordreArrivee"]
        with open(FILE, "w+") as file:
            file.write(json.dumps(result))
        return result
    except:
        return -1




def get_rapports(date, reunion, course, use_cache=True):
    URL = "https://tablette.turfinfo.api.pmu.fr/rest/client/1/programme/{}/R{}/C{}/rapports-definitifs?specialisation=TOUT".format(
        date, reunion, course
    )
    FILE = "{}cache/rapports/{}.json".format(
        PATH, "{}-{}-{}".format(date, reunion, course)
    )

    if use_cache:
        if os.path.exists(FILE):
            
            return json.loads(open(FILE, "r").read())
        elif use_cache == "Only":
            return -1
    try:
        result = requests.get(URL)
    except:
        time.sleep(0.1)
        print("Cannot download rapport {} R{}C{}, retyring...".format(date, reunion, course))
        return get_rapports(date, reunion, course)
    try:
        result_json = json.loads(result.text)
        if "service" in result_json:
            print("Something went wrong with the request: Cannot download {} R{}C{}".format(date, reunion, course))
            return -1
        with open(FILE, "w+") as file:
            file.write(json.dumps(result_json))
        return result_json
    except Exception as e:
        #print("Cannot download {} R{}C{}".format(date, reunion, course))
        # print(e)
        return -1

def get_prealable_rapports(date, reunion, course, use_cache=True, type_paris='',hippodrome=''):
    if type_paris=='' : 
        URL = "https://online.turfinfo.api.pmu.fr/rest/client/61/programme/{}/R{}/C{}/rapports/SIMPLE_GAGNANT".format(
            date, reunion, course
        )
    elif type_paris == 'E_simple_' : 
        URL = "https://online.turfinfo.api.pmu.fr/rest/client/61/programme/{}/R{}/C{}/rapports/E_SIMPLE_GAGNANT".format(
            date, reunion, course
        )
    elif type_paris == 'ZETURF_':
        URL = "https://www.zeturf.fr/fr/course/{}/R{}C{}-*/api/cotes".format(
            f"{date[4:]}-{date[2:4]}-{date[:2]}", reunion, course
        )
        URL_bis = "https://www.zeturf.fr/fr/course/{}/R{}C{}-*".format(
            f"{date[4:]}-{date[2:4]}-{date[:2]}", reunion, course
        )


    FILE = ("{}cache/{}rapports_prealable/{}.json").format(
        PATH,type_paris ,"{}-{}-{}".format(date, reunion, course)
    )


    if use_cache:
        if os.path.exists(FILE):
            return json.loads(open(FILE, "r").read())
        elif use_cache == "Only":
            return -1
    try:

        if type_paris == 'ZETURF_':
            result2 = requests.get(URL_bis)
            # Parse the HTML content
            soup = BeautifulSoup(result2.text, 'html.parser')
            # Extract the title
            title = soup.title.string
            hippo = title.split("-")[1].split(" ")[1]
            if hippodrome == "LA CEPIERE":
                hippodrome = "TOULOUSE"
            elif hippodrome == "LE BOUSCAT" :
                hippodrome = "BORDEAUX"
            elif hippodrome == "PONT DE VIVAUX" :
                hippodrome = "MARSEILLE"
            elif hippodrome == "KRIEAU (VIENNE)" :
                hippodrome = "VIENNE"
            elif hippodrome == "ParisLongchamp" :
                hippodrome = "PARIS"
            elif hippodrome == "BORELY" :
                hippodrome = "MARSEILLE" 
            elif hippodrome == "MARIENDORF" :
                hippodrome = "BERLIN" 

            hip=hippodrome.split(" ")[0].split("/")[0].split("-")[0]

            if hippo != hip:
                print(f"fail to match {hippo} and {hip}\n     {URL_bis}")
                return -1
        result = requests.get(URL)
    except:
        print("Cannot download rapports_prealable {} R{}C{}, retyring...".format(date, reunion, course))
        time.sleep(0.1)
        return get_rapports(date, reunion, course)
    try:
        result_json = json.loads(result.text)
        if "service" in result_json:
            print("Something went wrong with the request: Cannot download {} R{}C{}".format(date, reunion, course))

            return -1
        with open(FILE, "w+") as file:
            file.write(json.dumps(result_json))
            print(FILE+ "  created ")
        return result_json
    except Exception as e:
        # print("Cannot download {} R{}C{}".format(date, reunion, course))
        # print(e)
        return -1


def daterange(start_date, end_date):
    dt_range=[]
    while start_date < end_date:
        dt_range.append(start_date.strftime("%d%m%Y"))
        start_date += timedelta(days=1)
    return dt_range

def recup_infos(date_to_get):
    with open(PATH_TO_CACHE+"programmes/"+date_to_get+".json", 'r') as file:
        programme = json.loads(file.read())
    for reunion in programme["reunions"]:
        hippodrome = reunion["hippodrome"]["libelleCourt"]
        num_reunion = reunion['numOfficiel']
        for course in reunion['courses']:
            
            time.sleep(0.02)
            get_participants(date_to_get,str(num_reunion),str(course["numOrdre"]))
            time.sleep(0.02)
            get_prealable_rapports(date_to_get,str(num_reunion),str(course["numOrdre"]))
            get_prealable_rapports(date_to_get,str(num_reunion),str(course["numOrdre"]),type_paris="E_simple_")
            get_prealable_rapports(date_to_get,str(num_reunion),str(course["numOrdre"]),type_paris="ZETURF_",hippodrome=hippodrome)
            get_rapports(date_to_get,str(num_reunion),str(course["numOrdre"]))


    return 1


def recup_all_data(start_date, end_date):
    date_range = daterange(start_date, end_date)
    for date_to_get in date_range:
        
        get_programme(date_to_get, use_cache=True)
        # Recup races
        recup_infos(date_to_get)
        print(date_to_get)
        time.sleep(1)


def main():
    # build_dataset(date(2013, 6, 16), date(2024, 12, 31))
    print("Process n°0 Launched, Start date is 2013-04-01: End date is: 2024-12-31")
    # recup_all_data(date(2024, 4, 4), date(2024, 12, 31))
    process_list = [
        # Process(target = recup_all_data, args=(date(2024, 1, 1), date(2024, 2, 1))),
        # Process(target = recup_all_data, args=(date(2024, 2, 1), date(2024, 3, 1))),
        # Process(target = recup_all_data, args=(date(2024, 3, 1), date(2024, 4, 1))),
        # Process(target = recup_all_data, args=(date(2024, 4, 1), date(2024, 5, 1))),
        # Process(target = recup_all_data, args=(date(2024, 5, 1), date(2024, 6, 1))),
        # Process(target = recup_all_data, args=(date(2024, 6, 1), date(2024, 7, 1))),#in e_paris cotes after 01072024 havent been goten
        Process(target = recup_all_data, args=(date(2024, 7, 1), date(2024, 8, 1))),
        Process(target = recup_all_data, args=(date(2024, 8, 1), date(2024, 9, 1))),
        # Process(target = recup_all_data, args=(date(2024, 9, 1), date(2024, 10, 1))),
        # Process(target = recup_all_data, args=(date(2024, 10, 1), date(2024, 11, 1))),
        # Process(target = recup_all_data, args=(date(2024, 11, 1), date(2024, 12, 1))),
        # Process(target = recup_all_data, args=(date(2024, 12, 1), date(2024, 1, 1))),
    ]
    for process in process_list:
        print("Lauched process")
        process.start()

    for process in process_list:
        process.join()
    print("done")

if __name__ == "__main__":
    main()