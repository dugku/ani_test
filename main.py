from parser import Parser, frame_gen
from plotter import plot_frames
import polars as pl
def main():
    dem = Parser(file=r"C:\Users\Mike\Desktop\animation_test\novaq-vs-qmistry-m1-inferno.dem")
    dem.parse_demo()
    rounds = dem.filter_ticks()
    frames = frame_gen(rounds[5].roundNum, rounds[5].tick_df)

    plot_frames(frames)
if __name__ == "__main__":
    main()