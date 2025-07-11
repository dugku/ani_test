from awpy import Demo
from awpy.plot import gif, PLOT_SETTINGS
from tqdm import tqdm
import polars as pl
from translate_scale import translate_scale
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional


@dataclass
class Praser:
    dem = Demo
    file: str
    map_name: Optional[str] = ""

    def parse_demo(self):
        self.dem = Demo(self.file)
        self.dem.parse(player_props=["health", "armor_value", "pitch", "yaw"])
        header = self.dem.parse_header()

        self.map_name = header["map_name"]

    def filter_ticks(self):
        rounds = self.dem.rounds.select(
            pl.col("round_num").count()
        ).item()

        r = []

        for i in tqdm(range(rounds)):
            for tick in self.dem.ticks.filter(pl.col("round_num") == i + 1)["tick"].unique().to_list()[::10]:
                round_df = self.dem.ticks.filter(pl.col("tick") == tick)
                s_tick = self.dem.rounds.filter(pl.col("round_num") == i + 1)["start"].item()
                offical_end = self.dem.rounds.filter(pl.col("round_num") == i + 1)["official_end"].item()

                r_state = RoundState(roundNum=i + 1, startTick=s_tick, endTick=offical_end, tick_df=round_df)

                r.append(r_state)

        return rounds


@dataclass
class Map_Data:
    pass


@dataclass
class PlayerState:
    steam_id: int
    name: str
    side: str
    color: str
    track_pos = List[Tuple[float, float]]

    def add_pos(self, px: float, py: float):
        self.track_pos.append((px, py))

    @property
    def last_pos(self):
        return self.track_pos[-1]


@dataclass
class RoundState:
    roundNum: int
    startTick: int
    endTick: int
    tick_df: pl.DataFrame

    _players: Dict[int, pl.DataFrame] = field(default_factory=dict)


@dataclass
class Frames:
    pass


def parse(filename):
    dem = Demo(filename)
    dem.parse(player_props=["health", "armor_value", "pitch", "yaw"])

    return dem


def filter_ticks(dem):
    frames = []

    for tick in tqdm(dem.ticks.filter(pl.col("round_num") == 1)["tick"].unique().to_list()[::128]):
        frame_df = dem.ticks.filter(pl.col("tick") == tick)
        frame_df = frame_df[
            ["X", "Y", "Z", "health", "armor", "pitch", "yaw", "side", "name"]
        ]

        points = []
        point_settings = []

        for row in frame_df.iter_rows(named=True):
            p = (row["X"], row["Y"])

            x, y = translate_scale(p)

            points.append((x, y))

            settings = PLOT_SETTINGS[row["side"]].copy()

            # Add additional settings
            settings.update(
                {
                    "hp": row["health"],
                    "armor": row["armor"],
                    "direction": (row["pitch"], row["yaw"]),
                    "label": row["name"],
                }
            )
            point_settings.append(settings)
        # frames is just List[Dict[str, Points], Dict[str, style]]
        frames.append({
            "points": points,
            "style": point_settings
        })
    print(type(frames))
    return frames
        