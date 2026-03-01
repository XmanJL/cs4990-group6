"""
Stevens' Law visualizations - 1D (line plot), 2D (pie chart / area), 3D (bubble volume)
Topic: Monthly streaming hours by platform
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def makeGraphs(OUTPUT_DIR="../../results/project1"):

		# ── VIS 1: 1D Bar Chart ──────────────────────────────────────────────────────
	# Shows streaming hours per platform as a bar chart (1D length encoding)
	platforms = ["Netflix", "YouTube", "Hulu", "Disney+", "HBO Max"]
	hours     = [42, 65, 28, 35, 50]
	colors    = ["#E50914", "#FF0000", "#3DBB3D", "#113CCF", "#B5179E"]

	fig, ax = plt.subplots(figsize=(7, 5))
	bars = ax.bar(platforms, hours, color=colors, edgecolor="black", width=0.6)



	ax.set_ylabel("Average Monthly Hours")
	ax.set_title("Average Monthly Streaming Hours by Platform")
	ax.set_ylim(0, 80)
	ax.grid(axis="y", linestyle="--", alpha=0.5)
	plt.tight_layout()
	plt.savefig(f"{OUTPUT_DIR}/Diego_vis1.png", dpi=150)
	plt.show()

	
	
	# ── VIS 2: 2D Pie Chart ──────────────────────────────────────────────────────
	# Same data encoded as pie slices (2D angle/area encoding)
	colors = ["#E50914", "#FF0000", "#3DBB3D", "#113CCF", "#B5179E"]
	
	fig, ax = plt.subplots(figsize=(7, 5))
	wedges, texts, autotexts = ax.pie(
	    hours, labels=platforms, colors=colors,
	    autopct="", startangle=90,
	    wedgeprops={"edgecolor": "white", "linewidth": 1.5}
	)
	for at in autotexts:
	    at.set_fontsize(9)
	ax.set_title("Average Monthly Streaming Hours by Platform")
	plt.tight_layout()
	plt.savefig(f"{OUTPUT_DIR}/Diego_vis2.png", dpi=150)
	plt.show()
	
	
	# ── VIS 3: 3D Bar Chart ───────────────────────────────────────────────────
	fig3 = plt.figure(figsize=(12, 7))
	ax   = fig3.add_subplot(111, projection="3d")
	
	x_pos = np.arange(len(platforms))
	dx, dy = 0.5, 0.5

	ax.bar3d(x_pos, np.zeros(len(platforms)), np.zeros(len(platforms)),
	         dx, dy, hours,
	         color=colors, edgecolor="black", alpha=0.85, shade=True)
	
	
	
	ax.set_title("Average Monthly Streaming Hours by Platform\n(3D Bar – Volume Encoding)", fontsize=13, pad=20)
	ax.set_xticks(x_pos + dx/2)
	ax.set_xticklabels(platforms, fontsize=10)
	ax.set_yticks([])
	ax.set_zlabel("Hours", labelpad=10)
	ax.set_zlim(0, 80)
	ax.view_init(elev=25, azim=30)
	ax.set_proj_type("ortho")
	plt.savefig(f"{OUTPUT_DIR}/Diego_vis3.png", dpi=150)
	plt.show()
	