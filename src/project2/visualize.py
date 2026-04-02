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
    import math

    en_freq = Counter(en_tokens)
    fr_freq = Counter(fr_tokens)

    #   TF(w)     = raw count of word w in the document
    #   Df(w)     = number of documents containing word w
    #   N         = total number of documents in the corpus
    #   IDF(w)    = log(N / Df(w))
    #   TF-IDF(w) = TF(w) * log(N / Df(w))
    #
    # Our corpus has N=2 documents: the EN article and the FR article.
    # A word in both documents: Df=2 -> IDF = log(2/2) = 0 (no discriminating power).
    # A word in only one document: Df=1 -> IDF = log(2/1) ~= 0.693.
    N = 2
    all_words = set(en_freq) | set(fr_freq)
    df = {
        word: (1 if word in en_freq else 0) + (1 if word in fr_freq else 0)
        for word in all_words
    }

    def build_entries(freq):
        entries = []
        for word, count in freq.most_common(top_n):
            tf    = count                        # TF = raw frequency count
            idf   = math.log(N / df[word])       # IDF = log(N / Df(w))
            tfidf = round(tf * idf, 5)           # TF-IDF = TF * IDF
            entries.append({
                "word":  word,
                "count": count,
                "tf":    tf,
                "idf":   round(idf, 5),
                "tfidf": tfidf,
            })
        return entries

    data = {
        "en": build_entries(en_freq),
        "fr": build_entries(fr_freq),
    }

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"[export_json] Saved word cloud data to: {output_path}")