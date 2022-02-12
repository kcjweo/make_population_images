import requests
import time

from bs4 import BeautifulSoup
from logger.Log import log

class CoordinatesCollector(object):
    def __init__(self, api_url: str) -> None:
        """
        """
        self.api_url = api_url
        return None

    def get_lat_lon_from_address(self, address: str):
        """Get coordinates from location name
        reference: https://qiita.com/paulxll/items/7bc4a5b0529a8d784673
        """
        lonlats = []
        log.info(f"  Collecting coordinates.. {address}")

        payload = {"v": 1.1, 'q': address}
        r = requests.get(self.api_url, params=payload)
        ret = BeautifulSoup(r.content,'lxml')
        if ret.find('error'):
            raise ValueError(f"Invalid address submitted. {address}")
        else:
            lon = float(ret.find('lng').string)
            lat = float(ret.find('lat').string)
            lonlats = [lon,lat]
            time.sleep(5)

        if lon == 0 or lat == 0:
            log.error(f"Failed to get coordinates. {address}")
            log.error(f"This location will be ignored. {address}")
        return lonlats