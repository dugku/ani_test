from awpy import Demo
from awpy.plot import gif, PLOT_SETTINGS
from tqdm import tqdm
import polars as pl
from translate_scale import translate_scale

def parse(filename):
    dem = Demo(filename)
    dem.parse(player_props=["health", "armor_value", "pitch", "yaw" ])

    return dem

def filter_ticks(dem):
    frames = []

    for tick in tqdm(dem.ticks.filter(pl.col("round_num") == 10)["tick"].unique().to_list()[::3]):
        frame_df = dem.ticks.filter(pl.col("tick") == tick)
        frame_df = frame_df[
            ["X", "Y", "Z", "health", "armor", "pitch", "yaw", "side", "name"]
        ]

        points = []
        point_settings = []

        for row in frame_df.iter_rows(named=True):
            p = (row["X"], row["Y"])

            x, y = translate_scale(p)

            points.append((x,y))

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

        frames.append({
            "points": points, 
             "style": point_settings
        })

    return frames

        