from bs4 import BeautifulSoup
from lxml import etree
import requests

file_path = "C:/Users/NicolasBocage/Documents/projet/test/code_v5/data_prep/Exemple_html_extract_performances.xml"  # Replace with the path to your file
horse_name = "LOOK DE VEGA"
formated_horse_name = horse_name.replace(" ", "%20")
url = f"https://www.france-galop.com/fr/horses-and-people/search-ajax?mot={formated_horse_name}&type=all"

# Send a GET request to the URL
response = requests.get(url, verify=False)
# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find all the list items <li>
    horses = soup.find_all('li')
    # Iterate over the list items to extract the horse's name and link
    for horse in horses:
        # Find the anchor tag <a> within the <li>
        link_tag = horse.find('a', class_='nom-cheval')
        # Get the horse's name (text within <a>)
        horse_name = link_tag.text.strip()
        # Get the URL (href attribute of <a>)
        horse_url = link_tag['href']
        # Print the horse name and full URL
        print(f"Horse Name: {horse_name}")
        print(f"URL: https://www.france-galop.com{horse_url}")
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")

id_cheval = horse_url.split("/")[-1]
url = f"https://www.france-galop.com/fr/frglp-global/ajax?module=cheval_performances&id_cheval={id_cheval}&specialty=4&year=%20&jockey=%20&proprietaire=%20&entraineur=%20&nbResult=40"
response = requests.get(url, verify=False)
# # Load the XML file
# with open(file_path, 'r', encoding='utf-8') as file:
#     soup = BeautifulSoup(file, 'lxml')
soup = BeautifulSoup(response.text, 'html.parser')
td_elements = soup.find_all('td', class_='place')
# Extract the text from the <span> within each <td>
places = [td.find('span', class_='content_value').text for td in td_elements]

td_elements = soup.find_all('td', class_='a-r', attrs={'data-label': 'Gains'})
# Extract the text from each matching <td>
gains = [td.text for td in td_elements]
# Print the results
print(places)
print(gains)