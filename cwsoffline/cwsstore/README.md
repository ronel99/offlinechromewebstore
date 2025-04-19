# Offline Chrome Web Store

This project is an offline version of the Chrome Web Store, allowing users to browse and download Chrome extensions in a local environment.

## Features

- Browse a list of available Chrome extensions.
- View details of each extension, including descriptions and download links.
- Download CRX files for offline installation.

## Project Structure

```
offline-chrome-webstore
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── templates
│   │   ├── base.html
│   │   ├── index.html
│   │   └── extension.html
│   ├── static
│   │   ├── css
│   │   │   └── styles.css
│   │   ├── js
│   │   │   └── scripts.js
│   │   └── extensions_info.json
│   └── routes
│       ├── __init__.py
│       └── extensions.py
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd offline-chrome-webstore
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Editing Extensions

1. **Edit `extensions_info.json`:**
   - The file is located at `app/static/extensions_info.json`.
   - Add new extensions by appending objects with the following structure:
     ```json
     {
         "extension_id": "unique_extension_id",
         "name": "Extension Name",
         "description": "Short description of the extension.",
         "version": "Extension version",
         "author": "Author or organization name",
         "iconUrl": "/static/icons/extension_icon.png",
         "downloadUrl": "/static/extensions/unique_extension_id.crx",
         "rating": 4.5
     }
     ```

2. **Add CRX Files:**
   - Place the `.crx` files for the extensions in the `app/static/extensions` directory.
   - Ensure the `downloadUrl` in `extensions_info.json` matches the file path.

## Usage

1. Start the FastAPI application:
   ```
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. Open your web browser and navigate to `http://localhost:8000` to access the Offline Chrome Web Store.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.