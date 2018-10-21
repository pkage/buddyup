from flask import url_for, current_app, redirect, request
from rauth import OAuth2Service
import sys
import json, urllib.request

id = "75528957886-bgnjrf0cvt3lj410e644208ijoovsa19.apps.googleusercontent.com"
secret = "aWY_i8nnuafUZylygPej0my-"

class OAuthSignIn(object):
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        self.consumer_id = id
        self.consumer_secret = secret

    def authorize(self):
        pass

    def callback(self):
        pass

    def get_callback_url(self):
        return url_for('oauth_callback', provider=self.provider_name,
                        _external=True)

    @classmethod
    def get_provider(self, provider_name):
        if self.providers is None:
            self.providers={}
            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider
        return self.providers[provider_name]

class GoogleSignIn(OAuthSignIn):
    def __init__(self):
        super(GoogleSignIn, self).__init__('google')
        googleinfo = urllib.request.urlopen('https://accounts.google.com/.well-known/openid-configuration')
        google_params = json.load(googleinfo)
        self.service = OAuth2Service(
                name='google',
                client_id=self.consumer_id,
                client_secret=self.consumer_secret,
                authorize_url=google_params.get('authorization_endpoint'),
                base_url="https://www.googleapis.com/auth/calendar.readonly",
                access_token_url=google_params.get('token_endpoint'),
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            scope='https://www.googleapis.com/auth/calendar.readonly',
            response_type='code',
            redirect_uri=self.get_callback_url())
            )

    def callback(self):
        for r in request.args:
            print(r, file=sys.stdout)
        oauth_session = self.service.get_auth_session(
                data={'code': request.args['code'],
                      'scope': request.args['scope'],
                      'grant_type': 'authorization_code',
                      'redirect_uri': self.get_callback_url(),
                     }
        )
        print(oauth_session.get('').json, file=sys.stdout)
        return oauth_session
