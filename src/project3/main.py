# run the main pipeline of the program
from preprocess import preprocess
from plot import plot_parallel_coordinates

# main pipeline
if __name__ == "__main__":

    # preprocess the data
    processed_df = preprocess("./high_imm_pop.csv")

    # plot the parallel coordinates
    plot_parallel_coordinates(processed_df)