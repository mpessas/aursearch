# -*- coding: utf-8 -*-

"""
Interface with AUR for packages.
"""

import sys
import argparse
import json
import urllib
import logging


class QueryType(object):

    def __init__(self, term):
        self.logger = logging.getLogger('aursearch')
        self.term = term

    def url(self, type_):
        """Return the URL for the specified query."""
        url = 'http://aur.archlinux.org/rpc.php'
        url = ''.join([url, '?', 'type=', type_, '&arg=', self.term])    
        self.logger.info("URL is %s" % url)
        return url


class InfoQuery(QueryType):
    """Query type is info."""

    def __init__(self, name):
        super(InfoQuery, self).__init__(name)
        url = self.url()
        try:
            f = urllib.urlopen(url)
            self.info = json.loads(f.read())
        finally:
            f.close()
        self.logger.info(self.info)

    def url(self):
        return super(InfoQuery, self).url('info')

    def __str__(self):
        res = ''
        for key, value in self.info.iteritems():
            res += "%s: %s\n" % (key, value)
        return res


class SearchQuery(QueryType):
    """Query type is search."""

    def __init__(self, term):
        super(SearchQuery, self).__init__(term)
        url = self.url()
        try:
            f = urllib.urlopen(url)
            self.info = json.loads(f.read())
        finally:
            f.close()
        self.logger.info(self.info)        

    def url(self):
        return super(SearchQuery, self).url('search')

    def __str__(self):
        res = ''
        for key, value in self.info.iteritems():
            res += "%s: %s\n" % (key, value)
        return res


def setup_args():
    parser = argparse.ArgumentParser(description='Search AUR for a package')
    parser.add_argument(
        '-i', '--info', action='store_true', default=False,
        help=u'Show information for package'
    )
    parser.add_argument('term', help=u'The term to search for')
    parser.add_argument(
        '-v', '--verbose', action='store_true', help=u'Be verbose'
    )
    return parser.parse_args()

def main():
    args = setup_args()

    logger = logging.getLogger('aursearch')
    level = args.verbose and logging.INFO or logging.WARNING
    logger.setLevel(level)
    handler = logging.StreamHandler()
    logger.addHandler(handler)

    q = args.info and InfoQuery(args.term) or SearchQuery(args.term)

    print q
    


if __name__ == '__main__':
    sys.exit(main())
