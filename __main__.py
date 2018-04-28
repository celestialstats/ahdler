import argparse
import sys
import json
#import boto3
import zlib
import os.path
import re

from ahdler import *
from argparse import RawTextHelpFormatter
from time import sleep

_logger = logger.get_logger(__name__)
parser = argparse.ArgumentParser(
    description='CelestialStats Auction House Data Downloader',
    formatter_class=RawTextHelpFormatter
)
parser.add_argument(
    '--api-key',
    default=os.environ.get('AHDLER_API_KEY'),
    metavar='AHDLER_API_KEY',
    help='Battle.net API Key'
)
parser.add_argument(
    '--data-directory',
    default=os.environ.get('AHDLER_DATA_DIRECTORY'),
    metavar='AHDLER_DATA_DIRECTORY',
    help='Data Storage Directory'
)

def main(args=None):
    _logger.info("CelestialStats Auction House Data Downloader - Version 0.1")
    args = parser.parse_args()
    locale = 'en_US'
    urlregex = '^https?:\/\/.+\.worldofwarcraft\.com\/auction-data\/(?P<realmid>[a-z0-9]+)\/auctions.json$'
    loop_counter = 1

    while True:
        _logger.info("Beginning Realm Check (Loop " + str(loop_counter) + ")")
        realmloader = RealmLoader()
        ahloader = AHLoader()
        realms = realmloader.load_realms(args.api_key, locale)
        for cur_realm in realms:
            _logger.info("\t" + cur_realm['name'])
            file_info = ahloader.get_download_info(args.api_key, cur_realm['slug'], locale)
            if 'files' in file_info:
                realmid = re.match(urlregex, file_info['files'][0]['url']).group('realmid')
                destination_filename = os.path.join(args.data_directory, locale, cur_realm['slug'], str(file_info['files'][0]['lastModified']) + '-' + realmid + '.json.gz')
                if not os.path.isfile(destination_filename):
                    _logger.info("\t\tNewer Data Found!")
                    ahloader.download_file(destination_filename, file_info['files'][0]['url'])
                else:
                    _logger.info("\t\tNo New Data Found.")
            else:
                _logger.info("\t\tNo Files Found.")
        loop_counter = loop_counter + 1
    _logger.info("Done!")
    _logger.info("Exited.")


if __name__ == '__main__':
    # execute only if run as the entry point into the program
    main()