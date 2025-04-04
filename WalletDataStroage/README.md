**LoraLabs is a Web application designed to used to genearte Nfts with the help of ai.In order to fetch, process, and store
wallet data and character-related content from Firebase the follwoing system was developed which maintains an organized file structure for each user's wallet while ensuring
that no duplicate entries are created.**

📦 **WHAT IT DOES**


Fetches the latest user data from Firebase Realtime Database.


Extracts wallet addresses and character-related metadata.

**Stores:**
-A text file containing character details and Downloaded character images (from URLs) where both consists the character data.


-Zipped archives of the character data per user wallet.


-Prevents duplicate storage by checking existing files in the user's wallet folder.


🧠 **Features**
🔥 Integration with Firebase Realtime Database


📥 Automatic image downloading and archiving


📂 Folder-based wallet structure
🚫 Duplication check for character entries
🗃️ Clean zip archive packaging


🛠 **Technologies Used**
-Python 3
-Firebase Admin SDK
-Pandas
-Requests
-OS / shutil / zipfile
