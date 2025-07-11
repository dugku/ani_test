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
    img = plt.imread(r"de_inferno_radar_psd.png")
    h, w = img.shape[:2]

    fig, ax = plt.subplots(figsize=(4, 10))
    ax.imshow(img, extent=[0, w, 0, h])


def make_polygon():
    path = r"C:\Users\micha\Desktop\animation_test\de_inferno_radar_psd.png"
    img_rgba = cv2.imread(path, cv2.IMREAD_UNCHANGED)

    alpha = img_rgba[..., 3]
    mask = alpha > 0

    img_rgb = img_rgba[..., :3].copy()
    img_rgb[~mask] = (255, 255, 255)

    gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    _, bw = cv2.threshold(gray,  # try thresh ~ 60–80 for Inferno
                          70,  # tweak!  lower values -> more floor
                          255,
                          cv2.THRESH_BINARY_INV)

    bw[~mask] = 0

    kernel = np.ones((5, 5), np.uint8)
    clean = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel, iterations=2)

    contours, hierarchy = cv2.findContours(
        clean,
        cv2.RETR_CCOMP,  # <-- get a 2-level hierarchy
        cv2.CHAIN_APPROX_SIMPLE
    )
    hierarchy = hierarchy[0]

    polys = []
    for idx, cnt in enumerate(contours):
        parent = hierarchy[idx][3]
        if parent != -1:
            continue

        holes = []
        child = hierarchy[idx][2]  # firstChild
        while child != -1:
            hole_cnt = contours[child].squeeze()
            if cv2.contourArea(hole_cnt) > 1_000:  # filter tiny specks
                holes.append(hole_cnt)
            child = hierarchy[child][0]  # next sibling

        polys.append(
            Polygon(cnt.squeeze(), [h for h in holes])  # exterior, list-of-holes
        )

    floor_poly = unary_union(polys).buffer(0)

    return floor_poly


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


floor_poly = make_polygon()

num_points_to_generate = 55
random_pts = random_points(floor_poly, num_points_to_generate)
mpoints = MultiPoint(random_pts)

voro = voronoi_diagram(mpoints, envelope=floor_poly, edges=False)

clipped_cells = [cell.intersection(floor_poly)
                 for cell in voro.geoms
                 if not cell.is_empty]

img = plt.imread(r"de_inferno_radar_psd.png")
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
plt.show()