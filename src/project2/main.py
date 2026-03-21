# Main program for Project 2
from preprocess import preprocess_files
from visualize import generate_wordcloud
import os

# main pipeline
def main():
    OUTPUT_DIR = "../../results/project2"
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    EN_tokens, FR_tokens = preprocess_files()

    generate_wordcloud(EN_tokens, "English Word Cloud", f"{OUTPUT_DIR}/wordcloud_en.png")
    generate_wordcloud(FR_tokens, "French Word Cloud", f"{OUTPUT_DIR}/wordcloud_fr.png")

# run our main program!
if __name__ == "__main__":
    main()