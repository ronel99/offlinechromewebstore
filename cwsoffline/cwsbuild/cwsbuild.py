import os
import json
import zipfile

def extract_crx_files(src_folder, dest_folder):
    extensions_info = []

    for root, _, files in os.walk(src_folder):
        for file in files:
            if file.endswith('.crx'):
                crx_path = os.path.join(root, file)
                extension_id = os.path.splitext(file)[0]
                dest_path = os.path.join(dest_folder, extension_id)
                os.makedirs(dest_path, exist_ok=True)

                with zipfile.ZipFile(crx_path, 'r') as zip_ref:
                    zip_ref.extractall(dest_path)

                manifest_path = os.path.join(dest_path, 'manifest.json')
                if os.path.exists(manifest_path):
                    with open(manifest_path, 'r') as manifest_file:
                        manifest_data = json.load(manifest_file)
                        extension_info = {
                            'name': manifest_data.get('name', ''),
                            'extension_id': extension_id,
                            'description': manifest_data.get('description', ''),
                            'image_path_url': os.path.join(dest_path, manifest_data.get('icons', {}).get('128', '')),
                            'versions': [{'version': manifest_data.get('version', ''), 'path_url': crx_path}]
                        }
                        extensions_info.append(extension_info)

    return extensions_info

def save_extensions_info(extensions_info, output_file):
    with open(output_file, 'w') as json_file:
        json.dump(extensions_info, json_file, indent=4)

if __name__ == "__main__":
    src_folder = 'artifacts/extensions'
    dest_folder = 'assets'
    output_file = 'extensions_info.json'

    extensions_info = extract_crx_files(src_folder, dest_folder)
    save_extensions_info(extensions_info, output_file)