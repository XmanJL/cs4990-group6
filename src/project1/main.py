# Main program for building plots of Project 1
# Please save the plots to the "results" folder
import os
from jasper import generate_jasper_graphs
from natasha import generate_natasha_graphs
from Diego import makeGraphs
from sean import generate_sean_graphs

if __name__ == "__main__":
    OUTPUT_DIR = "../../results/project1"
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Jasper's work
    generate_jasper_graphs(OUTPUT_DIR)

    # Diego
    makeGraphs(OUTPUT_DIR)
    
    # Sean
    generate_sean_graphs(OUTPUT_DIR)

    # Natasha
    generate_natasha_graphs(OUTPUT_DIR)
