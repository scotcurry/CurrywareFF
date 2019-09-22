# This code is less impressive that I thought it would be.  It mostly just formats the
# information.
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from django.shortcuts import render
import logging


from stats.auth_helper import get_sign_in_url, get_token_from_code, store_token, remove_user_and_token, get_token, \
    store_user
from stats.yahoo_ff_helper import get_league_info, get_team_info

logFormatter = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(format=logFormatter, level=logging.INFO)
logger = logging.getLogger(__name__)


# This is the driver of the code.  This renders the index page which has the Yahoo login page.
def index(request):
    # context - this is what gets sent into the view objects.  This is how you make a view dynamic.  Right now,
    # there is noting being sent in.
    context = {}
    return render(request, 'stats/index.html', context)


# This code is used to determine whether or not the the user is authenticated.  It is used in the html page
# to determine if the user is logged in.
def initialize_context(request):
    context = {}

    # Check for any errors in the session
    error = request.session.pop('flash_error', None)

    if error is not None:
        context['errors'] = []
        context['errors'].append(error)

    # Check for user in the session
    context['user'] = request.session.get('user', {'is_authenticated': False})
    return context


# When the user clicks on the login link
def sign_in(request):
    # Get the sign-in URL
    sign_in_url, state = get_sign_in_url()
    # Save the expected state so we can validate in the callback
    # logging.info('Sign In State: %s', state)
    request.session['auth_state_2'] = state
    # Redirect to the Yahoo sign-in page
    return HttpResponseRedirect(sign_in_url)


def sign_out(request):
    # Clear out the user and token
    remove_user_and_token(request)
    return HttpResponseRedirect(reverse('index'))


# The first call is made to the sign in.  In the callback we get a code that need to be exchanged for an token.
def callback(request):
    # Get the state saved in session
    expected_state = request.session.get('auth_state_3', '')
    # logging.info('Callback Expected State: %s', expected_state)
    # Make the token request
    token = get_token_from_code(request.get_full_path(), expected_state)
    logging.info('Token: %s', token)

    # Save token and user
    store_user(request)
    store_token(request, token)

    return HttpResponseRedirect(reverse('index'))


def remove_token(request):
    remove_user_and_token(request)
    validate_state = request.session.get('auth_state_3', '')
    logging.info("Remove Token State: %s", validate_state)
    return HttpResponseRedirect(reverse('index'))


def show_league_info(request):
    context = initialize_context(request)
    token = get_token(request)
    league_info = get_league_info(token)
    # logging.info('League Name: %s', league_info)
    team_info = get_team_info(token)
    context['team_name'] = league_info
    return render(request, 'stats/league_info.html', context)
