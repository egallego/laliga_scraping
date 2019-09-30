from datetime import datetime
from dbconnector import DBConnector
from os import environ
from scraper import Scraper
from scraping_utils import remove_accents, split_string_to_list, remove_spaces

import pandas as pd


# ==========================================================================
#                     Functions
# ==========================================================================
def read_calendar(scraper, season, rnd):
    """
    Read page and scrap values for each season and round

    Parameters
    ----------
    scraper: Scraper object
        object formatting the general url
    season : str
        selected session
    rnd: int
        selected round

    Returns
    -------
    round_info: pandas.DF
        scraped information for selected round/season
    """
    # request html page
    page = scraper.read_page({'season': season, 'rnd': rnd}, delay=0.5)

    # Extract team_names and format names
    team_names = split_string_to_list(page,
                            str_pre='<span class="nombre-equipo" itemprop="name">',
                            str_after='</span>\n')

    team_names = map(remove_accents, team_names)
    team_names = map(remove_spaces, team_names)

    # Sort pairs of teams playing together
    games = zip(team_names[::2], team_names[1::2])

    # Extract times and format it as datetime
    times = split_string_to_list(page,
                       str_pre='<time itemprop="startDate" content="',
                       str_after='"></time>')

    times = map(lambda x: datetime.strptime(x[:-6], '%Y-%m-%dT%H:%M:%S'), times)

    # format data
    games_list = []
    for teams, time in zip(games, times):
        games_list.append({
            'season': season,
            'competition': 'LaLiga',
            'round': rnd,
            'local': teams[0],
            'visitant': teams[1],
            'date': time
        })

    round_info = pd.DataFrame(games_list)

    return round_info


# ==========================================================================
#                   Params and definitions
# ==========================================================================

db_object = DBConnector(data_base='laliga_scraping', table='calendar')
scraper = Scraper(url='https://resultados.as.com/resultados/futbol/primera/{season}/jornada/regular_a_{rnd}')

# ==========================================================================
#                           Code
# ==========================================================================

if_exists = 'replace'

for year in range(20, 0, -1):

    season = '20%02d_20%02d' % (year - 1, year)

    print 'Scrapig calendar session %s' % season

    for rnd in range(1, 39):

        if rnd % 5 == 0:
            print '\tround %d' % rnd

        # read calendar info
        calendar_info = read_calendar(scraper, season, rnd)

        # store info to DB
        db_object.store_values(calendar_info, if_exists=if_exists)

        # apply only replace on the first iteration
        if if_exists == 'replace':
            if_exists = 'append'

print 'End'
