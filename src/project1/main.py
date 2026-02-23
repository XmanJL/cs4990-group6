# Main program for building plots of Project 1
# Please save the plots to the "results" folder

import matplotlib.pyplot as plt
import os


if __name__ == "__main__":
    os.makedirs("../../results", exist_ok=True)
    # Jasper

    # figure 1: vertical line plot
    ethnicities = ["Asian", "Mexican", "American"]
    heights = [170, 168, 180]
    plt.vlines(x=ethnicities, ymin=0, ymax=heights, linewidth=4, color="blue")
    plt.ylabel("Average Height (cm)")
    plt.title("Synthetic Data for Average Heights by Ethnicity")
    plt.xticks(rotation=45)
    plt.savefig("../../results/vis1.png")
    plt.show()

    # Diego

    # Sean

    # Natasha