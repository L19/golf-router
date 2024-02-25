from dataclasses import dataclass
import math


@dataclass
class Spot:
    """特定の地点を表すクラス

    Attributes:
        id (int): 地点のID
        name (str): 地点の名前
        latitude (float): 地点の緯度
        longitude (float): 地点の経度
    """

    id: int
    name: str
    latitude: float
    longitude: float

    def __str__(self):
        return f"{self.id}: {self.name} ({self.latitude}, {self.longitude})"

    def calculate_distance(self, other: "Spot") -> float:
        """2つの地点間の距離を計算する

        Args:
            other (Spot): 他の地点

        Returns:
            float: 2つの地点間の距離
        """
        # approximate radius of earth in km
        R = 6373.0

        lat1 = math.radians(self.latitude)
        lon1 = math.radians(self.longitude)
        lat2 = math.radians(other.latitude)
        lon2 = math.radians(other.longitude)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return R * c

    @staticmethod
    def convert_to_decimal_degrees(
        degrees: float, minutes: float, seconds: float
    ) -> float:
        return degrees + minutes / 60 + seconds / 3600


@dataclass
class GolfCourse(Spot):
    """ゴルフ場を表すクラス"""

    pass


@dataclass
class Station(Spot):
    """駅を表すクラス"""

    pass
