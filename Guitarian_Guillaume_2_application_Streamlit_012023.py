import streamlit as st
import pandas as pd
import sys
import os
import numpy as np
import matplotlib.pyplot as plt


import requests
import base64
import json

import pickle




# répertoire courant, ne se termine PAS par un séparateur
current_path = os.path.abspath(os.getcwd())
# Séparateur de chemin d'accès en fonction de l'os
path_sep = os.path.sep

var_backup_filename_collaborative = "sorted_recomendations.pckl"

f = open(var_backup_filename_collaborative, 'rb')
sorted_recomendations = pickle.load(f)
f.close() 


st.title('Articles Recommendations')


label = st.markdown(
"""
***
### Please, choose a user !
"""
)

user_list = ['user #' + str(user_id) for user_id in sorted_recomendations]

reset_choice_label = 'reset choice'
user_list.insert(0, reset_choice_label)


selected_user = st.selectbox(
    'empty',
    user_list[:20],
    label_visibility="hidden"
)

#Local
#api_url = "http://localhost:7071/api/HttpTriggerFunc?user_id="
        

#Distant
#api_url = "https://fromlocalvs.azurewebsites.net/api/httptriggerfunc?user_id="

#Distant AVEC BLOB STORAGE
api_url = "https://fromlocalvs.azurewebsites.net/api/HttpTriggerFromVSwithBlob?user_id="



def get_prediction():
    
    global api_url
    
    if selected_user == reset_choice_label:
        st.write('Please select a user before trying to get prediction')
    else:
        # Get the prediction
        st.write("Getting the prediction, please wait...")

        try:
            
            #user_id = int(selected_user.split("#")[1])
            user_id = selected_user.split("#")[1]
            api_url = api_url + user_id
            
            response = requests.get(api_url)

            if response.status_code == 200:
                json_data = response.json()
                json_data
            else:
                error = F"La requête a échoué avec le code d'état : {response.status_code}"
                error
            
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            print(e) #for debug
            st.write("A network error occured, please try again")                
            
            
            
if st.button('Get Prediction'):
    get_prediction()