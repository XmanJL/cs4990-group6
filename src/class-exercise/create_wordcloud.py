import os
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

# just a file for testing the exercise5
if __name__ == "__main__":
    OUTPUT_DIR = "../../results/class-exercise"
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open("./words.txt", 'r') as file:
        text = file.read().strip()
        wordcloud = WordCloud(stopwords=STOPWORDS, background_color="white").generate(text)
        plt.imshow(wordcloud, interpolation="bilinear", cmap="plasma")
        plt.axis("off")
        plt.savefig(os.path.join(OUTPUT_DIR, "wordcloud.png"), dpi=100)
        plt.show()
    

