import logging

import json
import pickle
import sys
import os

import numpy as np 

import azure.functions as func

# répertoire courant, ne se termine PAS par un séparateur
current_path = os.path.abspath(os.getcwd())
# Séparateur de chemin d'accès en fonction de l'os
path_sep = os.path.sep

var_backup_filename_collaborative = "sorted_recomendations.pckl"

f = open(var_backup_filename_collaborative, 'rb')
sorted_recomendations = pickle.load(f)
f.close() 


def main(req: func.HttpRequest) -> func.HttpResponse:

    user_id = req.params.get('user_id')
    if not user_id:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            user_id = req_body.get('user_id')

    if user_id:

        user_id = int(str(user_id))

        recomendations_to_display = {}
        for key, value in sorted_recomendations[user_id].items(): 
            recomendations_to_display['Article N° ' + str(key)] = '(similiraty score = ' + str(round(value, 3)) + ')'

        reco_json = json.dumps(recomendations_to_display, indent = 4)
        return func.HttpResponse(reco_json)
        #return func.HttpResponse(f"Hello, {user_id}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a user_id in the query string or in the request body for a personalized response.",
             status_code=200
        )