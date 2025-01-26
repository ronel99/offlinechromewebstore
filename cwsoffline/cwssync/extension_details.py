import requests
from bs4 import BeautifulSoup

def get_extension_version(extension_id):
    url = f"https://chrome.google.com/webstore/detail/{extension_id}"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve the page, status code: {response.status_code}")
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the div containing the word "version"
    version_div = soup.find('div', string=lambda text: text and 'version' in text.lower())
    
    if version_div:
        # Get the next div element after the one containing the word "version"
        next_div = version_div.find_next('div')
        if next_div:
            return next_div.get_text(strip=True)
        else:
            raise ValueError("Could not find the div after the version-related div.")
    else:
        raise ValueError("Could not find a div containing the word 'version'.")

extension_id = 'dhdgffkkebhmkfjojejmpbldmpobfkfo'  # Replace with the extension ID
try:
    version = get_extension_version(extension_id)
    print(f"Extension Version: {version}")
except Exception as e:
    print(f"Error: {e}")
