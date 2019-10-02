from configurators import LaLigaConfig
from dbconnector import DBConnector, DBExplorer
from scraping_functions import extract_competition_information
from scraper import Scraper

import argparse

# ==========================================================================
#                     Functions
# ==========================================================================

# ==========================================================================
#                   Params and definitions
# ==========================================================================
db_object = DBExplorer(data_base='laliga_scraping', table='results')
game_ref_extractor = Scraper(url='https://resultados.as.com/resultados/futbol/primera/{season}/jornada/regular_a_{rnd}')
results_extractor = Scraper(url="https://resultados.as.com{game_ref}/estadisticas/")
configuration = LaLigaConfig()

# ==========================================================================
#                           Code
# ==========================================================================

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--season", help="Season to extract the data", default='2018_2019')

    args = parser.parse_args()

    print 'Scrapig %s session %s' % (configuration.competition, args.season)

    for rnd in range(1, 39):
        if db_object.count_games(args.season, rnd, configuration.competition) != configuration.number_games(rnd):
            print '\tRound %d' % rnd
            extract_competition_information(db_object, game_ref_extractor,
                                            results_extractor, configuration, args.season, rnd)
