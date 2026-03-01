import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def generate_sean_graphs(OUTPUT_DIR="../../results/project1"):
    genres = ["Drama", "Action", "Sci-Fi", "Romance", "Comedy", "Horror"]
    ratings = [8.0, 7.5, 7.7, 7.0, 7.2, 6.9] #average ratings for all film genres

    # 1D Bar Chart
    fig1, ax1 = plt.subplots(figsize=(7, 5))
    ax1.bar(genres, ratings, edgecolor="black")
    ax1.set_ylim(6.5, 8.5)
    ax1.set_ylabel("Average Rating")
    ax1.set_xlabel("Film Genre")
    ax1.set_title("Average Film Ratings by Genre")
    ax1.tick_params(axis='x', rotation=25)
    ax1.grid(axis="y", linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/Sean_vis1.png", dpi=150)
    plt.show()

    #2D Pie Chart
    fig2, ax2 = plt.subplots(figsize=(7, 5))

    wedges, texts, autotexts = ax2.pie(
        ratings,
        labels = genres,
        autopct = '%1.1f',
        startangle = 90,
        wedgeprops = {"edgecolor": "white", "linewidth": 1.5}
    )

    ax2.set_title("Average Film Ratings by Genre")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/Sean_vis2.png", dpi=150)
    plt.show()

    #3D Bar Chart
    fig3 = plt.figure(figsize=(11, 7))
    ax3 = fig3.add_subplot(111, projection="3d")

    x_pos = np.arange(len(genres))
    y_pos = np.zeros(len(genres))
    z_pos = np.zeros(len(genres))

    dx = np.full(len(genres), 0.6)
    dy = np.full(len(genres), 0.6)
    dz = np.array(ratings, dtype=float)

    ax3.bar3d(
        x_pos, y_pos, z_pos,
        dx, dy, dz,
        shade=True,
        color = ["red", "yellow", "green", "brown", "purple", "cyan"],
        edgecolor="black",
        alpha=0.85
    )

    ax3.set_xticks(x_pos + dx[0] / 2)
    ax3.set_xticklabels(genres, rotation=20, ha="right", fontsize=6)
    ax3.set_yticks([])
    ax3.set_zlabel("Average Rating (0–10)")
    ax3.set_zlim(0, 10)
    ax3.set_title("Average Film Ratings by Genre")
    ax3.view_init(elev=22, azim=50)      
    ax3.set_proj_type("ortho")             
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/Sean_vis3.png", dpi=150)
    plt.show()