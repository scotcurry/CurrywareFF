import yaml
from requests_oauthlib import OAuth2Session
import os
import time
import logging
import json

# This is necessary for testing with non-HTTPS localhost
# Remove this if deploying to production
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# This is necessary because Azure does not guarantee
# to return scopes in the same case and order as requested
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
os.environ['OAUTHLIB_IGNORE_SCOPE_CHANGE'] = '1'

# Load the oauth_settings.yml file
stream = open('oauth_settings.yml', 'r')
settings = yaml.load(stream, Loader=yaml.FullLoader)

# This is where the code builds out the URLs that get called from the oauth_settings.yaml file.
authorize_url = '{0}{1}'.format(settings['authority'], settings['authorize_endpoint'])
token_url = '{0}{1}'.format(settings['authority'], settings['token_endpoint'])

logger = logging.getLogger(__name__)
logFormatter = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(format=logFormatter, level=logging.INFO)


# Method to generate a sign-in url
# OAuth library documentation: https://docs.authlib.org/en/latest/client/api.html#authlib.client.OAuth2Session
# This code is a bit of a mystery to me.  I can't figure out how exactly the sign_in_url is being created.
def get_sign_in_url():
    # Initialize the OAuth client
    aad_auth = OAuth2Session(settings['app_id'], redirect_uri=settings['redirect'])
    sign_in_url, state = aad_auth.authorization_url(authorize_url, prompt='login')
    logging.debug('Sign In URL: %s', sign_in_url)
    logging.info('Auth Helper State: %s', state)
    return sign_in_url, state


# Method to exchange auth code for access token
def get_token_from_code(callback_url, expected_state):
    # Initialize the OAuth client
    logger.error('Token URL: %s', token_url)
    logger.info('Get Token From Code State: %s', expected_state)
    aad_auth = OAuth2Session(settings['app_id'], state=expected_state, redirect_uri=settings['redirect'])
    token = aad_auth.fetch_token(token_url, client_secret=settings['app_secret'], authorization_response=callback_url)
    access_token = token['access_token']
    return access_token


def store_token(request, token):
    request.session['oauth_token'] = token


def store_user(request, user):
    request.session['user'] = {
        'is_authenticated': True,
        'name': user['displayName'],
        'email': user['mail'] if (user['mail'] is not None) else user['userPrincipalName']
    }


# Code Note - Primary call to get the token to pass to O365
def get_token(request):
    token = request.session['oauth_token']
    if token is not None:
        # Check expiration
        now = time.time()
        # Subtract 5 minutes from expiration to account for clock skew
        expire_time = token['expires_at'] - 300
        if now >= expire_time:
            # Refresh the token
            aad_auth = OAuth2Session(settings['app_id'], token=token, scope=settings['scopes'],
                                     redirect_uri=settings['redirect'])
        else:
            aad_auth = OAuth2Session(settings['app_id'], token=token, scope=settings['scopes'],
                                     redirect_uri=settings['redirect'])

        refresh_params = {
            'client_id': settings['app_id'],
            'client_secret': settings['app_secret']
        }

        new_token = aad_auth.refresh_token(token_url, **refresh_params)

        # Save new token
        store_token(request, new_token)

        # Return new access token
        return new_token

    else:
        # Token still valid, just return it
        return token


def remove_user_and_token(request):
    if 'oauth_token' in request.session:
        del request.session['oauth_token']

    if 'user' in request.session:
        del request.session['user']

    if 'auth_state' in request.session:
        del request.session['auth_state']
