import requests
import json
import sys
import platform
from packaging import version


def get_latest_chrome_version():
    """
    Fetches the latest stable version of Chrome browser from Google's version API.
    Returns the version number as a string.
    """
    try:
        # Google's Chrome version API endpoint
        url = "https://versionhistory.googleapis.com/v1/chrome/platforms/linux/channels/stable/versions"
        
        # Send GET request to the API
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Parse the JSON response
        data = response.json()
        
        # Extract version numbers and sort them
        versions = []
        for version_data in data.get('versions', []):
            version_number = version_data.get('version')
            if version_number:
                versions.append(version_number)
        
        # Sort versions using packaging.version for proper version comparison
        sorted_versions = sorted(versions, key=lambda x: version.parse(x), reverse=True)
        
        if not sorted_versions:
            raise ValueError("No Chrome versions found in the API response")
            
        return sorted_versions[0]
    
    except requests.RequestException as e:
        print(f"Error fetching Chrome version: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing API response: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def main():
    latest_version = get_latest_chrome_version()
    
    if latest_version:
        print(f"\nLatest stable Chrome version: {latest_version}")
    else:
        print("Failed to fetch the latest Chrome version.")

if __name__ == "__main__":
    main()
    