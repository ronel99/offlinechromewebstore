import os
import requests

# Get API key from environment variable
api_key = os.getenv('EXTENSIONTOTAL_API_KEY')

if not api_key:
    raise ValueError("API key not found! Please set EXTENSIONTOTAL_API_KEY in your environment variables.")

# Chrome extension ID (replace with the one you want to check)
extension_id = 'gighmmpiobklfepjocnamgkkbiglidom'

# API endpoint
url = 'https://app.extensiontotal.com/api/getExtensionRisk'

# Headers with API Key
headers = {
    'Content-Type': 'application/json',
    'X-API-Key': api_key
}

# Payload with extension ID
payload = {
    'q': extension_id
}

# Send API request
response = requests.post(url, json=payload, headers=headers)

# Process response
if response.status_code == 200:
    data = response.json()
    risk_score = data.get('risk', 'No risk score available')
    print(f'Chrome Extension: {extension_id}\nRisk Score: {risk_score}')
else:
    print(f'Error: {response.status_code} - {response.text}')
