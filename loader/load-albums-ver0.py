import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
## ensures that fetchDataApi is not searched within the listing of python modules, but our root directories, WOW LOL
from fetchDataApi.last_fm import search_lastfm_album
from database.mongodb import db
# from pprint import pprint
import csv

count: int = 0

with open('Loader/Albums  - Sheet2.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        album = row['Album']
        artist = row['Aritst/Band']  # Note the typo in column header: "Aritst/Band"
        # print(f"Album: {album}, Artist: {artist}")
        data = search_lastfm_album(artist=artist, album=album)
        # pprint(data)

        if data == None:
            print("Skipped for", f" --> {album} by {artist} NOPE :(")
            continue
        result = db['albums'].insert_one(data)
        print("Inserted album with _id:", result.inserted_id, f" --> {album} by {artist} DONE :)")
        count += 1

print("-----"*10,":",count)