from typing import Optional

from imageio import imread
import os
#from test_shape import make_polygon
from dataclasses import dataclass, field
from shapely import Polygon, MultiPoint, Point
from shapely.ops import voronoi_diagram
import random
from pathlib import Path
import json
from typing import Optional
from test_shape import make_polygon

"""
A Counter-Strike in this representation needs several things so that it can function:
    First:
        A polygon of the playable region so that so that later on when the p-median model
        is implemented we can check to see if a candidate position is within the polygon
    Second:
        A Voronoi Diagram, this will be imperative since I want to display map control somehow
        and this way is used in soccer analytics so at least I will be able to go off something
    Third:
        The accurate map scaling data, this will be needed to scale points so that we can plot them
        since the units are in a weird valve hammer unit thing.
"""
@dataclass
class CSmap:
    img_file: Path
    map_name: str
    playable_region: Polygon
    pos_x: float
    pos_y: float
    scale: float
    num_Rndpts: int

    random_pts: Optional[MultiPoint] = field(default=None, init=False)
    voronoi: Optional[Polygon] = field(default=None, init=False)

    def compute_voronoiDiagram(self):
        return voronoi_diagram(self.random_pts, envelope=self.playable_region, edges=False)

    def sample_pts(self):
        minx, miny, maxx, maxy = self.playable_region.bounds
        p = []
        for i in range(self.num_Rndpts):
            ran_pt = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))

            p.append(ran_pt)
        return p

def map_dataLoader(metaPath, imgPath):
    maps_data = []

    for i in os.listdir(metaPath):
        with open(metaPath + "\\" +i, 'rb') as f:
            data = json.load(f)
            map_name = i.split('.')[0]
            x, y, scale = data["pos_x"], data["pos_y"], data["scale"]
            img_p = imgPath + "\\" + map_name + "_radar_psd.png"
            C_map = CSmap(img_file=img_p, map_name=map_name, playable_region = make_polygon(img_p), pos_x = x, pos_y = y, scale = scale, num_Rndpts = 90)

            maps_data.append(C_map)

    return maps_data
