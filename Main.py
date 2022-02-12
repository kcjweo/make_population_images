import os
import pandas
import yaml

from traceback import format_exc

from data.InfoExtoractor import InfoExtoractor
from imageeditor.ImageEditor import ImageEditor


class Main(object):
    """
    1. Get population for each location.
    2. Concat population csv with it.
    3. Get Average of populuation at prefecture.
    4. Draw circle with red at the place which is apper than average.
    5. Draw circle with red at the place which is lower than average.
    """

    # Contains prefectural office coodinates
    __supported_names = {"東京都": [139.6921328842392, 35.68977795847866]}

    def __init__(self) -> None:

        self.__is_initialized = False

        self.outputpath = str()
        api_url = str()
        self.targets = list()

        current_path = os.path.dirname(__file__)
        conf_path = os.path.join(current_path, "conf", "settings.yaml")
        try:
            with open(conf_path, "r") as yml:
                config = yaml.safe_load(yml)
            self.outputpath = config["Output"]["path"]
            api_url = config["API"]["coordinate_url"]
            self.targets = config["Target_Prefecture"]
        except Exception:
            print(format_exc())
            print("Failed to import config.")

        self.extoractor = InfoExtoractor(api_url)
        # print(config)

        self.__is_initialized = True

        return None

    def main(self):

        if not self.__is_initialized:
            return None

        for target in self.targets:
            if target not in self.__supported_names:
                print(f"{target} is not supported.")
                print(f"Supported : {self.__supported_names} ")
                return None

            print(f"Start to create image for {target}")
            info_df = self.extoractor.make_population_df(target)
            if info_df is None or type(info_df) != pandas.DataFrame or info_df.empty:
                return None

            imageeditor = ImageEditor(self.outputpath)
            if not imageeditor.is_initialized():
                print("Failed to initialized Image Editor.")
                return None
            _ = imageeditor.make_images(info_df, self.__supported_names[target], target)
            imageeditor = None

        print("Completed.")


if __name__ == "__main__":
    main = Main()
    main.main()
