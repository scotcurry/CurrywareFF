from bs4 import BeautifulSoup
import urllib.request

def get_out_players():
    http_handler = urllib.request.urlopen('http://www.nfl.com/injuries')
    injury_content = http_handler.read()
    soup = BeautifulSoup(injury_content)
    all_players = soup.find_all('head')