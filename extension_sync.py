import requests
import json
import os
from datetime import datetime
import schedule
import time

class ChromeExtensionSync:
    def __init__(self):
        self.extensions_file = 'recommended_extensions.json'
        self.download_dir = 'downloads'
        self.chrome_store_url = 'https://clients2.google.com/service/update2/crx'
        
    def load_recommended_extensions(self):
        """Load recommended extensions from JSON file"""
        if os.path.exists(self.extensions_file):
            with open(self.extensions_file, 'r') as f:
                return json.load(f)
        return []
    
    def download_extension(self, extension_id):
        """Download extension from Chrome Web Store"""
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
                if not os.path.exists(self.download_dir):
                    os.makedirs(self.download_dir)
                    
                file_path = os.path.join(self.download_dir, f'{extension_id}.crx')
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
            self.download_extension(ext['id'])
        
        print(f"Sync completed at {datetime.now()}")

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