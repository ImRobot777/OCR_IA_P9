import logging

import json
import pickle
import sys
import os
import io

#import numpy as np 

import azure.functions as func


def main(req: func.HttpRequest, blob: func.InputStream) -> func.HttpResponse:

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

        # Charger le fichier pickle
        try:
            pickled_data = blob.read()

            logging.info(type(pickled_data))

            sorted_recomendations = pickle.loads(pickled_data)
        except Exception as e:
            logging.error(f'Error loading pickle file: {e}')
            return func.HttpResponse(f'Error loading pickle file: {e}', status_code=500)


        recomendations_to_display = {}
        for key, value in sorted_recomendations[user_id].items(): 
            recomendations_to_display['Article N° ' + str(key)] = '(similiraty score = ' + str(round(value, 3)) + ')'

        reco_json = json.dumps(recomendations_to_display, indent = 4)
        return func.HttpResponse(reco_json)
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a user_id in the query string or in the request body for a personalized response.",
             status_code=200
        )