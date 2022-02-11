import os
from staticmap import StaticMap, CircleMarker
from traceback import format_exc

import pandas

class ImageEditor(object):
    
    def __init__(self, outputpath: str) -> None:
        """
        Args:
            outputpath (str): Path to output images
        """
        self.__is_initialized = False

        self.outputpath = outputpath

        try:
            os.makedirs(self.outputpath, exist_ok=True)
        except Exception:
            print(format_exc())
            print(f"Failed to create folder {self.outputpath}")
            return None

        if not os.path.exists(self.outputpath):
            print(f"Failed to create folder {self.outputpath}")
            return None

        self.__is_initialized = True

        return None

    def is_initialized(self) -> bool:
        """Returns initialization result
        """

        return self.__is_initialized

    def make_images(self, info_df: pandas.DataFrame, center_lonlats: list, target: str) -> None:
        """Make Images

        Args:
            info_df (pandas.DataFrame): infomation of pupulation, locationname and coordinates
            center_lonlats(list): prefectural office coodinates. This will be Center of Image.
            target(str): target prefecture name

        """
        print("Start to make Map.")

        if info_df is None or type(info_df) != pandas.DataFrame or info_df.empty:
            return None
        population_average = int(info_df["Population"].mean())

        basemap = StaticMap(800, 800, url_template='http://a.tile.osm.org/{z}/{x}/{y}.png')

        for index, row in info_df.iterrows():
            if row["Population"] >= population_average:
                color = "red"
            else:
                color = "blue"
            if row["Longitude"] == 0 or row["Latitude"] == 0:
                continue
            marker = CircleMarker((row["Longitude"], row["Latitude"]), color, 20)
            basemap.add_marker(marker)

        image = basemap.render(zoom=11, center=center_lonlats)

        imagename = os.path.join(self.outputpath, target) + ".png"
        image.save((imagename))
        print(f"Saved Image : {imagename}")

        return None
        