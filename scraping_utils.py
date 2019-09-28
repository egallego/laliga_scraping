# -*- coding: utf-8 -*-

import re


def split_page(string, str_pre, str_after, index_keep_after=0, ):
    """
    Split a string based on the values that need to be found before and after the strings of interest

    Parameters
    ----------
    string: str
        string to be splited
    str_pre: str
        string used to split before the interes string
    str_after: str
        string used to split after the interes string
    index_keep_after: int
        index to keep when the str_after is used

    Returns
    -------
    list_str: list[str]
    """
    splited_list = string.split(str_pre)[1:]
    list_str = map(lambda x: x.split(str_after)[index_keep_after], splited_list)
    return list_str


def remove_accents(input):
    """
    Remove accents from a list of strings or a string

    Parameters
    ----------
    input: list[str] or str
        string or list of strings to be examined

    Returns
    -------
    list[str] or str
    """
    if isinstance(input, list):
        return map(remove_accents_str, input)
    if isinstance(input, str):
        return remove_accents_str(input)


def remove_accents_str(string):
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

    return string
