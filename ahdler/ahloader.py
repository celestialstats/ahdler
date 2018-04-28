import ahdler
import time
import requests
import json
import pathlib
import os
import gzip


class AHLoader:
    _logger = ahdler.logger.get_logger(__name__)

    def RateLimited(maxPerSecond):
        minInterval = 1.0 / float(maxPerSecond)
        def decorate(func):
            lastTimeCalled = [0.0]
            def rateLimitedFunction(*args, **kargs):
                elapsed = time.clock() - lastTimeCalled[0]
                leftToWait = minInterval - elapsed
                if leftToWait > 0:
                    time.sleep(leftToWait)
                ret = func(*args, **kargs)
                lastTimeCalled[0] = time.clock()
                return ret
            return rateLimitedFunction
        return decorate

    @RateLimited(10)
    def get_download_info(self, api_key, realm, locale):
        req = requests.get('https://us.api.battle.net/wow/auction/data/' + realm + '?locale=' + locale + '&apikey=' + api_key)
        return req.json()

    def download_file(self, save_file, url):
        pathlib.Path(save_file).parent.mkdir(parents=True, exist_ok=True)
        r = requests.get(url, allow_redirects=True)
        gzip.open(save_file, 'wb').write(r.content)
        self._logger.info("\t\tDownloaded " +
                          os.path.basename(save_file) +
                          " (" + str(round(os.path.getsize(save_file) / 1024 / 1024, 2)) + " MB)"
        )
