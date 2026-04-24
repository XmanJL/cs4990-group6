import os
import numpy as np
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from matplotlib.path import Path
import pandas as pd
from preprocess import preprocess

def plot_parallel_coordinates(df):
	# mapping labels
	RACE_LABELS = {
		1: "White",
		2: "Black",
		4: "Asian",
	}
	RACE_COLORS = {
		"White": "#1f77b4",
		"Black": "#ff9896",
		"Asian": "#98df8a",   
	}

	# plotting function that borrows the idea from 
	# https://stackoverflow.com/questions/8230638/parallel-coordinates-plot-in-matplotlib
	columns = ["RACE", "YEAR", "POP_0_19", "POP_20_39", "POP_40_59", "POP_60_79", "POP_80_100"]
	axis_names = ["YEAR", "POP_0_19", "POP_20_39", "POP_40_59", "POP_60_79", "POP_80_100"]
	plot_df = df.loc[:, columns].copy()
	plot_df["RACE"] = plot_df["RACE"].map(RACE_LABELS)
	plot_df = plot_df.dropna(subset=["RACE"])

	for column in axis_names:
		plot_df[column] = pd.to_numeric(plot_df[column], errors="coerce")
	plot_df = plot_df.dropna(subset=axis_names)
	plot_df = plot_df.sort_values(["RACE", "YEAR"])

	values = plot_df[axis_names].to_numpy(dtype=float)
	ymins = values.min(axis=0)
	ymaxs = values.max(axis=0)
	dys = ymaxs - ymins
	ymins = ymins - dys * 0.05
	ymaxs = ymaxs + dys * 0.05
	dys = ymaxs - ymins

	zs = np.zeros_like(values)
	zs[:, 0] = values[:, 0]
	zs[:, 1:] = (values[:, 1:] - ymins[1:]) / dys[1:] * dys[0] + ymins[0]

	fig, host = plt.subplots(figsize=(14, 7))
	axes = [host] + [host.twinx() for _ in range(values.shape[1] - 1)]

	for index, ax in enumerate(axes):
		ax.set_ylim(ymins[index], ymaxs[index])
		ax.spines["top"].set_visible(False)
		ax.spines["bottom"].set_visible(False)
		if ax is not host:
			ax.spines["left"].set_visible(False)
			ax.yaxis.set_ticks_position("right")
			ax.spines["right"].set_position(("axes", index / (values.shape[1] - 1)))
			ax.patch.set_visible(False)

	host.set_xlim(0, values.shape[1] - 1)
	host.set_xticks(range(values.shape[1]))
	host.set_xticklabels(axis_names, fontsize=13)
	host.tick_params(axis="x", which="major", pad=7)
	host.spines["right"].set_visible(False)
	host.xaxis.tick_top()
	host.set_title("Parallel Coordinates Plot of Population Projections", fontsize=18)

	for ax, axis_name, ymin, ymax in zip(axes, axis_names, ymins, ymaxs):
		ticks = np.linspace(ymin, ymax, 5)
		ax.set_yticks(ticks)
		if axis_name == "YEAR":
			ax.set_yticklabels([f"{tick:.0f}" for tick in ticks])
		else:
			ax.set_yticklabels([f"{tick:.1e}" if tick != 0 else "0" for tick in ticks])

	for _, row in plot_df.iterrows():
		color = RACE_COLORS[row["RACE"]]
		verts = list(
			zip(
				[x for x in np.linspace(0, len(axis_names) - 1, len(axis_names) * 3 - 2, endpoint=True)],
				np.repeat(zs[plot_df.index.get_loc(row.name), :], 3)[1:-1],
			)
		)
		codes = [Path.MOVETO] + [Path.CURVE4 for _ in range(len(verts) - 1)]
		path = Path(verts, codes)
		patch = patches.PathPatch(path, facecolor="none", lw=0.8, edgecolor=color, alpha=0.7)
		host.add_patch(patch)

	legend_handles = [
		plt.Line2D([0], [0], color=color, lw=1.5, label=label)
		for label, color in RACE_COLORS.items()
	]
	host.legend(
		handles=legend_handles,
		title="Race",
		loc="center",
	)

	plt.tight_layout()

	output_dir = "../../results/project3"
	os.makedirs(output_dir, exist_ok=True)
	plt.savefig(f"{output_dir}/high_imm_pop_PC.png", dpi=150, bbox_inches="tight")

	plt.show()

# testing purposes
if __name__ == "__main__":
	processed_df = preprocess("./high_imm_pop.csv")
	plot_parallel_coordinates(processed_df)