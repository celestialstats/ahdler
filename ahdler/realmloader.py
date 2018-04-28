import ahdler
import time
import requests
import json


class RealmLoader:
    _logger = ahdler.logger.get_logger(__name__)

    def load_realms(self, api_key, locale):
        req = requests.get('https://us.api.battle.net/wow/realm/status?locale=' + locale + '&apikey=' + api_key)
        realms = req.json()['realms']
        self._logger.info("Loaded {:,} realms.".format(len(realms)))
        return realms
