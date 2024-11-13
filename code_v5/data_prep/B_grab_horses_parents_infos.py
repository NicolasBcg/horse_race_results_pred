import concurrent.futures
from tqdm import tqdm  # barre de progression pour suivre le traitement

from bs4 import BeautifulSoup
import time
from lxml import etree
import requests
from path import *
import os
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
saving_file = PATH_TO_DATASETS+"genealogy_parents.json"


# Check if the file exists
if os.path.exists(saving_file):
    # Open and read the file if it exists
    with open(saving_file, 'r') as file:
        horses_dict = json.load(file)
else:
    # Create the file with the specified structure if it does not exist
    horses_dict = {
        "Horses": {},# Name_Year_genre : id, [id_father, id_mother id_grand_pere_maternel]
        "parents": {}, #id : scores
        "not_found": [],
        "files_treated" : []
    }


def get_horse_id(horse_name,birth_year,genre):
    formated_horse_name = horse_name.replace(" ", "%20")
    url = f"https://www.france-galop.com/fr/horses-and-people/search-ajax?mot={formated_horse_name}&type=all"
    # Send a GET request to the URL
    response = requests.get(url, verify=False)
    time.sleep(0.003)
    found=False
    # Check if the request was successful
    try : 
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            # Find all the list items <li>
            horses = soup.find_all('li')
            if not horses:
                horses_dict["not_found"].append(horse_name+'_'+str(birth_year)+'_'+genre) #append internal id
                return "-1" 
            # Iterate over the list items to extract the horse's name and link
            for horse in horses:
                horse_split = horse.contents[1].get_text().split("\n")[-2].split(" ")

                if int(horse_split[-1])>= birth_year - 1 and int(horse_split[-1])<= birth_year + 1 and horse_split[-2] == genre: 
                    # Find the anchor tag <a> within the <li>
                    link_tag = horse.find('a', class_='nom-cheval')
                    # Get the horse's name (text within <a>)
                    horse_name = link_tag.text.strip()
                    # Get the URL (href attribute of <a>)
                    horse_url = link_tag['href']
                    found=True
                    break
                
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            return "-1" 
    except : 
        return "-1" 
    if found:
        return horse_url.split("/")[-1]
    else:
        horses_dict["not_found"].append(horse_name+'_'+str(birth_year)+'_'+genre) #append internal id
        return "-1" 


def get_horse_parents(horse_id):
    url = f"https://www.france-galop.com/fr/cheval/{horse_id}"
    response = requests.get(url, verify=False)
    time.sleep(0.001)
    # Check if the request was successful
    # try : 
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')  
        target_paragraphs = soup.find_all('p')
        for p in target_paragraphs:
            if p.find('span') and p.find('span').text == 'Par':
                # Find all <a> tags within this <p> tag
                links = p.find_all('a')
                ids = [str(link.get('href')).strip().split("/")[-1] for link in links]
                return ids
    return []

            
# print(get_horse_parents(get_horse_id("epi de",1999,"H")))
def get_horse_result(id_horse):
    try:
        url = f"https://www.france-galop.com/fr/frglp-global/ajax?module=cheval_performances&id_cheval={id_horse}&specialty=4&year=%20&jockey=%20&proprietaire=%20&entraineur=%20&nbResult=50"
        response = requests.get(url, verify=False)
        time.sleep(0.001)
        soup = BeautifulSoup(response.text, 'html.parser')
        td_elements = soup.find_all('td', class_='place')
        # Extract the text from the <span> within each <td>
        places = [td.find('span', class_='content_value').text for td in td_elements]

        td_elements = soup.find_all('td', class_='a-r', attrs={'data-label': 'Gains'})
        # Extract the text from each matching <td>
        gains = [td.text for td in td_elements]
        # Print the results
        return places,gains
    except:
        return ["-1"],[]



def calc_KPI(places,gains):
    res = [0,0,0,0,0,0]
    # print(places)
    for p in places: 
        # if p != 'TB' and p != 'AR' and p!='DB': 
        try:
            place = int(p)
        except:
            place=-1
        if place == 1 :
            res[0]+=1
        if place == 2 :
            res[1] +=1 
        if place == 3 :
            res[2] +=1
    res[3]=len(places)
    if gains != []:
        int_gains=[int(item.replace('.', '')) if item else 0 for item in gains]
        
        res[4]=max(int_gains)
        res[5]= sum(int_gains) / len(places)
    # print(res)
    return res

def get_files_to_treat(year):
    files = []
    all_files=os.listdir(PATH_TO_CACHE+"participants\\")
    print(len(all_files))
    for date in all_files:
        # print(date)
        if year==int(date[4:8]) and date not in horses_dict["files_treated"] :
            files.append(date) 
    print(len(files))
    return files

def get_info_horse(participant,year):
    horse_name=participant["nom"]
    birth_year=year-participant["age"]
    genre=participant["sexe"][0]
    # print(genre)
    internl_id=horse_name+'_'+str(birth_year)+'_'+genre
    return horse_name,birth_year,genre,internl_id

