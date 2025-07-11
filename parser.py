from awpy import Demo
from awpy.plot import gif, PLOT_SETTINGS
from tqdm import tqdm
import polars as pl
from translate_scale import translate_scale
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional
from pathlib import Path


@dataclass
class Parser:
    dem = Demo
    file: Path
    map_name: Optional[str] = ""

    def parse_demo(self):
        self.dem = Demo(self.file)
        self.dem.parse(player_props=["health", "armor_value", "pitch", "yaw"])
        header = self.dem.parse_header()

        self.map_name = header["map_name"]

    def filter_ticks(self):
        round_ids = (
            self.dem.rounds
            .select("round_num")
            .unique()
            .sort("round_num")
            ["round_num"]
            .to_list()
        )
        r = []

        for i in tqdm(round_ids):
            round_meta = self.dem.rounds.filter(pl.col("round_num") == i).select(
                "freeze_end", "official_end"
            ).row(0)

            samp_tick = self.dem.ticks.filter(
                (pl.col("round_num") == i) &
                (pl.col("tick") >= round_meta[0]) &
                (pl.col("tick") <= round_meta[1])
            ).sort("tick")

            round = RoundState(roundNum=i, startTick=round_meta[0], endTick=round_meta[1], tick_df=samp_tick)

            r.append(round)

        return r


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

def frame_gen(round_num, tick_df):
    frames = []
    print("Frames")
    for tick in tqdm(tick_df.filter(pl.col("round_num") == round_num)["tick"].unique().to_list()[::2]):
        frame_df = tick_df.filter(pl.col("tick") == tick)
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
    return frames
        