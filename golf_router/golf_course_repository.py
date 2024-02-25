import pandas as pd

from .spot import GolfCourse


class GolfCourseRepository:
    """ゴルフ場情報をCSVファイルから読み込むリポジトリクラス

    Args:
        csv_path (str): ゴルフ場情報が記載されたCSVファイルのパス

    Attributes:
    __df (pd.DataFrame): ゴルフ場情報が記載されたCSVファイルを読み込んだDataFrame

    Examples:
    >>> repo = GolfCourseRepository("golf_courses.csv")
    >>> repo.read(1)
    GolfCourse(id=1, name="東京ゴルフ倶楽部", latitude=35.6895, longitude=139.6917)
    >>> repo.read_randomly(3)
    [
        GolfCourse(id=1, name="東京ゴルフ倶楽部", latitude=35.6895, longitude=139.6917),
        GolfCourse(id=2, name="大阪ゴルフ倶楽部", latitude=34.6937, longitude=135.5023),
        GolfCourse(id=3, name="名古屋ゴルフ倶楽部", latitude=35.1815, longitude=136.9066),
    ]
    >>> repo.read_all()
    [
        GolfCourse(id=1, name="東京ゴルフ倶楽部", latitude=35.6895, longitude=139.6917),
        GolfCourse(id=2, name="大阪ゴルフ倶楽部", latitude=34.6937, longitude=135.5023),
        GolfCourse(id=3, name="名古屋ゴルフ倶楽部", latitude=35.1815, longitude=136.9066),
        ...
    ]
    """

    def __init__(self, csv_path: str):
        self.__df = pd.read_csv(csv_path)

    def read(self, id: int) -> GolfCourse:
        """指定したIDのゴルフ場情報を取得する

        Args:
            id (int): ゴルフ場ID

        Returns:
            GolfCourse: ゴルフ場情報
        """
        row = self.__df[self.__df["id"] == id].iloc[0]
        return GolfCourse(
            id=row["id"],
            name=row["golfCourseName"],
            latitude=row["latitude"],
            longitude=row["longitude"],
        )

    def read_randomly(self, num=1) -> list[GolfCourse]:
        """ランダムにゴルフ場情報を取得する

        Args:
            num (int): 取得するゴルフ場情報の数

        Returns:
            list[GolfCourse]: ゴルフ場情報のリスト
        """
        return [
            GolfCourse(
                id=row["id"],
                name=row["golfCourseName"],
                latitude=row["latitude"],
                longitude=row["longitude"],
            )
            for _, row in self.__df.sample(num).iterrows()
        ]

    def read_all(self) -> list[GolfCourse]:
        """全てのゴルフ場情報を取得する

        Returns:
            list[GolfCourse]: ゴルフ場情報のリスト
        """
        return [
            GolfCourse(
                id=row["id"],
                name=row["golfCourseName"],
                latitude=row["latitude"],
                longitude=row["longitude"],
            )
            for _, row in self.__df.iterrows()
        ]
