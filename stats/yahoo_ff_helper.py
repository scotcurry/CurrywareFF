from requests_oauthlib import OAuth2Session
import logging
import yaml

logFormatter = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(format=logFormatter, level=logging.ERROR)
logger = logging.getLogger(__name__)
yahoo_base_url = 'https://fantasysports.yahooapis.com/fantasy/v2'
query_params = {'format': 'json'}

stream = open('yahoo_settings.yml', 'r')
league_info_yaml = yaml.load(stream, Loader=yaml.FullLoader)
current_league = '{0}.l.{1}'.format(league_info_yaml['game_id'], league_info_yaml['league_id'])


def get_game_id(token):
    yahoo_client = OAuth2Session(token=token)
    game_id_call = yahoo_client.get('{0}/game/nfl'.format(yahoo_base_url), params=query_params)
    game_id_json = game_id_call.json()
    game_id = game_id_json['fantasy_content']['game'][0]['game_id']
    return game_id


def get_league_info(token):
    yahoo_client = OAuth2Session(token=token)
    url_to_get = '{0}/league/{1}'.format(yahoo_base_url, current_league)
    logging.info('League URL: %s', url_to_get)
    league_results = yahoo_client.get('{0}/league/{1}'.format(yahoo_base_url, current_league), params=query_params)
    league_json = league_results.json()
    league_name = league_json['fantasy_content']['league'][0]['name']
    return league_name


def get_team_info(token):
    yahoo_client = OAuth2Session(token=token)
    league_results = yahoo_client.get('{0}/league/{1}/teams'.format(yahoo_base_url, current_league), params=query_params)
    league_json = league_results.json()
    league_json = league_json['fantasy_content']['league'][1]['teams']

    return league_json


def get_available_players(token, position, count):
    yahoo_client = OAuth2Session(token=token)
    additional_params = {'status': 'FA', 'position': position, 'count': count, 'sort': 'OR'}
    query_params.update(additional_params)
    available_players = yahoo_client.get('{0}/league/{1}/players'.format(yahoo_base_url, current_league),
                                         params=query_params)
    players_json = available_players.json()
    # players_at_position = players_json['fantasy_content']['league'][0]['players']
    logging.info('Player JSON: %s', players_json)


def get_current_user_info(token, xoauth_user_guid):
    yahoo_client = OAuth2Session(token=token)
    user_info = yahoo_client.get('https://social.yahooapis.com/v1/user/{0}/profile)'.format(xoauth_user_guid),
                                 params=query_params)
