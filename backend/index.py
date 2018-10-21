# /index.py

from flask import Flask, request, jsonify, render_template, redirect, url_for
import os
import dialogflow
import requests
import json
import sys
import pusher
import dialogflow_v2 as dialogflow
import maps
import quickstart
from googleapiclient.discovery import build
from httplib2 import Http
from flask_login import login_user, logout_user, current_user, login_required
from flask_login.login_manager import LoginManager
from auth import GoogleSignIn, OAuthSignIn

################## to be saved
user_location = "" # string
nearbyUnis = {} # dictionary
user_university = "" # string
##################

login_manager = LoginManager()
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
            #nearbyUnis = maps.getUnisNearby(user_location, 1000)
            print("User location:", user_location)

        if response.query_result.intent.display_name == "setup_university":
            user_university = response.query_result.parameters["University"]
            print("University:", user_university)

        if response.query_result.intent.display_name == "setup_calendar":
            print("TODO")

    return response.query_result.fulfillment_text


@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    fulfillment_text = detect_intent_texts(project_id, "unique", message, 'en')
    response_text = { "message":  fulfillment_text }
    return jsonify(response_text)




@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    # Flask-Login function
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()

@app.route('/callback/<provider>')
def oauth_callback(provider):
    oauth = OAuthSignIn.get_provider(provider)
    service = oauth.callback()
    print(quickstart.getCalendars(oauth), file=sys.stdout)
    '''
    if email is None:
        # I need a valid email address for my user identification
        flash('Authentication failed.')
        return redirect(url_for('error'))
    # Log in the user, by default remembering them for their next visit
    # unless they log out.
    '''
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html', title='Sign In')

@app.route('/error')
def error():
    return render_template('error.html', title='Error')

# run Flask app
if __name__ == "__main__":
    app.run()
