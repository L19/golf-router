import pandas as pd

from .spot import Station


class StationRepository:
    """駅情報をCSVファイルから読み込むリポジトリクラス

    Args:
        csv_path (str): 駅情報が記載されたCSVファイルのパス

    Attributes:
        __df (pd.DataFrame): 駅情報が記載されたCSVファイルを読み込んだDataFrame

    Examples:
    >>> repo = StationRepository("stations.csv")
    >>> repo.read(1)
    Station(id=1, name="東京駅", latitude=35.6814, longitude=139.7661)
    >>> repo.read_randomly(3)
    [
        Station(id=1, name="東京駅", latitude=35.6814, longitude=139.7661),
        Station(id=2, name="新大阪駅", latitude=34.7228, longitude=135.4961),
        Station(id=3, name="名古屋駅", latitude=35.1709, longitude=136.8816),
    ]
    >>> repo.read_all()
    [
        Station(id=1, name="東京駅", latitude=35.6814, longitude=139.7661),
        Station(id=2, name="新大阪駅", latitude=34.7228, longitude=135.4961),
        Station(id=3, name="名古屋駅", latitude=35.1709, longitude=136.8816),
        ...
    ]"""

    def __init__(self, csv_path: str):
        self.__df = pd.read_csv(csv_path)

    def read(self, id: int) -> Station:
        """指定したIDの駅情報を取得する

        Args:
            id (int): 駅ID

        Returns:
            Station: 駅情報
        """
        row = self.__df[self.__df["station_code"] == id].iloc[0]
        return Station(
            id=row["station_code"],
            name=row["station_name"],
            latitude=row["station_lat"],
            longitude=row["station_lon"],
        )

    def read_randomly(self, num=4) -> list[Station]:
        """ランダムに駅情報を取得する

        Args:
            num (int): 取得する駅情報の数

        Returns:
            list[Station]: 駅情報のリスト
        """
        return [
            Station(
                id=row["station_code"],
                name=row["station_name"],
                latitude=row["station_lat"],
                longitude=row["station_lon"],
            )
            for _, row in self.__df.sample(num).iterrows()
        ]
