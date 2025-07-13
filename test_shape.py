from shapely import geometry, voronoi_polygons
from shapely import Polygon, MultiPoint, Point
import random
import matplotlib.pyplot as plt
from shapely.plotting import plot_points, plot_polygon
import cv2
import numpy as np
from shapely.ops import unary_union, voronoi_diagram
from shapely.geometry import Polygon, MultiPolygon, GeometryCollection


def plot_map():
    img = plt.imread(r"radar_images/de_inferno_radar_psd.png")
    h, w = img.shape[:2]

    fig, ax = plt.subplots(figsize=(4, 10))
    ax.imshow(img, extent=[0, w, 0, h])


def make_polygon(img_p):
    img = cv2.imread(img_p, cv2.IMREAD_UNCHANGED)
    alpha = img[..., 3]
    mask_a = alpha > 0

    num, labels, stats, _ = cv2.connectedComponentsWithStats(
        alpha.astype(np.uint8), connectivity=8
    )

    if num <= 1:
        raise RuntimeError("No painted pixels!")
    biggest = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])

    floor_mask = (labels == biggest).astype(np.uint8) * 255

    clean = cv2.morphologyEx(floor_mask, cv2.MORPH_CLOSE,
                             kernel=np.ones((5, 5), np.uint8), iterations=2)

    contours, hier = cv2.findContours(clean, cv2.RETR_CCOMP,
                                      cv2.CHAIN_APPROX_SIMPLE)
    hier = hier[0]

    polys = []
    for idx, cnt in enumerate(contours):
        if hier[idx][3] != -1:
            continue
        cnt = cnt.squeeze()
        if cnt.shape[0] < 4:
            continue
        holes = []
        child = hier[idx][2]
        while child != -1:
            h = contours[child].squeeze()
            if h.shape[0] >= 4:
                holes.append(h)
            child = hier[child][0]
        polys.append(Polygon(cnt, holes))


    return unary_union(polys).buffer(0)


def random_points(polygon, num_points):
    points = []
    min_x, min_y, max_x, max_y = polygon.bounds
    while len(points) < num_points:
        random_point = Point(random.uniform(min_x, max_x), random.uniform(min_y, max_y))
        if polygon.contains(random_point):
            points.append(random_point)
    return points


def iter_polys(g):
    """Yield every Polygon buried inside g (Polygon, MultiPolygon, or GeometryCollection)."""
    if isinstance(g, Polygon):
        yield g
    elif isinstance(g, (MultiPolygon, GeometryCollection)):
        for sub in g.geoms:
            yield from iter_polys(sub)


"""floor_poly = make_polygon()

num_points_to_generate = 55
random_pts = random_points(floor_poly, num_points_to_generate)
mpoints = MultiPoint(random_pts)

voro = voronoi_diagram(mpoints, envelope=floor_poly, edges=False)

clipped_cells = [cell.intersection(floor_poly)
                 for cell in voro.geoms
                 if not cell.is_empty]

img = plt.imread(r"radar_images/de_inferno_radar_psd.png")
h, w = img.shape[:2]
fig, ax = plt.subplots(figsize=(4, 10))
ax.imshow(img, extent=[0, w, 0, h], origin="lower")

for cell in clipped_cells:
    for poly in iter_polys(cell):
        x, y = poly.exterior.xy

        ax.fill(x, y, facecolor="none", edgecolor="black")

# outline & seeds as before
plot_polygon(floor_poly, ax=ax, facecolor="none", edgecolor="blue")

ax.set_aspect("equal")
ax.invert_yaxis()

plt.tight_layout()
plt.show()"""