def get_horses_res(year):
    k=0
    already_in_file=0
    parent_already_in_file = 0
    downloaded=0
    failed=0
    files=get_files_to_treat(year)
    for f in files:
        k+=1
        if k%100==0:
            print ("------------------------------------------------------------------------------------------")
            print(f"!!!! k {k}: already_in_file {already_in_file} ; parents in file {parent_already_in_file} ; downloaded {downloaded} ; failed {failed} ; !!!!!!!!!")
            print ("------------------------------------------------------------------------------------------")
        with open(PATH_TO_CACHE+"participants\\"+f, 'r') as file:
            participants = json.loads(file.read())
        for participant in participants["participants"]:                                                       # For each participant
            if "nom" in participant.keys() and "age" in participant.keys() and "sexe" in participant.keys():   # If infos are available
                horse_name,birth_year,genre,internl_id = get_info_horse(participant,year)                           # We get them and generate an ID
                if internl_id in horses_dict["Horses"].keys() or internl_id in horses_dict["not_found"]:       # If the horse is  in known horse or failed
                    already_in_file+=1                                                                         # count as in file
                else : 
                    current_horse_id = get_horse_id(horse_name,birth_year,genre)                               # We get horseID
                    if current_horse_id == "-1":    
                        failed += 1  
                    else :                                                         # If we can get it 
                        parents_id = get_horse_parents(current_horse_id)                                       # we grab parents id 
                        horses_dict["Horses"][internl_id]=(current_horse_id,parents_id)
                    
                            
                        for parent_id in parents_id:                                                                # For each parent (to know if we do with mother's father later)        
                            if parent_id in horses_dict["parents"].keys():                                          # If the horse is  in known horse or failed
                                parent_already_in_file+=1                                                           # count as parent in file
                            else :
                                places,gains = get_horse_result(parent_id)                                          # grab parents results
                                if places != ["-1"] :                                                               # in case of success 
                                    horses_dict["parents"][parent_id]=calc_KPI(places,gains)                        # process results
                                    downloaded += 1     
                                    if downloaded % 50 == 0:                                                        # every 50 new download
                                        with open(saving_file, 'w') as file:                                        # save progress
                                            json.dump(horses_dict, file, indent=4)
                                            print(f"DOWNLOADING {downloaded}")
                                else:
                                    pass
        horses_dict["files_treated"].append(f)        

    with open(saving_file, 'w') as file:
            json.dump(horses_dict, file, indent=4)

def process_file_2(f, year, horses_dict_, downloaded, failed, already_in_file, parent_already_in_file):
    with open(PATH_TO_CACHE + "participants/" + f, 'r') as file_:
        participants = json.load(file_)

    for participant in participants["participants"]:
        if {"nom", "age", "sexe"} <= participant.keys():  # vérification simplifiée
            horse_name, birth_year, genre, internl_id = get_info_horse(participant, year)

            # Si le cheval est déjà dans le dictionnaire, on le saute
            if internl_id in horses_dict_["Horses"] or internl_id in horses_dict_["not_found"]:
                already_in_file += 1
                continue

            current_horse_id = get_horse_id(horse_name, birth_year, genre)
            if current_horse_id == "-1":
                failed += 1
            else:
                parents_id = get_horse_parents(current_horse_id)
                horses_dict_["Horses"][internl_id] = (current_horse_id, parents_id)

                for parent_id in parents_id:
                    if parent_id in horses_dict_["parents"]:
                        parent_already_in_file += 1
                    else:
                        places, gains = get_horse_result(parent_id)
                        if places != ["-1"]:
                            horses_dict_["parents"][parent_id] = calc_KPI(places, gains)
                            downloaded += 1
    return downloaded, failed, already_in_file, parent_already_in_file


def get_horses_res_2(year):
    # Initialisation des compteurs et du dictionnaire
    already_in_file, parent_already_in_file, downloaded, failed = 0, 0, 0, 0
    files = get_files_to_treat(year)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_file_2, f, year, horses_dict, downloaded, failed, already_in_file,
                                   parent_already_in_file) for f in files]

        # Utilisation de tqdm pour suivre la progression avec des informations complémentaires
        with tqdm(total=len(futures), desc="Traitement des fichiers") as pbar:
            for future in concurrent.futures.as_completed(futures):
                res = future.result()
                downloaded += res[0]
                failed += res[1]
                already_in_file += res[2]
                parent_already_in_file += res[3]

                # Mise à jour de la barre de progression avec les informations de comptage
                pbar.update(1)
                pbar.set_postfix(downloaded=downloaded, failed=failed, already_in_file=already_in_file,
                                 parent_in_file=parent_already_in_file)

    # Sauvegarde finale
    with open(saving_file, 'w') as file_save:
        json.dump(horses_dict, file_save)
    print("Final save completed.")


# get_horses_res(2024)
get_horses_res_2(2023)
# get_horses_res(2022)
# get_horses_res(2021)
# get_horses_res(2020)
# get_horses_res(2019)


