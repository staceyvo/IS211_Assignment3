#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Create a program that returns a birthday or logs an error."""

import argparse
import csv
import re
import urllib2

from datetime import datetime


# download the web log file by a provided url using argparse
def download(url):
    """This function called download downloads the contents located at the url
        and returns it to the caller.

                Args:
                    url takes a string called url

                Returns:
                    Returns the contents located at the url.

        """
    response = urllib2.urlopen(url)
    return response.read()


# process file using csv module
def process(data):
    """This function called process will process the data using csv module.

                Args:
                    data holds our downloaded file

                Returns:
                    Returns userdata organized in a dictionary

        """
    items = data.split('\r\n')
    reader = csv.DictReader(items, fieldnames=[
        'path',
        'accessed',
        'browser',
        'status',
        'size'
    ])
    return [info for info in reader]


def search(userdata):
    """This function called search will search for images with regular expressions
                    Args:
                        userdata dictionary that holds image items and browser information

                    Returns:
                        Returns list of images found in weblog

       """

    return [info for info in userdata if re.search('\.(gif|jpg|png)$', info) is not None]


# find the most popular browser
def browser(userdata):
    """This function called browser will filter out image results by browser
                    Args:
                        userdata dictionary that holds image items and browser information

                    Returns:
                        Returns counts of browsers used

            """
    counts = {
        'Firefox': {'regex': ' Firefox/', 'count': 0},
        'Chrome': {'regex': ' Chrome/', 'count': 0},
        'Safari': {'regex': ' Safari/', 'count': 0},
        'MSIE': {'regex': ' MSIE', 'count': 0}
    }


    # loop on userdata

    for line in userdata['browser']:
        for key, value in counts.iteritems():
            regex = value['regex']
            if re.search(regex, line):
                value['count'] += 1



    # extra credit, print out hours and number of hits for all 24 hours in a day


def print_hits():
    raise Exception('Not implemented at this time')


if __name__ == '__main__':
    # 'http://s3.amazonaws.com/cuny-is211-spring2015/weblog.csv'
    # setting up argparse
    parser = argparse.ArgumentParser(description='weblog')
    parser.add_argument('--url', help='URL that represents browser user data', required=True)
    args = vars(parser.parse_args())

    data = download(args['url'])

    userdata = process(data)

    hits = search(userdata)
    print('Image requests account for {}% of all requests', len(hits) / float(len(userdata)))

    browser(userdata)

    print_hits()
