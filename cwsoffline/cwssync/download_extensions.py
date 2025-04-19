import os
import requests

class ChromeExtensionDownloader:
    def __init__(self, output_dir="downloads"):
        self.chrome_store_url = "https://clients2.google.com/service/update2/crx"
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def download_extension(self, extension_id, version="latest"):
        """
        Downloads a Chrome extension by its ID.
        :param extension_id: The ID of the Chrome extension.
        :param version: The version of the extension (default is "latest").
        """
        params = {
            "response": "redirect",
            "prodversion": "131.0.0.0",  # Replace with the latest Chrome version if needed
            "acceptformat": "crx2,crx3",
            "x": f"id={extension_id}&installsource=ondemand&uc"
        }

        try:
            response = requests.get(self.chrome_store_url, params=params, stream=True)
            if response.status_code == 200:
                file_path = os.path.join(self.output_dir, f"{extension_id}.crx")
                with open(file_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"Successfully downloaded: {file_path}")
                return file_path
            else:
                print(f"Failed to download extension {extension_id}: HTTP {response.status_code}")
        except Exception as e:
            print(f"Error downloading extension {extension_id}: {e}")

    def download_extensions_from_list(self, extension_ids):
        """
        Downloads multiple extensions from a list of IDs.
        :param extension_ids: A list of Chrome extension IDs.
        """
        for extension_id in extension_ids:
            self.download_extension(extension_id)

if __name__ == "__main__":
    downloader = ChromeExtensionDownloader(output_dir="artifacts/extensions")
    # Replace with the list of extension IDs you want to download
    extension_ids = [
        "dhdgffkkebhmkfjojejmpbldmpobfkfo",  # Example: Tampermonkey
        "aapbdbdomjkkjkaonfhkkikfgjllcleb"   # Example: Google Translate
    ]
    downloader.download_extensions_from_list(extension_ids)