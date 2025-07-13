from pandas.core.sample import sample
from shapely import MultiPoint

from parser import Parser, frame_gen
from plotter import plot_frames, plot_playable, plot_voro, plotter_handler
from map_classes import CSmap, map_dataLoader
import polars as pl
from tqdm import tqdm

imgPa = r"C:\Users\Mike\Desktop\animation_test\radar_images"
mataPa = r"C:\Users\Mike\Desktop\animation_test\metadata"
out_dir = r"C:\Users\Mike\Desktop\animation_test\frames_done"
def main():
    map_data = map_dataLoader(mataPa, imgPa)
    dem = Parser(file="novaq-vs-qmistry-m1-inferno.dem")
    dem.parse_demo()

    rounds = dem.filter_ticks()
    frames = frame_gen(rounds[5].roundNum, rounds[5].tick_df)

    data = None
    for m in map_data:
        if m.map_name == dem.map_name:
            data = m
            break
    print(data.scale, data.pos_x, data.pos_y)

    data.random_pts = MultiPoint(data.sample_pts())
    data.voronoi = data.compute_voronoiDiagram()

    tqdm(plotter_handler(frames, data, out_dir))

    #plot_frames(frames)
if __name__ == "__main__":
    main()