# Visualize tokens as an interactive word cloud
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# generate wordcloud
def generate_wordcloud(tokens, title="Word Cloud", output_path=None):
    if not tokens:
        return

    freq = Counter(tokens)

    wc = WordCloud(
        width=1000,
        height=500,
        background_color="white"
    ).generate_from_frequencies(freq)

    plt.figure(figsize=(12, 6))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.title(title)

    if output_path:
        plt.savefig(output_path, dpi=150, bbox_inches="tight")

    plt.show()