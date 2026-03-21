# preprocess files and generate token lists for visualization
import string
from pathlib import Path
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.tokenize import word_tokenize

# download resources
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")
nltk.download('punkt_tab')

# init tools
en_stop = set(stopwords.words("english"))
fr_stop = set(stopwords.words("french"))

lemmatizer = WordNetLemmatizer()
fr_stemmer = SnowballStemmer("french")

# read file
def read_text(file):
    return Path(file).read_text(encoding="utf-8")

# preprocess english
def preprocess_en(text):
    tokens = word_tokenize(text.lower())
    cleaned = []

    for w in tokens:
        if (w in en_stop or w in string.punctuation or not w.isalpha()):
            continue

        cleaned.append(lemmatizer.lemmatize(w))

    return cleaned

# preprocess french
def preprocess_fr(text):
    tokens = word_tokenize(text.lower())
    cleaned = []

    for w in tokens:
        if (w in fr_stop or w in string.punctuation or not w.isalpha()):
            continue

        cleaned.append(fr_stemmer.stem(w))

    return cleaned

# main preprocess
def preprocess_files(en_file="badminton_EN.txt", fr_file="badminton_FR.txt"):
    en_text = read_text(en_file)
    fr_text = read_text(fr_file)

    EN_tokens = preprocess_en(en_text)
    FR_tokens = preprocess_fr(fr_text)

    return EN_tokens, FR_tokens

# test
if __name__ == "__main__":
    EN_tokens, FR_tokens = preprocess_files()
    print(EN_tokens[:20])
    print(FR_tokens[:20])