from bs4 import BeautifulSoup
import time
from lxml import etree
import requests
# from path import *
import os
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
saving_file = PATH_TO_DATASETS+"horse_parents.json"


Check if the file exists
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
    time.sleep(0.05)
    
    # Check if the request was successful
    try : 
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            # Find all the list items <li>
            horses = soup.find_all('li')
            # if not horses:
            #     horses_dict["not_found"].append(horse_name.replace(" ", "_"))
            #     return "-1" 
            # Iterate over the list items to extract the horse's name and link
            for horse in horses:

                print(type(horse))
                # soup = BeautifulSoup(str(horse), 'html.parser')
                print(horse.contents[1].get_text().split("\n"))
                horse_split = horse.contents[1].get_text().split("\n")[-2].split(" ")
                print(horse_split)
                if int(horse_split[-1])>= birth_year - 1 and int(horse_split[-1])<= birth_year + 1 and horse_split[-2] == genre: 
                    # print(horse)
                    # Find the anchor tag <a> within the <li>
                    link_tag = horse.find('a', class_='nom-cheval')
                    # Get the horse's name (text within <a>)
                    horse_name = link_tag.text.strip()
                    # Get the URL (href attribute of <a>)
                    horse_url = link_tag['href']
                    break
                
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            return "-1" 
    except : 
        return "-1" 
    return horse_url.split("/")[-1]


def get_horse_parents(horse_id):
    url = f"https://www.france-galop.com/fr/cheval/{horse_id}"
    response = requests.get(url, verify=False)
    time.sleep(0.05)
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

            
print(get_horse_parents(get_horse_id("epi de",1999,"H")))
def get_horse_result(id_horse):
    try:
        url = f"https://www.france-galop.com/fr/frglp-global/ajax?module=cheval_performances&id_cheval={id_horse}&specialty=4&year=%20&jockey=%20&proprietaire=%20&entraineur=%20&nbResult=50"
        response = requests.get(url, verify=False)
        time.sleep(0.05)
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
    for date in all_files:
        # print(date)
        if year==int(date[4:8]) and date not in horses_dict["files_treated"] :
            files.append(date) 
    print(len(files))

def get_info_horse(participant,year):
    horse_name=participant[""]
    birth_year=year-participant[""]
    genre=participant[""]
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
                if internl_id in horses_dict["Horses"].keys() or horse_name in horses_dict["not_found"]:       # If the horse is  in known horse or failed
                    already_in_file+=1                                                                         # count as in file
                else : 
                    current_horse_id = get_horse_id(horse_name,birth_year,genre)                               # We get horseID
                    if current_horse_id != "-1":                                                               # If we can get it 
                        parents_id = get_horse_parents(current_horse_id)                                       # we grab parents id 
                        horses_dict["Horses"][internl_id]=(current_horse_id,parents_id)
                    else : 
                        failed += 1
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
# get_horses_res(2024)
# get_horses_res(2023)
# get_horses_res(2022)
# get_horses_res(2021)
# get_horses_res(2020)
# get_horses_res(2019)


