import imageio
import matplotlib.pyplot as plt
import imageio.v3 as iio
from tqdm import tqdm

def plot_frames(frames):
    filenames = []
    count = 0

    img = plt.imread(r'C:\Users\Mike\Desktop\animation_test\de_inferno_radar_psd.png')
    h, w = img.shape[:2]

    for i in tqdm(frames):
        count += 1
        ct_alive = []
        t_alive = []
        for points, styles in zip(i["points"], i["style"]):
            
            if styles["hp"]  == 0:
                continue
            
            if styles["color"] == "tab:cyan":
                ct_alive.append(points)
            if styles["color"] == "tab:olive":
                t_alive.append(points)

        ct_x_coords = [k[0] for k in ct_alive]
        ct_y_coords = [h - k[1] for k in ct_alive]

        t_x_coords = [k[0] for k in t_alive]
        t_y_coords = [h - k[1] for k in t_alive]


        fig, ax = plt.subplots(figsize=(10, 10))
        ax.imshow(img, extent=[0, w, 0, h]) 

        ax.scatter(ct_x_coords, ct_y_coords, color="cyan", )
        ax.scatter(t_x_coords, t_y_coords, color="yellow")

        fname = f"C:\\Users\\Mike\\Desktop\\animation_test\\frames_done\\frame_{count}.png"
        fig.savefig(fname, dpi=120, bbox_inches="tight")
        plt.close(fig)          
        filenames.append(fname)

    make_gif(tqdm(filenames))

def make_gif(filenames):
    writer = imageio.get_writer('test.mp4', fps=30)
    for im_path in filenames:  # Sort to ensure correct frame order
        im = iio.imread(im_path)
        writer.append_data(im)
    writer.close()

