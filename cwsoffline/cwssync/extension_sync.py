import requests
import json
import os
from datetime import datetime
import schedule
import time
from bs4 import BeautifulSoup


class ChromeExtensionSync:
    def __init__(self):
        self.extensions_file = 'recommended_extensions.json'
        self.download_dir = 'downloads'
        self.chrome_store_url = 'https://clients2.google.com/service/update2/crx'
        
    def load_recommended_extensions(self):
        """Load recommended extensions from JSON file"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.extensions_file = os.path.join(script_dir, self.extensions_file)
        if os.path.exists(self.extensions_file):
            with open(self.extensions_file, 'r') as f:
                return json.load(f)
        return []
    
    def download_extension(self, ext_details):
        """Download extension from Chrome Web Store"""
        extension_name, version, extension_id = ext_details
        try:
            params = {
                'response': 'redirect',
                'nacl_arch': 'x86-64',
                'acceptformat': "crx2,crx3",
                'prodversion': '131.0.0.0',
                'x': f'id={extension_id}&installsource=ondemand&uc'
            }
            response = requests.get(self.chrome_store_url, params=params, stream=True)
            
            if response.status_code == 200:
                artifact_dir = os.path.join('artifacts','extensions', extension_id, version)
                if not os.path.exists(artifact_dir):
                    os.makedirs(artifact_dir)
                extension_name = extension_name.replace(' ', '-')
                file_path = os.path.join(artifact_dir, f'{extension_id}_{extension_name}_{version}.crx')
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"Successfully downloaded extension: {extension_id}")
                return True
            else:
                print(f"Failed to download extension {extension_id}: Status {response.status_code}")
                return False
        except Exception as e:
            print(f"Error downloading extension {extension_id}: {str(e)}")
            return False
    
    def sync_extensions(self):
        """Sync all recommended extensions"""
        print(f"Starting sync at {datetime.now()}")
        extensions = self.load_recommended_extensions()
        
        for ext in extensions:
            ext_details = self.get_extension_details(ext['id'])
            self.download_extension(ext_details)
            #self.download_extension(ext['id'])
        
        print(f"Sync completed at {datetime.now()}")
    def get_extension_details(self, extension_id):
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

def main():
    syncer = ChromeExtensionSync()
    
    # Run initial sync
    syncer.sync_extensions()
    
    # Schedule periodic sync (every 24 hours)
    schedule.every(24).hours.do(syncer.sync_extensions)
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()