# -*- coding: utf-8 -*-

def split_string_3_times(x, str_pre, str_after, str_last, index_keep_pre=1, index_keep_after=0, index_keep_last=0):
    """
    splits a string using 3 different substrings

    Parameters
    ----------
    x: str
        string to be splited
    str_pre, str_after, str_last: str
        substrings used to split the original string
    index_keep_pre, index_keep_after, index_keep_last: int
        int to select the part of the splited string

    Returns
    -------
    final_string: str
    """
    first_split = split_string(x, str_pre, str_after, index_keep_pre, index_keep_after)
    final_string = first_split.split(str_last)[index_keep_last]
    return final_string


def split_string(x, str_pre, str_after, index_keep_pre=1, index_keep_after=0):
    """
    splits a string using 2 different substrings

    Parameters
    ----------
    x: str
        string to be splited
    str_pre, str_after: str
        substrings used to split the original string
    index_keep_pre, index_keep_after: int
        int to select the part of the splited string

    Returns
    -------
    final_string: str
    """
    final_string = x.split(str_pre)[index_keep_pre].split(str_after)[index_keep_after]
    return final_string


def split_string_to_list(string, str_pre, str_after, index_keep_after=0, start_beginning=True, index=1):
    """
    Split a string based on the values that need to be found before and after the strings of interest

    Parameters
    ----------
    string: str
        string to be splited
    str_pre, str_after: str
        substrings used to split the original string
    index_keep_after: int
        index to keep when the str_after is used
    start_beginning: bool
        starts selecting a list from the beginning
    index: int
        index to use to select the splited list
    Returns
    -------
    list_str: list[str]
    """
    # split the string into a list
    splited_list = string.split(str_pre)

    # select the desired part of the list
    if start_beginning:
        splited_list = splited_list[index:]
    else:
        splited_list = splited_list[:-1]

    # apply splitting to each element of the list
    list_str = map(lambda x: x.split(str_after)[index_keep_after], splited_list)
    return list_str
