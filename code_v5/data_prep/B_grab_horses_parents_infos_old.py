from bs4 import BeautifulSoup
import time
from lxml import etree
import requests
from path import *
import os
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
saving_file = PATH_TO_DATASETS+"horse_parents.json"
all_files=os.listdir(PATH_TO_CACHE+"participants\\")

# Check if the file exists
if os.path.exists(saving_file):
    print("exists")
    # Open and read the file if it exists
    with open(saving_file, 'r') as file:
        horses_dict = json.load(file)
else:
    # Create the file with the specified structure if it does not exist
    horses_dict = {
        "mothers": {},
        "fathers": {},
        "failed": [],
        "files_treated" : []
    }


def get_horse_id(horse_name):
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
            if not horses:
                horses_dict["failed"].append(horse_name.replace(" ", "_"))
                return "-1" 
            # Iterate over the list items to extract the horse's name and link
            horse = horses[0]
            # print(horse)
            # Find the anchor tag <a> within the <li>
            link_tag = horse.find('a', class_='nom-cheval')
            # Get the horse's name (text within <a>)
            horse_name = link_tag.text.strip()
            # Get the URL (href attribute of <a>)
            horse_url = link_tag['href']
                
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            return "-1" 
    except : 
        return "-1" 
    return horse_url.split("/")[-1]

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


def get_horses_res(year):
    k=0
    already_in_file=0
    downloaded=0
    failed=0
    print(len(all_files))
    files=[]
    for date in all_files:
        # print(date)
        if year==int(date[4:8]) and date not in horses_dict["files_treated"] :
            files.append(date) 
    print(len(files))
    for f in files:
        k+=1
        if k%100==0:
            print ("------------------------------------------------------------------------------------------")
            print(f"!!!! k {k}: already_in_file {already_in_file} ; downloaded {downloaded} ; failed {failed} ; !!!!!!!!!")
            print ("------------------------------------------------------------------------------------------")
        with open(PATH_TO_CACHE+"participants\\"+f, 'r') as file:
            participants = json.loads(file.read())
        for participant in participants["participants"]:
            if "nomMere" in participant.keys():
                mother_name= participant["nomMere"]
            if "nomPere" in participant.keys():   
                father_name= participant["nomPere"]
            # print(f" mere : {mother_name} pere : {father_name}")
            for horse_name,mother_or_father in zip([mother_name,father_name],["mothers","fathers"]):    
                # print(horses_dict)
                # print(horse_name)
                if horse_name in horses_dict[mother_or_father].keys() or str(horse_name).replace(" ", "_") in horses_dict["failed"]:
                    already_in_file+=1
                    # print("IN FILE")
                else :
                    id_horse = get_horse_id(horse_name)
                    if id_horse == "-1":
                        failed+=1
                        # print("FAILED ID")
                    else : 
                        places,gains = get_horse_result(id_horse)
                        if places != ["-1"] :
                            
                            horses_dict[mother_or_father][horse_name]=calc_KPI(places,gains)
                            downloaded += 1 
                            if downloaded % 50 == 0: 
                                with open(saving_file, 'w') as file:
                                    json.dump(horses_dict, file, indent=4)
                                    print(f"DOWNLOADING {downloaded}")
                        else:
                            # print("FAILED PLACES")
                            pass
        horses_dict["files_treated"].append(f)        
    
    with open(saving_file, 'w') as file:
            json.dump(horses_dict, file, indent=4)
get_horses_res(2024)
# get_horses_res(2023)
# get_horses_res(2022)
# get_horses_res(2021)
# get_horses_res(2020)
# get_horses_res(2019)


