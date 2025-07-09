from shapely import geometry, voronoi_polygons
from shapely import Polygon, MultiPoint

import matplotlib.pyplot as plt
from shapely.plotting import plot_points, plot_polygon

coords = ((20, 50), (30,30), (80, 15), (95, 45), (64, 80), (25,67))
polygon = MultiPoint(coords)

voro = voronoi_polygons(polygon, only_edges=True)

fig, ax = plt.subplots()

plot_points(polygon, ax=ax, color="red", zorder=3)
for poly in voro.geoms:
    plot_polygon(poly, ax=ax, facecolor="none", edgecolor="black")

plt.show()