# -*- coding: utf-8 -*-

import re


def remove_spaces(string):
    """
    remove spaces from a string

    Parameters
    ----------
    string: str
        str containing spaces

    Returns
    -------
    string: str
        string with spaces removed
    """
    return string.replace(' ', '')


def remove_accents(string):
    """
    remove accents from a string

    Parameters
    ----------
    string: str
        str containing accents
    Returns
    -------
    string: str
        string with accents removed
    """
    if type(string) is not unicode:
        string = unicode(string, encoding='utf-8')

    string = re.sub(u"[àáâãäå]", 'a', string)
    string = re.sub(u"[èéêë]", 'e', string)
    string = re.sub(u"[ìíîï]", 'i', string)
    string = re.sub(u"[òóôõö]", 'o', string)
    string = re.sub(u"[ùúûü]", 'u', string)
    string = re.sub(u"[ýÿ]", 'y', string)
    string = re.sub(u"[ÀÁ]", 'A', string)
    string = re.sub(u"[ÈÉ]", 'E', string)
    string = re.sub(u"[ÌÍ]", 'I', string)
    string = re.sub(u"[ÒÓ]", 'O', string)
    string = re.sub(u"[ÙÚ]", 'U', string)

    return string


def extract_team_name(x, str_pre, str_after):
    """
    extract team name from a part of an html page and format it

    Parameters
    ----------
    x: str
        part of html page
    str_pre: str
        string used to split before the interest string
    str_after: str
        string used to split after the interest string

    Returns
    -------
    team_name: str
        formatted team name
    """
    team_name = split_string(x, str_pre, str_after)
    team_name = correct_name(team_name)
    return team_name


def correct_name(x):
    """
    apply correct format to an string

    Parameters
    ----------
    x: str
        string to be formated

    Returns
    -------
    name: str
        formated string
    """
    name = remove_accents(x)
    name = remove_spaces(name)
    return name
