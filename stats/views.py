# This code is less impressive that I thought it would be.  It mostly just formats the
# information.
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from django.shortcuts import render
import logging

from stats.auth_helper import get_sign_in_url, get_token_from_code

logFormatter = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(format=logFormatter, level=logging.ERROR)
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
    request.session['state'] = state
    # Redirect to the Yahoo sign-in page
    return HttpResponseRedirect(sign_in_url)


def callback(request):
    # Get the state saved in session
    expected_state = request.session.pop('state', '')
    # Make the token request
    token = get_token_from_code(request.get_full_path(), expected_state)
    logging.error(token)
    # Get the user's profile

    # Save token and user
    # store_token(request, token)
    # store_user(request, user)

    return HttpResponseRedirect(reverse('index'))