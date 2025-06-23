import os
import json
import zipfile
import xml.etree.ElementTree as ET

def extract_crx_files(src_folder, dest_folder):
    extensions_info = []

    for root, _, files in os.walk(src_folder):
        for file in files:
            if file.endswith('.crx'):
                crx_path = os.path.join(root, file)
                extension_id = os.path.splitext(file)[0]
                print(f"extension_id: {extension_id}")
                dest_path = os.path.join(dest_folder, extension_id)
                os.makedirs(dest_path, exist_ok=True)

                with zipfile.ZipFile(crx_path, 'r') as zip_ref:
                    zip_ref.extractall(dest_path)

                manifest_path = os.path.join(dest_path, 'manifest.json')
                if os.path.exists(manifest_path):
                    with open(manifest_path, 'r') as manifest_file:
                        manifest_data = json.load(manifest_file)
                        ext_name = manifest_data.get('name', '')
                        ext_name = manifest_data.get('action', {}).get('default_title','') if '_' in ext_name else ext_name
                        ext_name = extension_id.split('_')[1] if ext_name == "" else ext_name
                        #print(manifest_data.get('icons', {}).get('128', ''))

                        try:
                            icons = manifest_data.get('icons', {})
                                             
                            #for s,ico_path in icons:
                            sorted_keys = sorted(icons.keys(), key=int, reverse=True)
                            # Iterate from biggest to smallest and find the first existing file
                            for key in sorted_keys:
                                image = os.path.join(dest_path, icons[key].lstrip('/'))
                                break
                            else:
                                image = os.path.join(dest_path, "icon.png")
                        except:
                            print("No icons found in manifest, using default icon.png")
                            image = os.path.join(dest_path, "icon.png")
                            
                        #image = os.path.join(dest_path, manifest_data.get('icons', {}).get('128', '').lstrip('/')) if manifest_data.get('icons', {}).get('128', '') != "" else os.path.join(dest_path, "icon.png")                        

                        print(f"image_path: {image}")

                        extension_info = {
                            'name': ext_name,
                            #'name': manifest_data.get('action', {}).get('default_title',''),
                            #'name': manifest_data.get('name', ''),
                            'extension_id': extension_id.split('_')[0],
                            #'description': manifest_data.get('description', ''),
                            'description': manifest_data.get('description', '') if '_' not in manifest_data.get('description', '') else '',
                            'image_path_url': image,
                            'versions': [{'version': manifest_data.get('version', ''), 'path_url': crx_path}]
                        }
                        extensions_info.append(extension_info)

    return extensions_info

def save_extensions_info(extensions_info, output_file):
    with open(output_file, 'w') as json_file:
        json.dump(extensions_info, json_file, indent=4)


if __name__ == "__main__":
    artifacts_folder = 'artifacts'
    src_folder = 'artifacts/extensions'
    dest_folder = 'assets'
    output_json_file = 'extensions_info.json'
    output_xml_file = 'extensions_info.xml'

    extensions_info = extract_crx_files(src_folder, dest_folder)
    save_extensions_info(extensions_info, os.path.join(artifacts_folder, output_json_file))
