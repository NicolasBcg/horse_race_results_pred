from get_data import *
from path import *
from datetime import date, timedelta
from multiprocessing import Process
import time 

def daterange(start_date, end_date):
    dt_range=[]
    while start_date < end_date:
        dt_range.append(start_date.strftime("%d%m%Y"))
        start_date += timedelta(days=1)
    return dt_range

def recup_infos(date_to_get):
    with open(PATH_TO_CACHE+"programmes\\"+date_to_get+".json", 'r') as file:
        programme = json.loads(file.read())
    for reunion in programme["reunions"]:
        num_reunion = reunion['numOfficiel']
        for course in reunion['courses']:
            
            time.sleep(0.01)
            get_participants(date_to_get,str(num_reunion),str(course["numOrdre"]))
            time.sleep(0.01)
            get_prealable_rapports(date_to_get,str(num_reunion),str(course["numOrdre"]))
            get_prealable_rapports(date_to_get,str(num_reunion),str(course["numOrdre"]),e_paris=True)
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
    # build_dataset(date(2013, 6, 16), date(2023, 12, 31))
    print("Process n°0 Launched, Start date is 2013-04-01: End date is: 2023-12-31")
    # recup_all_data(date(2023, 4, 4), date(2023, 12, 31))
    process_list = [
        Process(target = recup_all_data, args=(date(2023, 1, 1), date(2023, 2, 1))),
        Process(target = recup_all_data, args=(date(2023, 2, 1), date(2023, 3, 1))),
        Process(target = recup_all_data, args=(date(2023, 3, 1), date(2023, 4, 1))),
        # Process(target = recup_all_data, args=(date(2024, 4, 1), date(2024, 5, 1))),
        # Process(target = recup_all_data, args=(date(2023, 5, 1), date(2023, 6, 1))),
        # Process(target = recup_all_data, args=(date(2023, 6, 1), date(2023, 7, 1))),#in e_paris cotes after 01072023 havent been goten
        # Process(target = recup_all_data, args=(date(2023, 7, 1), date(2023, 8, 1))),
        # Process(target = recup_all_data, args=(date(2023, 8, 1), date(2023, 9, 1))),
        # Process(target = recup_all_data, args=(date(2023, 9, 1), date(2023, 10, 1))),
        # Process(target = recup_all_data, args=(date(2023, 10, 1), date(2023, 11, 1))),
        # Process(target = recup_all_data, args=(date(2023, 11, 1), date(2023, 12, 1))),
        # Process(target = recup_all_data, args=(date(2023, 12, 1), date(2024, 1, 1))),

    ]
    for process in process_list:
        print("Lauched process")
        process.start()

    for process in process_list:
        process.join()
    get_programme("28022023")
    recup_infos("28022023")

if __name__ == "__main__":
    main()
