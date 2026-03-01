import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def generate_natasha_graphs(OUTPUT_DIR="../../results/project1"):

    # figure 1: 1D line plot
    age_groups = ['6-20', '21-35', '36-50', '51-65', '66-80', '81-100']
    avg_steps = [9, 12, 8, 3, 4, 2]
    plt.xlim(-1, len(age_groups))
    plt.ylim(0, 15)
    plt.ylabel("Average steps per day (in thousands)")
    plt.xlabel("Age groups")
    plt.title("Average steps per day for different age groups")

    for i, steps in enumerate(avg_steps):
        plt.vlines(i, 0, steps, linestyles="solid", colors="blue")
    
    plt.xticks(range(len(age_groups)), age_groups)
    plt.savefig(f"{OUTPUT_DIR}/natasha_vis1.png", dpi=150)
    plt.show()

    # figure 2: 2D stacked area chart
    x=range(2010,2016)
    y1=[2,3,2,4,3,5]
    y2=[5,7,6,9,8,12]
    y3=[8,9,11,10,14,16]
    y4=[15,17,20,18,25,28]

    plt.stackplot(x,y1, y2, y3, y4, labels=['Rollerskates','Skateboards','Scooters', 'Bikes'])
    plt.legend(loc='upper left')
    plt.ylabel("Non-motor vehicle sales (in millions)")
    plt.xlabel("Year")
    plt.title("Non-motor vehicle sales by category over time (2010-2015)")
    plt.savefig(f"{OUTPUT_DIR}/natasha_vis2.png", dpi=150)
    plt.show()

    # figure 3: 3D volume graph
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    carats = [0.3, 0.5, 0.75, 0.9, 1.0]
    costs = [1248, 2018, 3329, 4574, 5388]
    xpos = range(len(carats))
    colors = ['steelblue', 'orange', 'green', 'red', 'purple']

    ax.bar3d([x - 0.2 for x in xpos], [-0.3]*len(carats), [0]*len(carats), [0.6]*len(carats), [0.6]*len(carats), costs, color=colors)
    ax.set_xlabel("Carat")
    ax.set_zlabel("Cost ($)")
    ax.set_title("Average Cost of Diamond Engagement Rings by Carat")
    ax.set_xticks(xpos)
    ax.set_xticklabels(carats)
    ax.set_yticks([])
    plt.savefig(f"{OUTPUT_DIR}/natasha_vis3.png", dpi=150)
    plt.show()