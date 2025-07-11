from parser import Parser
from plotter import plot_frames
import pprint
import polars as pl
def main():
    dem = Parser(file=r"C:\Users\Mike\Desktop\animation_test\novaq-vs-qmistry-m1-inferno.dem")
    dem.parse_demo()
    rounds = dem.filter_ticks()
    print(rounds)
if __name__ == "__main__":
    main()