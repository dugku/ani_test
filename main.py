from parser import parse, filter_ticks
from plotter import plot_frames
import pprint
def main():
    dem = parse(r"C:\Users\Mike\Desktop\animation_test\novaq-vs-qmistry-m1-inferno.dem")
    frames = filter_ticks(dem)
    plot_frames(frames)
if __name__ == "__main__":
    main()