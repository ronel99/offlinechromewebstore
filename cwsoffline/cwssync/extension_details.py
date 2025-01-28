import requests
from bs4 import BeautifulSoup

def get_extension_details(extension_id):
    url = f"https://chrome.google.com/webstore/detail/{extension_id}"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve the page, status code: {response.status_code}")
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    ans = None
    # Find the div containing the word "version"
    version_div = soup.find('div', string=lambda text: text and 'version' in text.lower())
    name_div = soup.find('h1', string=lambda text: text).get_text(strip=True)
    if version_div:
        # Get the next div element after the one containing the word "version"
        next_div = version_div.find_next('div')
        if next_div:
            return name_div, next_div.get_text(strip=True), extension_id
        else:
            raise ValueError("Could not find the div after the version-related div.")
    else:
        raise ValueError("Could not find a div containing the word 'version'.")

extension_ids = [
    'dhdgffkkebhmkfjojejmpbldmpobfkfo',
    'ejcfepkfckglbgocfkanmcdngdijcgld'
    ]
    # Replace with the extension ID
try:
    for id in extension_ids:
        extension_details = get_extension_details(id)
        print(extension_details)
        #print(f"Extension Id: {id}, Extension Version: {version}")
except Exception as e:
    print(f"Error: {e}")
