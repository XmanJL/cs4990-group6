# Jasper's work for Project 1
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_jasper_graphs(OUTPUT_DIR="../../results/project1"):
    
    # figure 1: 1D bar plot
    ethnicities = ["Chinese", "Japanese", "Mexican", "American"]
    scores = [6, 8.5, 7, 8]
    plt.bar(ethnicities, scores, color="blue")
    plt.ylabel("Average Score (out of 10)")
    plt.title("Average Exam Scores by Ethnicity")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/vis1.png", dpi=100)
    plt.show()

    # figure 2: 2D square plot
    squares = [
        ("PS5", 0, 1.25, 6),             # bottom-left
        ("Xbox", 10, 0, 8.5),            # bottom-right
        ("Switch", 0, 12, 7),            # top-left
        ("Nintendo", 10, 12, 8)          # top-right
    ]    
    fig, ax = plt.subplots()
    for name, x, y, side in squares:
        square = patches.Rectangle((x, y), side, side, facecolor="#FFCBA4", 
                                   edgecolor="black")
        mid_x = x + side / 2
        mid_y = y + side / 2
        ax.text(mid_x, mid_y, name, ha='center', va='center', color="black")
        ax.add_patch(square)

    ax.set_aspect('equal') 
    ax.autoscale()
    plt.title("Average Chess Board Sizes in different shops")
    plt.xlabel("Shop")
    plt.ylabel("Size (cm)")
    plt.savefig(f"{OUTPUT_DIR}/vis2.png", dpi=100)
    plt.show()

    # figure 3: 3D cube plot
    # name, color, x, y, side
    cubes = [
        ("Georgia", "red", 0, 0, 6),          # bottom-left
        ("Nevada", "lightblue", 0, 14, 7),    # top-left
        ("California", "green", 14, 0, 8),    # bottom-right
        ("Texas", "orange", 14, 14, 8.5),     # top-right
    ]
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    for name, color, x, y, s in cubes:
        ax.bar3d(x, y, 0, s, s, s, color=color, edgecolor="black", shade=True, alpha=0.6, label=name)

    ax.legend()
    
    xs = [x for _, _, x, _, _ in cubes] + [x + s for _, _, x, _, s in cubes]
    ys = [y for _, _, _, y, _ in cubes] + [y + s for _, _, _, y, s in cubes]

    max_xy = max(max(xs) - min(xs), max(ys) - min(ys))
    x0, x1 = min(xs), min(xs) + max_xy
    y0, y1 = min(ys), min(ys) + max_xy
    ax.set_xlim(x0, x1)
    ax.set_ylim(y0, y1)
    ax.set_zlim(0, max_xy)

    ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev=20, azim=35)
    ax.set_proj_type("ortho")
    ax.set_title("Average Magic Cube Sizes in Different Countries")
    plt.savefig(f"{OUTPUT_DIR}/vis3.png", dpi=100)
    plt.show()