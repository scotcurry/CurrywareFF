from requests_oauthlib import OAuth2Session
import logging

logFormatter = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(format=logFormatter, level=logging.ERROR)
logger = logging.getLogger(__name__)
yahoo_base_url = 'https://fantasysports.yahooapis.com/fantasy/v2'


def get_league_info(token):
    yahoo_client = OAuth2Session(token=token)
    league_results = yahoo_client.get('{0}/league/390.l.877754', yahoo_base_url)
    logging.info('League Results: %s', league_results)
