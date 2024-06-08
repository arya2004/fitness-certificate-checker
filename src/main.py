# -*- coding: utf-8 -*-
"""
Created on Sun Apr  9 00:33:08 2023
@author: arya2004
"""

# Importing necessary libraries
import easyocr
import requests
import json
from dateutil.parser import parse
import datetime
from gtts import gTTS
import os
import pymongo
from pymongo import MongoClient

# Establishing connection with MongoDB
client = MongoClient("mongodb://127.0.0.1:27017/test22")
db = client["v1"]
today = datetime.datetime.today()
language = 'en'

# Initializing EasyOCR reader
reader = easyocr.Reader(['en'])  # This needs to run only once to load the model into memory

# Reading text from an image using EasyOCR
result = reader.readtext('examples/TS06UC4622.png', detail=0)
for k in result:
    j = k
j = j[:2] + '0' + j[3:]  # Differentiating between zero and O in the text

# List of distribution IDs to be checked
urls = ['c77585eb-5808-5588-912a-5e640a7162b0',#sec oldest
        '266e7b7d-a174-544e-a12a-8de3c85de79a',
        'f8337d1e-213b-508b-8d17-486de76094c6',
        '107fdc6e-df03-592a-8db9-8f5e6d47a1d0',
        '1bde8ac0-a187-56dc-8dcf-3063907d46b0',
        'e8052405-0ab2-5908-9536-d3a5a0ff5bff',
        'fe27388a-2f22-55b3-8534-dbb0f97d912c',
        'd72e618f-9ff7-5cca-99fc-65d09f9cd9cc',
        '4ad08591-5b91-556c-a026-aa75d4035953',
        'c3df0d32-fa2e-5ac9-9563-21a1f00f7371',
        '117bf325-1bdc-5fb9-af9c-6696dded8726',
        '3f30d04a-8ba8-5cac-816b-bc34f31af454',
        '814e5c8a-9e66-519c-8626-2f9496e8ebea',
        'c52626c2-c383-55dc-ba31-5ebce9b043fe',
        '8a41d2c6-7f90-5e8d-b0d4-a8d37b57bb1c',
        'ff6c8d83-bee8-5e56-af4f-17dda8a83eda',
        'd3f4f174-0e02-5745-9df7-83e79c2783e9',
        'afa51caa-b472-5af2-a215-d6cc101fd102',
        'b6cd30f9-678e-5121-b196-aa7d805f7d84',
        '6117958a-c557-50b9-b6cc-92dcc6910a09',
        'e12d4b39-6d03-59ed-ae30-5bcc313e565f',
        '706723b5-efb7-50f8-80c7-47dbd9a06f60',
        'd094dee6-e1ed-555a-aa70-f032d5312329',
        '2b4de216-5710-5152-8d72-db63571a8716',
        '3d5b4947-b24a-5390-a9b4-6a665517a611',
        'ee8aa8f2-2c71-55d7-ae6f-6cdb2bc8a8b8',
        'c680f360-bff1-507b-bb04-062b72af3bb8',
        '7576e0c2-1c1c-5f69-b5e3-0aec1b96a055',#2021 data
        #'c77585eb-5808-5588-912a-5e640a7162b0',#sec oldest
        'cba46849-920a-5a5d-9a2a-bbc6922afc3c' #oldest one
        ]
# Checking fitness certificate status for each distribution ID
for distributionId in urls:
    r = requests.get(
        'https://data.telangana.gov.in/api/1/datastore/sql?query=%5BSELECT%20%2A%20FROM%20' + distributionId + '%5D%5BWHERE%20registrationno%20%3D%20%22' + j + '%22%5D%5BLIMIT%201%5D')
    m = json.loads(r.content)
    if str(m) != '[]':
        print(m)
        break

# Processing the retrieved data
for i in m:
    if parse(i["validTo"]) > today:
        # If fitness certificate is valid
        tutorial1 = {"registrationNo": i["registrationNo"], "time": today, "hasValidFitnessCertificate": True}
        tutorial = db.tutorial
        tutorial.insert_one(tutorial1)
        mytext = "Welcome " + i["registrationNo"]
        myobj = gTTS(text=mytext, lang=language, slow=False)
        myobj.save("audioOutput/hasValidFitnessCertificate/" + i["registrationNo"] + ".mp3")
        os.system(
            "C:/Users/arya2/Desktop/FitnessCertificateDetection/audioOutput/hasValidFitnessCertificate/" + i[
                "registrationNo"] + ".mp3")
        print(mytext)
    else:
        # If fitness certificate is not valid
        tutorial1 = {"registrationNo": i["registrationNo"], "time": today, "hasValidFitnessCertificate": False}
        tutorial = db.tutorial
        tutorial.insert_one(tutorial1)
        mytext = i["registrationNo"] + " does not have a fitness certificate. " + i[
            "registrationNo"] + " doesn't care about the environment"
        myobj = gTTS(text=mytext, lang=language, slow=False)
        myobj.save("audioOutput/noValidFitnessCertificate/" + i["registrationNo"] + ".mp3")
        os.system(
            "C:/Users/arya2/Desktop/FitnessCertificateDetection/audioOutput/noValidFitnessCertificate/" + i[
                "registrationNo"] + ".mp3")
        print(mytext)
