# -*- coding: utf-8 -*-

from datetime import datetime
from scraping_utils import split_string_3_times, split_string, split_string_to_list
from string_utils import extract_team_name, correct_name
import json
import pandas as pd


def get_time_bin_temporal_possession(x, str_pre):
    """
    get time bin of the temporal position

    Parameters
    ----------
    x: str
        part of an html page
    str_pre: str
        string used to split the data

    Returns
    -------
    possession_bin: str
    """
    possession_bin = split_string_3_times(x, str_pre, '<span class="posesion">', '%', 1, 1, 0)
    return possession_bin


def get_attempts_sub_str(x, index_keep_last):
    """
    get attempts information

    Parameters
    ----------
    x: str
        part of an html page
    index_keep_last: int
        index to keep (used to select local/visitant)

    Returns
    -------
    sub_string: str
    """
    sub_string = split_string_3_times(x,
                                      '<div class="grupo remates">\n<p>Remates</p>', '<ul class="leyenda-remates">',
                                      '<div class="campo-frontal fld-front fld-view-visitante" style="display:none;">',
                                      index_keep_last=index_keep_last)

    return sub_string


def extract_temporal_possession(information_part):
    """
    extract temporal possession

    Parameters
    ----------
    information_part: str
        string containg the temporal possession information

    Returns
    -------
    temporal_possession: dict
    """
    temporal_possession = {}
    for time_range in range(18):
        # define time window
        time_window = '%d - %d' % (time_range * 5, (time_range + 1) * 5)
        try:
            # get possession for that time bin
            time_part = information_part.split(''.join(['<time>', time_window, '</time>']))[1]

            # extract possession for each team
            possession_local = get_time_bin_temporal_possession(time_part, '<span class="dato-posesion local">')
            possession_visitant = get_time_bin_temporal_possession(time_part, '<span class="dato-posesion visitante">')

            # store info into a json
            temporal_possession[time_window] = [{'local': possession_local, 'visitant': possession_visitant}]
        except:
            # if it is not found copy previous one
            temporal_possession[time_window] = temporal_possession['%d - %d' % ((time_range - 1) * 5, time_range * 5)]
    return temporal_possession


def format_attempts(x):
    """
    format a dict with attempts information

    Parameters
    ----------
    x: list
        information to be defined in the dict
    Returns
    -------
    dict
    """
    return {'minute': x[0],
            'type': x[1],
            'name': x[2]}


def extract_attempt_information(x):
    """
    extract attempt information from substring

    Parameters
    ----------
    x: str
        string containing and html page or part of it

    Returns
    -------
    attempt_information: list[dict]
    """
    # extract minuts
    minutes = split_string_to_list(x, '<time class="s-L s-stext-nc"><strong>', '\xe2\x80\x99</strong></time>')
    minutes = map(int, minutes)

    # extract names
    names = split_string_to_list(x, str_pre='</span>\n</span>',
                                 str_after='<span class="dato">', start_beginning=False,
                                 index_keep_after=1, index=-1)
    names = map(correct_name, names)

    # extract attempt type
    attempt_type = split_string_to_list(x, '<span class="sts-marker s-pa ', '">')

    # group information
    attempt_information = map(format_attempts, zip(minutes, attempt_type, names))

    return attempt_information


def extract_information_from_reference(results_extractor, game_ref):
    """
    from a reference of a game, construct the url, obtain the web and extract information

    Parameters
    ----------
    results_extractor: object
        object formatting the general url
    game_ref: str
        reference of the game
    Returns
    -------
    information: dict
    """
    # get page
    page = results_extractor.read_page({'game_ref': game_ref}, delay=0.5)

    # select correct name to be used
    if '<div class="tit-modulo">\nEstadísticas</div>' in page:
        text_search = '<div class="tit-modulo">\nEstadísticas</div>'
    else:
        text_search = '<div class="tit-modulo">\nEstadísticas\n</div>'

    information_part = page.split(text_search)[1]

    # Extract team names
    local = extract_team_name(information_part, '<span class="nombre-equipo local s-left">', '<')
    visitant = extract_team_name(information_part, '<span class="nombre-equipo visitante s-right">', '<')

    # Extract goals
    local_goals = int(split_string(page, '<span class="tanteo-local">', '\n<'))
    visitant_goals = int(split_string(page, '<span class="tanteo-visit">', '\n<'))

    # Define result
    if local_goals > visitant_goals:
        result = '1'
    elif local_goals == visitant_goals:
        result = 'x'
    else:
        result = '2'

    # extract possession
    possession_part = information_part.split('<span class="porcentaje-posesion">')[1:]
    possession_local, possession_visitant = map(lambda x: float(x.split('%')[0]), possession_part)

    # extract temporal possession
    temporal_possession = extract_temporal_possession(information_part)

    # extract attempts information
    if '"grupo remates"' in information_part:

        attempts_local_sub_str = get_attempts_sub_str(information_part, 0)
        attempts_visitant_sub_str = get_attempts_sub_str(information_part, 1)

        attempts_local = extract_attempt_information(attempts_local_sub_str)
        attempts_visitant = extract_attempt_information(attempts_visitant_sub_str)

    else:

        attempts_local = {}
        attempts_visitant = {}

    # format correct result
    information = {'local': local, 'visitant': visitant, 'result': result,
                   'goals_local': local_goals, 'goals_visitant': visitant_goals,
                   'possession_local': possession_local, 'possession_visitant': possession_visitant,
                   'possession_temporal': json.dumps(temporal_possession),
                   'attempts_local': json.dumps(attempts_local),
                   'attempts_visitant': json.dumps(attempts_visitant),
                   'url': results_extractor.format_url({'game_ref': game_ref})}

    return information


def extract_competition_information(db_object, game_ref_extractor, results_extractor, config, season, rnd):
    """
    extract competition information

    Parameters
    ----------
    db_object: object
        object to connect to DB
    game_ref_extractor: object
        object to get data from the game
    results_extractor: object
        object to get data from results
    season: str
        season to be studied
    rnd: int
        round to be studied
    config: object
        object with the configuration to be scraped
    """
    page = game_ref_extractor.read_page({'season': season, 'rnd': rnd}, delay=0.5)

    # Split page looking for links and times
    sub_part_links = page.split(config.str_links)[1:]
    sub_part_times = page.split(config.str_time)[:-1]

    if len(sub_part_times) == 0:
        return

    # extract links
    lambda_game_ref_extractor = lambda x: split_string(x, config.str_extract_links_pre, config.str_extract_links_after)
    game_references = map(lambda_game_ref_extractor, sub_part_links)

    # extract times
    lambda_time_extractor = lambda x: datetime.strptime(split_string(x,
                                                                     config.str_extract_times_pre,
                                                                     config.str_extract_times_after)[:-6],
                                                        '%Y-%m-%dT%H:%M:%S')
    times = map(lambda_time_extractor, sub_part_times)

    games_info = []
    for game_ref, time in zip(game_references, times):

        url = results_extractor.format_url({'game_ref': game_ref})
        if db_object.check_url_present(url):
            print '\t%s already in the DB' % url
            continue

        # get information for that game
        try:
            information = extract_information_from_reference(results_extractor, game_ref)

        except:
            print '%s Reference error' % game_ref
            continue

        information['season'] = season
        information['round'] = rnd
        information['date'] = time
        information['competition'] = config.competition

        games_info.append(information)

    if len(games_info) > 0:
        games_info = pd.DataFrame(games_info)
        db_object.store_values(games_info)
