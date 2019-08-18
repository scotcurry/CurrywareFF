from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from django.shortcuts import render

from stats.auth_helper import get_sign_in_url


def index(request):
    # return HttpResponse("Hello, world. You're at the stats index page.")
    context = {}
    return render(request, 'stats/index.html', context)


def sign_in(request):
    # Get the sign-in URL
    sign_in_url, state = get_sign_in_url()
    # Save the expected state so we can validate in the callback
    request.session['auth_state'] = state
    # Redirect to the Azure sign-in page
    return HttpResponseRedirect(sign_in_url)


def callback(request):
    # Get the state saved in session
    expected_state = request.session.pop('auth_state', '')
    # Make the token request
    # token = get_token_from_code(request.get_full_path(), expected_state)

    # Get the user's profile
    # user = get_user(token)

    # Save token and user
    # store_token(request, token)
    # store_user(request, user)

    return HttpResponseRedirect(reverse('home'))