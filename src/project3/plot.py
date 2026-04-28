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

def plot_stacked_bar(df):
	import os
	import numpy as np
	import matplotlib.pyplot as plt

	RACE_LABELS = {
		1: "White",
		2: "Black",
		4: "Asian",
	}
	AGE_GROUPS = ["POP_0_19", "POP_20_39", "POP_40_59", "POP_60_79", "POP_80_100"]
	AGE_LABELS = {
		"POP_0_19": "0-19",
		"POP_20_39": "20-39",
		"POP_40_59": "40-59",
		"POP_60_79": "60-79",
		"POP_80_100": "80-100",
	}

	AGE_COLORS = {
		"POP_0_19": "#1f77b4",   # 0-19
		"POP_20_39": "#ff7f0e",  # 20-39
		"POP_40_59": "#2ca02c",  # 40-59
		"POP_60_79": "#d62728",  # 60-79
		"POP_80_100": "#9467bd", # 80-100
	}

	plot_df = df.copy()
	plot_df["RACE"] = plot_df["RACE"].map(RACE_LABELS)
	plot_df = plot_df.dropna(subset=["RACE"])

	# reduce years for readability
	years_to_plot = [2020, 2030, 2040, 2050, 2060]
	plot_df = plot_df[plot_df["YEAR"].isin(years_to_plot)]

	races = plot_df["RACE"].unique()
	x = np.arange(len(years_to_plot))
	bar_width = 0.25

	plt.figure(figsize=(12, 7))

	ax = plt.gca()
	bar_gap = 0.05
	n_races = len(races)
	total_bar_width = n_races * bar_width + (n_races - 1) * bar_gap * bar_width
	for i, race in enumerate(races):
		race_df = plot_df[plot_df["RACE"] == race].sort_values("YEAR")
		x_pos = x - (total_bar_width / 2) + (i * (bar_width + bar_gap * bar_width)) + (total_bar_width / 2 - (n_races * bar_width) / 2)
		bottoms = np.zeros(len(years_to_plot))
		for j, age in enumerate(AGE_GROUPS):
			values = race_df[age].values
			color = AGE_COLORS[age]
			bar = plt.bar(x_pos, values, width=bar_width, bottom=bottoms, color=color)
			bottoms += values
		for k, xpos in enumerate(x_pos):
			total_height = sum([race_df[age].values[k] for age in AGE_GROUPS])
			plt.text(xpos, total_height + max(ax.get_yticks())*0.01, race, ha='center', va='bottom', fontsize=11)

	plt.xlabel("Year")
	plt.ylabel("Population (millions)")
	plt.title("Stacked Bar Chart of Population Projections by Age Group and Race")

	try:
		black_idx = list(races).index('Black')
	except ValueError:
		black_idx = 0
	bar_gap = 0.05
	n_races = len(races)
	total_bar_width = n_races * bar_width + (n_races - 1) * bar_gap * bar_width
	black_x = x - (total_bar_width / 2) + (black_idx * (bar_width + bar_gap * bar_width)) + (total_bar_width / 2 - (n_races * bar_width) / 2)
	plt.xticks(black_x, years_to_plot)

	# set y-axis to display in millions using a formatter
	from matplotlib.ticker import FuncFormatter
	ax = plt.gca()
	def millions(x, pos):
		return f"{int(x/1e6)}" if x != 0 else "0"
	ax.yaxis.set_major_formatter(FuncFormatter(millions))

	import matplotlib.patches as mpatches

	legend_patches = [
		mpatches.Patch(color=AGE_COLORS[age], label=AGE_LABELS[age])
		for age in AGE_GROUPS
	]

	plt.legend(
		handles=legend_patches,
		bbox_to_anchor=(1.05, 1),
		loc='upper left',
		title="Age Group"
	)

	plt.tight_layout()

	output_dir = "../../results/project3"
	os.makedirs(output_dir, exist_ok=True)
	plt.savefig(f"{output_dir}/high_imm_pop_stacked_bar.png", dpi=150, bbox_inches="tight")

	plt.show()

# testing purposes
if __name__ == "__main__":
	processed_df = preprocess("./high_imm_pop.csv")
	plot_parallel_coordinates(processed_df)