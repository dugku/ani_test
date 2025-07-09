from shapely import geometry, voronoi_polygons
from shapely import Polygon, MultiPoint

import matplotlib.pyplot as plt
from shapely.plotting import plot_points, plot_polygon

coords = ((20, 50), (30,30), (80, 15), (95, 45), (64, 80), (25,67))
polygon = MultiPoint(coords)

voro = voronoi_polygons(polygon,  extend_to=polygon.envelope)

fig, ax = plt.subplots()

for poly in voro.geoms:
    x, y = poly.exterior.xy
    ax.fill(x , y, alpha=0.2, edgecolor='black')

plot_points(polygon, ax=ax, color="blue")

plt.show()