from typing import Sequence, Union
from itertools import permutations

from googlemaps import Client

from .spot import GolfCourse, Station


def find_route_by_distance(
    start: Station, vias: Sequence[Station], goal: GolfCourse
) -> tuple[Sequence[Union[GolfCourse, Station]], float]:
    """出発地から経由地を経由して目的地までの最短経路とその距離を求める

    Args:
        start (Station): 出発地
        vias (Sequence[Station]): 経由地
        goal (GolfCourse): 目的地

    Returns:
        tuple[Sequence[Union[GolfCourse, Station]], float]: 最短経路とその距離

    Examples:
    >>> start = Station(1, "東京駅", 35.6814, 139.7661)
    >>> vias = [
        ...     Station(2, "新大阪駅", 34.7228, 135.4961),
        ...     Station(3, "名古屋駅", 35.1709, 136.8816),
        ... ]
    >>> goal = GolfCourse(1, "東京ゴルフ倶楽部", 35.6895, 139.6917)
    >>> find_route_by_distance(start, vias, goal)
    ([
        Station(id=1, name="東京駅", latitude=35.6814, longitude=139.7661),
        Station(id=3, name="名古屋駅", latitude=35.1709, longitude=136.8816),
        Station(id=2, name="新大阪駅", latitude=34.7228, longitude=135.4961),
        GolfCourse(id=1, name="東京ゴルフ倶楽部", latitude=35.6895, longitude=139.6917),
    ], 641.0)
    """

    dist_min, route_min = float("inf"), []
    for idxs in permutations(range(len(vias)), len(vias)):
        dist = start.calculate_distance(vias[idxs[0]])
        for i in range(len(idxs) - 1):
            dist += vias[idxs[i]].calculate_distance(vias[idxs[i + 1]])
        dist += vias[idxs[-1]].calculate_distance(goal)
        if dist < dist_min:
            dist_min = dist
            route_min = [start] + [vias[idx] for idx in idxs] + [goal]

    return route_min, dist_min


def find_route_by_gmaps(
    client: Client, start: Station, vias: Sequence[Station], goal: GolfCourse, **kwargs
) -> tuple[Sequence[Union[GolfCourse, Station]], int]:
    """出発地から経由地を経由して目的地までの最短経路とその所要時間を Google Maps API を用いて求める

    Args:
        client (Client): Google Maps API クライアント
        start (Station): 出発地
        vias (Sequence[Station]): 経由地
        goal (GolfCourse): 目的地
        **kwargs: キーワード引数

    Returns:
        tuple[Sequence[Union[GolfCourse, Station]], int]: 最短経路とその所要時間
    """
    waypoints = [f"{via.latitude},{via.longitude}" for via in vias]
    directions_result = client.directions(
        f"{start.latitude},{start.longitude}",
        f"{goal.latitude},{goal.longitude}",
        waypoints=waypoints,
        mode="driving",
        optimize_waypoints=True,
        **kwargs,
    )

    route = [start] + [vias[i] for i in directions_result[0]["waypoint_order"]] + [goal]
    duration = sum([leg["duration"]["value"] for leg in directions_result[0]["legs"]])

    return route, duration
