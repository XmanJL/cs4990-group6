# Main program for Project 2
from preprocess import preprocess_files
from visualize import generate_wordcloud, export_json
import os
 
# main pipeline
def main():
    OUTPUT_DIR = "../../results/project2"
    os.makedirs(OUTPUT_DIR, exist_ok=True)
 
    EN_tokens, FR_tokens = preprocess_files()
 
    # generate static word cloud PNGs
    generate_wordcloud(EN_tokens, "English Word Cloud", f"{OUTPUT_DIR}/wordcloud_en.png")
    generate_wordcloud(FR_tokens, "French Word Cloud", f"{OUTPUT_DIR}/wordcloud_fr.png")
 
    # export JSON data for the interactive HTML word cloud
    export_json(EN_tokens, FR_tokens, f"{OUTPUT_DIR}/wordcloud_data.json")
 
# run our main program!
if __name__ == "__main__":
    main()