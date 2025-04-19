{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "99f6120f-dc82-4a67-976d-03bddea3e9e3",
   "metadata": {},
   "outputs": [],
   "source": [
    "with open(\".env\", \"w\") as f:\n",
    "    f.write(\"LASTFM_API_KEY=da87e77d2348b4b9227b38b60d31f7e9\\n\")\n",
    "    f.write(\"GENIUS_API_KEY=15TK9a5jJZpzxaxn39KcMjyrjr08ArZEllCdfYOe0E16mxjTs7x7BsmU-v7TLvBO\\n\")\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "51972d45-ed71-4b6f-99b2-2a2a9d29b44a",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "['.env', '.ipynb_checkpoints', 'full_track_metadata_detailed.json', 'genius.ipynb', 'genius.py', 'lastfm.ipynb', 'lastfm.py', 'musicbrainz.ipynb', 'musicbrainz.py', 'Untitled.ipynb', 'Untitled1.ipynb']\n"
     ]
    }
   ],
   "source": [
    "import os\n",
    "\n",
    "# List all files, including hidden ones\n",
    "print(os.listdir())\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "2996728a-7062-44fd-99f6-bc30942b4ce5",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "['.env',\n",
       " '.ipynb_checkpoints',\n",
       " 'full_track_metadata_detailed.json',\n",
       " 'genius.ipynb',\n",
       " 'genius.py',\n",
       " 'lastfm.ipynb',\n",
       " 'lastfm.py',\n",
       " 'musicbrainz.ipynb',\n",
       " 'musicbrainz.py',\n",
       " 'Untitled.ipynb',\n",
       " 'Untitled1.ipynb']"
      ]
     },
     "execution_count": 7,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "\n",
    "import os\n",
    "os.listdir('.')\n",
    "\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "8cf5a815-1027-4a0b-b802-a8c1920859b3",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
