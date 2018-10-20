# /index.py

from flask import Flask, request, jsonify, render_template
import os
import dialogflow
import requests
import json
import pusher
import dialogflow_v2 as dialogflow
import maps

################## to be saved
user_location = "" # string
nearbyUnis = {} # dictionary
user_university = "" # string
##################

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    if text:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(
            session=session, query_input=query_input)

        if response.query_result.intent.display_name == "setup_location":
            value = response.query_result.parameters["City"]
            user_location = maps.getCityLocation(value)
            nearbyUnis = maps.getUnisNearby(user_location, 1000)

        if response.query_result.intent.display_name == "setup_university":
            user_university = response.query_result.parameters["University"]

        return response.query_result.fulfillment_text


@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    fulfillment_text = detect_intent_texts(project_id, "unique", message, 'en')
    response_text = { "message":  fulfillment_text }
    return jsonify(response_text)

# run Flask app
if __name__ == "__main__":
    app.run()
