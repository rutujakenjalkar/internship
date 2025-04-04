import firebase_admin
from firebase_admin import db,credentials
import pandas as pd 
import os 
import zipfile
import requests
import json
import shutil


def process_character_data(latest_document, new_folder_path):
    
    try:
        # Step 1: Create a text file with character details
        text_file_name = latest_document["charactername"]
        file_name = f"{text_file_name}details.txt"
        file_path = os.path.join(new_folder_path, file_name)
        
        with open(file_path, "w") as file:
            file.write(f"character name: {latest_document['charactername']}\ncharacter description: {latest_document['characterdescription']}\n")
        print(f"Text file created: {file_path}")

        # Step 2: Download images from URLs
        image_url_list = latest_document.get('uploadedurllist', [])
        print(f"Image URLs: {image_url_list}")

        if not image_url_list:
            print("No image URLs found. Skipping image download.")
            return

        image_file_name = latest_document.get("charactername")
        image_folder = os.path.join(new_folder_path, f"{image_file_name}downloaded_images")
        zip_filename = os.path.join(new_folder_path, f"{image_file_name}images.zip")
        
        # Create the folder for downloaded images
        os.makedirs(image_folder, exist_ok=True)
        print(f"Folder '{image_folder}' is ready!")

        # Download images
        for idx, url in enumerate(image_url_list):
            url = url.strip()  # Remove any leading/trailing spaces

            if not url:
                print(f"Skipping empty URL at index {idx}")
                continue

            # Validate URL
            if not url.startswith("http"):
                print(f"Skipping invalid URL: {url}")
                continue

            # Define image path
            image_path = os.path.join(image_folder, f"image_{idx + 1}.jpg")

            try:
                # Download image
                response = requests.get(url, stream=True)
                if response.status_code == 200:
                    with open(image_path, "wb") as file:
                        for chunk in response.iter_content(1024):  # Write in chunks
                            file.write(chunk)
                    print(f"Downloaded: {image_path}")
                else:
                    print(f"Failed to download {url}")
            except Exception as e:
                print(f"Error downloading {url}: {e}")

        # Step 3: Zip the downloaded images
        with zipfile.ZipFile(zip_filename, "w") as zipf:
            for file in os.listdir(image_folder):
                file_path = os.path.join(image_folder, file)
                zipf.write(file_path, os.path.basename(file_path))
                print(f"Added {file} to ZIP")

        print(f"ZIP file created successfully: {zip_filename}")

        # Step 4: Clean up the downloaded images folder
        shutil.rmtree(image_folder)
        print(f"Folder '{image_folder}' deleted.")

    except Exception as e:
        print(f"An error occurred: {e}")

    #CREATING A ZIP FILE TO STORE BOTH ZIP OF IMAGES AND THE TEXT FILE
    character_zip = os.path.join(new_folder_path, f"{image_file_name}.zip")
    files_to_be_added_in_zip = [f for f in os.listdir(new_folder_path) if latest_document["charactername"] in f]
    print(files_to_be_added_in_zip)
    with zipfile.ZipFile(character_zip, "w") as zipf:
                for file in files_to_be_added_in_zip:
                    os.chdir(new_folder_path)
                    zipf.write(file)
                    os.remove(file)
    zipf.close()

    print("the zip file is creates in the wallet : Success!!")
        

                




#CONNECTION FOR FIREBASE

cred=credentials.Certificate("C:\\Users\\Abhay\\Downloads\\web3user-d60b4-firebase-adminsdk-fbsvc-12c23de398.json")
firebase_admin.initialize_app(cred,{"databaseURL":"https://web3user-d60b4-default-rtdb.firebaseio.com/"})

ref = db.reference("/Authentication")
try:
    data = ref.get()
    if data:
        print("Data fetched successfully from Firebase.")
    else:
        print("No data found in Firebase.")
except Exception as e:
    print(f"Error fetching data: {e}")
    exit()

try:
    
    snapshot = ref.order_by_child('datetime').limit_to_last(1).get()
    if snapshot:
        for key, val in snapshot.items():
            '''latest_document = 'key={0}, value={1}'.format(key, val)'''
            latest_document=val
            print("Latest Document:", latest_document)
    
    else:
          print("No documents found.")

except Exception as e:
     print(f"Error querying data: {e}")
print("Latest")
print(latest_document)







document_list=data.values()
walletaddress_list=[]


#obtain all the wallet in the response at the backend

for document in (document_list):
   walletaddress_list.append(document.get('walletaddress'))

print(walletaddress_list)

path="C:\\Users\\Abhay\\Documents\\internimage\\wallet_data"
new_folder_path = os.path.join(path,latest_document['walletaddress'])  #used to create the address

#check if the wallet exists in the directory & do the operations required
if os.path.exists(new_folder_path):
     print("ENTRY MADE IN EXISTING FOLDER")
     file_found=False
     #if wallet==latest_document['walletaddress']:
     files = [f for f in os.listdir(new_folder_path) if os.path.isfile(os.path.join(new_folder_path, f))]
     print( latest_document['walletaddress'] ,"Files in the folder",files)

     for file in files:
         file_name_without_extension=os.path.splitext(file)[0]
         if latest_document['charactername'].lower()   in file_name_without_extension.lower():
             file_found = True
                
     print("FILE FOUND:",file_found)

     if file_found==False:
         process_character_data(latest_document, new_folder_path)

else:
     print("CREATING A NEW FOLDER COMPLETELY")
     os.chdir("C:\\Users\\Abhay\\Documents\\internimage\\wallet_data")
     sanitized_wallet = latest_document['walletaddress'].strip().replace("\t", "").replace(" ", "_")
     print(sanitized_wallet)
     os.mkdir(sanitized_wallet)
     print("wallet created succesfully")
     new_folder_path = os.path.join(os.getcwd(), sanitized_wallet)
     process_character_data(latest_document, new_folder_path)


   
