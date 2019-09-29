# -*- coding: utf-8 -*-
import urllib2
import time


class Scraper(object):

    def __init__(self, url):
        self._url = url

    def format_url(self, args):
        """
        format url that will be scrapped

        Parameters
        ----------
        args: dict
            params to format the url

        Returns
        -------
        url: str
            url to be read
        """
        return self._url.format(**args)

    def read_page(self, args, delay=0.1):
        """
        formats url and return html page

        Parameters
        ----------
        args: dict
            params to format the url
        delay: float or None
            delay between page requests. if None delay=0

        Returns
        -------
        page: str
            html page returned
        """

        if delay is not None:
            time.sleep(delay)

        # format url and request page
        formated_url = self.format_url(args)
        page = urllib2.urlopen(formated_url)

        return page.read()
