import os
import pandas

from logger.Log import log
from pathlib import Path
from traceback import format_exc

from coordinates.CoordinatesCollector import CoordinatesCollector

class InfoExtoractor(object):
    """
    This class provides main controller to plot images
    """
    def __init__(self,api_url: str) -> None:

        self.api_url = api_url
        self.outputpath = str()

        return None

    def make_population_df(self, target_pref: str) -> pandas.DataFrame:
        """main controlelr to make images

        Args:
            target_pref (str): target prefecture name
        """
        collector = CoordinatesCollector(self.api_url)

        csvname = self.__get_csv_name(target_pref)
        if not csvname:
            return None

        root_dir = Path(os.path.dirname(__file__)).parent
        csvpath = os.path.join(root_dir, "constants", csvname)
        if not os.path.exists(csvpath):
            log.error(f"{csvpath} doesn't exist.")
            return None

        try:
            warddf = pandas.read_csv(csvpath)
            locationames = warddf["WardName"].tolist()
            addresses = warddf["Address"].tolist()
        except Exception:
            log.error(format_exc())
            return None

        if len(locationames) == 0:
            log.error(f"Failed to read {csvpath}")
            return None

        infovalues = list()
        for index_num in range(len(addresses)):
            lonlats = collector.get_lat_lon_from_address(addresses[index_num])
            if type(lonlats) != list or len(lonlats) != 2:
                return None
            infovalues.append([locationames[index_num], lonlats[0], lonlats[1]])

        lonlat_df = pandas.DataFrame(infovalues, columns=["WardName", "Longitude", "Latitude"])
        merged = pandas.merge(warddf, lonlat_df, on='WardName', how='left')

        return merged

    def __get_csv_name(self, key_name: str) -> str:
        """Returns ward filename of key_name

        Args:
            key_name (str): Prefeturename

        Returns:
            str: CSV Name
        """
        csvname = str()
        if "東京" in key_name:
            csvname = "tokyo_population.csv"
        else:
            log.error(f"Name: {key_name} is not supported.")

        return csvname