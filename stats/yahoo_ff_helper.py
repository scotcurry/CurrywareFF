from requests_oauthlib import OAuth2Session
import logging
import json

logFormatter = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(format=logFormatter, level=logging.ERROR)
logger = logging.getLogger(__name__)
yahoo_base_url = 'https://fantasysports.yahooapis.com/fantasy/v2'


def get_league_info(token):
    yahoo_client = OAuth2Session(token=token)
    query_params = {'format': 'json'}
    league_results = yahoo_client.get('{0}/league/390.l.877754'.format(yahoo_base_url), params=query_params)
    league_json = league_results.json()
    league_name = league_json['fantasy_content']['league'][0]['name']
    return league_name


def get_team_info(token):
    yahoo_client = OAuth2Session(token=token)
    query_params = {'format': 'json'}
    league_results = yahoo_client.get('{0}/league/390.l.877754/teams'.format(yahoo_base_url), params=query_params)
    league_json = league_results.json()
    league_json = league_json['fantasy_content']['league'][1]['teams']
    logging.info('Fantasy Content: %s', league_json)

    return league_json
