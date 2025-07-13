import imageio
import matplotlib.pyplot as plt
import imageio.v3 as iio
from imageio import imread
from tqdm import tqdm
import os
from shapely.plotting import plot_points, plot_polygon
from shapely.geometry import Polygon, MultiPolygon, GeometryCollection

def plot_frames(ax, frame, h):
    ct_alive = []
    t_alive = []
    for points, styles in zip(frame["points"], frame["style"]):

        if styles["hp"]  == 0:
            continue

        if styles["color"] == "tab:cyan":
            ct_alive.append(points)
        if styles["color"] == "tab:olive":
            t_alive.append(points)

    ct_x_coords = [k[0] for k in ct_alive]
    ct_y_coords = [k[1] for k in ct_alive]
    t_x_coords = [k[0] for k in t_alive]
    t_y_coords = [k[1] for k in t_alive]

    ax.scatter(ct_x_coords, ct_y_coords, color="cyan", s=5)
    ax.scatter(t_x_coords, t_y_coords, color="yellow", s=5)


def make_gif(filenames):
    writer = imageio.get_writer('test.mp4', fps=30)
    for im_path in filenames:  # Sort to ensure correct frame order
        im = iio.imread(im_path)
        writer.append_data(im)
    writer.close()

def plot_playable(polygon):
    fig, ax = plt.subplots()

    plot_polygon(polygon, ax=ax, add_points=False, color='purple')

    # Set equal aspect ratio
    ax.set_aspect('equal')

    # Display the plot
    ax.invert_yaxis()
    plt.show()

def iter_polys(g):
    """Yield every Polygon buried inside g (Polygon, MultiPolygon, or GeometryCollection)."""
    if isinstance(g, Polygon):
        yield g
    elif isinstance(g, (MultiPolygon, GeometryCollection)):
        for sub in g.geoms:
            yield from iter_polys(sub)

def plot_voro(voro, playable,img):
    diaplay_img = plt.imread(img)
    h, w = diaplay_img.shape[:2]

    fig, ax = plt.subplots()
    ax.imshow(diaplay_img, extent=[0, w, 0, h], origin="lower")

    clipped_cell = [cell.intersection(playable)
                 for cell in voro.geoms
                 if not cell.is_empty]

    for cell in clipped_cell:
        for poly in iter_polys(cell):
            x, y = poly.exterior.xy

            ax.fill(x, y, facecolor="none", edgecolor="black")

    plot_polygon(playable, ax=ax, facecolor="none", edgecolor="blue")

    ax.set_aspect("equal")
    ax.invert_yaxis()

    plt.tight_layout()
    plt.show()

def plot_voroFrame(poly, voro, ax):
    cl_cells = [cell.intersection(poly)
                for cell in voro.geoms
                if not cell.is_empty]

    for cell in cl_cells:
        for poly in iter_polys(cell):
            x, y = poly.exterior.xy
            ax.fill(x, y, facecolor="none", edgecolor="black")


def plotter_handler(frames, map_d, out_dir):
    poly = map_d.playable_region
    voro = map_d.voronoi

    fig, ax = plt.subplots()
    img = plt.imread(map_d.img_file)
    w, h = img.shape[:2]
    filenames = []

    for tick, frame in enumerate(frames, start=1):
        ax.cla()
        ax.imshow(img, extent=[0, w, 0, h], origin="lower")

        plot_voroFrame(poly, voro, ax)
        plot_frames(ax, frame, h)

        ax.invert_yaxis()
        ax.set_xlim([0, w]); ax.set_ylim([0, h])

        filena = os.path.join(out_dir, f"frame_{tick}.png")
        filenames.append(filena)
        fig.savefig(filena, dpi=250, bbox_inches='tight')

    make_gif(filenames)