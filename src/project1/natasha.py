import matplotlib.pyplot as plt

def generate_natasha_graphs(OUTPUT_DIR="../../results/project1"):

    # figure 1: 1D line plot
    age_groups = ['6-20', '21-35', '36-50', '51-65', '66-80', '81-100']
    avg_steps = [9, 12, 8, 3, 4, 2]  # in thousands
    plt.xlim(-1, len(age_groups))
    plt.ylim(0, 15)
    plt.ylabel("Average steps per day (in thousands)")
    plt.xlabel("Age groups")
    plt.title("Average steps per day for different age groups")

    for i, steps in enumerate(avg_steps):
        plt.vlines(i, 0, steps, linestyles="solid", colors="k")
    
    plt.xticks(range(len(age_groups)), age_groups)
    #plt.savefig(f"{OUTPUT_DIR}/natasha_vis1.png", dpi=100)
    plt.show()

if __name__ == "__main__":
    generate_natasha_graphs()