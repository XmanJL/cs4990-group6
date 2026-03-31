# Visualize tokens as an interactive word cloud
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import json
import os

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

# export token frequency data to JSON for the interactive HTML word cloud
def export_json(en_tokens, fr_tokens, output_path, top_n=80):
    def build_entries(tokens):
        freq = Counter(tokens)
        total = len(tokens)
        return [
            {"word": word, "count": count, "tf": round(count / total, 5)}
            for word, count in freq.most_common(top_n)
        ]

    data = {
        "en": build_entries(en_tokens),
        "fr": build_entries(fr_tokens)
    }

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"[export_json] Saved word cloud data to: {output_path}")