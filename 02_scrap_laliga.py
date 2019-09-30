from configurators import LaLigaConfig
from dbconnector import DBConnector, DBExplorer
from scraping_functions import extract_competition_information
from scraper import Scraper


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

for year in range(18, 14, -1):

    season = '20%02d_20%02d' % (year - 1, year)

    print 'Scrapig %s session %s' % (configuration.competition, season)

    for rnd in range(1, 39):
        if db_object.count_games(season, rnd, configuration.competition) != configuration.number_games(rnd):
            print '\tRound %d' % rnd
            extract_competition_information(db_object, game_ref_extractor,
                                            results_extractor, configuration, season, rnd)
